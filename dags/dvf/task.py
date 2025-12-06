"""Utilitaires pour récupérer les données DVF depuis data.gouv.fr."""

from __future__ import annotations

import io
import zipfile

import pandas as pd
import requests

RESOURCE_URL = "https://www.data.gouv.fr/api/1/datasets/r/4d741143-8331-4b59-95c2-3b24a7bdbe3c"


def download_and_preview_dvf(rows: int = 5) -> None:
    """Télécharge la dernière ressource DVF et affiche un aperçu avec pandas."""
    response = requests.get(RESOURCE_URL, timeout=60)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    data = response.content

    if "zip" in content_type or response.headers.get("Content-Disposition", "").endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            inner_name = archive.namelist()[0]
            with archive.open(inner_name) as file_obj:
                df = pd.read_csv(file_obj, sep="|", nrows=rows, low_memory=False)
    else:
        df = pd.read_csv(io.BytesIO(data), sep="|", nrows=rows, low_memory=False)

    print(df.columns)
    print("---------------------")
    print(df)


if __name__ == "__main__":
    download_and_preview_dvf()
