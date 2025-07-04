'''
Module display_utils provides functions to format and print various tables
related to queries and films, using ANSI color codes for terminal output.
'''

import tabulate

def display_query_counts_table(query_counts: dict) -> None:
    '''
    Prints a formatted table showing counts per query type.
    Args:
        query_counts (dict): Mapping of query type strings to counts.
    Returns:
        None
    '''

    data = [[q_type, count] for q_type, count in query_counts.items()]
    headers = ['Query Type', 'Count']
    print(tabulate.tabulate(data, headers=headers, tablefmt='grid'))


COLORS = {
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'red': '\033[91m',
    'reset': '\033[0m'
}

def colorize(text: str, color: str) -> str:
    '''
    Wraps the given text with ANSI escape sequences to colorize terminal output.
    Args:
        text (str): The text to colorize.
        color (str): The color name. Must be one of the keys in COLORS dict.
    Returns:
        str: Colorized text with ANSI codes.
    '''

    return f'{COLORS[color]}{text}{COLORS["reset"]}'


def display_queries_table(queries: list[dict]) -> None:
    '''
    Displays a formatted table of search queries.
    Only non-empty parameters for each query are shown.
    Args:
        queries (list of dict): List of query entries. Each entry should have keys
                                like '_id', 'query_type', 'timestamp', and 'params'.
    Returns:
        None
    '''

    if not queries:
        print('\nNo queries found.')
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


def display_top_parameters(top_params: list[tuple[str, int]]) -> None:
    '''
    Displays the top query parameters as a formatted table.
    Args:
        top_params (list of tuple): List of tuples where each tuple contains
                                    a string in the format 'query_type.key:value'
                                    and an integer count.
    Returns:
        None
    '''

    if not top_params:
        print('\nNo data to display.')
        return

    table = []
    for item, count in top_params:
        try:
            left, value = item.split(':', 1)
            query_type, key = left.split('.', 1)
        except ValueError:
            query_type, key, value = '', '', ''

        row = [query_type, key, value, count]
        table.append(row)

    headers = ['Query Type', 'Parameter', 'Value', 'Count']
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))


def display_films_table(films: list[dict]) -> None:
    '''
    Displays a formatted table of films.
    Args:
        films (list of dict): List of film entries with keys such as
                              'film_id', 'title', 'description', 'release_year',
                              'length', 'rating'.
    Returns:
        None
    '''

    if not films:
        print('\nNo films found.')
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
