import aiosqlite


class AsyncGetSorted:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    async def get_sorted(self, table_name, condition, order_by, limit, get_column):
        async with self.connection.cursor() as cursor:
            query = f'SELECT {get_column} FROM {table_name} WHERE {condition} ORDER BY {order_by} LIMIT {limit}'
            
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
