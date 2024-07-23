import sqlite3


class CheckColumns:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    @staticmethod
    def __get_existing_columns(cursor, table_name):
        query = f"PRAGMA table_info({table_name})"
        cursor.execute(query)
        columns = cursor.fetchall()
        return [column[1] for column in columns]

    def check_columns_for_changes(self, table_name: str, columns: list) -> bool:
        cursor = self.connection.cursor()
        try:
            existing_columns = self.__get_existing_columns(cursor, table_name)
            is_changed = False

            for column in columns:
                if column[0] not in existing_columns:
                    query = f'ALTER TABLE {table_name} ADD COLUMN {column[0]} {column[1]}'
                    if len(column) == 3:
                        query += f' DEFAULT {column[2]}'
                    cursor.execute(query)
                    is_changed = True

            for column_name in existing_columns:
                if column_name not in [col[0] for col in columns]:
                    query = f'ALTER TABLE {table_name} DROP COLUMN {column_name}'
                    cursor.execute(query)
                    is_changed = True

            self.connection.commit()
            return is_changed
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
