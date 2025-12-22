# Backend API

Minimal FastAPI backend with Docker support, PostgreSQL, and GraphQL.

## Getting Started

1. Configure environment variables (do not commit `.env`):
   ```bash
   cp .env.example .env
   ```

2. Start the project:
   ```bash
   make up
   ```

3. Access the API:
   - Health check: http://localhost:8000/health
   - Database config: http://localhost:8000/database/config
   - GraphQL: http://localhost:8000/graphql
   - Docs: http://localhost:8000/docs

4. Other commands:
   - `make logs`: View logs
   - `make down`: Stop containers
   - `make lint`: Run lint checks (ruff)

## Architecture

The backend follows a lightweight hexagonal layout:
- `domain/`: pure domain objects.
- `application/`: use cases/services producing responses.
- `adapters/rest` and `adapters/graphql`: transport adapters.
- `infra/`: database and other infrastructure (e.g., connection probe).

## Configuration

| Variable          | Description                                   | Default            |
| ----------------- | --------------------------------------------- | ------------------ |
| `APP_NAME`        | Application name                              | `Backend API`      |
| `DATABASE_URL`    | Full PostgreSQL URL (takes priority)          | _empty_            |
| `DB_HOST`         | Database host                                 | `db`               |
| `DB_PORT`         | Database port                                 | `5432`             |
| `DB_USER`         | Database user                                 | `perfectboulder`   |
| `DB_PASSWORD`     | Database password                             | `perfectboulder`   |
| `DB_NAME`         | Database name                                 | `perfectboulder`   |

> `docker-compose.yml` wires the backend to a `postgres:16` service with a persisted volume.
