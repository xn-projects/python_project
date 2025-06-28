'''
Модуль formatter содержит функции для форматирования логов MongoDB
в табличный текстовый формат.
'''

import collections
from typing import List, Dict, Any
from datetime import datetime

import tabulate


def format_mongo_logs(logs: List[Dict[str, Any]]) -> str:
    '''
    Форматирует список логов из MongoDB в виде табличной строки.
    logs: Список логов, в виде словарей с полями 'query' и 'timestamp'.
    return: Строка, содержащая отформатированную таблицу.
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

    headers = ['Тип запроса', 'Детали запроса', 'Время']
    return tabulate.tabulate(
        table,
        headers=headers,
        tablefmt='fancy_grid',
        stralign='left'
    )


def format_actor_full_log(actor_logs: List[Dict[str, Any]]) -> str:
    '''
    Форматирует историю запросов актёров с учётом частоты поиска и деталей.
    actor_logs: Список логов запросов, в виде словарей с полем 'query' и 'timestamp'.
    return: Строка, содержащая отформатированную таблицу.
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

    headers = ['Актёр (поиск)', 'Частота', 'Тип запроса', 'Детали запроса', 'Время']
    return tabulate.tabulate(
        table,
        headers=headers,
        tablefmt='fancy_grid',
        stralign='left'
    )
