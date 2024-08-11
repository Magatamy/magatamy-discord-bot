from copy import deepcopy
from datetime import time, datetime
from ..database_object import AsyncDatabaseObject

TABLE_NAME = 'saturday_channels'


class SaturdayChannelsTable(AsyncDatabaseObject):
    __channel_id_attribute = 'channel_id'
    __timezone_attribute = 'timezone'
    __time_attribute = 'time'
    __started_saturday_attribute = 'started_saturday'

    def __init__(self, channel_id: int = None):
        data_record = {self.__channel_id_attribute: channel_id}
        super().__init__(table_name=TABLE_NAME, primary_key=self.__channel_id_attribute, data_record=data_record)

    @property
    def channel_id(self) -> int:
        return self._data.get(self.__channel_id_attribute)

    @channel_id.setter
    def channel_id(self, value):
        self._data[self.__channel_id_attribute] = value

    @property
    def started_saturday(self) -> bool:
        return self._data.get(self.__started_saturday_attribute)

    @started_saturday.setter
    def started_saturday(self, value):
        self._data[self.__started_saturday_attribute] = value

    @property
    def timezone(self) -> str:
        return self._data.get(self.__timezone_attribute)

    @timezone.setter
    def timezone(self, value):
        self._data[self.__timezone_attribute] = value

    @property
    def time(self) -> time:
        value = self._data.get(self.__time_attribute)
        return datetime.strptime(value, '%H:%M:%S').time()

    @time.setter
    def time(self, value: time):
        self._data[self.__time_attribute] = value.strftime('%H:%M:%S')

    @property
    def columns(self) -> list:
        return [
            (self.__timezone_attribute, 'TEXT', 'NULL'),
            (self.__time_attribute, 'DATE', 'NULL'),
            (self.__started_saturday_attribute, 'BOOLEAN', 'FALSE')
        ]

    def get_objects_from_tuple(self, data: tuple[dict]) -> list:
        objects: list[SaturdayChannelsTable] = []
        for i in data:
            new_object = SaturdayChannelsTable(channel_id=i.get(self.__channel_id_attribute))
            new_object._data = deepcopy(i)
            new_object._static_data = deepcopy(i)
            objects.append(new_object)

        return objects

