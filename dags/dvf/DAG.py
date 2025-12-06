from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from dvf.task import download_and_preview_dvf


with DAG(
    dag_id="test_valeur_fonciere",
    description="Petit DAG de démonstration pour tester l'UI Airflow.",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["dvf"],
) as dag:
    PythonOperator(
        task_id="afficher_valeurs_foncieres",
        python_callable=download_and_preview_dvf,
    )
