'''
Main module of the console application for searching movies in the Sakila database.
Allows to:
1. Perform various types of movie searches.
2. View search query statistics.
3. Log queries.
'''

import ui
import mysql_connector
import log_writer
import log_stats

def handle_pagination(results: list, start_index: int) -> bool:
    '''Displays results and pagination menu.'''
    if start_index >= len(results):
        print('No more results available.')
        log_writer.log_error(f'Tried to display page starting at index {start_index}, but total results are {len(results)}.')
        return False

    ui.display_results(results, start_index=start_index)
    return ui.show_pagination_menu() == '1'

def handle_keyword_search() -> None:
    '''Handles search by keyword.'''
    keyword = ui.prompt_keyword()
    offset = 0
    while True:
        results = mysql_connector.search_by_keyword(keyword, offset)
        log_writer.log_query('keyword', {'keyword': keyword})
        if handle_pagination(results, offset):
            offset += 10
        else:
            break

def handle_genre_year_search() -> None:
    '''Handles search by genre and year range.'''
    genres, min_year, max_year = mysql_connector.get_genres_and_year_range()
    genre, year_from, year_to = ui.prompt_genre_and_years(genres, min_year, max_year)
    offset = 0
    while True:
        results = mysql_connector.search_by_genre_and_years(genre, year_from, year_to, offset)
        log_writer.log_query('genre_year', {
            'genre': genre,
            'year_from': year_from,
            'year_to': year_to
        })
        if handle_pagination(results, offset):
            offset += 10
        else:
            break

def handle_actor_search() -> None:
    '''Handles search by actor's name.'''
    first_name, last_name = ui.prompt_actor_name()
    offset = 0
    while True:
        results = mysql_connector.search_by_actor_name(first_name, last_name, offset)
        log_writer.log_query('actor_name', {
            'first_name': first_name,
            'last_name': last_name
        })
        if handle_pagination(results, offset):
            offset += 10
        else:
            break

def handle_length_search() -> None:
    '''Handles search by movie length.'''
    min_len_db, max_len_db = mysql_connector.get_length_range()
    print(f'\nAvailable movie length range: from {min_len_db} to {max_len_db} minutes.')
    min_length, max_length = ui.length_prompt()

    if min_length < min_len_db or max_length > max_len_db:
        print('Error: entered range is outside the allowed limits.')
        return

    offset = 0
    while True:
        results = mysql_connector.search_by_length_range(min_length, max_length, offset)
        log_writer.log_query('length_range', {
            'min_length': min_length,
            'max_length': max_length
        })
        if handle_pagination(results, offset):
            offset += 10
        else:
            break

def handle_search_menu() -> None:
    '''Handles user choice of search type.'''
    search_choice = ui.show_search_menu()
    if search_choice == '1':
        handle_keyword_search()
    elif search_choice == '2':
        handle_genre_year_search()
    elif search_choice == '3':
        handle_actor_search()
    elif search_choice == '4':
        handle_length_search()
    else:
        print('Invalid search method selection.')

def handle_actor_frequency_stat() -> None:
    '''
    Requests actor's name from user and displays query frequency statistics.
    '''
    actor_name = input('Enter the actor\'s name to get query statistics: ').strip()
    if not actor_name:
        print('Actor\'s name cannot be empty.')
        return

    count = log_stats.get_actor_query_frequency(actor_name)
    print(f'Number of queries for actor "{actor_name}": {count}')

def handle_stat_menu() -> None:
    '''Handles search query statistics menu.'''
    stat_choice = ui.show_stat_menu()
    if stat_choice == '1':
        top = log_stats.get_top_queries()
        print('\nTop 5 popular queries:')
        for query, count in top:
            print(f"{query}: {count}")
    elif stat_choice == '2':
        last = log_stats.get_last_queries()
        print('\nLast 5 queries:')
        for query in last:
            print(query)
    elif stat_choice == '3':
        type_name = input('Enter query type (keyword, genre_year, actor_name, length_range, rating): ').strip()
        filtered = log_stats.get_queries_by_type(type_name)
        print(f'\nQueries of type "{type_name}":')
        for query in filtered:
            print(query)
    elif stat_choice == '4':
        handle_actor_frequency_stat()
    else:
        print('Invalid choice.')

def main() -> None:
    '''Main program entry point.'''
    print('Welcome to the Sakila database movie search system.')

    while True:
        choice = ui.main_menu()
        if choice == '1':
            handle_search_menu()
        elif choice == '2':
            handle_stat_menu()
        elif choice == '0' and ui.confirm_exit():
            print('Goodbye!')
            break

if __name__ == '__main__':
    main()
