# Database Schema Documentation

## Overview

The database is built on **SQLite3** (`database.db`) using normalized 3NF table design to avoid data redundancy and maintain relational integrity.

## Entity Relationship Diagram

```mermaid
erDiagram
    SYMPTOMS {
        int id PK
        string symptom_name
        string normalized_name
        string synonyms
    }

    CONDITIONS {
        int id PK
        string condition_name
        string description
    }

    CONDITION_SYMPTOMS {
        int condition_id FK
        int symptom_id FK
    }

    MEDICINES {
        int id PK
        string medicine_name
        string generic_name
        string category
        string description
        string common_use
        string precautions
        string side_effects
        string contraindications
        string warning
    }

    CONDITION_MEDICINES {
        int condition_id FK
        int medicine_id FK
    }

    FEEDBACK {
        int id PK
        string name
        string email
        int rating
        string message
        timestamp created_at
    }

    CONDITIONS ||--o{ CONDITION_SYMPTOMS : HAS
    SYMPTOMS ||--o{ CONDITION_SYMPTOMS : BELONGS_TO
    CONDITIONS ||--o{ CONDITION_MEDICINES : TREATS
    MEDICINES ||--o{ CONDITION_MEDICINES : ASSOCIATED_WITH
```

## Table Specifications

### 1. `symptoms`
- `id` (INTEGER PRIMARY KEY)
- `symptom_name` (TEXT UNIQUE)
- `normalized_name` (TEXT)
- `synonyms` (TEXT)

### 2. `conditions`
- `id` (INTEGER PRIMARY KEY)
- `condition_name` (TEXT UNIQUE)
- `description` (TEXT)

### 3. `condition_symptoms`
- `condition_id` (INTEGER, FK -> conditions.id)
- `symptom_id` (INTEGER, FK -> symptoms.id)

### 4. `medicines`
- `id` (INTEGER PRIMARY KEY)
- `medicine_name` (TEXT)
- `generic_name` (TEXT)
- `category` (TEXT)
- `common_use` (TEXT)
- `precautions` (TEXT)
- `side_effects` (TEXT)
- `contraindications` (TEXT)
- `warning` (TEXT)

### 5. `condition_medicines`
- `condition_id` (INTEGER, FK -> conditions.id)
- `medicine_id` (INTEGER, FK -> medicines.id)

### 6. `feedback`
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `email` (TEXT)
- `rating` (INTEGER)
- `message` (TEXT)
- `created_at` (TIMESTAMP)
