# наброски запросов
SEARCH_TITLE_QUERY = """
    SELECT title, description, release_year
    FROM film
    WHERE title LIKE %s
    
"""
