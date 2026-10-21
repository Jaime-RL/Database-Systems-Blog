# Blog Manager — Layered Python + PostgreSQL App

Console application to manage **authors, blogs and posts** stored in **PostgreSQL**, built with a classic **three-layer architecture** and the **DAO pattern**.

## Architecture

```
presentation/   CLI menu and input/output helpers
     │
business/       managers (use cases) + entities (Author, Blog, Post)
     │
persistence/    DAO interfaces (ABC) + PostgreSQL implementations (psycopg2)
     │
PostgreSQL      author ─< blog ─< post
```

- **DAO interfaces** (`*_dao.py`) declare the operations with `abc.ABC`; `*_dao_sql.py` implement them with **parameterised queries** (no SQL injection).
- `daos_manager.py` wires interfaces to implementations (simple **dependency injection**), so the storage layer can be swapped without touching business code.
- Connection settings come from **environment variables** — no credentials in the code.

## Features

- Authors: list, find by id / username, insert, update and delete
- Blogs: find by id, with its author (`JOIN`), or with author **and** all its posts
- Posts: find, insert, update subject, list and delete

## Getting started

```bash
pip install -r requirements.txt

# 1. Create the database and load the sample data
psql -U postgres -f resources/blog-createDB.sql
psql -U postgres -d blog -f resources/blog-tablas.sql -f resources/blog-datos.sql

# 2. Configure the connection (see .env.example)
export DB_USER=postgres DB_PASSWORD=your_password

# 3. Run
python app.py
```

| Variable | Default |
|---|---|
| `DB_NAME` | `blog` |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | *(empty)* |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `5432` |

## Tech

Python 3 · PostgreSQL · psycopg2 · SQL

*Coursework from the Databases course — Computer Engineering, Universidad de Cantabria.*
