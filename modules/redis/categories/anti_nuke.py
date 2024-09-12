from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'anti_nuke'


class AntiNuke(RedisObject):
    __block_role_id_attribute = 'block_role_id'
    __log_channel_id_attribute = 'log_channel_id'
    __timeout_for_ban_attribute = 'timeout_for_ban'
    __ban_protection_count_attribute = 'ban_protection_count'
    __timeout_for_kick_attribute = 'timeout_for_kick'
    __kick_protection_count_attribute = 'kick_protection_count'

    def __init__(self, key: int = None):
        """key is guild_id"""
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def block_role_id(self) -> int:
        return self._data.get(self.__block_role_id_attribute)

    @block_role_id.setter
    def block_role_id(self, value: int):
        self._data[self.__block_role_id_attribute] = value

    @property
    def log_channel_id(self) -> int:
        return self._data.get(self.__log_channel_id_attribute)

    @log_channel_id.setter
    def log_channel_id(self, value: int):
        self._data[self.__log_channel_id_attribute] = value

    @property
    def timeout_for_ban(self) -> int:
        return self._data.get(self.__timeout_for_ban_attribute)

    @timeout_for_ban.setter
    def timeout_for_ban(self, value: int):
        self._data[self.__timeout_for_ban_attribute] = value

    @property
    def ban_protection_count(self) -> int:
        return self._data.get(self.__ban_protection_count_attribute)

    @ban_protection_count.setter
    def ban_protection_count(self, value: int):
        self._data[self.__ban_protection_count_attribute] = value

    @property
    def timeout_for_kick(self) -> int:
        return self._data.get(self.__timeout_for_kick_attribute)

    @timeout_for_kick.setter
    def timeout_for_kick(self, value: int):
        self._data[self.__timeout_for_kick_attribute] = value

    @property
    def kick_protection_count(self) -> int:
        return self._data.get(self.__kick_protection_count_attribute)

    @kick_protection_count.setter
    def kick_protection_count(self, value: int):
        self._data[self.__kick_protection_count_attribute] = value
