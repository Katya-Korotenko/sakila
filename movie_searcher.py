from mysql_connector import execute_query
from sql_queries import *

class MovieSearcher:

    def search_by_keyword(self, choice, offset=0):
        return execute_query(SEARCH_TITLE_QUERY, (f"%{choice}%", offset,))

    def get_genres(self):
        return execute_query(ALL_GENERS_QUERY)

    def get_year_range(self):
        return execute_query(MIN_MAX_YEAR_QUERY)

    def search_by_year(self, year_from, year_to, offset = 10):
        return execute_query(YEAR_RANGE_QUERY,(year_from, year_to, offset))

    def search_by_genre(self, genre,  offset=0):
        return execute_query(CHOICE_GENRE_QUERY, (genre, offset,))



