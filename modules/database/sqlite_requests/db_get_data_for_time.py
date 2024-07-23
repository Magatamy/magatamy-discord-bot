import aiosqlite


class AsyncGetDataForTime:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.connection = None

    async def get_data_for_time(self, table_name: str, condition_data: dict,
                                time_range: tuple, get_columns: str | tuple) -> tuple:
        async with self.connection.cursor() as cursor:
            if type(get_columns) is tuple:
                get_columns = ', '.join(get_columns)
            conditions = " AND ".join([f"{key} = ?" for key in condition_data.keys()])
            query = f"""
                SELECT {get_columns} 
                FROM {table_name}
                WHERE {conditions}
                AND {time_range[0]} BETWEEN ? AND ?
            """
            params = list(condition_data.values()) + [time_range[1], time_range[2]]
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
