# Notes pour l'agent Codex

## Aperçu du projet
- Dépôt pour lancer Apache Airflow en local via `docker compose` (stack officielle 2.10.0).
- Dossiers montés : `dags/`, `logs/`, `plugins/`, `config/`.
- Documentation utilisateur principale : `docs/airflow-setup.md` (guide d'installation, DAG de démo, rafraîchissement UI, désactivation des DAGs exemples).

## Dossiers importants
- `docker-compose.yaml` : configuration complète (Postgres, Redis, webserver, scheduler, worker, triggerer, init).
- `dags/` : DAGs disponibles (`hello_ui_demo.py`, `hello_re_test.py`, `dvf/DAG.py` + utilitaires).
- `.env` : définit `AIRFLOW_UID`/`AIRFLOW_GID` pour aligner les permissions.
- `requirements.txt` : dépendances Python additionnelles (pandas, requests) utilisées par le DAG DVF.

## Consignes
- Préférer `docker compose` (et non `docker-compose`).
- Lorsqu'on ajoute des DAGs, garder un style simple (PythonOperator, logs explicites) pour faciliter les tests via l'UI.
- Si des instructions supplémentaires sont nécessaires, enrichir `docs/airflow-setup.md` plutôt que d'éparpiller la doc.
- Pour toute demande de commit/push, faire systématiquement un "tech check" :
  - `git status -sb` pour voir les fichiers modifiés.
  - `git diff` (ou `git diff --stat`) pour examiner les évolutions.
  - Résumer les changements avant de lancer `git add/commit/push`.

## Commandes utiles
- Initialisation : `docker compose up airflow-init`
- Lancement complet : `docker compose up`
- Arrêt : `docker compose down`
- Réinitialisation : `docker compose down --volumes --remove-orphans`

Ces notes doivent aider à répondre rapidement aux requêtes liées au projet Airflow local et à assurer un flux de commits propre.
