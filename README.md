# Gemstone Marketplace

FastAPI application with CRUD APIs for users and gemstones.

## Run locally

```powershell
uv sync
docker compose up -d
uv run alembic upgrade head
uv run uvicorn --app-dir src gemstone_marketplace.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs
