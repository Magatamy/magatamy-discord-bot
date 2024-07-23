import disnake
import os
import json
import aiofiles

from config import LANGUAGES_DEFAULT


class Localized(disnake.Localized):
    def __init__(self, text_key: str):
        default_file_path = f'languages/{LANGUAGES_DEFAULT}.json'
        with open(default_file_path, encoding='utf-8-sig') as default_file:
            default_json = json.load(default_file)
        string = default_json.get('slash_commands', {}).get(text_key, '')

        translations = {}

        for filename in os.listdir('languages'):
            lang_name, ext = os.path.splitext(filename)
            if ext == '.json' and lang_name != LANGUAGES_DEFAULT:
                lang_file_path = os.path.join('languages', filename)
                with open(lang_file_path, encoding='utf-8-sig') as lang_file:
                    lang_json = json.load(lang_file)
                translations[lang_name] = lang_json.get('slash_commands', {}).get(text_key, '')

        super().__init__(string=string, data=translations)


class LanguageManager:
    def __init__(self, locale):
        self.locale = locale

    async def get_slash_commands_name(self, slash_command_key: str) -> str:
        json_data = await self._get_json_data(key='slash_commands')
        return json_data.get(slash_command_key, '')

    async def get_embed_data(self, json_key: str) -> dict:
        return await self._get_json_data(key=json_key)

    async def get_image_data(self, image_key: str, *args, **kwargs) -> dict:
        json_data = await self._get_json_data(key='image_data')
        data = json_data.get(image_key, {})

        for key in data:
            value = data[key]
            if isinstance(value, str):
                data[key] = value.format(*args, **kwargs)
        return data

    async def _get_json_data(self, key: str = None) -> dict:
        locale_path = f'languages/{self.locale}.json'
        default_path = f'languages/{LANGUAGES_DEFAULT}.json'

        try:
            async with aiofiles.open(locale_path, encoding='utf-8-sig') as file:
                json_data = json.loads(await file.read())
        except FileNotFoundError:
            async with aiofiles.open(default_path, encoding='utf-8-sig') as file:
                json_data = json.loads(await file.read())

        if key:
            return json_data.get(key, {})
        else:
            return json_data
