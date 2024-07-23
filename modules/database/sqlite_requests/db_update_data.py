import aiosqlite


class AsyncUpdateData:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    async def update_data(self, table_name: str, data: dict, condition_data: dict):
        async with self.connection.cursor() as cursor:
            condition = ' AND '.join(f'{key} = ?' for key in condition_data.keys())
            set_values = ', '.join(f'{key} = ?' for key in data.keys())

            query = f'UPDATE {table_name} SET {set_values} WHERE {condition}'

            query_values = tuple(data.values()) + tuple(condition_data.values())
            await cursor.execute(query, query_values)
            await self.connection.commit()

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
