import aiosqlite


class AsyncDeleteData:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    async def delete_data(self, table_name: str, condition_data: dict) -> bool:
        async with self.connection.cursor() as cursor:
            conditions = " AND ".join([f"{key} = ?" for key in condition_data.keys()])
            query = f"DELETE FROM {table_name} WHERE {conditions}"

            await cursor.execute(query, tuple(condition_data.values()))
            await self.connection.commit()
            result = cursor.rowcount > 0

            return result

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
