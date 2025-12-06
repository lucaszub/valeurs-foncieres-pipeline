from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG(
    dag_id="test_prisma",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False
):
    test = PostgresOperator(
        task_id="check_conn",
        postgres_conn_id="pg_prisma",
        sql="SELECT now();"
    )
