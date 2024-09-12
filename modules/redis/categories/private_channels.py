from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'private_channels'


class PrivateChannels(RedisObject):
    __owner_id_attribute = 'owner_id'

    def __init__(self, key: int = None):
        """key is channel_id"""
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def owner_id(self) -> int:
        return self._data.get(self.__owner_id_attribute)

    @owner_id.setter
    def owner_id(self, value: int):
        self._data[self.__owner_id_attribute] = value
