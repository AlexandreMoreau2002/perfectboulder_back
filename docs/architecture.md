# Backend Architecture - Perfect Boulder

**Version** : 1.0
**Date** : 2026-02-09
**Pattern** : Hexagonal (Ports & Adapters)
**Stack** : FastAPI + Strawberry GraphQL + PostgreSQL + SQLAlchemy

---

## Structure des dossiers

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
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

---

## Flux de dependances

```
GraphQL (adapters)
    ↓
Services (application)
    ↓
Entities (domain)
    ↑
Repositories (infra/database)
    ↑
SQLAlchemy Models (infra/database)
```

**Regle d'or :** Les couches internes (domain) ne dependent JAMAIS des couches externes (infra/adapters).

---

## Responsabilites par couche

### 1. domain/ (Core metier)

**Entities pures** - Pas de dependance externe (ni FastAPI, ni SQLAlchemy, ni GraphQL).

```python
# domain/entities/video.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Video:
    id: str
    user_id: str
    video_url: str
    caption: Optional[str]
    color: str
    grade: str
    status: str  # flash | top | project
    session_id: Optional[str]
    croix_id: Optional[str]
    created_at: datetime
```

**Exceptions metier** :
```python
# domain/exceptions.py
class VideoNotFoundError(Exception): pass
class UnauthorizedError(Exception): pass
```

---

### 2. application/ (Business logic)

**Services** - Orchestration metier, pas de framework.

```python
# application/services/video_service.py
from domain.entities.video import Video
from infra.database.repositories.video_repo import VideoRepository

class VideoService:
    def __init__(self, video_repo: VideoRepository):
        self.video_repo = video_repo

    def get_feed(self, limit: int, offset: int) -> list[Video]:
        return self.video_repo.find_all(limit=limit, offset=offset)

    def create_video(self, user_id: str, data: dict) -> Video:
        video = Video(...)  # validation metier ici
        return self.video_repo.save(video)
```

**DTOs** - Pour passer des donnees entre couches.

---

### 3. adapters/graphql/ (Interface GraphQL)

**Schema GraphQL** - Point d'entree API.

```python
# adapters/graphql/schema.py
import strawberry
from .queries import Query
from .mutations import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

**Types GraphQL** :
```python
# adapters/graphql/types.py
import strawberry

@strawberry.type
class VideoType:
    id: str
    user_id: str
    video_url: str
    caption: str | None
    color: str
    grade: str
    status: str
    like_count: int
    is_liked_by_me: bool
    created_at: str
```

**Queries** :
```python
# adapters/graphql/queries.py
import strawberry
from application.services.video_service import VideoService

@strawberry.type
class Query:
    @strawberry.field
    def feed(self, limit: int = 10, offset: int = 0) -> list[VideoType]:
        service = VideoService(...)  # injection dependance
        videos = service.get_feed(limit, offset)
        return [VideoType(...) for v in videos]
```

**Mutations** :
```python
# adapters/graphql/mutations.py
import strawberry

@strawberry.type
class Mutation:
    @strawberry.mutation
    def post_video(self, video_url: str, caption: str, ...) -> VideoType:
        # validation + appel service
        pass
```

---

### 4. infra/database/ (Acces donnees)

**SQLAlchemy Models** :
```python
# infra/database/models.py
from sqlalchemy import Column, String, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VideoModel(Base):
    __tablename__ = 'videos'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    video_url = Column(Text, nullable=False)
    caption = Column(Text)
    color = Column(String(20), nullable=False)
    grade = Column(String(10), nullable=False)
    status = Column(Enum('flash', 'top', 'project', name='video_status'))
    # ...
```

**Repositories** :
```python
# infra/database/repositories/video_repo.py
from sqlalchemy.orm import Session
from infra.database.models import VideoModel
from domain.entities.video import Video

class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self, limit: int, offset: int) -> list[Video]:
        models = self.db.query(VideoModel)\
            .order_by(VideoModel.created_at.desc())\
            .limit(limit).offset(offset).all()
        return [self._to_entity(m) for m in models]

    def save(self, video: Video) -> Video:
        model = VideoModel(**video.__dict__)
        self.db.add(model)
        self.db.commit()
        return video

    def _to_entity(self, model: VideoModel) -> Video:
        return Video(
            id=str(model.id),
            user_id=str(model.user_id),
            # ...
        )
```

---

### 5. infra/storage/ (Cloudflare R2)

**R2 Client** :
```python
# infra/storage/r2_client.py
import boto3

class R2Client:
    def __init__(self, account_id: str, access_key: str, secret_key: str):
        self.s3 = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def generate_presigned_url(self, bucket: str, key: str) -> str:
        """URL signee pour upload direct client → R2"""
        return self.s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600,  # 1h
        )
```

---

## GraphQL Schema complet (MVP)

```graphql
type User {
  id: ID!
  pseudo: String!
  avatar_url: String
  bio: String
}

type Video {
  id: ID!
  user: User!
  video_url: String!
  caption: String
  color: String!
  grade: String!
  status: VideoStatus!
  like_count: Int!
  is_liked_by_me: Boolean!
  created_at: String!
}

enum VideoStatus {
  FLASH
  TOP
  PROJECT
}

type Session {
  id: ID!
  date: String!
  gym: Gym
  feeling: Int
  notes: String
  croix: [Croix!]!
}

type Croix {
  id: ID!
  photo_url: String!
  color: String!
  grade: String!
  status: VideoStatus!
  notes: String
}

type Gym {
  id: ID!
  name: String!
  location: String
}

type AuthPayload {
  token: String!
  user: User!
}

type Query {
  feed(limit: Int = 10, offset: Int = 0): [Video!]!
  video(id: ID!): Video
  user(id: ID!): User
  me: User!
  searchUsers(query: String!): [User!]!
  mySessions: [Session!]!
  myCroix: [Croix!]!
}

type Mutation {
  signup(email: String!, password: String!, pseudo: String!): AuthPayload!
  login(email: String!, password: String!): AuthPayload!

  postVideo(
    video_url: String!
    caption: String
    color: String!
    grade: String!
    status: VideoStatus!
    session_id: ID
  ): Video!

  likeVideo(video_id: ID!): Boolean!
  unlikeVideo(video_id: ID!): Boolean!

  createSession(
    date: String!
    gym_id: ID
    feeling: Int
    notes: String
  ): Session!

  createCroix(
    session_id: ID
    photo_url: String!
    color: String!
    grade: String!
    status: VideoStatus!
    notes: String
  ): Croix!

  getPresignedUploadUrl(filename: String!): String!
}
```

---

## Workflow dev backend

### Ajouter une nouvelle feature

1. **Domain** : Creer entite pure (`domain/entities/`)
2. **Infra** : Creer model SQLAlchemy + migration (`infra/database/models.py`)
3. **Infra** : Creer repository (`infra/database/repositories/`)
4. **Application** : Creer service (`application/services/`)
5. **Adapters** : Creer type GraphQL + query/mutation (`adapters/graphql/`)
6. **Main** : Injecter dependances dans le schema

### Exemple : Ajouter endpoint "getVideoLikes"

1. **Query GraphQL** :
```python
@strawberry.field
def video_likes(self, video_id: str) -> list[UserType]:
    service = VideoService(...)
    return service.get_video_likes(video_id)
```

2. **Service** :
```python
def get_video_likes(self, video_id: str) -> list[User]:
    return self.like_repo.find_by_video(video_id)
```

3. **Repository** :
```python
def find_by_video(self, video_id: str) -> list[User]:
    # SQL query
```

---

## Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY: str
    R2_SECRET_KEY: str
    R2_BUCKET: str
    JWT_SECRET: str

    class Config:
        env_file = '.env'

settings = Settings()
```

---

## Migrations (Alembic)

```bash
# Init
alembic init migrations

# Creer migration
alembic revision --autogenerate -m "create videos table"

# Appliquer
alembic upgrade head
```

---

## Tests

```python
# tests/test_video_service.py
def test_get_feed():
    repo = MockVideoRepository()
    service = VideoService(repo)
    videos = service.get_feed(limit=10, offset=0)
    assert len(videos) == 10
```

---

## Commandes Docker

```bash
# Demarrer
make start

# Logs
make log

# Shell backend
make code

# Rebuild
make reset
```
