'''
The formatter module contains functions for formatting MongoDB logs
into a tabular text format.
'''

import collections
from typing import List, Dict, Any
from datetime import datetime

import tabulate


def format_mongo_logs(logs: List[Dict[str, Any]]) -> str:
    '''
    Formats a list of MongoDB logs as a tabular string.
    logs: List of log entries as dictionaries with 'query' and 'timestamp' fields.
    return: A string containing the formatted table.
    '''
    table = []
    for entry in logs:
        query_type = entry.get('query', {}).get('type', '—')
        details = {
            i: j
            for i, j in entry.get('query', {}).items()
            if i != 'type'
        }
        timestamp = entry.get('timestamp')

        timestamp_str = (
            timestamp.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(timestamp, datetime)
            else '—'
        )

        table.append([query_type, details, timestamp_str])

    headers = ['Query Type', 'Query Details', 'Timestamp']
    return tabulate.tabulate(
        table,
        headers=headers,
        tablefmt='fancy_grid',
        stralign='left'
    )


def format_actor_full_log(actor_logs: List[Dict[str, Any]]) -> str:
    '''
    Formats actor query history including search frequency and details.
    actor_logs: List of query logs as dictionaries with 'query' and 'timestamp' fields.
    return: A string containing the formatted table.
    '''
    table = []
    actor_counter = collections.Counter()

    for entry in actor_logs:
        query = entry.get('query', {})
        actor_name = ''

        first = query.get('first_name', '')
        last = query.get('last_name', '')
        if first and last:
            actor_name = f"{first} {last}"
        elif first:
            actor_name = first
        elif last:
            actor_name = last
        else:
            actor_name = '—'

        actor_counter[actor_name] += 1

        query_type = query.get('type', '—')
        details = {
            i: j
            for i, j in query.items()
            if i != 'type'
        }
        timestamp = entry.get('timestamp')
        timestamp_str = (
            timestamp.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(timestamp, datetime)
            else '—'
        )

        table.append([actor_name, actor_counter[actor_name], query_type, details, timestamp_str])

    headers = ['Actor (Search)', 'Frequency', 'Query Type', 'Query Details', 'Timestamp']
    return tabulate.tabulate(
        table,
        headers=headers,
        tablefmt='fancy_grid',
        stralign='left'
    )
