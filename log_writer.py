'''
The log_writer module contains functions for writing and formatting query logs
to MongoDB and displaying them in a tabular format.
'''

from datetime import datetime, timezone
from tabulate import tabulate
import settings


POSSIBLE_KEYS = [
    'keyword',
    'genre',
    'year_from',
    'year_to',
    'first_name',
    'last_name',
    'min_length',
    'max_length'
]


def log_query(query_type: str, query_params: dict) -> None:
    '''
    Writes a query log to MongoDB with fixed keys.
    query_type: Type of the query (e.g., 'genre_year', 'actor_partial', etc.).
    query_params: Dictionary with query parameters.
    '''
    base_params = {key: None for key in POSSIBLE_KEYS}
    base_params.update(query_params)

    db = settings.MONGO_CLIENT['ich_edit']
    collection = db['final_project_100125_Kseniia']

    collection.insert_one({
        'query_type': query_type,
        'params': base_params,
        'timestamp': datetime.now(timezone.utc)
    })


def format_mongo_logs(logs: list[dict]) -> str:
    '''
    Formats a list of logs from MongoDB into a tabular representation.
    Expected log structure: keys 'query_type', 'params' (dict), 'timestamp'.
    logs: List of MongoDB documents with query logs.
    return: A string with the formatted logs table.
    '''
    table = []
    for entry in logs:
        query_type = entry.get('query_type', '—')
        params = entry.get('params', {})
        timestamp = entry.get('timestamp')
        time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else '—'

        params_str = ', '.join(
            f"{key}={repr(params.get(key))}" for key in POSSIBLE_KEYS if key in params
        )
        table.append([query_type, params_str, time_str])

    headers = ['Query Type', 'Parameters', 'Time']
    return tabulate(table, headers=headers, tablefmt='fancy_grid', stralign='left')


def format_actor_frequency(freq_list: list[tuple[str, int]]) -> str:
    '''
    Formats statistics of actor search query frequency into a table.
    freq_list: List of tuples (actor, query count).
    return: A string with the formatted frequency table.
    '''
    table = [[actor, count] for actor, count in freq_list]
    headers = ['Actor (name part)', 'Number of Queries']
    return tabulate(table, headers=headers, tablefmt='fancy_grid', stralign='left')


def log_error(message: str):
    with open('error.log', 'a', encoding='utf-8') as f:
        f.write(f"[ERROR] {message}\n")