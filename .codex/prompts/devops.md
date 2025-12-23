# DevOps & Infrastructure Context

## Docker Setup

### Services

From `docker-compose.yml`:
- **backend**: FastAPI app (port 8000)
- **db**: PostgreSQL 16 (port 5432)

### Volumes

- `postgres_data`: Persistent database storage
- `./uploads`: Backend uploads (to be created when needed)

### Networking

- Backend connects to DB via hostname `db`
- Default credentials: `perfectboulder` / `perfectboulder`
- Database name: `perfectboulder`

## Makefile Commands

Reference: `backend/Makefile`

| Command            | Action                                  | Safety    |
|--------------------|-----------------------------------------|-----------|
| `make start`       | Start containers (detached)             | Safe      |
| `make start-build` | Rebuild and start                       | Safe      |
| `make restart`     | Stop then start (no rebuild)            | Safe      |
| `make stop`        | Stop and remove containers              | Safe      |
| `make reset`       | Rebuild everything                      | Safe      |
| `make reset-volumes` | **Nuclear**: Destroys DB volumes      | Dangerous |
| `make code`        | Open bash in backend container          | Safe      |
| `make log`         | Tail backend logs (50 lines)            | Safe      |
| `make lint`        | Run Ruff linter                         | Safe      |

**Dangerous commands** require confirmation!

## Environment Files

- `.env`: Local environment (NEVER commit)
- `.env.example`: Template with defaults (safe to commit)
- `.env.exemple`: Old template (to be removed)

## Database Administration

### Connect via psql

```bash
docker compose exec db psql -U perfectboulder -d perfectboulder
```

### Common psql commands

```sql
\dt              -- List tables
\d table_name    -- Describe table
\q               -- Quit
```

### Backup/Restore (when needed)

```bash
# Backup
docker compose exec db pg_dump -U perfectboulder perfectboulder > backup.sql

# Restore
docker compose exec -T db psql -U perfectboulder -d perfectboulder < backup.sql
```

## Deployment Patterns (Future)

From `.agent/infra.md`:

### CI/CD Principles
- Separate pipelines: `develop` (dev) vs `main` (prod)
- Artifact-based: Build archive, deploy to server
- Pre-deploy: Run tests (unit + coverage minimum)
- Deploy: Backup previous build + `.env`, then atomic swap

### Environment Separation
- DEV and PROD strictly separated
- Different domains/ports/paths
- Environment variables via CI secrets
- Never mix dev/prod configs

### Nginx (when added)

**Routes**:
- `/api/`: Proxy to backend, rewrite prefix, CORS enabled
- `/uploads/`: Alias to backend uploads folder, cache enabled

**Security**:
- Rate limiting on API + login endpoints
- Security headers (XFO, nosniff, referrer policy)
- Block dotfiles and config files
- Bot protection

**Deployment**:
- Test config in sandbox before applying
- Backup current config
- Graceful reload (`nginx -s reload`)
- Refuse dev/prod mixing (safeguards in script)

## Monitoring & Debugging

### View Logs

```bash
# Live logs
make log

# All services
docker compose logs -f

# Specific service
docker compose logs -f db
```

### Inspect Containers

```bash
# List running containers
docker compose ps

# Container stats
docker stats

# Network inspection
docker network ls
docker network inspect backend_default
```

### Database Connection Issues

1. Check service is running: `docker compose ps`
2. Check DB logs: `docker compose logs db`
3. Verify connection from backend:
   ```bash
   make code
   # Inside container:
   python -c "import psycopg; conn = psycopg.connect('postgresql://perfectboulder:perfectboulder@db:5432/perfectboulder'); print('OK')"
   ```

## Code Quality

### Linting with Ruff

Config: `.ruff.toml`

```bash
# Check (inside container)
docker compose exec backend python -m ruff check app

# Format (inside container)
docker compose exec backend python -m ruff format app

# Auto-fix
docker compose exec backend python -m ruff check app --fix
```

## Uploads Management (Future)

- Location: `./uploads/` (volume-mounted)
- Sanitization: Unicode → ASCII, safe characters only
- Size limit: 5MB recommended
- MIME allowlist: `image/jpeg`, `image/png`, `image/jpg`
- Serving: Via Nginx `/uploads/` route (not backend static)

## Testing Strategy (When Implemented)

- Runner: pytest (to be installed)
- Coverage: 80% threshold
- Mock external deps: DB, network, time
- No real DB connections in tests
- CI: Tests must pass before deployment
