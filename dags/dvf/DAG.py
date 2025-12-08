from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from dvf.task import load_dvf_to_postgres


with DAG(
    dag_id="load_dvf_to_postgres",
    description="Charge un échantillon DVF dans Postgres.",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["dvf"],
) as dag:
    PythonOperator(
        task_id="charger_dvf_dans_postgres",
        python_callable=load_dvf_to_postgres,
        op_kwargs={"rows": 1000000, "postgres_conn_id": "pg_prisma"},
    )
