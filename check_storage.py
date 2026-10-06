"""Run against the configured S3 endpoint: uv run python check_storage.py."""

import asyncio
from io import BytesIO
from uuid import uuid4

import httpx
from fastapi import Depends, FastAPI

from storage import S3Storage, get_storage, get_storage_settings, open_storage


async def main() -> None:
    settings = get_storage_settings()
    key = f"checks/{uuid4().hex}.txt"
    payload = b"Gemstone storage integration check"
    app = FastAPI()

    @app.get("/check")
    async def check_dependency(storage: S3Storage = Depends(get_storage)) -> dict[str, str]:
        return {"url": await storage.get_file_url(key)}

    async with open_storage(settings) as storage:
        await storage.ensure_bucket()
        try:
            await storage.upload_file(key, BytesIO(payload), "text/plain")
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test") as api:
                response = await api.get("/check")
                response.raise_for_status()
                url = response.json()["url"]
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                assert response.content == payload
                assert response.headers["content-type"].startswith("text/plain")
                unsigned = await client.get(url.split("?", 1)[0])
                assert unsigned.status_code == 403, "Object should not be public"
        finally:
            await storage.delete_file(key)
        async with httpx.AsyncClient() as client:
            response = await client.get(await storage.get_file_url(key))
            assert response.status_code == 404
    print("PASS: bucket, upload, FastAPI DI, signed download, private access and deletion")


if __name__ == "__main__":
    asyncio.run(main())
