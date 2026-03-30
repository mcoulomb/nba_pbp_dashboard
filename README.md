# NBA Play-by-Play Dashboard

A comprehensive data pipeline and interactive dashboard for analyzing NBA play-by-play data. This project combines Apache Airflow for orchestration, dbt for data transformation, and Streamlit for visualization.

## Problem Description:
NBA Play by Play data can be quite inaccessible, or requires loading datasets into dataframes and manipulating the data directly. This project seeks to do the following:
  1. Create an easy to use pipeline for loading nba play by play data into a data warehouse.
  2. Transform the data to get insights into shot distribution per team over the years.
  3. Transform the data to compare playmaking on the highest value shots across the different quarters of the game.
     
<img width="2485" height="1232" alt="image" src="https://github.com/user-attachments/assets/37d6611c-9a9e-4dac-982f-4928a1bedcae" />

**Key Features:**
- 🎯 Infrastructure-as-Code with Terraform for reproducible deployments
- 🔄 Apache Airflow DAGs for automated data ingestion and processing
- 🌩️ Google Cloud Storage and BigQuery for scalable data warehousing
- 🏗️ dbt-powered data transformations in Google BigQuery: Data warehouse tables are **clustered** on year and is_field_goal columns to support downstream reporting.
- 🏀 Interactive Streamlit dashboard for exploring NBA play-by-play data (2020-2025 seasons)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Detailed Setup](#detailed-setup)
  - [1. Python Environment Setup](#1-python-environment-setup)
  - [2. Environment Configuration](#2-environment-configuration)
  - [3. GCP Setup](#3-gcp-setup)
  - [4. Terraform Infrastructure](#4-terraform-infrastructure)
  - [5. Docker & Airflow](#5-docker--airflow)
- [Project Architecture](#project-architecture)
  - [Data Flow](#data-flow)
  - [Project Structure](#project-structure)
- [Running the Dashboard](#running-the-dashboard)
  - [Airflow DAGs](#airflow-dags)
  - [dbt Models](#dbt-models)
  - [Streamlit App](#streamlit-app)
- [Troubleshooting](#troubleshooting)
- [Further Reading](#further-reading)

---

## Prerequisites

### Required
- **Python 3.13 or higher** — Install from [python.org](https://www.python.org/downloads/)
- **Docker & Docker Compose** — [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Git** — For cloning the repository
- **GCP Project** — With BigQuery and Cloud Storage APIs enabled
- **Terraform** — For infrastructure management
- **dbt CLI** — For running dbt models manually
- **Airflow** — For running Dags to extract and load data to GCP.

### Python Version Check
```bash
python3 --version
# Output should be: Python 3.13.x or higher
```

---

## Detailed Setup

### 1. Python Environment Setup

#### Clone the Repository
```bash
git clone <repository-url>
cd nba_pbp_dashboard
```

#### Install Dependencies
This project uses `pyproject.toml` with modern Python packaging. Install all dependencies:

```bash
# Using pip
pip install -e .

# Or using uv (faster alternative, if installed)
uv pip install -e .
```

**Installed Packages:**
- `streamlit>=1.55.0` — Interactive dashboard framework
- `plotly>=6.6.0` — Advanced charting library
- `jupyter>=1.1.1` & `notebook>=7.5.5` — Notebook environment for analysis
- `pandas` — Data manipulation (dependency of above packages)
- `google-cloud-bigquery` & `google-oauth2` — GCP integration

#### Verify Installation
```bash
python3 -c "import streamlit; print(streamlit.__version__)"
streamlit --version
```

---

### 2. Environment Configuration

#### Create `.env` File
Copy the template and add your GCP credentials:

```bash
cp .env.example .env
```

#### Edit `.env` with Required Variables
```env
# Airflow Configuration (for Docker Compose)
AIRFLOW_UID=1000

# GCP Configuration
GOOGLE_APPLICATION_CREDENTIALS={path-to-service-account-json}
GCP_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-gcs-bucket-name

# Optional: Custom settings
AIRFLOW_ADMIN_USERNAME=airflow
AIRFLOW_ADMIN_PASSWORD=airflow
AIRFLOW_DAGS_FOLDER=./dags
```

#### GCP Credentials File
1. Download your service account JSON from [GCP Console](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Place it in your project root (e.g., `gcp-credentials.json`)
3. Update `GOOGLE_APPLICATION_CREDENTIALS` in `.env` with the path

---

### 3. GCP Setup

For first-time GCP setup, follow this guide:

1. **Create a GCP Project** — [Quick Start Guide](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
2. **Enable Required APIs:**
   - Google Cloud Storage API
   - BigQuery API
   - Cloud Logging API
3. **Create a Service Account** — [Instructions](https://cloud.google.com/iam/docs/service-accounts-create)
4. **Create and Download a Key** — [JSON Key Setup](https://cloud.google.com/iam/docs/keys-create-delete)
5. **Set Required Permissions:**
   - `roles/storage.admin` — Cloud Storage access
   - `roles/bigquery.admin` — BigQuery access
   - `roles/logging.logWriter` — Logging access

> For detailed step-by-step instructions, see [GCP Project Setup Guide](https://cloud.google.com/docs/authentication/getting-started)

---

### 4. Terraform Infrastructure

Terraform manages GCP infrastructure as code. Set up your cloud resources before running Airflow.

#### Prerequisites
- Install [Terraform](https://www.terraform.io/downloads.html)
- Have GCP credentials configured (same service account as Airflow/Streamlit)

#### Configure Variables
Edit `variables.tf`:
- `project` — GCP project ID
- `region` — GCP region (default: `US`)

#### Deploy Infrastructure
```bash
# Initialize Terraform (first time only)
terraform init

# Review planned changes
terraform plan

# Apply infrastructure changes (creates GCS bucket)
terraform apply

# Verify deployment
terraform show
```

#### What Terraform Deploys
- **GCS Bucket** (`mcoulomb-nba-pbp-data`) — Stores parquet files
  - Uniform bucket-level access enabled for security
  - Versioning enabled to track file changes
  - Auto-deletion policy: files deleted after 30 days
  - Force destroy enabled for safe local development cleanup

#### Destroy Infrastructure (Only for cleanup)
```bash
# WARNING: This will delete all resources and data
terraform destroy
```

---

### 5. Docker & Airflow

#### Start Airflow Services
```bash
# Initialize Airflow database (required on first-time setup)
docker-compose up airflow-init

# Start all services (Airflow, PostgreSQL, Redis)
docker-compose up -d

# Verify services are running
docker-compose ps
```

#### Access Airflow UI
- **URL:** http://localhost:8080
- **Username:** airflow
- **Password:** airflow (default, change in production)

#### View Logs
```bash
# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
```

#### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

---

## Project Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        External Data Source                      │
│  (NBA play-by-play data from github.com/shufinskiy/nba_data)    │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   Airflow DAG: move_pbp_data    │
        │  - Download .tar.xz from GitHub │
        │  - Extract CSV files            │
        │  - Convert to Parquet format    │
        │  - Upload to GCS bucket         │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────────────┐
        │   Google Cloud Storage (GCS) Bucket     │
        │  (Raw parquet files)                    │
        └────────────────┬─────────────────────────┘
                         │
        ┌────────────────▼────────────────────────┐
        │   Airflow DAG: create_bigquery_table    │
        │  - Create external BigQuery table       │
        │  - Reference parquet files in GCS       │
        └────────────────┬─────────────────────────┘
                         │
        ┌────────────────▼────────────────────────┐
        │    Google BigQuery (Data Warehouse)     │
        │  (External tables referencing GCS)      │
        └────────────────┬─────────────────────────┘
                         │
        ┌────────────────▼────────────────────────┐
        │   dbt Transformations (Optional)        │
        │  - Transform raw data into models       │
        │  - Create analytics tables              │
        │  - Generate mart tables                 │
        └────────────────┬─────────────────────────┘
                         │
        ┌────────────────▼────────────────────────┐
        │   Streamlit Dashboard                   │
        │  - Interactive visualizations           │
        │  - Dynamic filtering                    │
        │  - Real-time data exploration           │
        └─────────────────────────────────────────┘
```

### Project Structure

```
nba_pbp_dashboard/
├── README.md                              # This file
├── pyproject.toml                         # Python dependencies & project config
├── .env                                   # Environment variables (GCP, Airflow)
├── .env.example                           # Template for .env
│
├── nba_dashboard_streamlit.py            # Main Streamlit application
├── visualize.py                           # Visualization utilities
├── main.py                                # CLI entry point (placeholder)
│
├── dags/                                  # Airflow DAGs
│   ├── move_pbp_data_into_gcs_bucket_dag.py
│   │   └── Downloads NBA data, converts to parquet, uploads to GCS
│   └── create_bigquery_external_table_dag.py
│       └── Creates external BigQuery tables referencing GCS data
│
├── nba_pbp_dashboard_dbt/                # dbt project (optional)
│   ├── dbt_project.yml                    # dbt project configuration
│   ├── dbt_profiles.yml                   # dbt profile for BigQuery connection
│   ├── models/                            # SQL transformation models
│   ├── analyses/                          # One-off analysis queries
│   ├── tests/                             # Data quality tests
│   ├── macros/                            # Reusable dbt macros
│   └── seeds/                             # Static reference data
│
├── docker-compose.yaml                   # Local Airflow setup (services, volumes)
├── airflow.cfg                            # Airflow configuration
├── config/                                # Additional configuration files
│
├── main.tf                                # Terraform: GCS bucket definition
├── variables.tf                           # Terraform: variable definitions
├── terraform.tfstate                      # Terraform state (auto-generated)
│
├── plugins/                               # Custom Airflow plugins
├── logs/                                  # Airflow logs (auto-generated)
├── iframe_figures/                        # Cached HTML figures for dashboard
└── __pycache__/                           # Python cache (auto-generated)
```

---

## Running the Dashboard

### Airflow DAGs

#### List Available DAGs
```bash
# Via Docker
docker-compose exec airflow-webserver airflow dags list

# Via Airflow UI
# Navigate to http://localhost:8080 → DAGs tab
```

#### Manually Trigger a DAG
```bash
# Trigger via command-line
docker-compose exec airflow-webserver airflow dags trigger move_pbp_data_into_gcs_bucket \
  --conf '{"dataset": "cdnnba", "year": "2025"}'

# Trigger via Airflow UI
# 1. Go to http://localhost:8080
# 2. Find the DAG in the DAGs list
# 3. Click the DAG name → Trigger DAG button
# 4. Enter parameters in the JSON config field and submit
```

#### Monitor DAG Runs
```bash
# View DAG runs
docker-compose exec airflow-webserver airflow dags list-runs \
  --dag-id move_pbp_data_into_gcs_bucket

# View task logs
docker-compose exec airflow-webserver airflow tasks logs \
  move_pbp_data_into_gcs_bucket run_id task_id
```

#### Available DAGs

**1. `move_pbp_data_into_gcs_bucket`**
- Downloads NBA play-by-play data from GitHub repository
- Extracts `.tar.xz` archives to CSV
- Converts CSV to Parquet format (optimized for BigQuery)
- Uploads Parquet files to Google Cloud Storage
- **Parameters:**
  - `dataset`: Data source (e.g., `cdnnba`)
  - `year`: Season year (e.g., `2025`)

**2. `create_bigquery_external_table`**
- Creates BigQuery external tables referencing Parquet files in GCS
- Enables querying raw data without loading into BigQuery
- Optimizes cost (only charged for data scanned, not stored)

---

### dbt Models

After Airflow DAGs have successfully processed and loaded data into BigQuery, use dbt to transform the raw data into analytics-ready tables.

#### Install dbt-bigquery
```bash
# If not already installed
pip install dbt-bigquery
```

#### Configure dbt Profile
Ensure `nba_pbp_dashboard_dbt/dbt_profiles.yml` has correct BigQuery credentials.

#### Run dbt Models
```bash
cd nba_pbp_dashboard_dbt

# Test the connection
dbt debug

# Run all models (creates transformed tables in BigQuery)
dbt run

# Run only specific model
dbt run --select model_name

# Generate documentation
dbt docs generate
dbt docs serve
```

#### Available Models
See `nba_pbp_dashboard_dbt/models/` directory for SQL transformation models.

---

### Streamlit App

Once Airflow DAGs have loaded data and dbt has transformed it, run the interactive dashboard.

#### Start the Application
```bash
streamlit run nba_dashboard_streamlit.py
```

The app will:
- Open automatically at http://localhost:8501
- Display the NBA Play-by-Play Dashboard with interactive charts
- Allow filtering by game, player, quarter, and play type

#### Configuration
The app connects to BigQuery using credentials from `GOOGLE_APPLICATION_CREDENTIALS` environment variable. Ensure your service account has `bigquery.dataViewer` role.

#### Stop the App
Press `Ctrl+C` in the terminal or close the browser tab.

#### Troubleshooting
- **"Credentials not found"** → Check `.env` and ensure `GOOGLE_APPLICATION_CREDENTIALS` path is correct
- **"Permission denied"** → Verify service account has BigQuery read access
- **"Table not found"** → Ensure Airflow DAGs have run and dbt models have been executed

---

## Troubleshooting

### Common Issues

#### 1. Python Version Error
**Error:** `Python 3.13 or higher required`

**Solution:**
```bash
# Check your Python version
python3 --version

# If using an older version, install Python 3.13+
# macOS: brew install python@3.13
# Ubuntu: sudo apt-get install python3.13
# or use pyenv for version management
```

#### 2. Streamlit Connection Refused
**Error:** `ConnectionRefusedError: [Errno 111] Connection refused`

**Solution:**
```bash
# Ensure GCP credentials are configured
echo $GOOGLE_APPLICATION_CREDENTIALS
cat .env  # Verify GCP_PROJECT_ID and other settings

# Test BigQuery connection
python3 -c "from google.cloud import bigquery; bq = bigquery.Client(); print(bq.project)"
```

#### 3. Airflow Cannot Start
**Error:** `docker-compose up` fails or services don't start

**Solution:**
```bash
# Check Docker is running
docker ps

# Initialize Airflow database first
docker-compose up airflow-init

# View detailed logs
docker-compose logs airflow-init
docker-compose logs airflow-webserver

# Reset and start fresh
docker-compose down -v
docker-compose up -d
```

#### 4. DAG Not Found in Airflow
**Error:** DAGs not appearing in Airflow UI even though files exist in `dags/`

**Solution:**
```bash
# Restart the DAG processor
docker-compose restart airflow-dagprocessor

# Check DAG file syntax
python3 dags/your_dag.py

# Verify dags folder path in Airflow config
docker-compose exec airflow-webserver airflow config get-value core dags_folder
```

#### 5. Permission Denied (GCP)
**Error:** `google.api_core.exceptions.PermissionDenied: 403`

**Solution:**
1. Verify service account has required roles:
   - `roles/storage.admin` (GCS)
   - `roles/bigquery.admin` (BigQuery)
   - `roles/logging.logWriter` (Logging)
2. Re-download service account key JSON
3. Update `GOOGLE_APPLICATION_CREDENTIALS` in `.env`

---

## Further Reading

### Official Documentation
- **[Streamlit Docs](https://docs.streamlit.io/)** — Dashboard framework
- **[Apache Airflow Docs](https://airflow.apache.org/docs/)** — Orchestration platform
- **[dbt Docs](https://docs.getdbt.com/)** — Data transformation
- **[Google Cloud Documentation](https://cloud.google.com/docs)** — GCP services
- **[Terraform AWS/GCP](https://registry.terraform.io/providers/hashicorp/google/latest)** — Infrastructure as code

### NBA Data Source
- **[shufinskiy/nba_data](https://github.com/shufinskiy/nba_data)** — Raw NBA statistics datasets

### Related Repositories & Examples
- [Streamlit BigQuery Demo](https://github.com/streamlit/demo-app-bigquery)
- [Airflow on Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose.html)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

---

## Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly (especially Airflow DAGs and BigQuery queries)
4. Submit a pull request

---

## License

[Add your license here]

---

## Support

For issues, questions, or suggestions:
- Check the [Troubleshooting](#troubleshooting) section
- Review logs: `docker-compose logs`
- Open an issue in the repository

---

**Last Updated:** March 2026
