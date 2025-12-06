from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def holla() -> None:
    """Affiche un message pour confirmer que le DAG tourne bien."""
    print("holla this is Lulus")


with DAG(
    dag_id="lukus_test",
    description="Petit dag de lulus",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["lukus"],
) as dag:
    PythonOperator(
        task_id="hola_luks",
        python_callable=holla,
    )
