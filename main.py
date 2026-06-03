import ui
from mongo_connector import close_connection


def main() -> None:
    """Main entry point of the movie searcher application."""
    try:
        menu: ui.Menu = ui.Menu()
        menu.show_menu(menu.main_options)
    finally:
        close_connection()


if __name__ == '__main__':
    main()