"""Utilitaires pour charger les données DVF dans Postgres (tout en texte)."""

from __future__ import annotations

import io
import zipfile
from typing import Dict, List

import pandas as pd
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook

RESOURCE_URL = (
    "https://www.data.gouv.fr/api/1/datasets/r/4d741143-8331-4b59-95c2-3b24a7bdbe3c"
)

DVF_COLUMN_MAPPING: Dict[str, str] = {
    "Identifiant de document": "identifiant_document",
    "Reference document": "reference_document",
    "1 Articles CGI": "article_1_cgi",
    "2 Articles CGI": "article_2_cgi",
    "3 Articles CGI": "article_3_cgi",
    "4 Articles CGI": "article_4_cgi",
    "5 Articles CGI": "article_5_cgi",
    "No disposition": "numero_disposition",
    "Date mutation": "date_mutation",
    "Nature mutation": "nature_mutation",
    "Valeur fonciere": "valeur_fonciere",
    "No voie": "numero_voie",
    "B/T/Q": "btq",
    "Type de voie": "type_de_voie",
    "Code voie": "code_voie",
    "Voie": "voie",
    "Code postal": "code_postal",
    "Commune": "commune",
    "Code departement": "code_departement",
    "Code commune": "code_commune",
    "Prefixe de section": "prefixe_section",
    "Section": "section",
    "No plan": "numero_plan",
    "No Volume": "numero_volume",
    "1er lot": "lot1_numero",
    "Surface Carrez du 1er lot": "lot1_surface_carrez",
    "2eme lot": "lot2_numero",
    "Surface Carrez du 2eme lot": "lot2_surface_carrez",
    "3eme lot": "lot3_numero",
    "Surface Carrez du 3eme lot": "lot3_surface_carrez",
    "4eme lot": "lot4_numero",
    "Surface Carrez du 4eme lot": "lot4_surface_carrez",
    "5eme lot": "lot5_numero",
    "Surface Carrez du 5eme lot": "lot5_surface_carrez",
    "Nombre de lots": "nombre_lots",
    "Code type local": "code_type_local",
    "Type local": "type_local",
    "Identifiant local": "identifiant_local",
    "Surface reelle bati": "surface_reelle_bati",
    "Nombre pieces principales": "nombre_pieces_principales",
    "Nature culture": "nature_culture",
    "Nature culture speciale": "nature_culture_speciale",
    "Surface terrain": "surface_terrain",
}

DVF_COLUMNS: List[str] = list(DVF_COLUMN_MAPPING.values())


def _read_csv(handle, rows: int | None) -> pd.DataFrame:
    return pd.read_csv(
        handle,
        sep="|",
        dtype=str,
        nrows=rows,
        na_filter=False,
        low_memory=False,
    )


def _download_dvf_dataframe(rows: int | None = None) -> pd.DataFrame:
    """Retourne un DataFrame DVF nettoyé et renommé."""
    response = requests.get(RESOURCE_URL, timeout=60)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()
    content_disposition = response.headers.get("Content-Disposition", "")
    data = response.content

    is_zip = "zip" in content_type or content_disposition.endswith(".zip")

    if is_zip:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            inner_name = archive.namelist()[0]
            with archive.open(inner_name) as file_obj:
                df = _read_csv(file_obj, rows)
    else:
        df = _read_csv(io.BytesIO(data), rows)

    missing = [col for col in DVF_COLUMN_MAPPING if col not in df.columns]
    if missing:
        raise ValueError(
            "Colonnes manquantes dans la ressource DVF: " + ", ".join(missing)
        )

    df = df.rename(columns=DVF_COLUMN_MAPPING)
    return df[DVF_COLUMNS]


def _prepare_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    clean_df = raw_df.copy()
    clean_df = clean_df.replace({"": None})
    return clean_df


def load_dvf_to_postgres(
    rows: int = 1000000,
    postgres_conn_id: str = "pg_prisma",
    table_name: str = "dvf_raw",
) -> None:
    """Charge un échantillon DVF dans Postgres via un PostgresHook."""
    raw_df = _download_dvf_dataframe(rows=rows)
    clean_df = _prepare_dataframe(raw_df)

    rows_to_insert = [tuple(row) for row in clean_df.itertuples(index=False, name=None)]

    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    hook.insert_rows(
        table=table_name,
        rows=rows_to_insert,
        target_fields=DVF_COLUMNS,
        commit_every=1000000,
    )
    print(f"Inséré {len(rows_to_insert)} lignes dans {table_name}")


if __name__ == "__main__":
    load_dvf_to_postgres(rows=10)