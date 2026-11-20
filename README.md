# Automated Ads Reporting

Bruin pipeline that splits a Kaggle advertising dataset into four channels and builds BigQuery reports for campaign, creative, and channel performance.

## Explore the implementation

Follow one campaign from the shared source file to a daily report. The loader replaces raw tables by default. The staging SQL uses the dataset name `brunt_raw_ads` explicitly.

- [Download and split by channel](bruin/bruin-pipeline/assets/ingestion/ingest_data.py)
- [Normalize Meta Ads records](bruin/bruin-pipeline/assets/staging/stg_meta_ads.sql)
- [Daily campaign metrics](bruin/bruin-pipeline/assets/reports/rpt_campaign_performance_daily.sql)

## From source file to dashboard

1. The ingestion asset downloads one Kaggle dataset and writes a CSV for each of Google, Meta, TikTok, and LinkedIn.
2. The BigQuery loader reads those CSVs. Four SQL staging views standardize the fields before the reporting queries calculate channel and campaign metrics.
3. Explore the published [Looker Studio dashboard](https://lookerstudio.google.com/reporting/e9ac6c38-c7ab-45b9-af8a-61c94bda8a97) or inspect [all five reporting queries](bruin/bruin-pipeline/assets/reports).

## Run the pipeline

Install the Bruin CLI and configure Kaggle API authentication. In your local Bruin environment, configure the GCP connection `gcp-marketing` with BigQuery access. The raw loader defaults to `us-central1`. Review table references in staging and reports before changing the dataset name.

```bash
cd bruin/bruin-pipeline
python -m pip install -r requirements.txt
bruin validate .
bruin run .
```

The [pipeline definition](bruin/bruin-pipeline/pipeline.yml) specifies a daily schedule. A scheduled deployment needs a runner that invokes Bruin.

## Data Model

### Staging Schema

All staging views standardize to this schema:

| Field | Type | Description |
|-------|------|-------------|
| `campaign_id` | STRING | Unique campaign identifier |
| `campaign_objective` | STRING | Campaign goal (awareness, consideration, conversion) |
| `platform` | STRING | Advertising platform |
| `start_date` | DATE | Campaign start date |
| `impressions` | INT64 | Ad views |
| `clicks` | INT64 | Click-throughs |
| `conversions` | INT64 | Conversion events |
| `ad_spend` | NUMERIC | Advertising spend |
| `revenue` | NUMERIC | Generated revenue |
| `profit` | NUMERIC | Net profit |
| `CTR`, `CPC`, `CPA`, `ROAS` | FLOAT64 | Calculated metrics |

---

## License

This project is provided as-is for educational and business use.

---
