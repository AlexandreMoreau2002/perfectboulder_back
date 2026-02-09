# Architecture Hexagonale

**Pattern** : Ports & Adapters
**Principe** : Separation domain/infrastructure

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

Contenu :
- Entities (User, Video, Session, Croix)
- Exceptions metier (VideoNotFoundError, UnauthorizedError)
- Value objects si necessaire

**Ce qu'on PEUT faire :**
- Dataclasses Python pures
- Logique metier pure (validation, calculs)
- Lever des exceptions metier

**Ce qu'on NE PEUT PAS faire :**
- Importer SQLAlchemy
- Importer FastAPI/Strawberry
- Faire des appels DB/API
- Dependre de infra/adapters

---

### 2. application/ (Business logic)

**Services** - Orchestration metier, pas de framework.

Contenu :
- Services (AuthService, VideoService, SessionService)
- DTOs (Data Transfer Objects)
- Interfaces de repositories (abstractions)

**Ce qu'on PEUT faire :**
- Orchestrer plusieurs repositories
- Appliquer la logique metier
- Valider les entrees
- Transformer entities ↔ DTOs

**Ce qu'on NE PEUT PAS faire :**
- Importer FastAPI/Strawberry
- Connaitre GraphQL/REST
- Acceder directement a SQLAlchemy
- Dependre de infra (sauf interfaces)

---

### 3. adapters/ (Interfaces externes - inbound)

**GraphQL** - Point d'entree API.

Contenu :
- Schema GraphQL
- Queries
- Mutations
- Types GraphQL

**Responsabilites :**
- Valider input GraphQL
- Appeler services
- Formatter output GraphQL
- Gerer auth (JWT)

**PAS de logique metier ici** - Tout delegue aux services.

---

### 4. infra/ (Infrastructure - outbound)

**Database + Storage** - Implementations techniques.

Contenu :
- Models SQLAlchemy
- Repositories (implementations)
- DB session factory
- R2 client (Cloudflare)

**Responsabilites :**
- Acces BDD
- Acces stockage (R2)
- Mapper models ↔ entities
- Gerer transactions

---

## Flux typique (exemple : poster une video)

```
1. GraphQL Mutation postVideo(...)
   ↓
2. VideoService.create_video(...)
   ↓
3. VideoRepository.save(video_entity)
   ↓
4. SQLAlchemy VideoModel.insert(...)
   ↓
5. PostgreSQL INSERT
```

**Retour :**
```
PostgreSQL → VideoModel → Video (entity) → VideoType (GraphQL) → Client
```

---

## Pourquoi hexagonal ?

**Avantages :**
- Domain metier isole (testable sans DB/framework)
- Changement de framework facile (GraphQL → REST, FastAPI → autre)
- Changement de BDD facile (PostgreSQL → MongoDB)
- Tests simples (mock repositories)

**Prix a payer :**
- Plus de fichiers
- Mapping entity ↔ model
- Apprentissage pattern

**Conclusion :** Indispensable pour projets >3 mois.
