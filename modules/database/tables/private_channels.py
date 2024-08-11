from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'private_channels'


class PrivateChannelsTable(AsyncDatabaseObject):
    __channel_id_attribute = 'channel_id'
    __owner_id_attribute = 'owner_id'

    def __init__(self, channel_id: int = None, owner_id: int = None):
        data_record = {self.__channel_id_attribute: channel_id}
        if owner_id:
            data_record.update({self.__owner_id_attribute: owner_id})
        super().__init__(table_name=TABLE_NAME, primary_key=self.__channel_id_attribute, data_record=data_record)

    @property
    def owner_id(self) -> int:
        return self._data.get(self.__owner_id_attribute)

    @owner_id.setter
    def owner_id(self, value):
        self._data[self.__owner_id_attribute] = value

    @property
    def columns(self) -> list:
        return [
            (self.__owner_id_attribute, 'INTEGER', '0')
        ]
