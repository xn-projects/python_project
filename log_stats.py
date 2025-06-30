'''
The log_stats module contains functions for statistical processing of query logs
from MongoDB.
'''

import collections
from datetime import datetime
import settings


def get_queries_by_type(query_type: str) -> list[dict]:
    '''
    Returns a list of MongoDB documents filtered by query type.
    query_type: Type of the query (e.g., 'actor_partial', 'category', 'title', etc.).
    return: A list of dictionaries (documents) sorted by timestamp descending.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    return list(
        collection.find({'query_type': query_type}).sort('timestamp', -1)
    )


def get_actor_search_frequency(limit: int = 10) -> list[tuple[str, int]]:
    '''
    Returns the most frequent actor search queries.
    limit: Number of top frequent queries to return.
    return: A list of tuples (search query, occurrence count),
            sorted by descending frequency.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    cursor = collection.find({'query_type': 'actor_partial'})
    names = [
        doc.get('query', '').strip().lower()
        for doc in cursor
        if 'query' in doc
    ]
    counter = collections.Counter(names)
    return counter.most_common(limit)


def get_top_queries(limit: int = 10) -> list[tuple[str, int]]:
    '''
    Returns the most popular search queries of any type.
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
    Returns the most recent search queries.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    return list(collection.find({}).sort('timestamp', -1).limit(limit))


def get_actor_query_frequency(actor_name: str) -> int:
    '''
    Returns the number of queries for a specific actor.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    count = collection.count_documents({
        'query_type': 'actor_partial',
        'query': {'$regex': f'^{actor_name}$', '$options': 'i'}
    })
    return count