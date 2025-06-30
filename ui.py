'''
The ui module contains functions for user interaction:
displaying menus, requesting input data, and showing results in the console.
'''

import tabulate
import settings

def main_menu():
    '''Displays the main menu and returns the user's choice.'''
    prompt = (
    f'{settings.COLORS['yellow']}\n=== Main Menu ==={settings.COLORS['reset']}\n'
    f'{settings.COLORS['blue']}1. Search for films{settings.COLORS['reset']}\n'
    f'{settings.COLORS['blue']}2. Query statistics{settings.COLORS['reset']}\n'
    f'{settings.COLORS['red']}0. Exit{settings.COLORS['reset']}\n\n'
    'Enter menu item number (0–2): '
)
    
    while True:
        choice = input(prompt).strip()
        if choice in ('0', '1', '2'):
            return choice
        print('\nInvalid choice. Please try again.')


def confirm_exit():
    '''Asks the user to confirm program exit.'''
    print(f'{settings.COLORS['yellow']}\nDo you really want to exit?{settings.COLORS['reset']}')
    print(f'{settings.COLORS['red']}\n0. Yes, exit{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}1. No, return to main menu{settings.COLORS['reset']}\n')
    return input('Your choice: ').strip()


def show_search_menu():
    '''Displays the film search menu and returns the user's choice.'''
    print(f'{settings.COLORS['yellow']}\n=== Film Search ==={settings.COLORS['reset']}\n')
    print(f'{settings.COLORS['blue']}1. By keyword{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}2. By genre and year range{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}3. By actor (first and last name){settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}4. By film length{settings.COLORS['reset']}\n')
    return input('Choose search method: ').strip()


def show_pagination_menu():
    '''Displays pagination menu and returns the user's choice.'''
    print(f'{settings.COLORS['yellow']}\nShow next 10 films?{settings.COLORS['reset']}\n')
    print(f'{settings.COLORS['blue']}1. Yes{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}2. No, return to menu{settings.COLORS['reset']}\n')
    return input('Your choice: ').strip()


def show_stat_menu():
    '''Displays the statistics menu and returns the user's choice.'''
    print(f'{settings.COLORS['yellow']}\n=== Statistics ==={settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}1. Top 5 popular queries{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}2. Last 5 queries{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}3. Search queries by type{settings.COLORS['reset']}')
    print(f'{settings.COLORS['blue']}4. Query frequency by actors{settings.COLORS['reset']}\n')
    return input('Choose an option: ').strip()


def prompt_keyword():
    '''Asks the user for a keyword to search film titles.'''
    return input('\nEnter a keyword to search in film titles: ').strip()


def prompt_actor_name():
    '''Asks the user for the actor's first and last name to search.'''
    print(f'{settings.COLORS['yellow']}\nEnter actor details for search (can be left empty):{settings.COLORS['reset']}\n')
    first = input(f'{settings.COLORS['blue']}Actor first name: {settings.COLORS['reset']}\n').strip()
    last = input(f'{settings.COLORS['blue']}Actor last name: {settings.COLORS['reset']}\n').strip()
    return first, last


def prompt_genre_and_years(genres, min_year, max_year):
    '''Asks the user for genre and year range to search films.'''
    print(f'{settings.COLORS['yellow']}\nGenres in the database:{settings.COLORS['reset']}\n')
    for genre in genres:
        print(f'- {genre}')
    print(f'{settings.COLORS['yellow']}\nAvailable years: from {min_year} to {max_year}{settings.COLORS['reset']}\n')

    while True:
        genre = input('Enter genre: ').strip()
        if genre not in genres:
            print('Invalid genre. Please try again.')
            continue
        break

    while True:
        try:
            year_from = int(input(f'Enter start year (from {min_year}): ').strip())
            year_to = input(f'Enter end year (up to {max_year}, or leave empty for single year): ').strip()
            year_to = int(year_to) if year_to else year_from

            if (
                min_year <= year_from <= max_year
                and min_year <= year_to <= max_year
                and year_from <= year_to
            ):
                return genre, year_from, year_to
        except ValueError:
            pass
        print('Input error. Please try again.')


def length_prompt():
    '''Asks the user for minimum and maximum film length.'''
    while True:
        try:
            min_length = int(input('Enter minimum film length (in minutes): ').strip())
            max_length = input('Enter maximum film length (in minutes, or leave empty): ').strip()
            max_length = int(max_length) if max_length else min_length
            if 0 < min_length <= max_length:
                return min_length, max_length
        except ValueError:
            pass
        print('\nInvalid input. Please try again.')


def display_results(results, start_index=1):
    '''
    Displays search results as a table.
    results: List of dictionaries with film information.
    start_index: Number to start numbering results from.
    '''
    if not results:
        print('\nNo results found.')
        return

    table = []
    for i, row in enumerate(results, start=start_index):
        table.append(
            [
                i,
                row.get('title', ''),
                row.get('release_year', ''),
                row.get('category', ''),
                row.get('rating', ''),
                row.get('length', ''),
                row.get('actors', ''),
            ]
        )

    headers = ['No.', 'Title', 'Year', 'Genre', 'Rating', 'Length', 'Actors']
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))


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
        filtered_params = {k: v for k, v in entry.get('params', {}).items() if v not in (None, '')}
        params_str = ', '.join(f"{k}={v}" for k, v in filtered_params.items())

        row = [
            str(entry.get('_id', '')),
            entry.get('query_type', ''),
            entry.get('timestamp').strftime('%Y-%m-%d %H:%M:%S') if entry.get('timestamp') else '',
            params_str,
        ]
        table.append(row)

    headers = ['ID', 'Query Type', 'Timestamp', 'Params Summary']
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))
