from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'users'


class UsersTable(AsyncDatabaseObject):
    __member_id_attribute = 'member_id'

    def __init__(self, member_id=None):
        data_record = {self.__member_id_attribute: member_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__member_id_attribute, data_record=data_record)

    @property
    def columns(self) -> list:
        return []
