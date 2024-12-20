from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'subscriptions'


class Subscriptions(RedisObject):
    __user_id_attribute = 'user_id'
    __expiry_ts_attribute = 'expiry_ts'
    __is_forever_attribute = 'is_forever'

    def __init__(self, key: int = None):
        """key is guild_id"""
        self.key = key
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def user_id(self) -> int:
        return self._data.get(self.__user_id_attribute)

    @user_id.setter
    def user_id(self, value: int):
        self._data[self.__user_id_attribute] = value

    @property
    def expiry_ts(self) -> int:
        return self._data.get(self.__expiry_ts_attribute)

    @expiry_ts.setter
    def expiry_ts(self, value: int):
        self._data[self.__expiry_ts_attribute] = value

    @property
    def is_forever(self) -> bool:
        return self._data.get(self.__is_forever_attribute)

    @is_forever.setter
    def is_forever(self, value: bool):
        self._data[self.__is_forever_attribute] = value
