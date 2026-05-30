import sys
import re

from movie_searcher import MovieSearcher


class Menu(MovieSearcher):

    def __init__(self):
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
        pattern = r'^(\d{4})(?:-(\d{4}))?$'
        years = self.get_year_range()
        for year in years:
            print(f"Choose a year range between {year['min']} and {year['max']}")
        input_year = input("Enter year: ")
        match = re.match(pattern, input_year)
        if match:
            year_from = int(match.group(1))
            year_to = int(match.group(2)) if match.group(2) else year_from
            movies = self.search_by_year(year_from, year_to, offset=0)
            self.print_films(movies, lambda offset: self.search_by_year(year_from, year_to, offset))

    #  поиск по жанру
    def handle_genre_search(self):
        genres = self.get_genres()
        selected = self.print_genres(genres)
        movies = self.search_by_genre(selected, offset=0)
        self.print_films(movies, lambda offset: self.search_by_genre(selected, offset))
    #поиск по ключевому слову
    def handle_keyword_search(self):
        choice = input("What movie do you want to search?: ")
        movies = self.search_by_keyword(choice, offset=0)
        self.print_films(movies, lambda offset: self.search_by_keyword(choice, offset))

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




