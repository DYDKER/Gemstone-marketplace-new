import asyncio
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from functools import lru_cache
from typing import Annotated, BinaryIO

import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError
from fastapi import Depends
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    endpoint_url: str
    public_endpoint_url: str | None = None
    access_key: str
    secret_key: SecretStr
    region: str = "us-east-1"
    bucket: str = "gemstone-images"
    url_ttl: int = Field(default=900, ge=1, le=604800)

    model_config = SettingsConfigDict(env_prefix="S3_", env_file=".env", extra="ignore")


@lru_cache
def get_storage_settings() -> StorageSettings:
    return StorageSettings()


class S3Storage:
    def __init__(self, client, bucket: str, url_ttl: int, signing_client=None):
        self.client = client
        self.signing_client = signing_client if signing_client is not None else client
        self.bucket = bucket
        self.url_ttl = url_ttl

    async def upload_file(self, key: str, file: BinaryIO, content_type: str = "application/octet-stream") -> str:
        await self.client.upload_fileobj(file, self.bucket, key, ExtraArgs={"ContentType": content_type})
        return key

    async def delete_file(self, key: str) -> None:
        await self.client.delete_object(Bucket=self.bucket, Key=key)

    async def get_file_url(self, key: str) -> str:
        return await self.signing_client.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=self.url_ttl)

    async def ensure_bucket(self) -> None:
        try:
            await self.client.head_bucket(Bucket=self.bucket)
        except ClientError as exc:
            if exc.response["Error"]["Code"] not in {"404", "NoSuchBucket", "NotFound"}:
                raise
            options = {"Bucket": self.bucket}
            region = self.client.meta.region_name
            if region != "us-east-1":
                options["CreateBucketConfiguration"] = {"LocationConstraint": region}
            try:
                await self.client.create_bucket(**options)
            except ClientError as create_exc:
                if create_exc.response["Error"]["Code"] != "BucketAlreadyOwnedByYou":
                    raise


@asynccontextmanager
async def open_storage(settings: StorageSettings) -> AsyncIterator[S3Storage]:
    session = aioboto3.Session()
    config = Config(signature_version="s3v4", s3={"addressing_style": "path"}, connect_timeout=5, read_timeout=30)
    options = dict(region_name=settings.region, aws_access_key_id=settings.access_key, aws_secret_access_key=settings.secret_key.get_secret_value(), config=config)
    public_endpoint = settings.public_endpoint_url or settings.endpoint_url
    async with AsyncExitStack() as stack:
        client = await stack.enter_async_context(session.client("s3", endpoint_url=settings.endpoint_url, **options))
        signing_client = client
        if public_endpoint != settings.endpoint_url:
            signing_client = await stack.enter_async_context(session.client("s3", endpoint_url=public_endpoint, **options))
        yield S3Storage(client, settings.bucket, settings.url_ttl, signing_client)


async def get_storage(settings: Annotated[StorageSettings, Depends(get_storage_settings)]) -> AsyncIterator[S3Storage]:
    async with open_storage(settings) as storage:
        yield storage


async def init_storage() -> None:
    async with open_storage(get_storage_settings()) as storage:
        await storage.ensure_bucket()
        print(f"Bucket ready: {storage.bucket}")


if __name__ == "__main__":
    asyncio.run(init_storage())
