from ..redis_object import RedisObject

CATEGORY_NAME = 'guild_settings'


class GuildSettings(RedisObject):
    __private_voice_channel_id_attribute = 'private_voice_channel_id'
    __private_category_id_attribute = 'private_voice_category_id'
    __language_attribute = 'language'

    def __init__(self, key: int = None):
        """key is guild_id"""
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def private_voice_channel_id(self) -> int:
        return self._data.get(self.__private_voice_channel_id_attribute)

    @private_voice_channel_id.setter
    def private_voice_channel_id(self, value: int):
        self._data[self.__private_voice_channel_id_attribute] = value

    @property
    def private_category_id(self) -> int:
        return self._data.get(self.__private_category_id_attribute)

    @private_category_id.setter
    def private_category_id(self, value: int):
        self._data[self.__private_category_id_attribute] = value

    @property
    def language(self) -> str:
        return self._data.get(self.__language_attribute)

    @language.setter
    def language(self, value: str):
        self._data[self.__language_attribute] = value
