from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
import tarfile
from airflow.sdk import task
from airflow.models import Param

@task(task_id="extract_tar")
def extract_tar(**context):
    dataset_name = f"{context["params"]["dataset"]}_{context["params"]["year"]}"
    # Open and extract the .tar.xz file
    with tarfile.open(f'dags/{dataset_name}.tar.xz', "r:xz") as tar:
        tar.extract(f'{dataset_name}.csv',dag.folder)  # Extract to a specified directory   

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
    params={
        "year": Param("2025", type="string"),
        "dataset": Param("cdnnba", type="string")
    }
)

# Define tasks
download_task = BashOperator(task_id='download_task',cwd=dag.folder, bash_command=f'wget https://github.com/shufinskiy/nba_data/raw/refs/heads/main/datasets/{dag.params["dataset"]}_{dag.params["year"]}.tar.xz',dag=dag)
upload_file = LocalFilesystemToGCSOperator(
    task_id="upload_file",
    src=f"{dag.folder}/{dag.params["dataset"]}_{dag.params["year"]}.csv",
    dst=f'{dag.params["dataset"]}_{dag.params["year"]}.csv',
    bucket='mcoulomb-nba-pbp-data',
    gcp_conn_id='gcp',
    dag=dag
)

delete_tar_files = BashOperator(task_id='delete_tar_files_task',cwd=dag.folder, bash_command='find . -name "*.tar.xz" -type f -delete',dag=dag, trigger_rule="all_done")
delete_csv_files = BashOperator(task_id='delete_csv_files_task',cwd=dag.folder, bash_command='find . -name "*.csv" -type f -delete',dag=dag, trigger_rule="all_done")

# Set task dependencies
download_task >> extract_tar() >> upload_file >> delete_tar_files >> delete_csv_files   

#if __name__ == "__main__":
 #   dag.test()