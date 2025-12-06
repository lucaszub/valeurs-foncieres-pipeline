# 1. Prérequis

- Docker installé
- Docker Compose installé
- Minimum : 4 Go RAM dédiée à Docker

---

# 2. Créer un dossier projet

```
mkdir airflow
cd airflow
```

---

# 3. Télécharger le docker-compose officiel d’Airflow

```
curl -LfO https://airflow.apache.org/docs/apache-airflow/2.10.0/docker-compose.yaml
```

(Vérifie la version sur le site officiel si besoin.)

---

# 4. Créer les dossiers nécessaires

```
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

---

# 5. Initialiser Airflow

```
docker compose up airflow-init
```

Cela crée :

- la base Postgres interne
- l’utilisateur admin
- la structure Airflow

---

# 6. Lancer Airflow

```
docker compose up
```

L'UI Web est accessible sur :

```
http://localhost:8080
```

Identifiants par défaut :

```
login : airflow
mdp   : airflow
```

---

# 7. Ajouter tes DAGS

Place tes fichiers `.py` dans :

```
./dags/
```

Airflow les détecte automatiquement.

---

# 8. Stopper Airflow

```
docker compose down
```

---

# 9. Reset complet si tu veux repartir de zéro

⚠️ Efface la base + tous les runs.

```
docker compose down --volumes --remove-orphans
docker compose up airflow-init
docker compose up
```


---

# 10. DAG de démonstration

Un DAG minimal nommé `hello_ui_demo` est déjà disponible dans `./dags/hello_ui_demo.py`.  
Il ne fait qu'exécuter une fonction Python qui écrit "Bonjour depuis Airflow !" dans les logs.

1. Assure-toi que les services tournent (`docker compose up`).
2. Va dans l'UI → menu *DAGs* → recherche `hello_ui_demo`.
3. Active l'interrupteur à gauche, puis clique sur le bouton **Play** pour lancer un run manuel.

Tu peux t'en servir comme point de départ pour créer tes propres workflows.

---

# 11. Mettre à jour un DAG et forcer l'UI à se rafraîchir

Airflow recharge automatiquement les fichiers du dossier `./dags/`, mais tu peux accélérer les choses avec ce flux rapide :

1. Modifie ou ajoute ton fichier dans `./dags/` puis sauvegarde-le.
2. Vérifie que le scheduler détecte bien la mise à jour en regardant les logs :  
   `docker compose logs -f airflow-scheduler`
3. Si l'UI ne montre toujours pas la nouvelle version, redémarre uniquement les services concernés :  
   `docker compose restart airflow-scheduler airflow-webserver`
4. Dans l'UI, clique sur `Refresh` (bouton en haut à droite) ou recharge la page pour forcer l'UI à recharger la liste.

Ces étapes évitent de tout redémarrer et garantissent que les modifications de DAG sont visibles rapidement depuis l'interface web.


---

# 12. Désactiver les DAGs exemples fournis par Airflow

Le fichier `docker-compose.yaml` force maintenant `AIRFLOW__CORE__LOAD_EXAMPLES` à `false`.
Cela évite que les DAGs tutoriels livrés par défaut apparaissent dans l'UI.

- Si tu lances l'environnement pour la première fois après ce changement, il n'y aura simplement aucun DAG exemple.
- Si tu avais déjà démarré Airflow avant, supprime la base pour repartir propre :
  `docker compose down --volumes --remove-orphans` puis `docker compose up airflow-init` et `docker compose up`.

Tu peux bien sûr remettre la valeur à `true` dans `docker-compose.yaml` si tu veux les tutoriels à nouveau.
