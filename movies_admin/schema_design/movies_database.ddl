-- Crear el schema content
CREATE SCHEMA IF NOT EXISTS content;

-- Extensión para generar UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- TABLA: genre
-- ============================================================
CREATE TABLE IF NOT EXISTS content.genre (
    id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    created     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- TABLA: film_work
-- ============================================================
CREATE TABLE IF NOT EXISTS content.film_work (
    id            uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT CHECK (rating >= 0 AND rating <= 100),
    type          VARCHAR(20) NOT NULL CHECK (type IN ('movie', 'tv_show')),
    certificate   VARCHAR(512),
    file_path     TEXT,
    created       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- TABLA: person
-- ============================================================
CREATE TABLE IF NOT EXISTS content.person (
    id        uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    created   TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- TABLA intermedia: genre_film_work
-- ============================================================
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id           uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    genre_id     uuid NOT NULL REFERENCES content.genre(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    created      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT genre_film_work_film_work_id_genre_id_uniq
        UNIQUE (film_work_id, genre_id)
);

-- ============================================================
-- TABLA intermedia: person_film_work
-- ============================================================
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id           uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id    uuid NOT NULL REFERENCES content.person(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    role         VARCHAR(20) CHECK (role IN ('actor', 'writer', 'director')),
    created      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT person_film_work_person_id_film_work_id_role_uniq
        UNIQUE (person_id, film_work_id, role)
);

-- ============================================================
-- ÍNDICES para rendimiento de consultas
-- ============================================================
CREATE INDEX IF NOT EXISTS film_work_creation_date_idx
    ON content.film_work(creation_date);

CREATE INDEX IF NOT EXISTS film_work_rating_idx
    ON content.film_work(rating);

CREATE INDEX IF NOT EXISTS genre_film_work_film_work_idx
    ON content.genre_film_work(film_work_id);

CREATE INDEX IF NOT EXISTS genre_film_work_genre_idx
    ON content.genre_film_work(genre_id);

CREATE INDEX IF NOT EXISTS person_film_work_film_work_idx
    ON content.person_film_work(film_work_id);

CREATE INDEX IF NOT EXISTS person_film_work_person_idx
    ON content.person_film_work(person_id);