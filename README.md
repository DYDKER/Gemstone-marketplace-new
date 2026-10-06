# Gemstone-marketplace-new

## Database migrations

The root `database.py` provides the shared settings, engine, session factory,
and model base for both applications.

Run the applications from the repository root in separate terminals:

```shell
uv run python -m uvicorn auth_service.main:app --app-dir services/auth-service/src --port 8000
uv run python -m uvicorn gemstone_service.main:app --app-dir services/gemstone-service/src --port 8001
```

Run all Alembic commands from the repository root. The root configuration
loads both the auth and gemstone models and manages one migration history.
Set `DATABASE_URL` in the environment or the root `.env` file before running:

```shell
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "Describe the schema change"
uv run alembic check
```

Review generated migrations before applying them, especially type changes and
data conversions.

### Existing databases with separate migration histories

Do not run the combined history against an existing `gemstones` table without
reconciling its version records first: Alembic would try to create it again.
Back up the database and verify that its schema matches the corresponding
revisions in both old histories. Then consolidate the version records into
`alembic_version` and remove the old `gemstone_alembic_version` table in one
transaction. Resolve any schema differences before marking revisions applied;
`stamp` only changes version records and does not update the schema.

## Docker startup

Run `docker compose up --build -d` after starting Docker Desktop.
PostgreSQL starts first, then migrations run, then both APIs start.

- Auth API: http://localhost:8000/docs
- Gemstone API: http://localhost:8001/docs

View logs with `docker compose logs -f`. Stop containers with `docker compose down`.
