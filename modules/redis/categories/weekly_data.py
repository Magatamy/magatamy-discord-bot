import json
from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'weekly_data'


class WeeklyData(RedisObject):
    __weekly_servers_attribute = 'weekly_servers'
    __weekly_users_attribute = 'weekly_users'
    __weekday_number_attribute = 'weekday_number'

    def __init__(self, key: int = None):
        """key is client_id"""
        self.key = key
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def weekday_number(self) -> int:
        return self._data.get(self.__weekday_number_attribute)

    @weekday_number.setter
    def weekday_number(self, value: int):
        self._data[self.__weekday_number_attribute] = value

    @property
    def weekly_servers(self) -> list:
        data = self._data.get(self.__weekly_servers_attribute)
        if data is None:
            return [0, 0, 0, 0, 0, 0, 0]
        return json.loads(data)

    @weekly_servers.setter
    def weekly_servers(self, value: list):
        self._data[self.__weekly_servers_attribute] = json.dumps(value)

    @property
    def weekly_users(self) -> list:
        data = self._data.get(self.__weekly_users_attribute)
        if data is None:
            return [0, 0, 0, 0, 0, 0, 0]
        return json.loads(data)

    @weekly_users.setter
    def weekly_users(self, value: list):
        self._data[self.__weekly_users_attribute] = json.dumps(value)