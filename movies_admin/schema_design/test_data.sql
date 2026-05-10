-- Genera 5000 películas de prueba
INSERT INTO content.film_work (title, description, creation_date, rating, type)
SELECT
    'Film ' || i,
    'Description for film ' || i,
    DATE '2000-01-01' + (random() * 8000)::int,
    (random() * 100)::numeric(4,1),
    CASE WHEN random() > 0.3 THEN 'movie' ELSE 'tv_show' END
FROM generate_series(1, 5000) AS s(i);

-- Genera 200 géneros
INSERT INTO content.genre (name, description)
SELECT 'Genre ' || i, 'Description ' || i
FROM generate_series(1, 200) AS s(i);

-- Genera 2000 personas
INSERT INTO content.person (full_name)
SELECT 'Person ' || i
FROM generate_series(1, 2000) AS s(i);