# Gemstone Marketplace

FastAPI application with CRUD APIs for users and gemstones.

## Run locally

```powershell
uv sync
Copy-Item .env.example .env
docker compose up -d
uv run alembic upgrade head
uv run uvicorn --app-dir src gemstone_marketplace.main:app --reload
```

Replace `JWT_SECRET_KEY` in `.env` with a random value before starting the app.
You can generate one with:

```powershell
uv run python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Swagger UI: http://127.0.0.1:8000/docs

## Authentication

- `POST /auth/register` creates a user with an Argon2 password hash.
- `POST /auth/login` returns a JWT access token.
- `GET /users/me` requires `Authorization: Bearer <token>`.
