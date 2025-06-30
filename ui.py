'''
The ui module contains functions for user interaction:
displaying menus, requesting input data, and showing results in the console.
'''

import tabulate


def main_menu():
    '''Displays the main menu and returns the user's choice.'''
    prompt = (
        '\n=== Main Menu ===\n'
        '1. Search for films\n'
        '2. Query statistics\n'
        '0. Exit\n\n'
        'Enter menu item number (0–2): '
    )

    while True:
        choice = input(prompt).strip()
        if choice in ('0', '1', '2'):
            return choice
        print('Invalid choice. Please try again.')


def confirm_exit():
    '''Asks the user to confirm program exit.'''
    print('\nDo you really want to exit?')
    print('0. Yes, exit')
    print('1. No, return to main menu')
    return input('Your choice: ').strip()


def show_search_menu():
    '''Displays the film search menu and returns the user's choice.'''
    print('\n=== Film Search ===')
    print('1. By keyword')
    print('2. By genre and year range')
    print('3. By actor (first and last name)')
    print('4. By film length')
    return input('Choose search method: ').strip()


def show_pagination_menu():
    '''Displays pagination menu and returns the user's choice.'''
    print('\nShow next 10 films?')
    print('1. Yes')
    print('2. No, return to menu')
    return input('Your choice: ').strip()


def show_stat_menu():
    '''Displays the statistics menu and returns the user's choice.'''
    print('\n=== Statistics ===')
    print('1. Top 5 popular queries')
    print('2. Last 5 queries')
    print('3. Search queries by type')
    print('4. Query frequency by actors')
    return input('Choose an option: ').strip()


def prompt_keyword():
    '''Asks the user for a keyword to search film titles.'''
    return input('\nEnter a keyword to search in film titles: ').strip()


def prompt_actor_name():
    '''Asks the user for the actor's first and last name to search.'''
    print('\nEnter actor details for search (can be left empty):')
    first = input('Actor first name: ').strip()
    last = input('Actor last name: ').strip()
    return first, last


def prompt_genre_and_years(genres, min_year, max_year):
    '''Asks the user for genre and year range to search films.'''
    print('\nGenres in the database:')
    for genre in genres:
        print(f'- {genre}')
    print(f'Available years: from {min_year} to {max_year}')

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
        print('Invalid input. Please try again.')


def display_results(results, start_index=1):
    '''
    Displays search results as a table.
    results: List of dictionaries with film information.
    start_index: Number to start numbering results from.
    '''
    if not results:
        print('No results found.')
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
