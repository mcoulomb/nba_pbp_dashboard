from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.sdk import task
from airflow.models import Param

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    dag_id='create_bigquery_external_table_dag',
    default_args=default_args,
    description='Creates a bigquery external table with a GCS bucket as the source',
    schedule='@yearly',
    catchup=False,
    tags=['external table', 'BQ'],
    params={
        "bucket": Param("mcoulomb-nba-pbp-data", type="string"),
        "external_table_name": Param("mcoulomb-nba-pbp-data-raw", type="string")
    }
)

# Define tasks
create_external_table = GCSToBigQueryOperator(
    task_id="create_external_table",
    bucket="mcoulomb-nba-pbp-data",
    source_objects=["*.csv"],
    source_format="csv",
    destination_project_dataset_table=f"nba_pbp_data_raw.nba_pbp_data_external",
    write_disposition="WRITE_TRUNCATE",
    external_table=True,
    autodetect=True,
    field_delimiter=",",
    quote_character='"',
    deferrable=True,
    gcp_conn_id='gcp',
    force_delete=True,
    allow_jagged_rows=True,
    dag=dag
)


# Set task dependencies
create_external_table

#if __name__ == "__main__":
 #   dag.test()