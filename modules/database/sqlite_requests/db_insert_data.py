import aiosqlite


class AsyncInsertData:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    async def insert_data(self, table_name: str, data: dict):
        async with self.connection.cursor() as cursor:
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))

            query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

            await cursor.execute(query, tuple(data.values()))
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
