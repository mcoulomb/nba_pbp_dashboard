terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "static" {
  name          = "mcoulomb-nba-pbp-data"
  location      = "US"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
  
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id   = var.big_query_dataset_name
  project      = var.project
  location     = var.region
  friendly_name = var.big_query_dataset_name
  description  = "Dataset for raw data from GCS"
}