'''
Модуль log_stats содержит функции для статистической обработки логов запросов
из MongoDB.
'''

import collections
import settings


def get_queries_by_type(query_type: str) -> list[dict]:
    '''
    Возвращает список документов из MongoDB, отфильтрованных по типу запроса.
    query_type: Тип запроса (например, 'actor_partial', 'category', 'title' и т.д.).
    return: Отсортированный по времени список словарей (документов).
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    return list(
        collection.find({'query.type': query_type}).sort('timestamp', -1)
    )


def get_actor_search_frequency(limit: int = 10) -> list[tuple[str, int]]:
    '''
    Возвращает наиболее часто встречающиеся актёрские поисковые запросы.
    limit: Количество самых частотных запросов, которое нужно вернуть.
    return: Список кортежей (поисковый запрос, количество вхождений), 
             отсортированных по убыванию частоты.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    cursor = collection.find({'query.type': 'actor_partial'})
    names = [
        doc['query']['query'].strip().lower()
        for doc in cursor
        if 'query' in doc and 'query' in doc['query']
    ]
    counter = collections.Counter(names)
    return counter.most_common(limit)


def get_top_queries(limit: int = 10) -> list[tuple[str, int]]:
    '''
    Возвращает самые популярные поисковые запросы любого типа.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    cursor = collection.find({})
    queries = [
        doc['query']['query'].strip().lower()
        for doc in cursor
        if 'query' in doc and 'query' in doc['query']
    ]
    counter = collections.Counter(queries)
    return counter.most_common(limit)


def get_last_queries(limit: int = 10) -> list[dict]:
    '''
    Возвращает последние поисковые запросы.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    return list(collection.find({}).sort('timestamp', -1).limit(limit))


def get_actor_query_frequency(actor_name: str) -> int:
    '''
    Возвращает количество запросов для конкретного актёра.
    '''
    mongo_db = settings.MONGO_CLIENT['ich_edit']
    collection = mongo_db['final_project_100125_Kseniia']

    count = collection.count_documents({
        'query.type': 'actor_partial',
        'query.query': {'$regex': f'^{actor_name}$', '$options': 'i'}
    })
    return count
