import ui

from mongo_connector import *


def main():
    try:
        menu = ui.Menu()
        menu.show_menu(menu.main_options)
    finally:
        close_connection()


if __name__ == '__main__':
    main()

