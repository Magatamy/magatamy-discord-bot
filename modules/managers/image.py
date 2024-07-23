import aiofiles
import base64

from disnake import File
from io import BytesIO


class ImageManager:
    def __init__(self, name: str = 'image', is_base64: bool = False):
        self.is_base64 = is_base64
        self.name = f'{name}.png'
        self.attachment_url = f'attachment://{self.name}'

    async def get_static(self, static_key: str) -> File | str:
        dir_key = f'static/{static_key}'
        return await self._get_image(key=dir_key)

    async def _get_image(self, key: str) -> File | str:
        async with aiofiles.open(f'images/{key}.png', "rb") as image_file:
            image_data = await image_file.read()
            if self.is_base64:
                return base64.b64encode(image_data).decode('utf-8')
            else:
                image_stream = BytesIO(image_data)
                return File(image_stream, filename=self.name)
