"""@bruin
name: load_raw_to_bq
depends:
  - ingest_data
connection: gcp-marketing
secrets:
  - key: gcp-marketing
    inject_as: GCP_CONNECTION
@bruin"""

from __future__ import annotations

import json
import os
from pathlib import Path

from google.cloud import bigquery
from google.oauth2 import service_account

BASE_DIR = Path(__file__).resolve().parent.parent        # assets
RAW_DIR = BASE_DIR / "data" / "raw"
DEFAULT_LOCATION = "us-central1"
DEFAULT_DATASET = "brunt_raw_ads"


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _ensure_dataset(client: bigquery.Client, dataset_id: str, location: str) -> bigquery.Dataset:
    try:
        ds = client.get_dataset(dataset_id)
    except Exception:
        ds = bigquery.Dataset(dataset_id)
        ds.location = location
        return client.create_dataset(ds, exists_ok=True)

    if (ds.location or "").lower() != location.lower():
        raise RuntimeError(
            f"Dataset {dataset_id} exists in location {ds.location!r}, "
            f"but this loader is configured for {location!r}."
        )
    return ds


def _table_id_for_csv(csv_path: Path) -> str:
    # Keep table names predictable: google_ads_raw.csv -> google_ads_raw
    return csv_path.stem.lower()


def _bigquery_client_from_bruin_secret(env_var: str) -> tuple[bigquery.Client, str]:
    """
    Build a BigQuery client from a Bruin-injected GCP connection secret.
    """
    raw = os.environ.get(env_var)
    if not raw:
        raise RuntimeError(
            f"Missing Bruin secret in env var {env_var!r}. "
            "Ensure the asset 'secrets' header is configured correctly."
        )

    conn = json.loads(raw)
    project_id = conn.get("project_id")
    if not project_id:
        raise RuntimeError("Bruin GCP connection secret is missing 'project_id'.")

    sa_json = conn.get("service_account_json")
    if not sa_json:
        raise RuntimeError("Bruin GCP connection secret is missing 'service_account_json'.")

    sa_info = json.loads(sa_json)
    creds = service_account.Credentials.from_service_account_info(sa_info)
    client = bigquery.Client(project=project_id, credentials=creds)
    return client, project_id


def main() -> None:
    dataset_name = _env("BQ_DATASET", DEFAULT_DATASET)
    location = _env("BQ_LOCATION", DEFAULT_LOCATION)

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Raw directory not found: {RAW_DIR.resolve()}")

    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {RAW_DIR.resolve()}")

    client, project_id = _bigquery_client_from_bruin_secret("GCP_CONNECTION")
    dataset_id = f"{project_id}.{dataset_name}"
    _ensure_dataset(client, dataset_id, location)

    write_mode = (_env("BQ_WRITE_DISPOSITION", "WRITE_TRUNCATE") or "WRITE_TRUNCATE").upper()
    if write_mode not in {"WRITE_TRUNCATE", "WRITE_APPEND"}:
        raise ValueError("BQ_WRITE_DISPOSITION must be WRITE_TRUNCATE or WRITE_APPEND")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=write_mode,
        allow_quoted_newlines=True,
    )

    for csv_path in csv_files:
        table_id = f"{dataset_id}.{_table_id_for_csv(csv_path)}"
        with csv_path.open("rb") as f:
            job = client.load_table_from_file(
                f,
                table_id,
                job_config=job_config,
                location=location,
            )
        job.result()
        table = client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows into {table_id} from {csv_path.as_posix()}")


if __name__ == "__main__":
    main()