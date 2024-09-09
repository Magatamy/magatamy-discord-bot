from ..redis_object import RedisObject
from copy import deepcopy
from time import time

CATEGORY_NAME = 'saturday_channels'


class SaturdayChannels(RedisObject):
    __timezone_attribute = 'timezone'
    __time_attribute = 'time'
    __started_saturday_attribute = 'started_saturday'

    def __init__(self, key: int = None):
        """key is channel_id"""
        self.key = key
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def channel_id(self) -> int:
        return self._data.get(self.__channel_id_attribute)

    @channel_id.setter
    def channel_id(self, value: int):
        self._data[self.__channel_id_attribute] = value

    @property
    def started_saturday(self) -> bool:
        return self._data.get(self.__started_saturday_attribute)

    @started_saturday.setter
    def started_saturday(self, value: bool):
        self._data[self.__started_saturday_attribute] = value

    @property
    def timezone(self) -> str:
        return self._data.get(self.__timezone_attribute)

    @timezone.setter
    def timezone(self, value: str):
        self._data[self.__timezone_attribute] = value

    @property
    def timestamp(self) -> int:
        return self._data.get(self.__time_attribute)

    @timestamp.setter
    def timestamp(self, value: int):
        self._data[self.__time_attribute] = value
