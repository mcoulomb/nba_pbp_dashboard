variable "project" {
  description = "GCP Project ID"
  default = "nba-pbp-dashboard"
  type = string
}

variable "region" {
  description = "GCP Region"
  default = "us-central1"
  type = string
}

variable "google_storage_bucket_name" {
  description = "GCP Bucket Name"
  default = "mcoulomb-nba-pbp-data"
  type = string
}

variable "location" {
  description = "Country Code"
  default = "US"
  type = string
}

variable "big_query_dataset_name" {
  description = "Name of the bigquery dataset to create"
  default = "nba_pbp_data_raw"
  type = string
}