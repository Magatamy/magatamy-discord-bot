from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'guild_settings'


class GuildSettingsTable(AsyncDatabaseObject):
    __guild_id_attribute = 'guild_id'
    __private_voice_channel_id_attribute = 'private_voice_channel_id'
    __private_category_id_attribute = 'private_voice_category_id'
    __language_attribute = 'language'

    def __init__(self, guild_id: int = None):
        data_record = {self.__guild_id_attribute: guild_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__guild_id_attribute, data_record=data_record)

    @property
    def private_voice_channel_id(self) -> int:
        return self._data.get(self.__private_voice_channel_id_attribute)

    @private_voice_channel_id.setter
    def private_voice_channel_id(self, value):
        self._data[self.__private_voice_channel_id_attribute] = value

    @property
    def private_category_id(self) -> int:
        return self._data.get(self.__private_category_id_attribute)

    @private_category_id.setter
    def private_category_id(self, value):
        self._data[self.__private_category_id_attribute] = value

    @property
    def language(self) -> str:
        return self._data.get(self.__language_attribute)

    @language.setter
    def language(self, value: str):
        self._data[self.__language_attribute] = value

    @property
    def columns(self) -> list:
        return [
            (self.__private_voice_channel_id_attribute, 'INTEGER', 'NULL'),
            (self.__private_category_id_attribute, 'INTEGER', '0'),
            (self.__language_attribute, 'TEXT', 'NULL')
        ]
