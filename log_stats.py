'''
The log_stats module contains functions for statistical processing of query logs
from MongoDB.
'''

import collections
from datetime import datetime
from log_writer import POSSIBLE_KEYS
import settings
import display_utils


def get_top_queries(limit: int = 5) -> list[tuple[str, int]]:
    '''
    Collects all parameter values from query_type and params,
    and returns the top most popular combinations.
    Args:
        limit (int): Number of top items to return. Defaults to 5.
    Returns:
        List of tuples (parameter_combination, count) sorted by count descending.
    '''

    collection = settings.get_mongo_collection()
    cursor = collection.find({})

    all_items = []

    for doc in cursor:
        query_type = doc.get('query_type')
        params = doc.get('params', {})
        if not query_type or not isinstance(params, dict):
            continue

        for key in POSSIBLE_KEYS:
            value = params.get(key)
            if value is not None and value != '':
                item = f"{query_type}.{key}:{value}".strip().lower()
                all_items.append(item)

    counter = collections.Counter(all_items)
    return counter.most_common(limit)


def get_last_queries(limit: int = 10) -> list[dict]:
    '''
    Fetches the most recent search queries from the logs.
    Args:
        limit (int): Number of recent queries to retrieve. Defaults to 10.
    Returns:
        List of MongoDB documents representing recent query logs, sorted by timestamp descending.
    '''

    collection = settings.get_mongo_collection()
    return list(collection.find({}).sort('timestamp', -1).limit(limit))


def get_queries_by_type(query_type: str, limit: int = 5, fetch_limit: int = 100) -> list[dict]:
    '''
    Retrieves up to `limit` unique entries by query_type,
    uniqueness based on params, from the last `fetch_limit` records.
    Args:
        query_type (str): The query type to filter by.
        limit (int): Maximum number of unique results to return. Defaults to 5.
        fetch_limit (int): Number of recent records to fetch from DB. Defaults to 100.
    Returns:
        List of unique query documents filtered by query_type.
    '''

    collection = settings.get_mongo_collection()

    recent = list(collection.find({'query_type': query_type}).sort('timestamp', -1).limit(fetch_limit))

    unique_params = set()
    unique_results = []

    for doc in recent:
        params = doc.get('params', {})
        params_tuple = tuple(sorted(params.items()))

        if params_tuple not in unique_params:
            unique_params.add(params_tuple)
            unique_results.append(doc)

            if len(unique_results) >= limit:
                break

    return unique_results


def handle_query_count(query_type: str = None, show: bool = False) -> None:
    '''
    Logs a query type occurrence in MongoDB and optionally displays counts per query type.
    Args:
        query_type (str, optional): The type of query to log. If invalid, a warning is printed.
        show (bool): If True, displays the count of queries per type.
    Returns:
        None
    '''

    collection = settings.get_mongo_collection()

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

        display_utils.display_query_counts_table(dict(data))
