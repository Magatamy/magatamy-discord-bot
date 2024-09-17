import os
import aiofiles

from io import BytesIO
from disnake import File
from htmlwebshot import WebShot

WEB_SHOT_PARAMS = {"--encoding": "utf-8"}
WEB_SHOT_FLAGS = [
    '--quiet',
    '--disable-smart-width',
    '--disable-javascript',
    '--stop-slow-scripts'
]


class ImageGenerator(WebShot):
    def __init__(self, json_schema: dict, image_key: str, height: int, width: int, user_id: int = None):
        super().__init__(params=WEB_SHOT_PARAMS, quality=80, flags=WEB_SHOT_FLAGS, size=(height, width))
        self.id = user_id if user_id else image_key
        self.image_key = image_key
        self.json_schema = json_schema

    @property
    def attachment_url(self) -> str:
        return f'attachment://{self.id}.png'

    @property
    def temp_html(self) -> str:
        return f"images/temp/{self.id}.html"

    @property
    def temp_image(self) -> str:
        return f'images/temp/{self.id}.png'

    def __clear_files(self, clear: bool, image_path: str):
        if clear and os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(self.temp_html):
            os.remove(self.temp_html)

    async def __generic_image_files(self):
        path = f'images/generic/{self.image_key}.html'
        async with aiofiles.open(path, 'r') as file:
            content = await file.read()
            image_html = content.format(**self.json_schema)

        async with aiofiles.open(self.temp_html, 'w', encoding='utf-8') as temp_file:
            await temp_file.write(image_html)

    async def get_image_file(self, clear: bool = True) -> File:
        await self.__generic_image_files()
        image_path = await self.create_pic_async(url=self.temp_html, output=self.temp_image)

        try:
            async with aiofiles.open(image_path, 'rb') as file:
                image_data = await file.read()
                image_stream = BytesIO(image_data)
                return File(fp=image_stream, filename=os.path.basename(image_path))
        finally:
            self.__clear_files(clear=clear, image_path=image_path)
