import aiosqlite


class AsyncGetAllData:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    async def get_all_data(self, table_name: str, get_columns: str | tuple) -> tuple:
        async with self.connection.cursor() as cursor:
            if type(get_columns) is tuple:
                get_columns = ', '.join(get_columns)

            query = f'SELECT {get_columns} FROM {table_name}'
            await cursor.execute(query)
            result = await cursor.fetchall()

            return tuple({cursor.description[i][0]: value for i, value in enumerate(record)} for record in result)

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
