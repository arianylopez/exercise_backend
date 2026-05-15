import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
import logging
import os
from dotenv import load_dotenv

from models import Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork
from sqlite_extractor import SQLiteExtractor
from postgres_saver import PostgresSaver

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

dotenv_path = os.path.join(BASE_DIR, 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: psycopg2.extensions.connection):
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    tables_mapping = {
        'genre': Genre,
        'film_work': FilmWork,
        'person': Person,
        'genre_film_work': GenreFilmWork,
        'person_film_work': PersonFilmWork
    }

    for table_name, dataclass_type in tables_mapping.items():
        logger.info(f"Extracting data from {table_name}...")
        try:
            for batch in sqlite_extractor.extract_data(table_name, batch_size=200):
                data = []
                for row in batch:
                    row_dict = dict(row)
                    
                    if 'created_at' in row_dict:
                        row_dict['created'] = row_dict.pop('created_at')
                    if 'updated_at' in row_dict:
                        row_dict['modified'] = row_dict.pop('updated_at')
                        
                    data.append(dataclass_type(**row_dict))
                
                postgres_saver.save_all_data(data, table_name, dataclass_type)
            logger.info(f"Tabla migrada con éxito: {table_name}")
        except Exception as e:
            logger.error(f"Error migrando la tabla {table_name}: {e}")
            pg_conn.rollback()

if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', '5432')
    }

    sqlite_db_path = os.path.join(BASE_DIR, 'db.sqlite')

    try:
        with sqlite3.connect(sqlite_db_path) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            sqlite_conn.row_factory = sqlite3.Row
            load_from_sqlite(sqlite_conn, pg_conn)
    except Exception as e:
        logger.error(f"Error fatal de conexión a base de datos: {e}")