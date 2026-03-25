from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
import tarfile
from airflow.sdk import task

@task(task_id="extract_tar")
def extract_tar(**context):
    # Open and extract the .tar.xz file
    with tarfile.open('dags/nbastats_2016.tar.xz', "r:xz") as tar:
        tar.extract('nbastats_2016.csv',dag.folder)  # Extract to a specified directory   

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    dag_id='move_pbp_data_into_gcs_bucket',
    default_args=default_args,
    description='Retrieves pbp dataset from https://github.com/shufinskiy/nba_data and loads it into a GCS bucket',
    schedule='@daily',
    catchup=False,
    tags=['example', 'hello-world'],
)

# Define tasks
download_task = BashOperator(task_id='download_task',cwd=dag.folder, bash_command='wget https://github.com/shufinskiy/nba_data/raw/refs/heads/main/datasets/nbastats_2016.tar.xz',dag=dag)
upload_file = LocalFilesystemToGCSOperator(
    task_id="upload_file",
    src=f"{dag.folder}/nbastats_2016.csv",
    dst='nbastats_2016.csv',
    bucket='mcoulomb-nba-pbp-data',
    gcp_conn_id='gcp',
    dag=dag
)

# Set task dependencies
download_task >> extract_tar() >> upload_file   

#if __name__ == "__main__":
 #   dag.test()