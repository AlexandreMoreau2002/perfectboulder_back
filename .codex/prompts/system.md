# System Context - perfectBoulder Backend

## Project Identity

**perfectBoulder** is a climbing/bouldering application with a FastAPI backend following Hexagonal Architecture principles.

## Core Architecture

### Hexagonal Layout (Ports & Adapters)

```
app/
├── domain/          # Pure business entities (no framework dependencies)
├── application/     # Use cases / services (orchestration logic)
├── adapters/
│   ├── rest/       # HTTP/REST endpoints (FastAPI routes)
│   └── graphql/    # GraphQL endpoints (Strawberry)
├── infra/          # Infrastructure (database connections, external services)
├── config.py       # Centralized settings (pydantic-settings)
└── main.py         # Application factory
```

**Key Principle**: Routes/adapters NEVER contain business logic. They only:
- Receive requests
- Delegate to application services
- Return responses

### Technology Stack

- **Framework**: FastAPI (async)
- **GraphQL**: Strawberry GraphQL
- **Database**: PostgreSQL 16
- **ORM/Query**: Direct psycopg queries (no ORM currently)
- **Config**: Pydantic Settings
- **Validation**: Pydantic models
- **Linting**: Ruff 0.6.8
- **Runtime**: Uvicorn (ASGI server)
- **Containerization**: Docker + Docker Compose

## Configuration Philosophy

### Environment Variables

The app supports **two modes** for database config:

1. **Monolithic**: `DATABASE_URL` (full PostgreSQL connection string)
2. **Discrete**: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

Priority: `DATABASE_URL` takes precedence if both are provided.

**Implementation**: See `app/config.py` - `resolved_database_url` property handles the logic.

### Settings Pattern

```python
from app.config import get_settings

settings = get_settings()  # Cached via @lru_cache
database_url = settings.resolved_database_url
safe_url = settings.safe_database_url  # For logging (password masked)
```

## Startup Behavior

On application startup (`main.py`):
1. Settings are loaded from `.env`
2. FastAPI app is created
3. Routers are registered (health, graphql)
4. **Database connection probe runs** (`ensure_database_ready`)
   - If DB unreachable: app fails to start (fail-fast)
   - Logs safe connection string (password masked)

## API Endpoints

When running (`make start`):
- **Health**: `GET /health` - Returns app status + DB config (safe)
- **GraphQL**: `POST /graphql` - Strawberry GraphQL endpoint
- **Docs**: `GET /docs` - Auto-generated OpenAPI/Swagger UI

## Import Ordering Rule

**"Escalier" style** (staircase):
- Imports sorted by length (shortest to longest)
- Grouped by category: stdlib → third-party → local
- Applied when possible (doesn't break functionality)

Example:
```python
from app.config import get_settings
from app.domain.health.entities import HealthStatus
from app.infra.database.probe import ensure_database_ready
```

## Development Workflow

1. **Start services**: `make start` or `make start-build`
2. **View logs**: `make log`
3. **Access container**: `make code`
4. **Lint code**: `make lint`
5. **Connect to DB**: `make db-connect` (or via tasks: `db-connect`)

## Common Patterns

### Adding a New Feature

1. **Domain**: Create entity in `domain/<feature>/entities.py`
2. **Application**: Create service in `application/<feature>/service.py`
3. **Adapter**: Create route/schema in `adapters/rest/<feature>.py` or `adapters/graphql/`
4. **Wire**: Register router in `main.py`
5. **Test**: Verify manually or write tests
6. **Document**: Update README/COMMANDS if behavior changed

### Database Operations

Currently using raw `psycopg` (no ORM):
- Connection probe: `app/infra/database/probe.py`
- Pattern: Pass settings to functions that need DB access
- Future: Migrations will run at container startup

## Dos and Don'ts

### ✅ DO
- Respect layer boundaries (domain → application → adapters)
- Use `get_settings()` for all config access
- Fail fast on startup if DB unavailable
- Log safe URLs (use `settings.safe_database_url`)
- Keep routes thin (delegate to services)
- Return structured responses: `{"error": bool, "message": str, "data": ...}`

### ❌ DON'T
- Put business logic in routes
- Access database directly from routes
- Log passwords or secrets
- Hardcode configuration values
- Skip the startup database check
- Create cyclic dependencies between layers

## Security Reminders

- Auth tokens: `Authorization: Bearer <token>` pattern (not yet implemented)
- File uploads: Sanitize names, limit size, allowlist MIME types
- Input validation: Use Pydantic models
- SQL: Use parameterized queries (prevent injection)
- Secrets: Never in code, logs, or commits
