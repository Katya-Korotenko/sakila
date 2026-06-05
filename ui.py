import sys
import re
from typing import Any, Callable, Optional

from movie_searcher import MovieSearcher
from history_search import SearchLogger
from statistic_search import Statistic


class Menu:
    """Interactive CLI menu for searching movies in the Sakila database."""

    YEAR_PATTERN: re.Pattern = re.compile(r'^(\d{4})(?:(?:\s*-\s*|\s+)(\d{4}))?$')

    def __init__(self) -> None:
        """Initializes searcher, logger, statistics and main menu options."""
        self.logger: SearchLogger = SearchLogger()
        self.searcher: MovieSearcher = MovieSearcher()
        self.statistic: Statistic = Statistic()
        self.main_options: dict[str, tuple[str, Callable[[], Any]]] = {
            "1": ("Search movies.", self.show_submenu_for_movies),
            "2": ("Top searches movies.", self.top_searches),
            "0": ("Exit", lambda: sys.exit(0)),
        }

    def show_submenu_for_movies(self) -> None:
        """Displays submenu for selecting movie search type."""
        sub_options: dict[str, tuple[str, Callable[[], Any]]] = {
            "1": ("Search movies by keyword.", self.handle_keyword_search),
            "2": ("Search movies by genre.", self.handle_genre_search),
            "3": ("Search movies by year.", self.handle_year_search),
            "0": ("Back", lambda: self.show_menu(self.main_options)),
        }
        self.show_menu(sub_options)

    @staticmethod
    def show_menu(options: dict[str, tuple[str, Callable[[], Any]]]) -> None:
        """Displays menu options and handles user selection.

        Args:
            options: Dictionary mapping keys to labels and handler functions.
        """
        while True:
            for key, (label, _) in options.items():
                print(f"{key}. {label}")

            choice: str = input("Select a menu option: ").strip()
            if choice in options:
                options[choice][1]()
            else:
                print("Invalid choice, try again")

    def run_search(self, search_type: str, params: dict[str, Any],
                   search_func: Callable[[int], list[dict[str, Any]]]) -> None:
        """Executes search, logs results and displays movies.

        Args:
            search_type: Type of search (keyword, genre, year).
            params: Search parameters.
            search_func: Function that takes offset and returns movies.
        """
        try:
            movies: list[dict[str, Any]] = search_func(0)
        except Exception as e:
            print(f"Error while searching: {e}")
            self.post_action_menu()
            return

        self.log_search(search_type, params, movies)

        try:
            self.print_films(movies, search_func)
            self.show_submenu_for_movies()
        except Exception as e:
            print(f"Error while printing results: {e}")
            self.post_action_menu()
            return

    def log_search(self, search_type: str, params: dict[str, Any], movies: list[dict[str, Any]]) -> None:
        """Saves search query to MongoDB history."""
        self.logger.log_search(
            search_type=search_type,
            params=params,
            results_count=len(movies)
        )

    def handle_keyword_search(self) -> None:
        """Prompts user for keyword and searches movies by title."""
        keyword: str = input("What movie do you want to search?: ").strip()
        if not keyword:
            print("Keyword cannot be empty.")
            self.post_action_menu()
            return

        self.run_search(
            "keyword",
            {"keyword": keyword},
            lambda offset: self.searcher.search_by_keyword(keyword, offset)
        )

    def handle_genre_search(self) -> None:
        """Displays genres, prompts user to select one and searches movies."""
        try:
            genres: list[dict[str, Any]] = self.searcher.get_genres()
            if not genres:
                print("Genres not found.")
                self.post_action_menu()
                return
        except Exception as e:
            print(f"Error loading genres: {e}")
            self.post_action_menu()
            return

        genre: Optional[str] = self.print_genres(genres)
        if genre is None:
            self.show_submenu_for_movies()
            return

        self.run_search(
            "genre",
            {"genre": genre},
            lambda offset: self.searcher.search_by_genre(genre, offset)
        )

    def handle_year_search(self) -> None:
        """Prompts user for year or range and searches movies by release year."""
        try:
            years: list[dict[str, Any]] = self.searcher.get_year_range()
        except Exception as e:
            print(f"Error loading year range: {e}")
            self.post_action_menu()
            return

        min_year: int = int(years[0]["min"])
        max_year: int = int(years[0]["max"])

        print(f"Choose a year range between {min_year} and {max_year}")

        while True:
            input_year: str = input("Enter year or range (YYYY or YYYY-YYYY): ").strip()
            match = self.YEAR_PATTERN.match(input_year)
            if not match:
                print("Invalid format.")
                continue

            year_from: int = int(match.group(1))
            year_to: int = int(match.group(2) or year_from)

            if not (min_year <= year_from <= max_year and min_year <= year_to <= max_year):
                print(f"Years must be between {min_year} and {max_year}")
                continue
            if year_from > year_to:
                print("Start year cannot be greater than end year.")
                continue

            break

        self.run_search(
            "year",
            {"year_from": year_from, "year_to": year_to},
            lambda offset: self.searcher.search_by_year(year_from, year_to, offset)
        )

    def top_searches(self) -> None:
        """Displays top 5 most frequent search queries from history."""
        try:
            top: list[dict[str, Any]] = self.statistic.get_top_searches()
        except Exception as e:
            print(f"Error loading statistics: {e}")
            self.post_action_menu()
            return

        print("=== Top 5 searches ===")
        for index, item in enumerate(top, start=1):
            params: dict[str, Any] = item["_id"]
            params_str: str = ", ".join(f"{k}: {v}" for k, v in params.items())
            print(f"{index}. {params_str} — {item['count']} times")

        self.post_action_menu()

    def print_genres_list(self, genres: list[dict[str, Any]]) -> None:
        """Prints numbered list of genres."""
        for index, gen in enumerate(genres, start=1):
            print(f"{index}. {gen['name']}")

    def print_genres(self, genres: list[dict[str, Any]]) -> Optional[str]:
        """Prompts user to select a genre by number.

        Returns selected genre name or None if user goes back.
        """
        while True:
            print("===Genres===")
            self.print_genres_list(genres)

            choice: str = input("Select genre number (or [0] to go back): ").strip()
            if choice == "0":
                return None

            if choice.isdigit() and 1 <= int(choice) <= len(genres):
                return str(genres[int(choice) - 1]["name"])

            print("Invalid choice")

    def show_movie(self, movie: dict[str, Any]) -> None:
        """Prints formatted movie card with title, year, genre and description."""
        print("─" * 60)
        print(f"[{movie['release_year']}] {movie['title']}")
        print(f"   Genre: {movie['name']}")
        print(f"   {movie['description']}\n")

    def print_films(self, movies: list[dict[str, Any]],
                    search_func: Callable[[int], list[dict[str, Any]]], offset: int = 0) -> None:
        """Displays movies page by page with navigation to next 10 results."""

        def show_page(movies_list: list[dict[str, Any]]) -> None:
            print("===Result===")
            for movie in movies_list:
                self.show_movie(movie)

        if not movies:
            print("Movies not found.")
            self.post_action_menu()
            return

        show_page(movies)

        while True:
            if len(movies) < 10:
                break
            try:
                choice: str = input("Next [n] | Back [0]: ").strip().lower()
            except EOFError:
                print("\nInput error. Returning to menu.")
                self.post_action_menu()
                return
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting.")
                sys.exit(0)

            if choice == "n":
                offset += 10
                try:
                    movies = search_func(offset)
                except Exception as e:
                    print(f"Error loading next page: {e}")
                    self.post_action_menu()
                    return
                if not movies:
                    print("No more movies.")
                    self.post_action_menu()
                    return
                show_page(movies)
                continue
            elif choice == "0":
                self.post_action_menu()
                return
            else:
                print("Invalid choice. Please enter 'n' or '0'.")
                continue
        self.post_action_menu()

    @staticmethod
    def post_action_menu() -> None:
        """Prompts user to go back or exit the program."""
        while True:
            try:
                choice: str = input("\n[b] Back | [e] Exit: ").strip().lower()
            except EOFError:
                print("\nInput error. Returning to menu.")
                return None
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting.")
                sys.exit(0)
            if choice == "b":
                return None
            if choice == "e":
                sys.exit(0)