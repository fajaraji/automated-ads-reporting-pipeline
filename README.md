# Automated Ads Reporting Suite

A fully automated data pipeline that consolidates, transforms, and visualizes digital advertising performance data across multiple platforms (Google Ads, Meta Ads, TikTok Ads, LinkedIn Ads).

[**📊 View Live Dashboard**](https://lookerstudio.google.com/reporting/e9ac6c38-c7ab-45b9-af8a-61c94bda8a97)

---

## Overview

This project automates the entire advertising reporting workflow:

1. **Ingest** raw campaign data from a Kaggle dataset
2. **Transform** and standardize data across all advertising platforms
3. **Load** into Google BigQuery for analytics
4. **Visualize** in Looker Studio for executive reporting

Built with [Bruin](https://getbruin.com) for pipeline orchestration and Google BigQuery for data warehousing.

---

## Features

- 🔄 **Multi-Platform Consolidation** - Unifies data from Google, Meta, TikTok, and LinkedIn Ads into a single source of truth
- 📈 **Automated ETL Pipeline** - Scheduled daily execution with Bruin orchestrator
- 🎯 **Pre-Built Reports** - 5 ready-to-use report views for different business needs
- 📊 **Looker Studio Integration** - Live dashboard for executive visibility
- 🔒 **Production-Ready** - Uses BigQuery secrets management and secure GCP connections

---

## Pipeline Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Kaggle API    │ ──► │   Ingestion      │ ──► │   Staging       │ ──► │   Reports        │ ──► │  Looker Studio  │
│   (Raw Data)    │     │   (Python)       │     │   (SQL Views)   │     │   (SQL Views)    │     │   Dashboard     │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                        │                        │
                               ▼                        ▼                        ▼
                         raw CSVs                BigQuery                 BigQuery
                         (per platform)          staging views            report views
```

---

## Pipeline Layers

### 1. Ingestion Layer

| Asset | Description |
|-------|-------------|
| `ingest_data.py` | Downloads digital advertising dataset from Kaggle, splits by platform into separate CSV files |
| `load_raw_to_bq.py` | Loads raw CSV files into BigQuery tables with proper schema detection |

### 2. Staging Layer

Standardizes schema across all platforms with consistent column names and data types.

| Asset | Source |
|-------|--------|
| `stg_google_ads.sql` | Google Ads raw data |
| `stg_meta_ads.sql` | Meta/Facebook/Instagram Ads raw data |
| `stg_tiktok_ads.sql` | TikTok Ads raw data |
| `stg_linkedin_ads.sql` | LinkedIn Ads raw data |

### 3. Reports Layer

Business-ready views for analytics and dashboards.

| Report | Description |
|--------|-------------|
| `rpt_campaign_performance_daily.sql` | Daily performance metrics by campaign, platform, and targeting dimensions |
| `rpt_channel_performance_daily.sql` | Daily aggregated performance by platform/channel |
| `rpt_creative_performance.sql` | Performance analysis by creative format, emotion, placement, and device |
| `rpt_objective_funnel_performance.sql` | Performance breakdown by campaign objective and funnel stage |
| `rpt_executive_summary_monthly.sql` | Monthly executive summary with MoM growth calculations |

---

## Key Metrics

All reports include standard advertising KPIs:

| Metric | Formula | Description |
|--------|---------|-------------|
| **Impressions** | - | Total ad views |
| **Clicks** | - | Total click-throughs |
| **Conversions** | - | Completed conversion events |
| **CTR** | Clicks ÷ Impressions | Click-through rate |
| **CPC** | Spend ÷ Clicks | Cost per click |
| **Conversion Rate** | Conversions ÷ Clicks | Conversion percentage |
| **CPA** | Spend ÷ Conversions | Cost per acquisition |
| **ROAS** | Revenue ÷ Spend | Return on ad spend |
| **Profit** | Revenue - Spend | Net profit from campaigns |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Orchestration** | Bruin |
| **Data Warehouse** | Google BigQuery |
| **Visualization** | Google Looker Studio |
| **Languages** | Python, SQL |
| **Data Source** | Kaggle Digital Advertising Dataset |
| **Cloud Platform** | Google Cloud Platform (GCP) |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Google Cloud Platform account with BigQuery enabled
- Kaggle account (for API access)
- Bruin CLI installed

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/fajaraji/automated-ads-reporting-pipeline.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure connections**
   
   Create or update `.bruin.yml` with your GCP connection:
   ```yaml
   default_environment: default
   environments:
     default:
       connections:
         google-cloud-platform:
           - name: "gcp-marketing"
             project_id: "your-gcp-project-id"
             service_account_json: "${GCP_SERVICE_ACCOUNT}"
   ```

4. **Set environment variables**
   ```bash
   export KAGGLE_USERNAME=your_username
   export KAGGLE_KEY=your_api_key
   export GCP_SERVICE_ACCOUNT='{"type":"service_account",...}'
   ```

### Running the Pipeline

```bash
# Run the entire pipeline
bruin run .

# Run specific assets
bruin run assets/ingestion/ingest_data.py
bruin run assets/staging/stg_meta_ads.sql

# Run with downstream dependencies
bruin run assets/ingestion/ingest_data.py --downstream

# Validate pipeline
bruin validate .
```

### Pipeline Schedule

The pipeline is configured to run **daily** (see `pipeline.yml`):
```yaml
schedule: daily
```

---

## Project Structure

```
automated-ads-reporting-suite/
└── bruin/
    └── bruin-pipeline/
        ├── pipeline.yml              # Pipeline configuration
        ├── requirements.txt          # Python dependencies
        ├── README.md                 # Bruin sample docs
        └── assets/
            ├── ingestion/
            │   ├── ingest_data.py    # Kaggle data download & split
            │   └── load_raw_to_bq.py # Load CSVs to BigQuery
            ├── staging/
            │   ├── stg_google_ads.sql
            │   ├── stg_meta_ads.sql
            │   ├── stg_tiktok_ads.sql
            │   └── stg_linkedin_ads.sql
            ├── reports/
            │   ├── rpt_campaign_performance_daily.sql
            │   ├── rpt_channel_performance_daily.sql
            │   ├── rpt_creative_performance.sql
            │   ├── rpt_executive_summary_monthly.sql
            │   └── rpt_objective_funnel_performance.sql
            └── data/
                └── raw/              # Downloaded CSV files
```

---

## Looker Studio Dashboard

The live dashboard provides interactive visualizations of all report data:

🔗 **[Open Dashboard](https://lookerstudio.google.com/reporting/e9ac6c38-c7ab-45b9-af8a-61c94bda8a97)**

### Dashboard Views

- **Executive Summary** - High-level KPIs, trends, and MoM comparisons
- **Channel Performance** - Platform-by-platform breakdown and comparison
- **Campaign Analysis** - Deep dive into individual campaign performance
- **Creative Insights** - Which creatives, formats, and messages perform best
- **Funnel Analysis** - Performance by campaign objective and funnel stage

---

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

## Contributing

1. Create a new branch for your feature
2. Add new assets under the appropriate layer (`ingestion/`, `staging/`, `reports/`)
3. Update `pipeline.yml` if adding new dependencies
4. Test with `bruin validate` before committing

---

## License

This project is provided as-is for educational and business use.

---

## Support

For issues or questions:
- Bruin Documentation: https://getbruin.com/docs
- BigQuery Documentation: https://cloud.google.com/bigquery/docs

---

<p align="center">
  <strong>Built with Bruin + Google BigQuery + Looker Studio</strong>
</p>
