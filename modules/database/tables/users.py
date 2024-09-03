from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'users'


class UsersTable(AsyncDatabaseObject):
    __member_id_attribute = 'member_id'
    __ban_count_attribute = 'ban_count'

    def __init__(self, member_id: int = None):
        data_record = {self.__member_id_attribute: member_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__member_id_attribute, data_record=data_record)

    @property
    def ban_count(self) -> int:
        return self._data.get(self.__ban_count_attribute)

    @ban_count.setter
    def ban_count(self, value):
        self._data[self.__ban_count_attribute] = value

    @property
    def columns(self) -> list:
        return [
            (self.__ban_count_attribute, 'INTEGER', 'NULL')
        ]

