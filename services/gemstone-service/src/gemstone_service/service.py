import logging

from PIL import Image, UnidentifiedImageError

from starlette.concurrency import run_in_threadpool

from storage import S3Storage

from fastapi import UploadFile

from uuid import uuid4

from .exceptions import ImageSaveRejectedError, InvalidImageError, StoneNotFoundError, StoneImageNotFoundError
from .repository import GemstoneRepository
from .schemas import GemstoneCreate, GemstoneResponse, GemstoneUpdate, GemstoneImageResponse

logger = logging.getLogger(__name__)

class GemstoneService:
    def __init__(self, repository: GemstoneRepository, storage: S3Storage):
        self.repository = repository
        self.storage = storage

    async def get_gems(self) -> list[GemstoneResponse]:
        items = await self.repository.get_all()
        return [GemstoneResponse.model_validate(gem) for gem in items]

    async def get_gem(self, gemstone_id: int) -> GemstoneResponse:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        return GemstoneResponse.model_validate(gem)

    async def create_gem(self, gemstone_data: GemstoneCreate) -> GemstoneResponse:
        gem = await self.repository.create(**gemstone_data.model_dump())
        return GemstoneResponse.model_validate(gem)

    async def update_gem(self, gemstone_id: int, gemstone_data: GemstoneUpdate) -> GemstoneResponse:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        changes = gemstone_data.model_dump(exclude_unset=True)
        gem = await self.repository.update(gem, changes)
        return GemstoneResponse.model_validate(gem)

    async def delete_gem(self, gemstone_id: int) -> None:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        image_key = gem.image_key

        await self.repository.delete(gem)

        if image_key:
            try:
                await self.storage.delete_file(image_key)
            except Exception:
                logger.exception("Камень удален, но не удалось удалить фотографию: %s", image_key)

    async def upload_image(self, gemstone_id: int, file: UploadFile) -> GemstoneResponse:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        old_key = gem.image_key

        allowed_types = {"image/jpeg", "image/png", "image/webp"}
        max_size = 5 * 1024 * 1024

        if file.content_type not in allowed_types:
            raise InvalidImageError("Допустимы только JPEG, PNG и WebP")

        if file.size is None or file.size == 0:
            raise InvalidImageError("Файл пустой или его размер неизвестен")

        if file.size > max_size:
            raise InvalidImageError("Размер изображения не должен превышать 5МБ")

        content_type = await run_in_threadpool(self.validate_image, file)

        extension = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
        key = f"gems/{gemstone_id}/{uuid4().hex}{extension[content_type]}"

        await self.storage.upload_file(key, file.file, content_type)

        try:
            gem = await self.repository.set_image_key(gem, key)
        except ImageSaveRejectedError:
            try:
                await self.storage.delete_file(key)
            except Exception:
                logger.exception("Не удалось удалить новый файл после отказа БД: %s", key)
            raise

        if old_key and old_key != key:
            try:
                await self.storage.delete_file(old_key)
            except Exception:
                logger.exception("Не удалось удалить старое изображение: %s", old_key)

        return GemstoneResponse.model_validate(gem)


    def validate_image(self, file: UploadFile) -> str:
        formats = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}

        try:
            file.file.seek(0)

            with Image.open(file.file) as image:
                if image.format not in formats:
                    raise InvalidImageError("Допустимы только JPEG, PNG, WebP")

                content_type = formats[image.format]
                image.verify()

            return content_type
        except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError) as exc:
            raise InvalidImageError("Файл повреждён или не является допустимым изображением") from exc
        finally:
            file.file.seek(0)


    async def get_image_url(self, gemstone_id: int) -> GemstoneImageResponse:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        if not gem.image_key:
            raise StoneImageNotFoundError()

        url = await self.storage.get_file_url(gem.image_key)
        return GemstoneImageResponse(url=url)