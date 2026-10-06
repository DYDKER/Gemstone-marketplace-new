# Gemstone-marketplace-new

## Run the whole project with Docker

Start Docker Desktop. If `.env` does not exist, copy `.env.example` to `.env`
and replace the example S3 secret with your own value. Do not overwrite an
existing `.env`. Then run from the repository root:

```powershell
docker compose up --build -d
```

The shared `Dockerfile` installs Python dependencies from `uv.lock`. The `init`
container waits for PostgreSQL and applies Alembic migrations.
Both APIs start only after initialization succeeds. An exited `init`
container with code 0 is expected. Python is not required on the host.

- Users Swagger: http://localhost:8000/docs
- Gemstones Swagger: http://localhost:8001/docs
- RustFS console: http://localhost:9001/rustfs/console/

Stop any manually started APIs on ports 8000/8001 before starting the stack.
After code changes, rerun the build command above. Check startup failures with
`docker compose logs init auth-api gemstone-api`. Stop with `docker compose down`;
named volumes remain. Do not add `-v` unless you intend to delete stored data.

## Local S3 storage (RustFS)

From the repository root, copy `.env.example` to `.env` if it does not exist.
Set `S3_SECRET_KEY` to a random value. Compose and the Python client read the
same `S3_ACCESS_KEY` and `S3_SECRET_KEY`. The local `.env` is ignored by Git.

```powershell
uv sync
docker compose up -d rustfs
uv run python storage.py
uv run python check_storage.py
```

Wait for RustFS to start before running the Python commands. `storage.py`
creates the configured bucket if missing; it does not make it public.
`check_storage.py` uploads a uniquely named test object, checks a signed download,
checks private access and deletes the test object. It also exercises FastAPI DI.

- S3 endpoint: http://localhost:9000
- Browser console: http://localhost:9001/rustfs/console/ (login with the S3 keys from `.env`)
- Files persist in the Compose volume `rustfs_data` across container restarts.
- Do not use `docker compose down -v` if you want to keep stored data.

The standalone infrastructure module `storage.py` provides:

```python
from fastapi import Depends
from storage import S3Storage, get_storage

# Add this parameter to your own dependency or handler:
# storage: S3Storage = Depends(get_storage)

# await storage.upload_file(key, file, content_type)
# await storage.get_file_url(key)
# await storage.delete_file(key)
```

`file` is a binary file object, such as `UploadFile.file` or `BytesIO`.
Uploads start at its current position. The caller owns and closes this file.
`get_storage` closes the S3 client after the request. Signed links expire after
`S3_URL_TTL` seconds (900 by default); treat them as temporary access credentials.
Store object keys rather than expiring URLs in your database.

For local Python execution, `S3_ENDPOINT_URL` is `http://localhost:9000`.
Compose overrides it to `http://rustfs:9000` for container-to-container requests.
`S3_PUBLIC_ENDPOINT_URL` is the address reachable by the browser, locally
`http://localhost:9000`. A separate client signs download links for this address;
uploads and deletions still use the internal endpoint. Both clients use the same
credentials, bucket and region. If the public endpoint is omitted, links use
`S3_ENDPOINT_URL`. Do not replace the hostname in an already signed URL because
the signature includes it. Bucket initialization remains a manual step
(`uv run python storage.py`).

Image upload, replacement and signed download URLs are available through the
gemstone API. This local configuration exposes APIs and storage on this computer.

References: [RustFS Docker setup](https://docs.rustfs.com/en/installation/container/docker),
[aioboto3 client lifecycle](https://aioboto3.readthedocs.io/en/latest/usage.html).

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
