from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'users_click_button'


class UsersClickButton(RedisObject):
    __last_click_button_ts_attribute = 'last_click_button_ts'

    def __init__(self, key: int = None):
        """key is member_id"""
        self.key = key
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def last_click_button_ts(self) -> int:
        return self._data.get(self.__last_click_button_ts_attribute)

    @last_click_button_ts.setter
    def last_click_button_ts(self, value: int):
        self._data[self.__last_click_button_ts_attribute] = value
