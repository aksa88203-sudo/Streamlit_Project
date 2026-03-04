# FastAPI + MySQL Production-Ready CRUD

This scaffold provides a clean, layered architecture:

- `API layer`: request/response routing
- `Service layer`: business logic and validations
- `Repository layer`: database access
- `DB layer`: SQLAlchemy session and Alembic migrations

## Folder Architecture

```text
fastapi_backend/
  app/
    api/
      deps.py
      v1/
        endpoints/
          items.py
        router.py
    core/
      config.py
    db/
      base.py
      init_db.py
      session.py
    models/
      base.py
      item.py
    repositories/
      item.py
    schemas/
      item.py
    services/
      item.py
    main.py
  alembic/
    env.py
    script.py.mako
    versions/
      20260301_0001_create_items_table.py
  .env.example
  Dockerfile
  docker-compose.yml
  requirements.txt
```

## Quick Start (Local Python)

1. Create environment file:
```bash
cp .env.example .env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run MySQL:
```bash
docker compose up -d db
```

4. Apply migrations:
```bash
alembic upgrade head
```

5. Start API:
```bash
uvicorn app.main:app --reload
```

## Quick Start (Docker)

1. Set env file:
```bash
cp .env.example .env
```

2. Start full stack (MySQL + API):
```bash
docker compose up --build -d
```

3. Check logs:
```bash
docker compose logs -f api
```

4. Stop containers:
```bash
docker compose down
```

API docs:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Endpoints (Items CRUD)

- `GET /api/v1/items/`
- `GET /api/v1/items/{item_id}`
- `POST /api/v1/items/`
- `PUT /api/v1/items/{item_id}`
- `DELETE /api/v1/items/{item_id}`
- `GET /health`

## Example Payload

```json
{
  "name": "Wireless Mouse",
  "description": "2.4Ghz ergonomic mouse",
  "sku": "MOUSE-001",
  "price": 29.99,
  "quantity": 100
}
```

## Production Notes

- Keep `DEBUG=false` in production.
- Prefer migrations over `AUTO_CREATE_TABLES`.
- Add auth, rate limiting, and structured logging before going live.
