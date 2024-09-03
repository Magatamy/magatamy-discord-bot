from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'anti_nuke'


class AntiNukeTable(AsyncDatabaseObject):
    __guild_id_attribute = 'guild_id'
    __block_role_id_attribute = 'block_role_id'

    def __init__(self, guild_id: int = None):
        data_record = {self.__guild_id_attribute: guild_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__guild_id_attribute, data_record=data_record)

    @property
    def block_role_id(self) -> int:
        return self._data.get(self.__block_role_id_attribute)

    @block_role_id.setter
    def block_role_id(self, value):
        self._data[self.__block_role_id_attribute] = value

    @property
    def columns(self) -> list:
        return [
            (self.__block_role_id_attribute, 'INTEGER', 'NULL')
        ]
