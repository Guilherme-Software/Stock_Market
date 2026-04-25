from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="stocks_pipeline",
    start_date=datetime(2026, 4, 25, 16, 55),
    schedule="25 20 * * *", 
    catchup=False
) as dag:
    task = BashOperator(
        task_id="stocks_task",
        bash_command="jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.kernel_name=python3 /opt/airflow/dags/main.ipynb"
    )