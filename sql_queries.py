# наброски запросов
SEARCH_TITLE_QUERY = """
                     SELECT f.title, f.description, f.release_year, c.name
                     FROM film f
                              LEFT JOIN film_category fc ON fc.film_id = f.film_id
                              LEFT JOIN category c ON c.category_id = fc.category_id
                     WHERE title LIKE %s LIMIT 10
                     OFFSET %s;
                     """

MIN_MAX_YEAR_QUERY = """
                     select min(release_year) as min, max(release_year) as max
                     from film;"""

YEAR_RANGE_QUERY = """
                   SELECT title, description, release_year, c.name
                   from film f
                            join film_category fc on fc.film_id = f.film_id
                            join category c on c.category_id = fc.category_id
                   where release_year between %s and %s limit 10
                   OFFSET %s;"""

ALL_GENERS_QUERY = """
                   SELECT DISTINCT name
                   FROM category;"""

CHOICE_GENRE_QUERY = """
                     SELECT f.title, f.description, f.release_year, c.name
                     FROM film f
                              LEFT JOIN film_category fc ON fc.film_id = f.film_id
                              LEFT JOIN category c ON c.category_id = fc.category_id
                     WHERE name LIKE %s LIMIT 10
                     OFFSET %s;"""
