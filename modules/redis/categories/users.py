from ..redis_object import RedisObject

CATEGORY_NAME = 'users'


class Users(RedisObject):
    __member_id_attribute = 'member_id'
    __name_attribute = 'name'

    def __init__(self, member_id: int = None):
        super().__init__(category=CATEGORY_NAME, key=member_id)

    @property
    def name(self) -> str:
        return self._data.get(self.__name_attribute)

    @name.setter
    def name(self, value: str):
        self._update_data[self.__name_attribute] = value
