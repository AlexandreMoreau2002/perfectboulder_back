# Commandes du Projet (Backend)

Ce fichier recense les commandes utiles pour le développement, similaires aux `scripts` d'un `package.json`.

## Environnement Docker (Makefile)

Les commandes suivantes s'exécutent via `make <commande>` :

- **`make up`** : Démarre l'environnement en arrière-plan (reconstruit si nécessaire).
  - *Equivalent* : `docker compose up --build -d`
- **`make down`** : Arrête et supprime les conteneurs.
  - *Equivalent* : `docker compose down`
- **`make logs`** : Affiche les logs du backend en continu.
  - *Equivalent* : `docker compose logs -f`
- **`make shell`** : Ouvre un terminal Bash dans le conteneur backend.
  - *Equivalent* : `docker compose exec backend /bin/bash`
- **`make lint`** : Lance l'analyse statique du code avec Ruff.
  - *Equivalent* : `python -m ruff check app` (Note: à exécuter de préférence dans le conteneur ou venv)

## Base de Données

Commandes pour interagir avec PostgreSQL :

- **Se connecter à la DB en ligne de commande (psql)** :
  ```bash
  docker compose exec db psql -U perfectboulder -d perfectboulder
  ```
  *(Note : L'utilisateur et la base sont `perfectboulder` par défaut, définis dans `docker-compose.yml`)*

## Tests & Qualité

- **Linter (Ruff)** :
  ```bash
  docker compose exec backend python -m ruff check app
  ```
- **Formatter (si installé)** :
  Si vous utilisez Ruff comme formateur :
  ```bash
  docker compose exec backend python -m ruff format app
  ```
