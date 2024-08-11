from copy import deepcopy
from datetime import datetime, timedelta
from .sqlite_requests import (db_insert_data, db_creator, db_get_data, db_get_data_for_time,
                              db_update_data, db_get_sorted, db_check_columns, db_delete_data)

DATABASE = 'database.db'


class AsyncDatabaseObject:
    def __init__(self, table_name: str, primary_key: str, data_record: dict = None, data_insert: dict = None):
        self.table_name = table_name
        self.primary_key = primary_key
        self.data_record = data_record
        self.data_insert = data_insert
        self._data_for_time = None
        self._static_data = None
        self._data = None

    def __create_table(self, columns: list) -> bool:
        with db_creator.DatabaseCreator(DATABASE) as db:
            return db.create_table(self.table_name, columns)

    def __check_columns_for_changes(self, columns: list) -> bool:
        with db_check_columns.CheckColumns(DATABASE) as db:
            return db.check_columns_for_changes(self.table_name, columns)

    def create_table(self, columns: list):
        columns.insert(0, (self.primary_key, 'INTEGER PRIMARY KEY'))

        result = self.__create_table(columns)

        if not result:
            self.__check_columns_for_changes(columns)

    async def load_data(self, get_columns='*', condition_data: dict = None, time_in_minutes: int = None,
                        create: bool = True) -> bool:
        if not condition_data:
            condition_data = self.data_record
        if not get_columns:
            get_columns = tuple([self.primary_key])

        if not time_in_minutes:
            async with db_get_data.AsyncGetData(DATABASE) as db:
                result = await db.get_data(self.table_name, condition_data, get_columns)

                if not result and self.data_record and create:
                    await self.insert_data(self.data_record)
                    result = await db.get_data(self.table_name, condition_data, get_columns)

                if not result:
                    return False

                self._data = deepcopy(result[0])
                self._static_data = deepcopy(result[0])

        else:
            today = datetime.now()
            seven_days_ago = today - timedelta(minutes=time_in_minutes)
            time_range = ('date', seven_days_ago.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S'))

            async with db_get_data_for_time.AsyncGetDataForTime(DATABASE) as db:
                result = await db.get_data_for_time(self.table_name, condition_data, time_range, get_columns)
                self._data = result

        if result:
            return True

    async def insert_data(self, data: dict = None):
        if not data:
            data = self.data_insert
        async with db_insert_data.AsyncInsertData(DATABASE) as db:
            await db.insert_data(self.table_name, data)

    async def delete_data(self, condition_data: dict = None) -> bool:
        if not condition_data:
            condition_data = self.data_record
        async with db_delete_data.AsyncDeleteData(DATABASE) as db:
            return await db.delete_data(self.table_name, condition_data)

    async def update_data(self, data: dict = None, condition_data: str = None):
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
