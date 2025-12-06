# Notes pour l'agent Codex

## Aperçu du projet
- Dépôt minimal pour lancer Apache Airflow en local via `docker compose` (stack officielle 2.10.0).
- Dossiers montés : `dags/`, `logs/`, `plugins/`, `config/`.
- Documentation utilisateur principale : `docs/airflow-setup.md` (guide d'installation + sections sur le DAG de démo et la mise à jour via l'UI).

## Dossiers importants
- `docker-compose.yaml` : configuration complète (Postgres, Redis, webserver, scheduler, worker, triggerer, init).
- `dags/` : contient les DAGs d'exemple (`hello_ui_demo.py`, `hello_re_test.py`).
- `.env` : définit `AIRFLOW_UID`/`AIRFLOW_GID` pour aligner les permissions.

## Consignes
- Préférer `docker compose` (et non `docker-compose`).
- Lorsqu'on ajoute des DAGs, garder un style simple (PythonOperator, logs explicites) pour faciliter les tests via l'UI.
- Si des instructions supplémentaires sont nécessaires, enrichir `docs/airflow-setup.md` plutôt que d'éparpiller la doc.

## Commandes utiles
- Initialisation : `docker compose up airflow-init`
- Lancement complet : `docker compose up`
- Arrêt : `docker compose down`
- Réinitialisation : `docker compose down --volumes --remove-orphans`

Ces notes doivent aider à répondre rapidement aux futures requêtes liées au projet Airflow local.
