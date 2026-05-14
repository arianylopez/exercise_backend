import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Genre:
    id: uuid.UUID
    name: str
    created: datetime
    modified: datetime
    description: Optional[str] = None

@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    type: str
    created: datetime
    modified: datetime
    description: Optional[str] = None
    creation_date: Optional[str] = None
    rating: Optional[float] = None
    certificate: Optional[str] = None
    file_path: Optional[str] = None

@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created: datetime
    modified: datetime

@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created: datetime

@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created: datetime