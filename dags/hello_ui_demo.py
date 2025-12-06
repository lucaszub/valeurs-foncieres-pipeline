from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def say_hello() -> None:
    """Log a short message pour valider que le DAG fonctionne."""
    print("Bonjour depuis Airflow !")


with DAG(
    dag_id="hello_ui_demo",
    description="Petit DAG de démonstration pour tester l'UI Airflow.",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["demo"],
) as dag:
    PythonOperator(
        task_id="afficher_message",
        python_callable=say_hello
    )
