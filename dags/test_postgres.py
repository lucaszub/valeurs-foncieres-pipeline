from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

SQL_CREATE_DVF = """
CREATE TABLE IF NOT EXISTS dvf_raw (
    identifiant_document TEXT,
    reference_document TEXT,
    article_1_cgi TEXT,
    article_2_cgi TEXT,
    article_3_cgi TEXT,
    article_4_cgi TEXT,
    article_5_cgi TEXT,
    numero_disposition TEXT,
    date_mutation TEXT,
    nature_mutation TEXT,
    valeur_fonciere TEXT,
    numero_voie TEXT,
    btq TEXT,
    type_de_voie TEXT,
    code_voie TEXT,
    voie TEXT,
    code_postal TEXT,
    commune TEXT,
    code_departement TEXT,
    code_commune TEXT,
    prefixe_section TEXT,
    section TEXT,
    numero_plan TEXT,
    numero_volume TEXT,
    lot1_numero TEXT,
    lot1_surface_carrez TEXT,
    lot2_numero TEXT,
    lot2_surface_carrez TEXT,
    lot3_numero TEXT,
    lot3_surface_carrez TEXT,
    lot4_numero TEXT,
    lot4_surface_carrez TEXT,
    lot5_numero TEXT,
    lot5_surface_carrez TEXT,
    nombre_lots TEXT,
    code_type_local TEXT,
    type_local TEXT,
    identifiant_local TEXT,
    surface_reelle_bati TEXT,
    nombre_pieces_principales TEXT,
    nature_culture TEXT,
    nature_culture_speciale TEXT,
    surface_terrain TEXT
);
"""

with DAG(
    dag_id="test_prisma",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
):
    PostgresOperator(
        task_id="create_dvf_table",
        postgres_conn_id="pg_prisma",
        sql=SQL_CREATE_DVF,
    )
