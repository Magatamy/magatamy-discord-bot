import sqlite3


class DatabaseCreator:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def create_table(self, table_name: str, columns: list) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            existing_table = cursor.fetchone()

            if existing_table:
                return False
            else:
                query = f'CREATE TABLE IF NOT EXISTS {table_name} ('
                query += ', '.join(
                    [f'{column[0]} {column[1]} DEFAULT {column[2]}' if len(column) == 3 else f'{column[0]} {column[1]}'
                     for column in columns])
                query += ')'

                cursor.execute(query)
                self.connection.commit()
                return True
        finally:
            cursor.close()

    def __connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def __close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()
