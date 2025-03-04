from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='crypto_etl_dag',
    default_args=default_args,
    schedule_interval='*/3 * * * *',  # Chạy mỗi 3 phút
    catchup=False  # Tránh chạy backlog quá khứ
) as dag:

    extract_task = BashOperator(
        task_id='extract_coingecko_file',
        bash_command='python /opt/airflow/dags/scripts/extract_coingecko.py'
    )

    load_task = BashOperator(
        task_id='load_to_postgres_file',
        bash_command='python /opt/airflow/dags/scripts/load_to_postgres.py'
    )

    extract_task >> load_task
