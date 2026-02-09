# Backend Documentation

**FastAPI + Strawberry GraphQL + PostgreSQL + Cloudflare R2**

---

## Fichiers

| Fichier | Description |
|---------|-------------|
| `architecture.md` | Architecture hexagonale complete + exemples code |
| `graphql-schema.md` | Schema GraphQL complet (a creer si besoin) |
| `workflows.md` | Workflows dev (a creer si besoin) |

---

## Pour commencer

1. Lis `/docs/README.md` (point d'entree projet)
2. Lis `/docs/WORKFLOW.md` (etape en cours)
3. Lis `/docs/prd.md` (scope MVP)
4. Lis `architecture.md` (archi backend)
5. Lis `/docs/specs/data-model.md` (schema BDD)

---

## Structure backend

```
backend/
├── app/
│   ├── domain/          # Entities pures
│   ├── application/     # Services metier
│   ├── adapters/        # GraphQL
│   ├── infra/           # Database + R2
│   ├── config.py
│   └── main.py
├── migrations/          # Alembic
├── tests/
└── docs/               ← Tu es ici
```

---

## Commandes

```bash
make start         # Demarrer services
make log           # Voir logs
make code          # Shell backend
make reset         # Rebuild
```

---

## Regles architecture

**Hexagonal (Ports & Adapters) :**
- Domain ne depend de RIEN (entites pures)
- Application depend de Domain uniquement
- Adapters/Infra dependent de Application + Domain

**Flux :** `GraphQL → Service → Repository → Database`

---

*Voir `architecture.md` pour details complets*
