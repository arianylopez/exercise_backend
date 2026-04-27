CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.genre (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    created     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.film_work (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT CHECK (rating >= 0 AND rating <= 10),
    type          VARCHAR(50) NOT NULL DEFAULT 'movie',
    created       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.person (
    id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    created   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    genre_id     UUID NOT NULL REFERENCES content.genre(id)     ON DELETE CASCADE,
    film_work_id UUID NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    created      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id    UUID NOT NULL REFERENCES content.person(id)    ON DELETE CASCADE,
    film_work_id UUID NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    role         VARCHAR(100),
    created      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

ALTER TABLE content.genre_film_work
    ADD CONSTRAINT uq_genre_film_work UNIQUE (genre_id, film_work_id);

ALTER TABLE content.person_film_work
    ADD CONSTRAINT uq_person_film_work UNIQUE (person_id, film_work_id, role);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);

CREATE INDEX film_work_rating_idx ON content.film_work(rating);

CREATE INDEX film_work_type_idx ON content.film_work(type);

CREATE INDEX person_full_name_idx ON content.person(full_name);

CREATE INDEX genre_film_work_film_work_id_idx ON content.genre_film_work(film_work_id);

CREATE INDEX person_film_work_film_work_id_idx ON content.person_film_work(film_work_id);

CREATE INDEX person_film_work_role_idx ON content.person_film_work(role);