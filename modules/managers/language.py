import disnake
import os
import json

from config import LANGUAGES_DEFAULT, LANGUAGES_DIRECTORY


class Localized(disnake.Localized):
    def __init__(self, text_key: str):
        default_file_path = f'{LANGUAGES_DIRECTORY}/{LANGUAGES_DEFAULT}.json'
        with open(default_file_path, encoding='utf-8-sig') as default_file:
            default_json = json.load(default_file)
        string = default_json.get('slash_commands', {}).get(text_key, '')

        translations = {}

        for filename in os.listdir(LANGUAGES_DIRECTORY):
            lang_name, ext = os.path.splitext(filename)
            if ext == '.json' and lang_name != LANGUAGES_DEFAULT:
                lang_file_path = os.path.join(LANGUAGES_DIRECTORY, filename)
                with open(lang_file_path, encoding='utf-8-sig') as lang_file:
                    lang_json = json.load(lang_file)
                translations[lang_name] = lang_json.get('slash_commands', {}).get(text_key, '')

        super().__init__(string=string, data=translations)

    @staticmethod
    def load_all_language_data() -> dict:
        data = {}
        for filename in os.listdir(LANGUAGES_DIRECTORY):
            lang_name, ext = os.path.splitext(filename)
            locale_path = f'{LANGUAGES_DIRECTORY}/{filename}'
            with open(locale_path, encoding='utf-8') as file:
                json_data = json.loads(file.read())
            data.update({lang_name: json_data})

        return data


LANGUAGES_DATA = Localized.load_all_language_data()


class LanguageManager:
    def __init__(self, locale: disnake.Locale, language: str = None):
        self.locale = locale if not language else language
        self._data = self.__load_json_data()

    def __load_json_data(self) -> dict:
        language_data = LANGUAGES_DATA.get(self.locale)
        if not language_data:
            language_data = LANGUAGES_DATA.get(LANGUAGES_DEFAULT)
        return language_data

    def get_slash_commands_name(self, slash_command_key: str | list) -> str | list:
        language_data = self._data.get('slash_commands')
        if isinstance(slash_command_key, list):
            return [language_data.get(key, '') for key in slash_command_key]
        return language_data.get(slash_command_key, '')

    def get_static(self, text_key: str | list) -> str | list[str]:
        language_data = self._data.get('static_text')
        if isinstance(text_key, list):
            return [language_data.get(key, '') for key in text_key]
        return language_data.get(text_key, '')

    def get_embed_data(self, json_key: str | list) -> dict | list:
        if isinstance(json_key, list):
            return [self._data.get(key) for key in json_key]
        return self._data.get(json_key)
