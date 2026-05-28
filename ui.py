import sys

from mysql_connector import get_cursor
from sql_queries import SEARCH_TITLE_QUERY


class MovieSearcher:

    def execute_query(self, query, parameter = None):
        with get_cursor() as cursor:
            cursor.execute(query, parameter)
            return cursor.fetchall()

    def search_by_keyword(self):
        choice = input("What movie do you want to search?: ")
        result = self.execute_query(SEARCH_TITLE_QUERY, (f"%{choice.upper()}%",))
        return (row for row in result)


    # в процессе реализации
    def search_by_gener(self):
        print("Search by gener")


    # в процессе реализации
    def top_searches(self):
        print("Top searches")

class Menu(MovieSearcher):

    def __init__(self):
        self.main_options = {
            "1": ("Search film.", self.show_submenu_for_movies),
            "2": ("Top searches films.", self.top_searches),
            "0": ("Exit", lambda: sys.exit(0)),
        }

    def show_submenu_for_movies(self):
        sub_options = {
            "1": ("Search film by keyword.", lambda: self.print_films(self.search_by_keyword())),
            "2": ("Search film by gener.", self.search_by_gener),
            "0": ("Back", lambda: self.show_menu(self.main_options)),
        }
        self.show_menu(sub_options)

    def print_films(self, movies):
        print("===Result===")
        if not movies:
            print("No films found.")
            self.show_menu(self.main_options)
        for movie in movies:
            print(f"{movie['title']}({movie['release_year']})---{movie['description']}")


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




