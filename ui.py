'''
The ui module contains functions for user interaction:
displaying menus, requesting input data, and showing results in the console.
'''

import tabulate
import mysql_connector
import log_writer
import log_stats


COLORS = {
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "red": "\033[91m",
    "green": "\033[92m",
    "reset": "\033[0m"
}

def colorize(text: str, color: str) -> str:
    return f"{COLORS[color]}{text}{COLORS['reset']}"

@log_writer.log_error(display=True)
def main_menu():
    '''Displays the main menu and returns the user's choice.'''
    prompt = (
        f'{colorize("\n=== Main Menu ===", "yellow")}\n\n'
        f'{colorize("1. Search for films", "blue")}\n'
        f'{colorize("2. Query statistics", "blue")}\n'
        f'{colorize("3. Exit", "red")}\n\n'
        'Enter menu item number (0–2): '
    )

    while True:
        choice = input(prompt).strip()
        if choice in ('1', '2', '3'):
            return choice
        print('\nInvalid choice. Please try again.')

@log_writer.log_error(display=True)
def confirm_exit(conn):
    '''Asks the user to confirm program exit.'''
    print(f'{colorize("\nDo you really want to exit?", "yellow")}')
    print(f'{colorize("\n1. Yes, exit", "red")}')
    print(f'{colorize("2. No, return to main menu", "blue")}\n')
    return input('Your choice: ').strip()

@log_writer.log_error(display=True)
def handle_search_menu(conn) -> None:
    '''Displays the film search menu and handles user choice of search type.'''
    print(f'{colorize("\n=== Film Search ===", "yellow")}\n')
    print(f'{colorize("1. By keyword", "blue")}')
    print(f'{colorize("2. By genre and year range", "blue")}')
    print(f'{colorize("3. By actor (first and last name)", "blue")}')
    print(f'{colorize("4. By film length", "blue")}\n')

    search_choice = input('Choose search method: ').strip()

    if search_choice == '1':
        handle_keyword_search(conn)
    elif search_choice == '2':
        handle_genre_year_search(conn)
    elif search_choice == '3':
        handle_actor_search(conn)
    elif search_choice == '4':
        handle_length_search(conn)
    else:
        print('Invalid search method selection.')

@log_writer.log_error(display=True)
def handle_keyword_search(conn) -> None:
    '''Prompts user for keyword and handles search by keyword with pagination.'''
    keyword = input('\nEnter a keyword to search in film titles: ').strip()
    offset = 0
    while True:
        results = mysql_connector.search_by_keyword(conn, keyword, offset)
        log_writer.log_query('keyword', {'keyword': keyword})
        if handle_pagination(results, offset, display_films_table):
            offset += 10
        else:
            break

@log_writer.log_error(display=True)
def handle_actor_search(conn) -> None:
    '''Prompts user for actor's first and last name, then handles search with pagination.'''
    print(f'{colorize("\nEnter actor details for search (can be left empty):", "yellow")}\n')
    first_name = input(f'{colorize("Actor first name: ", "blue")}').strip()
    last_name = input(f'{colorize("Actor last name: ", "blue")}').strip()

    name_part = f"{first_name} {last_name}".strip() or first_name or last_name

    offset = 0
    while True:
        results = mysql_connector.search_by_actor_name_partial(conn, name_part, offset)
        log_writer.log_query('actor_name', {
            'first_name': first_name,
            'last_name': last_name
        })
        if handle_pagination(results, offset, display_films_table):
            offset += 10
        else:
            break

@log_writer.log_error(display=True)
def handle_genre_year_search(conn) -> None:
    '''Prompts user for genre and year range, then handles search with pagination.'''
    genres, min_year, max_year = mysql_connector.get_genres_and_year_range(conn)

    print(f'{colorize("\nGenres in the database:", "yellow")}\n')
    for g in genres:
        print(f'- {colorize(g, "blue")}')
    print(f'\n{colorize(f"Available years: from {min_year} to {max_year}", "yellow")}\n')

    while True:
        genre = input('Enter genre: ').strip()
        if genre not in genres:
            print('\nInvalid genre. Please try again.')
            continue
        break

    while True:
        try:
            year_from = int(input(f'\nEnter start year (from {min_year}): ').strip())
            year_to_input = input(f'\nEnter end year (up to {max_year}, or leave empty for single year): ').strip()
            year_to = int(year_to_input) if year_to_input else year_from

            if (
                min_year <= year_from <= max_year
                and min_year <= year_to <= max_year
                and year_from <= year_to
            ):
                break
            print('Year range is invalid. Please try again.')
        except ValueError:
            print('Input error. Please enter valid years.')

    offset = 0
    while True:
        results = mysql_connector.search_by_genre_and_years(
            conn, genre, year_from, year_to, offset=offset
        )
        log_writer.log_query('genre_year', {
            'genre': genre,
            'year_from': year_from,
            'year_to': year_to
        })
        if handle_pagination(results, offset, display_films_table):
            offset += 10
        else:
            break

@log_writer.log_error(display=True)
def handle_length_search(conn) -> None:
    '''
    Handles search by movie length with pagination.
    '''
    min_len_db, max_len_db = mysql_connector.get_length_range(conn)
    print(colorize(
        f"\nAvailable movie length range: from {min_len_db} to {max_len_db} minutes.",
        "yellow"
    ))

    while True:
        try:
            min_length = int(input('\nEnter minimum film length (in minutes): ').strip())
            max_length_input = input('Enter maximum film length (in minutes, or leave empty for same as minimum): ').strip()
            max_length = int(max_length_input) if max_length_input else min_length

            if min_length < min_len_db or max_length > max_len_db:
                print(f'\nError: Entered range is outside allowed limits ({min_len_db}–{max_len_db}).')
                continue

            if min_length > max_length:
                print('\nError: Minimum length cannot be greater than maximum length.')
                continue

            break
        except ValueError:
            print('\nInvalid input. Please enter valid integers.')

    offset = 0
    while True:
        results = mysql_connector.search_by_length_range(conn, min_length, max_length, offset)
        log_writer.log_query('length_range', {
            'min_length': min_length,
            'max_length': max_length
        })

        if handle_pagination(results, offset, display_films_table):
            offset += 10
        else:
            break

@log_writer.log_error(display=True)
def handle_pagination(results: list[dict], start_index: int, display_function: callable) -> bool:
    '''
    Universal pagination function.
    - results: a list of dictionaries with the results.
    - start_index: the index to start displaying the page from.
    - display_function: a function to display the current page (takes a list of dictionaries).
    Returns True if the user wants to continue pagination, otherwise False.
    '''
    page_size = 10
    end_index = start_index + page_size
    page_results = results[start_index:end_index]

    if not page_results:
        print('\nNo more results available.')
        log_writer.log_error(f'Tried to display page starting at index {start_index}, but total results are {len(results)}.')
        return False

    display_function(page_results)

    print(f'{colorize(f"\nShow next {page_size} results?", "yellow")}\n')
    print(f'{colorize("1. Yes", "blue")}')
    print(f'{colorize("2. No, return to menu", "blue")}\n')

    choice = input('Your choice: ').strip()
    return choice == '1'

@log_writer.log_error(display=True)
def display_films_table(films: list[dict]) -> None:
    if not films:
        print("\nNo films found.")
        return

    table = []
    for film in films:
        row = [
            film.get('film_id', ''),
            film.get('title', ''),
            (film.get('description', '')[:50] + '...') if film.get('description') else '',
            film.get('release_year', ''),
            film.get('length', ''),
            film.get('rating', ''),
        ]
        table.append(row)

    headers = ['ID', 'Title', 'Description', 'Year', 'Length', 'Rating']
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))

@log_writer.log_error(display=True)
def display_queries_table(queries: list[dict]) -> None:
    """
    Universal function to display search queries as a formatted table.
    Shows only non-empty parameters from each query.
    """
    if not queries:
        print("\nNo queries found.")
        return

    table = []
    for entry in queries:
        filtered_params = {i: j for i, j in entry.get('params', {}).items() if j not in (None, '')}
        params_str = ', '.join(f"{i}={j}" for i, j in filtered_params.items())

        row = [
            str(entry.get('_id', '')),
            entry.get('query_type', ''),
            entry.get('timestamp').strftime('%Y-%m-%d %H:%M:%S') if entry.get('timestamp') else '',
            params_str
        ]
        table.append(row)

    headers = ['ID', 'Query Type', 'Timestamp', 'Parameters']
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))

@log_writer.log_error(display=True)
def handle_stat_menu() -> None:
    '''Displays the statistics menu and handles user choice.'''
    print(f'{colorize("\n=== Statistics ===", "yellow")}\n')
    print(f'{colorize("1. Top 5 popular queries", "blue")}')
    print(f'{colorize("2. Last 5 queries", "blue")}')
    print(f'{colorize("3. Search queries by type", "blue")}')
    print(f'{colorize("4. Frequency by query type", "blue")}\n')

    stat_choice = input('Choose an option: ').strip()

    if stat_choice == '1':
        top = log_stats.get_top_queries()
        print('\nTop 5 popular queries:')
        for query, count in top:
            print(f"{query}: {count}")

    elif stat_choice == '2':
        last = log_stats.get_last_queries(limit=5)
        print('\nLast 5 queries:')
        display_queries_table(last)

    elif stat_choice == '3':
        type_name = input('Enter query type (keyword, genre_year, actor_name, length_range): ').strip()
        filtered = log_stats.get_queries_by_type(type_name)
        print(f'\nQueries of type "{type_name}":')
        display_queries_table(filtered)

    elif stat_choice == '4':
        log_stats.handle_query_count(show=True)

    else:
        print('Invalid choice.')

def show_error(message: str) -> None:
    '''
    Displays an error message colored in red.
    '''
    print(colorize(message, 'red'))
