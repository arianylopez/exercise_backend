import sqlite3
from typing import Generator, List

class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def extract_data(self, table_name: str, batch_size: int = 100) -> Generator[List[sqlite3.Row], None, None]: 
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch 