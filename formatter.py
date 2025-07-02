'''
The formatter module contains functions for formatting MongoDB logs
into a tabular text format.
'''

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
