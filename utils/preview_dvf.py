"""Petit script pour afficher les colonnes DVF depuis la ressource publique."""

from __future__ import annotations

import io
import zipfile

import pandas as pd
import requests

RESOURCE_URL = (
    "https://www.data.gouv.fr/api/1/datasets/r/4d741143-8331-4b59-95c2-3b24a7bdbe3c"
)


def show_dvf_columns(rows: int | None = None) -> None:
    """Télécharge le fichier DVF et affiche les colonnes + un aperçu."""
    response = requests.get(RESOURCE_URL, timeout=60)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()
    content_disposition = response.headers.get("Content-Disposition", "")
    data = response.content

    if "zip" in content_type or content_disposition.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            inner_name = archive.namelist()[0]
            with archive.open(inner_name) as file_obj:
                df = pd.read_csv(file_obj, sep="|", dtype=str, nrows=rows)
    else:
        df = pd.read_csv(io.BytesIO(data), sep="|", dtype=str, nrows=rows)

    print("Colonnes DVF :")
    for col in df.columns:
        print(f"- {col}")

    print("\nDimensions du DataFrame :")
    print(df.shape)

if __name__ == "__main__":
    show_dvf_columns()
