'''
The log_stats module contains functions for statistical processing of query logs
from MongoDB.
'''

import collections
from datetime import datetime
import tabulate
import settings


def get_top_queries(limit: int = 10) -> list[tuple[str, int]]:
    '''
    Retrieves the most popular search queries across all types.
    Args:
        limit (int): The maximum number of top queries to return. Defaults to 10.
    Returns:
        List of tuples where each tuple contains a query string and its count,
        ordered from most to least frequent.
    Raises:
        None explicitly, but connection errors may occur on DB access.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    cursor = collection.find({})
    queries = [
        doc.get('query', '').strip().lower()
        for doc in cursor
        if 'query' in doc
    ]
    counter = collections.Counter(queries)
    return counter.most_common(limit)


def get_last_queries(limit: int = 10) -> list[dict]:
    '''
    Fetches the most recent search queries from the logs.
    Args:
        limit (int): Number of recent queries to retrieve. Defaults to 10.
    Returns:
        List of MongoDB documents representing recent query logs, sorted by timestamp descending.
    Raises:
        None explicitly, but connection errors may occur on DB access.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    return list(collection.find({}).sort('timestamp', -1).limit(limit))

def get_queries_by_type(query_type: str) -> list[dict]:
    '''
    Retrieves query log entries filtered by a specific query type.
    Args:
        query_type (str): Type of the query to filter by (e.g., 'actor_partial', 'category', etc.).
    Returns:
        List of MongoDB documents matching the query_type, sorted by timestamp descending.
    Raises:
        None explicitly, but connection errors may occur on DB access.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    return list(
        collection.find({'query_type': query_type}).sort('timestamp', -1)
    )


def handle_query_count(query_type: str = None, show: bool = False) -> None:
    '''
    Logs a query type occurrence in MongoDB and optionally displays counts per query type.
    Args:
        query_type (str, optional): The type of query to log. If invalid, a warning is printed.
        show (bool): If True, displays the count of queries per type.
    Returns:
        None
    Raises:
        None explicitly, but connection errors may occur on DB access.
    '''

    db = settings.MONGO_CLIENT['ich_edit']
    collection = db['final_project_100125_Kseniia']

    valid_types = ['keyword', 'genre_year', 'length_range', 'actor_name']

    if query_type:
        if query_type in valid_types:
            collection.insert_one({
                'query_type': query_type,
                'timestamp': datetime.utcnow()
            })
        else:
            print(f'Warning: Unknown query type "{query_type}"')

    if show:
        pipeline = [
            {
                '$group': {
                    '_id': '$query_type',
                    'count': {'$sum': 1}
                }
            }
        ]
        results = list(collection.aggregate(pipeline))
        counts = {item['_id']: item['count'] for item in results}

        data = []
        for q_type in valid_types:
            data.append([q_type, counts.get(q_type, 0)])

        display_query_counts_table(dict(data))


def display_query_counts_table(query_counts: dict) -> None:
    """
    Prints a formatted table showing counts per query type.
    Args:
        query_counts (dict): Mapping of query type strings to counts.
    Returns:
        None
    Raises:
        None
    """
    data = [[q_type, count] for q_type, count in query_counts.items()]
    headers = ['Query Type', 'Count']
    print(tabulate.tabulate(data, headers=headers, tablefmt='grid'))
