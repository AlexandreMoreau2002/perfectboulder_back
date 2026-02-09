# GraphQL Schema

**API GraphQL complet pour Perfect Boulder MVP**

---

## Endpoint

**URL :** `http://localhost:8000/graphql`

---

## Types

### User

```graphql
type User {
  id: ID!
  pseudo: String!
  avatar_url: String
  bio: String
}
```

**Description :** Utilisateur de l'application.

---

### Video

```graphql
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
```

**Description :** Video postee dans le feed social.

**Champs :**
- `user` : Auteur de la video
- `video_url` : URL de la video (Cloudflare R2)
- `caption` : Texte libre (optionnel)
- `color` : Couleur de la prise
- `grade` : Cotation (ex: "6A+")
- `status` : Flash / Top / Projet
- `like_count` : Nombre de likes
- `is_liked_by_me` : Like par l'utilisateur courant
- `created_at` : Date de creation (ISO 8601)

---

### VideoStatus

```graphql
enum VideoStatus {
  FLASH
  TOP
  PROJECT
}
```

**Description :** Statut de reussite d'un bloc.

---

### Session

```graphql
type Session {
  id: ID!
  date: String!
  gym: Gym
  feeling: Int
  notes: String
  croix: [Croix!]!
}
```

**Description :** Seance de grimpe (logbook prive).

**Champs :**
- `date` : Date de la seance (ISO 8601)
- `gym` : Salle (optionnel)
- `feeling` : Ressenti 1-5 (optionnel)
- `notes` : Notes libres (optionnel)
- `croix` : Liste des croix de la seance

---

### Croix

```graphql
type Croix {
  id: ID!
  photo_url: String!
  color: String!
  grade: String!
  status: VideoStatus!
  notes: String
}
```

**Description :** Croix = bloc tente/reussi dans une seance (photo privee).

**Champs :**
- `photo_url` : URL de la photo du bloc
- `color` : Couleur de la prise
- `grade` : Cotation
- `status` : Flash / Top / Projet
- `notes` : Notes libres (optionnel)

---

### Gym

```graphql
type Gym {
  id: ID!
  name: String!
  location: String
}
```

**Description :** Salle d'escalade.

---

### AuthPayload

```graphql
type AuthPayload {
  token: String!
  user: User!
}
```

**Description :** Reponse d'authentification (signup/login).

**Champs :**
- `token` : JWT pour authentification
- `user` : Utilisateur connecte

---

## Queries

### feed

```graphql
feed(limit: Int = 10, offset: Int = 0): [Video!]!
```

**Description :** Recupere le feed de videos (ordre chronologique inverse).

**Parametres :**
- `limit` : Nombre de videos a retourner (defaut: 10)
- `offset` : Decalage pour pagination (defaut: 0)

**Exemple :**
```graphql
query {
  feed(limit: 10, offset: 0) {
    id
    user {
      pseudo
      avatar_url
    }
    video_url
    caption
    color
    grade
    status
    like_count
    is_liked_by_me
    created_at
  }
}
```

---

### video

```graphql
video(id: ID!): Video
```

**Description :** Recupere une video par ID.

**Parametres :**
- `id` : ID de la video

---

### user

```graphql
user(id: ID!): User
```

**Description :** Recupere un utilisateur public par ID.

**Parametres :**
- `id` : ID de l'utilisateur

---

### me

```graphql
me: User!
```

**Description :** Recupere l'utilisateur courant (authentifie).

**Authentification :** Requise (JWT)

---

### searchUsers

```graphql
searchUsers(query: String!): [User!]!
```

**Description :** Recherche d'utilisateurs par pseudo.

**Parametres :**
- `query` : Texte de recherche (pseudo)

**Exemple :**
```graphql
query {
  searchUsers(query: "alex") {
    id
    pseudo
    avatar_url
  }
}
```

---

### mySessions

```graphql
mySessions: [Session!]!
```

**Description :** Recupere les seances de l'utilisateur courant (logbook).

**Authentification :** Requise (JWT)

**Exemple :**
```graphql
query {
  mySessions {
    id
    date
    gym {
      name
    }
    feeling
    notes
    croix {
      id
      color
      grade
      status
    }
  }
}
```

---

### myCroix

```graphql
myCroix: [Croix!]!
```

**Description :** Recupere toutes les croix de l'utilisateur courant.

**Authentification :** Requise (JWT)

---

## Mutations

### signup

```graphql
signup(
  email: String!
  password: String!
  pseudo: String!
): AuthPayload!
```

**Description :** Creer un compte utilisateur.

**Parametres :**
- `email` : Email unique
- `password` : Mot de passe (min 8 caracteres)
- `pseudo` : Pseudo unique

**Exemple :**
```graphql
mutation {
  signup(
    email: "alex@example.com"
    password: "securepass123"
    pseudo: "alex"
  ) {
    token
    user {
      id
      pseudo
    }
  }
}
```

---

### login

```graphql
login(
  email: String!
  password: String!
): AuthPayload!
```

**Description :** Connexion utilisateur.

**Parametres :**
- `email` : Email
- `password` : Mot de passe

---

### postVideo

```graphql
postVideo(
  video_url: String!
  caption: String
  color: String!
  grade: String!
  status: VideoStatus!
  session_id: ID
): Video!
```

**Description :** Poster une video dans le feed.

**Authentification :** Requise (JWT)

**Parametres :**
- `video_url` : URL de la video (deja uploadee sur R2)
- `caption` : Texte libre (optionnel)
- `color` : Couleur de la prise
- `grade` : Cotation
- `status` : FLASH / TOP / PROJECT
- `session_id` : ID de la seance (optionnel, pour lier video → session)

**Exemple :**
```graphql
mutation {
  postVideo(
    video_url: "https://r2.example.com/videos/abc123.mp4"
    caption: "Premier 7A !"
    color: "Jaune"
    grade: "7A"
    status: FLASH
  ) {
    id
    video_url
    like_count
  }
}
```

---

### likeVideo

```graphql
likeVideo(video_id: ID!): Boolean!
```

**Description :** Liker une video.

**Authentification :** Requise (JWT)

**Parametres :**
- `video_id` : ID de la video

**Retour :** `true` si succes

---

### unlikeVideo

```graphql
unlikeVideo(video_id: ID!): Boolean!
```

**Description :** Retirer le like d'une video.

**Authentification :** Requise (JWT)

**Parametres :**
- `video_id` : ID de la video

**Retour :** `true` si succes

---

### createSession

```graphql
createSession(
  date: String!
  gym_id: ID
  feeling: Int
  notes: String
): Session!
```

**Description :** Creer une seance de grimpe (logbook).

**Authentification :** Requise (JWT)

**Parametres :**
- `date` : Date de la seance (ISO 8601)
- `gym_id` : ID de la salle (optionnel)
- `feeling` : Ressenti 1-5 (optionnel)
- `notes` : Notes libres (optionnel)

**Exemple :**
```graphql
mutation {
  createSession(
    date: "2026-02-09T18:00:00Z"
    gym_id: "gym-123"
    feeling: 4
    notes: "Bonne seance !"
  ) {
    id
    date
  }
}
```

---

### createCroix

```graphql
createCroix(
  session_id: ID
  photo_url: String!
  color: String!
  grade: String!
  status: VideoStatus!
  notes: String
): Croix!
```

**Description :** Ajouter une croix (bloc tente/reussi).

**Authentification :** Requise (JWT)

**Parametres :**
- `session_id` : ID de la seance (optionnel)
- `photo_url` : URL de la photo du bloc
- `color` : Couleur de la prise
- `grade` : Cotation
- `status` : FLASH / TOP / PROJECT
- `notes` : Notes libres (optionnel)

**Exemple :**
```graphql
mutation {
  createCroix(
    session_id: "session-456"
    photo_url: "https://r2.example.com/photos/bloc1.jpg"
    color: "Bleu"
    grade: "6B"
    status: TOP
    notes: "Reussi au 3e essai"
  ) {
    id
    color
    grade
  }
}
```

---

### getPresignedUploadUrl

```graphql
getPresignedUploadUrl(filename: String!): String!
```

**Description :** Genere une URL signee pour upload direct vers Cloudflare R2.

**Authentification :** Requise (JWT)

**Parametres :**
- `filename` : Nom du fichier a uploader

**Retour :** URL signee (valide 1h)

**Workflow upload :**
1. Frontend appelle `getPresignedUploadUrl(filename: "video.mp4")`
2. Backend retourne URL signee
3. Frontend upload via PUT vers l'URL signee
4. Frontend appelle `postVideo(video_url: "...")` avec l'URL finale

**Exemple :**
```graphql
mutation {
  getPresignedUploadUrl(filename: "mon-bloc.mp4")
}
```

---

## Authentification

**Header JWT :**
```http
Authorization: Bearer <token>
```

**Queries/Mutations protegees :**
- `me`
- `mySessions`
- `myCroix`
- `postVideo`
- `likeVideo`
- `unlikeVideo`
- `createSession`
- `createCroix`
- `getPresignedUploadUrl`

---

## Erreurs

**Format :**
```json
{
  "errors": [
    {
      "message": "Unauthorized",
      "extensions": {
        "code": "UNAUTHORIZED"
      }
    }
  ]
}
```

**Codes erreur :**
- `UNAUTHORIZED` : Token manquant/invalide
- `NOT_FOUND` : Ressource introuvable
- `VALIDATION_ERROR` : Donnees invalides
- `INTERNAL_ERROR` : Erreur serveur

---

## Exemples complets

### Feed + Like

```graphql
# Recuperer le feed
query GetFeed {
  feed(limit: 10) {
    id
    user {
      pseudo
      avatar_url
    }
    video_url
    caption
    color
    grade
    status
    like_count
    is_liked_by_me
  }
}

# Liker une video
mutation LikeVideo {
  likeVideo(video_id: "video-123")
}
```

---

### Upload + Post video

```graphql
# 1. Obtenir URL signee
mutation GetUploadUrl {
  getPresignedUploadUrl(filename: "bloc-7a.mp4")
}

# 2. Upload via PUT (hors GraphQL)
# PUT https://r2.example.com/videos/bloc-7a.mp4

# 3. Poster la video
mutation PostVideo {
  postVideo(
    video_url: "https://r2.example.com/videos/bloc-7a.mp4"
    caption: "Mon premier 7A !"
    color: "Jaune"
    grade: "7A"
    status: FLASH
  ) {
    id
    like_count
  }
}
```

---

### Logbook (Session + Croix)

```graphql
# Creer une seance
mutation CreateSession {
  createSession(
    date: "2026-02-09T18:00:00Z"
    gym_id: "gym-1"
    feeling: 5
    notes: "Excellente seance"
  ) {
    id
  }
}

# Ajouter une croix
mutation AddCroix {
  createCroix(
    session_id: "session-123"
    photo_url: "https://r2.example.com/photos/bloc1.jpg"
    color: "Rouge"
    grade: "7B"
    status: PROJECT
    notes: "A retravailler"
  ) {
    id
  }
}

# Recuperer mes seances
query MySessions {
  mySessions {
    id
    date
    gym {
      name
    }
    croix {
      color
      grade
      status
    }
  }
}
```
