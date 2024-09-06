from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'request_vanilla'


class RequestVanilla(AsyncDatabaseObject):
    __member_id_attribute = 'member_id'
    __status_attribute = 'status'
    __nickname_attribute = 'nickname'
    __name_and_age_attribute = 'name_and_age'
    __found_info_attribute = 'found_info'
    __action_on_server_attribute = 'action_on_server'
    __read_rule_attribute = 'read_rule'

    def __init__(self, member_id: int = None):
        data_record = {self.__member_id_attribute: member_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__member_id_attribute, data_record=data_record)

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

    @property
    def columns(self) -> list:
        return [
            (self.__status_attribute, 'INTEGER', 'NULL'),
            (self.__nickname_attribute, 'TEXT', 'NULL'),
            (self.__name_and_age_attribute, 'TEXT', 'NULL'),
            (self.__found_info_attribute, 'TEXT', 'NULL'),
            (self.__action_on_server_attribute, 'TEXT', 'NULL'),
            (self.__read_rule_attribute, 'TEXT', 'NULL')
        ]

