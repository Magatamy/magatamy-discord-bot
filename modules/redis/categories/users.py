from ..redis_object import RedisObject

CATEGORY_NAME = 'users'


class Users(RedisObject):
    __name_attribute = 'name'

    def __init__(self, key: int = None):
        """key is member_id"""
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def name(self) -> str:
        return self._data.get(self.__name_attribute)

    @name.setter
    def name(self, value: str):
        self._data[self.__name_attribute] = value
