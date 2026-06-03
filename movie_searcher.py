from typing import Any
from mysql_connector import execute_query
from sql_queries import (
    SEARCH_TITLE_QUERY, ALL_GENERS_QUERY,
    MIN_MAX_YEAR_QUERY, YEAR_RANGE_QUERY, CHOICE_GENRE_QUERY
)


class MovieSearcher:
    """Handles operational interactions and queries against the MySQL movie catalog."""

    def search_by_keyword(self, choice: str, offset: int = 0) -> list[dict[str, Any]]:
        """Queries the database for movies containing a partial string match in their titles.

        Args:
            choice: The phrase or keyword to look up.
            offset: The pagination index offset.
        """
        return execute_query(SEARCH_TITLE_QUERY, (f"%{choice}%", offset))

    def get_genres(self) -> list[dict[str, Any]]:
        """Extracts a distinct list of all available movie genres available in the database."""
        return execute_query(ALL_GENERS_QUERY)

    def get_year_range(self) -> list[dict[str, Any]]:
        """Fetches the lower and upper bounds of movie release years from the database."""
        return execute_query(MIN_MAX_YEAR_QUERY)

    def search_by_year(self, year_from: int, year_to: int, offset: int = 0) -> list[dict[str, Any]]:
        """Retrieves movies published within a specific bounding window of years.

        Args:
            year_from: The starting year of the filter interval.
            year_to: The ending year of the filter interval.
            offset: The pagination index offset.
        """
        return execute_query(YEAR_RANGE_QUERY, (year_from, year_to, offset))

    def search_by_genre(self, genre: str, offset: int = 0) -> list[dict[str, Any]]:
        """Extracts movies categorized strictly under a designated genre category name.

        Args:
            genre: The exact name value of the target genre category.
            offset: The pagination index offset.
        """
        return execute_query(CHOICE_GENRE_QUERY, (genre, offset))