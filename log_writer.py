"""
The log_writer module contains functions for writing and formatting query logs
to MongoDB and displaying them in a tabular format.
"""

import logging
from functools import wraps
from datetime import datetime, timezone
from tabulate import tabulate
import settings
import ui

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

    collection = settings.get_mongo_collection()

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


def log_error(display=True):
    '''
    Decorator for logging exceptions and optionally displaying them.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.exception(e)
                if display:
                    ui.show_error(f'Error: {e}')
                return None
        return wrapper
    return decorator
