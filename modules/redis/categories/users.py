from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'users'


class Users(RedisObject):
    __private_name_attribute = 'private_name'
    __private_limit_attribute = 'private_limit'
    __private_hide_attribute = 'private_hide'
    __private_close_attribute = 'private_close'
    __private_mute_all_attribute = 'private_mute_all'

    def __init__(self, key: int = None):
        """key is member_id"""
        self.key = key
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def private_name(self) -> str:
        return self._data.get(self.__private_name_attribute)

    @private_name.setter
    def private_name(self, value: str):
        self._data[self.__private_name_attribute] = value

    @property
    def private_limit(self) -> int:
        return self._data.get(self.__private_limit_attribute)

    @private_limit.setter
    def private_limit(self, value: int):
        self._data[self.__private_limit_attribute] = value

    @property
    def private_hide(self) -> bool:
        return self._data.get(self.__private_hide_attribute)

    @private_hide.setter
    def private_hide(self, value: bool):
        self._data[self.__private_hide_attribute] = value

    @property
    def private_close(self) -> bool:
        return self._data.get(self.__private_close_attribute)

    @private_close.setter
    def private_close(self, value: bool):
        self._data[self.__private_close_attribute] = value

    @property
    def private_mute_all(self) -> bool:
        return self._data.get(self.__private_mute_all_attribute)

    @private_mute_all.setter
    def private_mute_all(self, value: bool):
        self._data[self.__private_mute_all_attribute] = value
