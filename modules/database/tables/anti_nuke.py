from ..database_object import AsyncDatabaseObject
from datetime import time, datetime

TABLE_NAME = 'anti_nuke'


class AntiNukeTable(AsyncDatabaseObject):
    __guild_id_attribute = 'guild_id'
    __block_role_id_attribute = 'block_role_id'
    __log_channel_id_attribute = 'log_channel_id'
    __timeout_for_ban_attribute = 'timeout_for_ban'
    __ban_protection_count_attribute = 'ban_protection_count'
    __timeout_for_kick_attribute = 'timeout_for_kick'
    __kick_protection_count_attribute = 'kick_protection_count'

    def __init__(self, guild_id: int = None):
        data_record = {self.__guild_id_attribute: guild_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__guild_id_attribute, data_record=data_record)

    @property
    def block_role_id(self) -> int:
        return self._data.get(self.__block_role_id_attribute)

    @block_role_id.setter
    def block_role_id(self, value):
        self._data[self.__block_role_id_attribute] = value

    @property
    def log_channel_id(self) -> int:
        return self._data.get(self.__log_channel_id_attribute)

    @log_channel_id.setter
    def log_channel_id(self, value):
        self._data[self.__log_channel_id_attribute] = value

    @property
    def timeout_for_ban(self) -> time:
        value = self._data.get(self.__timeout_for_ban_attribute)
        return datetime.strptime(value, '%H:%M:%S').time()

    @timeout_for_ban.setter
    def timeout_for_ban(self, value: time):
        self._data[self.__timeout_for_ban_attribute] = value.strftime('%H:%M:%S')

    @property
    def ban_protection_count(self) -> int:
        return self._data.get(self.__ban_protection_count_attribute)

    @ban_protection_count.setter
    def ban_protection_count(self, value):
        self._data[self.__ban_protection_count_attribute] = value

    @property
    def timeout_for_kick(self) -> time:
        value = self._data.get(self.__timeout_for_kick_attribute)
        return datetime.strptime(value, '%H:%M:%S').time()

    @timeout_for_kick.setter
    def timeout_for_kick(self, value: time):
        self._data[self.__timeout_for_kick_attribute] = value.strftime('%H:%M:%S')

    @property
    def kick_protection_count(self) -> int:
        return self._data.get(self.__kick_protection_count_attribute)

    @kick_protection_count.setter
    def kick_protection_count(self, value):
        self._data[self.__kick_protection_count_attribute] = value

    @property
    def columns(self) -> list:
        return [
            (self.__block_role_id_attribute, 'INTEGER', 'NULL'),
            (self.__log_channel_id_attribute, 'INTEGER', 'NULL'),
            (self.__timeout_for_ban_attribute, 'DATE', 'NULL'),
            (self.__ban_protection_count_attribute, 'INTEGER', 'NULL'),
            (self.__timeout_for_kick_attribute, 'DATE', 'NULL'),
            (self.__kick_protection_count_attribute, 'INTEGER', 'NULL')
        ]
