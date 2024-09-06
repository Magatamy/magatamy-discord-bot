from copy import deepcopy
from datetime import time
from .sqlite_requests import (db_insert_data, db_creator, db_get_data, db_get_all_data, db_get_data_for_time,
                              db_update_data, db_get_sorted, db_check_columns, db_delete_data)

DATABASE = 'database.db'


class AsyncDatabaseObject:
    def __init__(self, table_name: str, primary_key: str, data_record: dict = None):
        self.table_name = table_name
        self.primary_key = primary_key
        self.data_record = data_record
        self._static_data = None
        self._data = None

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self._data):
            result = self._data[self._iter_index]
            self._iter_index += 1
            return result
        else:
            raise StopIteration

    def __create_table(self, columns: list) -> bool:
        with db_creator.DatabaseCreator(DATABASE) as db:
            return db.create_table(self.table_name, columns)

    def __check_columns_for_changes(self, columns: list) -> bool:
        with db_check_columns.CheckColumns(DATABASE) as db:
            return db.check_columns_for_changes(self.table_name, columns)

    def create_table(self):
        columns = deepcopy(self.columns)
        columns.insert(0, (self.primary_key, 'INTEGER PRIMARY KEY'))

        result = self.__create_table(columns)

        if not result:
            self.__check_columns_for_changes(columns)

    async def load(self, get_columns='*', condition_data: dict = None, create: bool = True) -> bool:
        if not condition_data:
            condition_data = self.data_record
        if not get_columns:
            get_columns = tuple([self.primary_key])

        async with db_get_data.AsyncGetData(DATABASE) as db:
            result = await db.get_data(self.table_name, condition_data, get_columns)

            if not result and self.data_record and create:
                await self.insert(self.data_record)
                result = await db.get_data(self.table_name, condition_data, get_columns)

            if not result:
                return False

            self._data = deepcopy(result[0])
            self._static_data = deepcopy(result[0])

        if result:
            return True

    async def load_all(self, get_columns='*') -> bool:
        if not get_columns:
            get_columns = tuple([self.primary_key])

        async with db_get_all_data.AsyncGetAllData(DATABASE) as db:
            result = await db.get_all_data(self.table_name, get_columns)
            self._data = self.get_objects_from_tuple(data=result)

        if result:
            return True

    async def load_for_time(self, time_column: str, condition_data: dict = None, time_range: time = None, get_columns='*') -> bool:
        if not get_columns:
            get_columns = tuple([self.primary_key])
        if not condition_data:
            condition_data = self.data_record
        if not time_range:
            time_range = time(hour=1)

        async with db_get_data_for_time.AsyncGetDataForTime(DATABASE) as db:
            result = await db.get_data_for_time(self.table_name, condition_data, time_range, get_columns, time_column)
            self._data = self.get_objects_from_tuple(data=result)

        if result:
            return True

    async def insert(self, data: dict = None):
        if not data:
            data = self.data_record
        async with db_insert_data.AsyncInsertData(DATABASE) as db:
            await db.insert_data(self.table_name, data)

    async def delete(self, condition_data: dict = None) -> bool:
        if not condition_data:
            condition_data = self.data_record
        async with db_delete_data.AsyncDeleteData(DATABASE) as db:
            return await db.delete_data(self.table_name, condition_data)

    async def update(self, data: dict = None, condition_data: str = None):
        if not data:
            if not self._data:
                return
            data = {}
            for i in self._data:
                if self._data[i] == self._static_data.get(i):
                    continue
                data.update({i: self._data[i]})
            if not data:
                return

        if not condition_data:
            condition_data = self.data_record

        async with db_update_data.AsyncUpdateData(DATABASE) as db:
            await db.update_data(self.table_name, data, condition_data)

    async def get_sorted(self, condition_where: str, order_by: str, limit: int, get_column: str):
        async with db_get_sorted.AsyncGetSorted(DATABASE) as db:
            return await db.get_sorted(self.table_name, condition_where, order_by, limit, get_column)

    @staticmethod
    def get_objects_from_tuple(data: tuple[dict]) -> list:
        return list()

    @property
    def columns(self) -> list:
        return list()
