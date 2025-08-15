# SnapWave Database Schema

This document provides a comprehensive overview of the SnapWave application's database schema, including tables, relationships, and field descriptions.

## Overview

SnapWave uses PostgreSQL as its primary database for structured data. The schema follows a relational design pattern to support the social media platform's core features including user management, media sharing, and social interactions.

## Database Tables

### 1. Users Table

The `users` table stores user account information and profile data.

#### Schema

| Column Name                  | Data Type         | Constraints                | Description                                      |
|------------------------------|-------------------|----------------------------|--------------------------------------------------|
| id                           | Integer           | Primary Key, Auto-increment | Unique identifier for the user                   |
| email                        | String            | Unique, Not Null, Indexed  | User's email address                             |
| username                     | String            | Unique, Not Null, Indexed  | User's chosen username                           |
| hashed_password              | String            | Not Null                   | Securely hashed user password                    |
| full_name                    | String            | Nullable                   | User's full name                                 |
| bio                          | String            | Nullable                   | User's profile biography or description          |
| profile_picture              | String            | Nullable                   | Path or URL to user's profile picture            |
| is_active                    | Boolean           | Default: true              | Flag indicating if account is active             |
| is_superuser                 | Boolean           | Default: false             | Flag indicating admin privileges                 |
| reset_token                  | String            | Nullable, Indexed          | Token for password reset                         |
| reset_token_expires_at       | DateTime          | Nullable                   | Expiration timestamp for reset token             |
| email_verified               | Boolean           | Default: false             | Flag indicating if email has been verified       |
| verification_token           | String            | Nullable, Indexed          | Token for email verification                     |
| verification_token_expires_at| DateTime          | Nullable                   | Expiration timestamp for verification token      |
| created_at                   | DateTime          | Default: current timestamp | Account creation timestamp                       |
| updated_at                   | DateTime          | On update: current timestamp | Last update timestamp                          |

#### Indexes
- `ix_users_id`: Index on `id` column
- `ix_users_email`: Unique index on `email` column
- `ix_users_username`: Unique index on `username` column
- `ix_users_reset_token`: Index on `reset_token` column
- `ix_users_verification_token`: Index on `verification_token` column

### 2. Media Table (Planned)

The `media` table will store information about user-uploaded media files.

#### Schema (Planned)

| Column Name    | Data Type         | Constraints                | Description                                      |
|----------------|-------------------|----------------------------|--------------------------------------------------|
| id             | Integer           | Primary Key, Auto-increment | Unique identifier for the media                  |
| user_id        | Integer           | Foreign Key (users.id)     | ID of the user who uploaded the media            |
| title          | String            | Nullable                   | Title of the media                               |
| description    | String            | Nullable                   | Description of the media                         |
| file_path      | String            | Not Null                   | Path to the media file in the storage layer      |
| thumbnail_path | String            | Nullable                   | Path to the thumbnail image                      |
| media_type     | String            | Not Null                   | Type of media (image, video, etc.)               |
| metadata       | JSON              | Nullable                   | Additional metadata about the media              |
| is_private     | Boolean           | Default: false             | Whether the media is private or public           |
| created_at     | DateTime          | Default: current timestamp | Upload timestamp                                 |
| updated_at     | DateTime          | On update: current timestamp | Last update timestamp                          |

#### Indexes
- `ix_media_id`: Index on `id` column
- `ix_media_user_id`: Index on `user_id` column

### 3. Interactions Table (Planned)

The `interactions` table will store user interactions with media, such as likes, comments, and shares.

#### Schema (Planned)

| Column Name    | Data Type         | Constraints                | Description                                      |
|----------------|-------------------|----------------------------|--------------------------------------------------|
| id             | Integer           | Primary Key, Auto-increment | Unique identifier for the interaction            |
| user_id        | Integer           | Foreign Key (users.id)     | ID of the user performing the interaction        |
| media_id       | Integer           | Foreign Key (media.id)     | ID of the media being interacted with            |
| interaction_type| String           | Not Null                   | Type of interaction (like, comment, share)       |
| content        | String            | Nullable                   | Content of the interaction (e.g., comment text)  |
| parent_id      | Integer           | Foreign Key (self), Nullable| ID of parent interaction (for comment replies)   |
| created_at     | DateTime          | Default: current timestamp | Interaction timestamp                            |
| updated_at     | DateTime          | On update: current timestamp | Last update timestamp                          |

#### Indexes
- `ix_interactions_id`: Index on `id` column
- `ix_interactions_user_id`: Index on `user_id` column
- `ix_interactions_media_id`: Index on `media_id` column
- `ix_interactions_parent_id`: Index on `parent_id` column

### 4. Follows Table (Planned)

The `follows` table will track user follow relationships.

#### Schema (Planned)

| Column Name    | Data Type         | Constraints                      | Description                                   |
|----------------|-------------------|----------------------------------|-----------------------------------------------|
| id             | Integer           | Primary Key, Auto-increment       | Unique identifier for the follow relationship |
| follower_id    | Integer           | Foreign Key (users.id), Not Null | ID of the follower user                       |
| followed_id    | Integer           | Foreign Key (users.id), Not Null | ID of the followed user                       |
| created_at     | DateTime          | Default: current timestamp       | When the follow relationship was created      |

#### Indexes
- `ix_follows_follower_id`: Index on `follower_id` column
- `ix_follows_followed_id`: Index on `followed_id` column
- Unique constraint on the combination of `follower_id` and `followed_id`

## Entity Relationships

### User Relationships
- One user can upload many media items (One-to-Many)
- One user can have many interactions (One-to-Many)
- Users can follow many other users (Many-to-Many through the follows table)

### Media Relationships
- Each media belongs to one user (Many-to-One)
- Each media can have many interactions (One-to-Many)

### Interaction Relationships
- Each interaction belongs to one user (Many-to-One)
- Each interaction belongs to one media item (Many-to-One)
- Interactions can have parent interactions (self-referencing relationship for comments)

## Database Migrations

The database schema is managed using Alembic for migrations. Key migration files:

1. `c821532bc4eb_initial_database_setup.py`: Initial creation of the users table
2. `d6290a7f5f2b_add_password_reset_fields.py`: Added password reset functionality
3. `e8f213a9c45d_add_email_verification_fields.py`: Added email verification functionality

To create new migrations:
```bash
alembic revision -m "description_of_changes"
```

To apply migrations:
```bash
alembic upgrade head
```

To revert migrations:
```bash
alembic downgrade -1  # Downgrade by one revision
```

## Schema Diagrams

### Current Schema
```
┌─────────────────────────┐
│          Users          │
├─────────────────────────┤
│ id                      │
│ email                   │
│ username                │
│ hashed_password         │
│ full_name               │
│ bio                     │
│ profile_picture         │
│ is_active               │
│ is_superuser            │
│ reset_token             │
│ reset_token_expires_at  │
│ email_verified          │
│ verification_token      │
│ verification_token_expires_at │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
```

### Planned Schema
```
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│          Users          │      │          Media          │      │      Interactions       │
├─────────────────────────┤      ├─────────────────────────┤      ├─────────────────────────┤
│ id                      │◄─┐   │ id                      │◄─┐   │ id                      │
│ email                   │  │   │ user_id (FK)            │  │   │ user_id (FK)            │
│ username                │  │   │ title                   │  │   │ media_id (FK)           │
│ hashed_password         │  │   │ description             │  │   │ interaction_type        │
│ ...                     │  │   │ file_path               │  │   │ content                 │
└─────────────────────────┘  │   │ ...                     │  │   │ parent_id (FK)          │
                             │   └─────────────────────────┘  │   │ ...                     │
                             │                                │   └─────────────────────────┘
                             └────────────────────────────────┘
                             │
                             │   ┌─────────────────────────┐
                             │   │         Follows         │
                             │   ├─────────────────────────┤
                             └──►│ follower_id (FK)        │
                                 │ followed_id (FK)        │
                                 │ ...                     │
                                 └─────────────────────────┘
```

## Notes on Schema Design

1. **Timezone-aware Timestamps**: All datetime fields use timezone information for accurate time tracking across different regions.

2. **Soft Delete Consideration**: The `is_active` flag on users allows for "soft delete" functionality, where user data is preserved but accounts are deactivated.

3. **Security Features**: The schema includes several security-oriented features:
   - Password storage as secure hashes (not plaintext)
   - Email verification mechanism
   - Password reset token system with expiration

4. **Performance Optimizations**:
   - Appropriate indexes on frequently queried columns
   - Foreign key relationships for data integrity

5. **Future Considerations**:
   - Partitioning strategy for the media table as it grows
   - Archiving strategy for older interactions
   - Potential denormalization for feed generation performance

## Additional Information

For database connection and configuration details, refer to the `/backend/app/core/config.py` file.

For model definitions and ORM mappings, see the Python classes in `/backend/app/models/`.
