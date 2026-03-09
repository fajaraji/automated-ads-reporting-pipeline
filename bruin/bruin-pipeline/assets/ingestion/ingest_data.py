"""@bruin
name: ingest_data
@bruin"""

import os
import re
import glob
from pathlib import Path   # <— tambahkan ini
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

DATASET_URL = "https://www.kaggle.com/datasets/juniornsa/digital-advertising-campaign-performance-dataset"
BASE_DIR = Path(__file__).resolve().parent.parent       
RAW_PATH = BASE_DIR / "data" / "raw"            


def _dataset_id_from_kaggle_url(url: str) -> str:
    """
    Converts a Kaggle dataset URL like:
      https://www.kaggle.com/datasets/<owner>/<dataset>
    into the Kaggle API dataset id:
      <owner>/<dataset>
    """
    match = re.search(r"kaggle\.com/datasets/([^/]+/[^/?#]+)", url)
    if not match:
        raise ValueError(f"Invalid Kaggle dataset URL: {url}")
    return match.group(1)


def _normalize_platform(value) -> str:
    if value is None:
        return ""
    s = str(value).strip().lower()
    s = re.sub(r"[_\-]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _pick_downloaded_csv(raw_path: str) -> str:
    csv_candidates = glob.glob(os.path.join(raw_path, "*.csv"))
    if not csv_candidates:
        raise FileNotFoundError(f"No .csv files found in {raw_path} after download/unzip.")

    # Prefer a single obvious candidate; otherwise pick the largest CSV.
    if len(csv_candidates) == 1:
        return csv_candidates[0]

    def score(path: str) -> tuple[int, int]:
        name = os.path.basename(path).lower()
        keywords = ("campaign", "advert", "digital", "dataset")
        keyword_hits = sum(1 for k in keywords if k in name)
        size = os.path.getsize(path)
        return (keyword_hits, size)

    return sorted(csv_candidates, key=score, reverse=True)[0]


def _find_platform_column(df: pd.DataFrame) -> str:
    cols = {str(c).strip().lower(): c for c in df.columns}
    if "platform" in cols:
        return cols["platform"]
    raise KeyError("Could not find a 'platform' column in the downloaded dataset.")


def main():
    # 1. Setup Kaggle API
    # It will automatically look for the KAGGLE_API_TOKEN env var
    api = KaggleApi()
    api.authenticate()

    dataset = _dataset_id_from_kaggle_url(DATASET_URL)
    
    # Create directory if not exists
    os.makedirs(RAW_PATH, exist_ok=True)

    print(f"Downloading dataset from: {DATASET_URL}")
    # Download and unzip
    api.dataset_download_files(dataset, path=RAW_PATH, unzip=True)
    
    # Identify the downloaded CSV (filename may change over time)
    csv_file = _pick_downloaded_csv(RAW_PATH)
    df = pd.read_csv(csv_file)

    # 2. Split data by Platform to simulate "Multiple Sources"
    platform_col = _find_platform_column(df)
    normalized_platforms = df[platform_col].map(_normalize_platform)

    platforms = [
        ("google ads", {"google ads", "google", "adwords", "google adwords"}, "google_ads_raw.csv"),
        ("meta ads", {"meta ads", "meta", "facebook", "facebook ads", "instagram", "instagram ads"}, "meta_ads_raw.csv"),
        ("tiktok ads", {"tiktok ads", "tiktok"}, "tiktok_ads_raw.csv"),
        ("linkedin ads", {"linkedin ads", "linkedin"}, "linkedin_ads_raw.csv"),
    ]

    print("Splitting data into 4 source files...")
    for platform_name, aliases, file_name in platforms:
        mask = normalized_platforms.isin({_normalize_platform(a) for a in aliases})
        platform_df = df[mask].copy()
        
        output_file = os.path.join(RAW_PATH, file_name)
        platform_df.to_csv(output_file, index=False)
        print(f"Created: {output_file} ({len(platform_df)} rows)")

    # Clean up the original large file to save space
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print("Cleaned up original dataset file.")

if __name__ == "__main__":
    main()