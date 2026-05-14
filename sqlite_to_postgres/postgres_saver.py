import psycopg2
from psycopg2.extras import execute_values
from dataclasses import astuple, fields

class PostgresSaver:
    def __init__(self, connection):
        self.connection = connection
    
    def save_all_data(self, data: list, table_name: str, dataclass_type):
        if not data: 
            return
        
        cursor = self.connection.cursor()
        field_names = [field.name for field in fields(dataclass_type)]
        columns = ', '.join(field_names)

        update_cols = [f"{col} = EXCLUDED.{col}" for col in field_names if col != 'id']
        if update_cols:
            on_conflict = f"ON CONFLICT (id) DO UPDATE SET {', '.join(update_cols)}"
        else:
            on_conflict = "ON CONFLICT (id) DO NOTHING"

        query = f"""
            INSERT INTO content.{table_name} ({columns})
            VALUES %s
            {on_conflict}
        """

        values = [astuple(item) for item in data] 
        execute_values(cursor, query, values)
        self.connection.commit()