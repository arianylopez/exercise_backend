-- SIN INDEX

"QUERY PLAN"
"Bitmap Heap Scan on film_work  (cost=4.31..15.47 rows=3 width=90) (actual time=0.107..0.115 rows=2 loops=1)"
"  Recheck Cond: (creation_date = '2020-01-01'::date)"
"  Heap Blocks: exact=2"
"  ->  Bitmap Index Scan on idx_film_work_creation_date  (cost=0.00..4.31 rows=3 width=0) (actual time=0.097..0.097 rows=2 loops=1)"
"        Index Cond: (creation_date = '2020-01-01'::date)"
"Planning Time: 41.451 ms"
"Execution Time: 0.251 ms"

-- CON INDEX

"Bitmap Heap Scan on film_work  (cost=4.31..15.47 rows=3 width=90) (actual time=0.023..0.026 rows=2 loops=1)"
"  Recheck Cond: (creation_date = '2020-01-01'::date)"
"  Heap Blocks: exact=2"
"  ->  Bitmap Index Scan on idx_film_work_creation_date  (cost=0.00..4.31 rows=3 width=0) (actual time=0.017..0.017 rows=2 loops=1)"
"        Index Cond: (creation_date = '2020-01-01'::date)"
"Planning Time: 0.086 ms"
"Execution Time: 0.048 ms"