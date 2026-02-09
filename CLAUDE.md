# Backend - Perfect Boulder

**FastAPI + Strawberry GraphQL + PostgreSQL + Cloudflare R2**

---

## AVANT TOUTE CHOSE

**Lis ces fichiers dans cet ordre :**

1. `/docs/README.md` - Point d'entree projet
2. `/docs/WORKFLOW.md` - Etape en cours
3. `/docs/prd.md` - Scope MVP
4. `backend/docs/architecture.md` - Archi backend complete
5. `/docs/specs/data-model.md` - Schema BDD

**Regles :** Architecture hexagonale stricte. Pas de dependance domain → infra.

---

## Structure

```
backend/
├── app/
│   ├── domain/          # Entities pures (pas de framework)
│   ├── application/     # Services metier
│   ├── adapters/        # GraphQL (inbound)
│   ├── infra/           # Database + R2 (outbound)
│   ├── config.py
│   └── main.py
├── migrations/          # Alembic
├── tests/
├── requirements.txt
└── docker-compose.yml
```

---

## Commandes

```bash
# Demarrer
make start

# Logs
make log

# Shell backend
make code

# Rebuild
make reset

# Migrations
alembic revision --autogenerate -m "message"
alembic upgrade head
```

---

## GraphQL

**Endpoint :** `http://localhost:8000/graphql`

**Schema :** Voir `/docs/specs/backend-architecture.md`

---

## Stack

- **FastAPI** : Framework web
- **Strawberry** : GraphQL
- **SQLAlchemy** : ORM
- **PostgreSQL** : Base de donnees
- **Alembic** : Migrations
- **Cloudflare R2** : Stockage video (S3-compatible)

---

## Regles de dev

1. **Domain** = entites pures (pas de SQLAlchemy, pas de FastAPI)
2. **Application** = services metier (pas de framework)
3. **Adapters** = GraphQL uniquement (pas de logique metier)
4. **Infra** = Database + R2 (implementations techniques)

**Flux :** GraphQL → Service → Repository → Database

---

## Tests

```bash
# Unit tests
pytest tests/unit

# Integration tests
pytest tests/integration
```

---

## Variables d'environnement

Voir `.env.exemple`

```env
DATABASE_URL=postgresql://user:pass@db:5432/perfectboulder
R2_ACCOUNT_ID=...
R2_ACCESS_KEY=...
R2_SECRET_KEY=...
R2_BUCKET=perfectboulder-videos
JWT_SECRET=...
```

---

## Documentation detaillee

- Architecture complete : `backend/docs/architecture.md`
- Data model : `/docs/specs/data-model.md`
- Lexique : `/docs/lexique.md`
