import sys
import re

from movie_searcher import MovieSearcher
from history_search import SearchLogger
from statistic_search import Statistic


class Menu:
    YEAR_PATTERN = re.compile(r'^(\d{4})(?:(?:\s*-\s*|\s+)(\d{4}))?$')

    def __init__(self):
        self.logger = SearchLogger()
        self.searcher = MovieSearcher()
        self.statistic = Statistic()
        self.main_options = {
            "1": ("Search movies.", self.show_submenu_for_movies),
            "2": ("Top searches movies.", self.top_searches),
            "0": ("Exit", lambda: sys.exit(0)),
        }

    # ---------------- MENU SYSTEM ----------------

    def show_submenu_for_movies(self):
        sub_options = {
            "1": ("Search movies by keyword.", self.handle_keyword_search),
            "2": ("Search movies by genre.", self.handle_genre_search),
            "3": ("Search movies by year.", self.handle_year_search),
            "0": ("Back", lambda: self.show_menu(self.main_options)),
        }
        self.show_menu(sub_options)

    @staticmethod
    def show_menu(options):
        while True:
            for key, (label, _) in options.items():
                print(f"{key}. {label}")

            choice = input("Select a menu option: ").strip()
            if choice in options:
                options[choice][1]()
                return
            print("Invalid choice, try again")

    # ---------------- SEARCH WRAPPER ----------------

    def run_search(self, search_type, params, search_func):
        try:
            movies = search_func(0)
        except Exception as e:
            print(f"Error while searching: {e}")
            self.post_action_menu()
            return

        self.log_search(search_type, params, movies)

        try:
            self.print_films(movies, search_func)
        except Exception as e:
            print(f"Error while printing results: {e}")
            self.post_action_menu()
            return

    def log_search(self, search_type, params, movies):
        self.logger.log_search(
            search_type=search_type,
            params=params,
            results_count=len(movies)
        )

    # ---------------- SEARCH HANDLERS ----------------

    def handle_keyword_search(self):
        keyword = input("What movie do you want to search?: ").strip()
        if not keyword:
            print("Keyword cannot be empty.")
            self.post_action_menu()
            return

        self.run_search(
            "keyword",
            {"keyword": keyword},
            lambda offset: self.searcher.search_by_keyword(keyword, offset)
        )

    def handle_genre_search(self):
        try:
            genres = self.searcher.get_genres()
            if not genres:
                print("Genres not found.")
                self.post_action_menu()
                return
        except Exception as e:
            print(f"Error loading genres: {e}")
            self.post_action_menu()
            return

        genre = self.print_genres(genres)

        self.run_search(
            "genre",
            {"genre": genre},
            lambda offset: self.searcher.search_by_genre(genre, offset)
        )

    def handle_year_search(self):
        try:
            years = self.searcher.get_year_range()
        except Exception as e:
            print(f"Error loading year range: {e}")
            self.post_action_menu()
            return

        min_year = years[0]["min"]
        max_year = years[0]["max"]

        print(f"Choose a year range between {min_year} and {max_year}")

        while True:
            input_year = input("Enter year or range (YYYY or YYYY-YYYY): ").strip()
            match = self.YEAR_PATTERN.match(input_year)
            if not match:
                print("Invalid format.")
                continue

            year_from = int(match.group(1))
            year_to = int(match.group(2) or year_from)

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

    # ---------------- TOP SEARCHES ----------------

    def top_searches(self):
        try:
            top = self.statistic.get_top_searches()
        except Exception as e:
            print(f"Error loading statistics: {e}")
            self.post_action_menu()
            return

        print("=== Top 5 searches ===")
        for index, item in enumerate(top, start=1):
            params = item["_id"]
            params_str = ", ".join(f"{k}: {v}" for k, v in params.items())
            print(f"{index}. {params_str} — {item['count']} times")

        self.post_action_menu()

    # ---------------- GENRE SELECTION ----------------

    def print_genres_list(self, genres):
        for index, gen in enumerate(genres, start=1):
            print(f"{index}. {gen['name']}")

    def print_genres(self, genres):
        while True:
            print("===Genres===")
            self.print_genres_list(genres)

            choice = input("Select genre number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(genres):
                return genres[int(choice) - 1]["name"]

            print("Invalid choice")

    # ---------------- MOVIE OUTPUT ----------------

    def show_movie(self,movie):
        print("─" * 60)
        print(f"[{movie['release_year']}] {movie['title']}")
        print(f"   Genre: {movie['name']}")
        print(f"   {movie['description']}\n")

    def print_films(self, movies, search_func, offset=0):

        def show_page(movies):
            print("===Result===")
            for movie in movies:
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
                choice = input("Next [n] | Back [0]: ").strip().lower()
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

    # ---------------- POST ACTION MENU ----------------

    @staticmethod
    def post_action_menu():
        while True:
            try:
                choice = input("\n[b] Back | [e] Exit: ").strip().lower()
            except EOFError:
                print("\nInput error. Returning to menu.")
                return
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting.")
                sys.exit(0)
            if choice == "b":
                return
            if choice == "e":
                sys.exit(0)
