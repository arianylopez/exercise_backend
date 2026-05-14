import sqlite3
import psycopg2
import pytest
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(BASE_DIR, 'config', '.env')
load_dotenv(dotenv_path=env_path)

@pytest.fixture(scope='session')
def sqlite_cursor():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sqlite_db_path = os.path.join(BASE_DIR, 'db.sqlite')
    
    conn = sqlite3.connect(sqlite_db_path)
    yield conn.cursor()
    conn.close()

@pytest.fixture(scope='session')
def postgres_cursor():
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432)
    }
    conn = psycopg2.connect(**dsl)
    yield conn.cursor()
    conn.close()

def test_film_work_count(sqlite_cursor, postgres_cursor):
    sqlite_cursor.execute("SELECT COUNT(*) FROM film_work;")
    postgres_cursor.execute("SELECT COUNT(*) FROM content.film_work;")
    assert sqlite_cursor.fetchone()[0] == postgres_cursor.fetchone()[0]

def test_film_work_content(sqlite_cursor, postgres_cursor):
    original_film_work_batch = sqlite_cursor.execute(
        "SELECT id, title, description FROM film_work ORDER BY id;"
    ).fetchall()
    
    postgres_cursor.execute("SELECT id::text, title, description FROM content.film_work ORDER BY id;")
    transferred_film_work_batch = postgres_cursor.fetchall()
    
    assert len(original_film_work_batch) == len(transferred_film_work_batch)
    assert original_film_work_batch == transferred_film_work_batch

def test_person_consistency(sqlite_cursor, postgres_cursor):
    original_persons_batch = sqlite_cursor.execute(
        "SELECT id, full_name FROM person ORDER BY id;"
    ).fetchall()
    
    postgres_cursor.execute("SELECT id::text, full_name FROM content.person ORDER BY id;")
    transferred_persons_batch = postgres_cursor.fetchall()
    
    assert len(original_persons_batch) == len(transferred_persons_batch)
    assert original_persons_batch == transferred_persons_batch

def test_genre_consistency(sqlite_cursor, postgres_cursor):
    original_genres_batch = sqlite_cursor.execute(
        "SELECT id, name, description FROM genre ORDER BY id;"
    ).fetchall()
    
    postgres_cursor.execute("SELECT id::text, name, description FROM content.genre ORDER BY id;")
    transferred_genres_batch = postgres_cursor.fetchall()
    
    assert len(original_genres_batch) == len(transferred_genres_batch)
    assert original_genres_batch == transferred_genres_batch

def test_genre_film_work_consistency(sqlite_cursor, postgres_cursor):
    original_relations_batch = sqlite_cursor.execute(
        "SELECT id, genre_id, film_work_id FROM genre_film_work ORDER BY id;"
    ).fetchall()
    
    postgres_cursor.execute("SELECT id::text, genre_id::text, film_work_id::text FROM content.genre_film_work ORDER BY id;")
    transferred_relations_batch = postgres_cursor.fetchall()
    
    assert len(original_relations_batch) == len(transferred_relations_batch)
    assert original_relations_batch == transferred_relations_batch

def test_person_film_work_consistency(sqlite_cursor, postgres_cursor):
    original_relations_batch = sqlite_cursor.execute(
        "SELECT id, person_id, film_work_id, role FROM person_film_work ORDER BY id;"
    ).fetchall()
    
    postgres_cursor.execute("SELECT id::text, person_id::text, film_work_id::text, role FROM content.person_film_work ORDER BY id;")
    transferred_relations_batch = postgres_cursor.fetchall()
    
    assert len(original_relations_batch) == len(transferred_relations_batch)
    assert original_relations_batch == transferred_relations_batch