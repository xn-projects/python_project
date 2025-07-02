'''
Main module: запуск программы, обработка меню и подключение к БД.
'''

import ui
import settings


def main() -> None:
    '''
    Main entry point of the program.
    Establishes connections to MySQL and MongoDB, displays a welcome message,
    and starts the main menu loop to handle user choices:
    - Perform film searches
    - Show query statistics
    - Exit the program with confirmation
    Catches and reports any unexpected exceptions and ensures that the
    database connection is properly closed upon exit.
    Args:
        None
    Returns:
        None
    Raises:
        Exception: Propagates any unexpected exceptions encountered during execution,
        which are caught and logged inside the function.
'''
    connection_query = None
    try:
        connection_query = settings.create_mysql_connection()

        print(f'{ui.colorize("\nWelcome to the Sakila database movie search system.", "yellow")}')

        while True:
            choice = ui.main_menu()

            if choice == '1':
                ui.handle_search_menu(connection_query)

            elif choice == '2':
                ui.handle_stat_menu()

            elif choice == '3' and ui.confirm_exit(connection_query):
                print(f'{ui.colorize("\nGoodbye!", "yellow")}')
                break

            else:
                print(f'{ui.colorize("\nInvalid choice, please try again", "red")}')

    except Exception as e:
        print(f'{ui.colorize(f"\nAn unexpected error occurred: {e}", "red")}')

    finally:
        if connection_query:
            connection_query.close()

if __name__ == '__main__':
    main()
