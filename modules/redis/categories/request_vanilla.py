from ..redis_object import RedisObject

CATEGORY_NAME = 'request_vanilla'


class RequestVanilla(RedisObject):
    __status_attribute = 'status'
    __nickname_attribute = 'nickname'
    __name_and_age_attribute = 'name_and_age'
    __found_info_attribute = 'found_info'
    __action_on_server_attribute = 'action_on_server'
    __read_rule_attribute = 'read_rule'

    def __init__(self, key: int = None):
        """key is member_id"""
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def read_rule(self) -> str:
        return self._data.get(self.__read_rule_attribute)

    @read_rule.setter
    def read_rule(self, value: str):
        self._data[self.__read_rule_attribute] = value

    @property
    def action_on_server(self) -> str:
        return self._data.get(self.__action_on_server_attribute)

    @action_on_server.setter
    def action_on_server(self, value: str):
        self._data[self.__action_on_server_attribute] = value

    @property
    def found_info(self) -> str:
        return self._data.get(self.__found_info_attribute)

    @found_info.setter
    def found_info(self, value: str):
        self._data[self.__found_info_attribute] = value

    @property
    def nickname(self) -> str:
        return self._data.get(self.__nickname_attribute)

    @nickname.setter
    def nickname(self, value: str):
        self._data[self.__nickname_attribute] = value

    @property
    def name_and_age(self) -> str:
        return self._data.get(self.__name_and_age_attribute)

    @name_and_age.setter
    def name_and_age(self, value: str):
        self._data[self.__name_and_age_attribute] = value

    @property
    def status(self) -> int:
        return self._data.get(self.__status_attribute)

    @status.setter
    def status(self, value: int):
        self._data[self.__status_attribute] = value
