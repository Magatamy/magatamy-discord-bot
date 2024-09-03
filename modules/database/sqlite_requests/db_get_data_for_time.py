import aiosqlite

from datetime import datetime, time, timedelta


class AsyncGetDataForTime:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.connection = None

    async def get_data_for_time(self, table_name: str, condition_data: dict, time_range: time,
                                get_columns: str | tuple, time_column: str) -> tuple:
        async with self.connection.cursor() as cursor:
            if isinstance(get_columns, tuple):
                get_columns = ', '.join(get_columns)

            duration = timedelta(hours=time_range.hour, minutes=time_range.minute, seconds=time_range.second)
            current_time = datetime.now()
            start_time = current_time - duration
            end_time = current_time

            conditions = " AND ".join([f"{key} = ?" for key in condition_data.keys()])
            query = f"""
                SELECT {get_columns} 
                FROM {table_name}
                WHERE {conditions}
                AND {time_column} BETWEEN ? AND ?
            """
            params = list(condition_data.values()) + [start_time, end_time]

            await cursor.execute(query, params)
            return tuple(await cursor.fetchall())

    async def __connect(self):
        self.connection = await aiosqlite.connect(self.db_name)

    async def __close(self):
        if self.connection:
            await self.connection.close()

    async def __aenter__(self):
        await self.__connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__close()
