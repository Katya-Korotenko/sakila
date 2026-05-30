import sys
import re

from movie_searcher import MovieSearcher
from history_search import *


class Menu(MovieSearcher):

    def __init__(self):
        self.logger = SearchLogger()
        self.main_options = {
            "1": ("Search movies.", self.show_submenu_for_movies),
            "2": ("Top searches movies.", self.top_searches),
            "0": ("Exit", lambda: sys.exit(0)),}

    def show_submenu_for_movies(self):
        sub_options = {
            "1": ("Search movies by keyword.",self.handle_keyword_search),
            "2": ("Search movies by genre.", self.handle_genre_search),
            "3": ("Search movies by year ",self.handle_year_search),
            "0": ("Back", lambda: self.show_menu(self.main_options)),}
        self.show_menu(sub_options)
    # основной поиск по году
    def handle_year_search(self):
        pattern = r'^(\d{4})(?:(?:\s*-\s*|\s+)(\d{4}))?$'
        years = self.get_year_range()
        min_year = years[0]['min']
        max_year = years[0]['max']
        print(f"Choose a year range between {min_year} and {max_year}")
        input_year = input("Enter year: ")
        match = re.match(pattern, input_year)
        if match:
            year_from = int(match.group(1))
            year_to = int(match.group(2)) if match.group(2) else year_from
            if not (min_year <= year_from <= max_year and min_year <= year_to <= max_year):
                print(f"Years must be between {min_year} and {max_year}")
                self.handle_year_search()
                return
            movies = self.search_by_year(year_from, year_to, offset=0)
            self.logger.log_search(
                search_type="year",
                params={"year_from": year_from, "year_to": year_to},
                results_count=len(movies))
            self.print_films(movies, lambda offset: self.search_by_year(year_from, year_to, offset))

        else:
            print("Invalid format.")
            self.handle_year_search()

            #  поиск по жанру
    def handle_genre_search(self):
        genres = self.get_genres()
        genre = self.print_genres(genres)
        movies = self.search_by_genre(genre, offset=0)
        self.logger.log_search(
            search_type="genre",
            params={"genre": genre},
            results_count=len(movies)
        )
        self.print_films(movies, lambda offset: self.search_by_genre(genre, offset))
    #поиск по ключевому слову
    def handle_keyword_search(self):
        keyword = input("What movie do you want to search?: ")
        movies = self.search_by_keyword(keyword, offset=0)
        self.logger.log_search(
            search_type="keyword",
            params={"keyword": keyword},
            results_count=len(movies)
        )
        self.print_films(movies, lambda offset: self.search_by_keyword(keyword, offset))

    # в процессе реализации
    def top_searches(self):
        print("Top searches")


    # вывод всех жанров
    def print_genres(self, genres):
        print("===Genres===")
        for index, gen in enumerate(genres, start=1):
            print(f"{index}. {gen['name']}")

        choice = input("Select genre number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(genres):
            return genres[int(choice) - 1]['name']
        print("Invalid choice")
        return self.print_genres(genres)

    # выводит фильмы
    def print_films(self, movies, search_func, offset=0):
        print("===Result===")
        if not movies:
            print("Movies not found.")
            self.show_menu(self.main_options)
        for movie in movies:
            print(f"{movie['title']}({movie['release_year']})---{movie['name']}---{movie['description']}")

        if len(movies) >= 10:
            choice = input("Back to menu [0] | Next 10 movies [n]").lower()
            if choice == 'n':
                next_movies = search_func(offset + 10)
                self.print_films(next_movies, search_func, offset + 10)
            self.show_menu(self.main_options)
        self.show_menu(self.main_options)



    # выводит меню
    @staticmethod
    def show_menu(options):

        for key, (label, _) in options.items():
            print(f"{key}. {label}")

        choice = input("Select a menu option: ")

        if choice in options:
            options[choice][1]()
        else:
            print("Invalid choice, try again")
            Menu.show_menu(options)




