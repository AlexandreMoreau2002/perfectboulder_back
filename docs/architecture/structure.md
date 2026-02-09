# Structure Backend

**Organisation des dossiers**

---

## Arborescence

```
backend/
├── app/
│   ├── domain/              # Core metier (entities pures)
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   ├── video.py
│   │   │   ├── session.py
│   │   │   └── croix.py
│   │   └── exceptions.py
│   │
│   ├── application/         # Use cases / business logic
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── video_service.py
│   │   │   └── session_service.py
│   │   └── dtos/
│   │       ├── video_dto.py
│   │       └── session_dto.py
│   │
│   ├── adapters/            # Interfaces externes (inbound)
│   │   └── graphql/
│   │       ├── schema.py         # Schema GraphQL principal
│   │       ├── queries.py        # Queries GraphQL
│   │       ├── mutations.py      # Mutations GraphQL
│   │       └── types.py          # Types GraphQL
│   │
│   ├── infra/               # Infrastructure (outbound)
│   │   ├── database/
│   │   │   ├── models.py         # SQLAlchemy models
│   │   │   ├── repositories/
│   │   │   │   ├── user_repo.py
│   │   │   │   ├── video_repo.py
│   │   │   │   └── session_repo.py
│   │   │   └── session.py        # DB session factory
│   │   │
│   │   └── storage/
│   │       └── r2_client.py      # Cloudflare R2 client
│   │
│   ├── config.py            # Settings (pydantic)
│   └── main.py              # FastAPI app + GraphQL mount
│
├── migrations/              # Alembic migrations
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                    # Documentation technique
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

---

## Conventions

- **Fichiers** : snake_case (`video_service.py`)
- **Classes** : PascalCase (`VideoService`)
- **Fonctions** : snake_case (`get_feed()`)
- **Constantes** : UPPER_CASE (`MAX_VIDEO_SIZE`)
