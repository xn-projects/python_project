'''
Модуль log_writer содержит функции для записи и форматирования логов запросов
в MongoDB и вывода их в табличном виде.
'''

from datetime import datetime
from tabulate import tabulate
import settings


def log_query(query_type: str, query_params: dict) -> None:
    '''
    Записывает лог запроса в MongoDB с указанием типа запроса, параметров и временной метки.
    query_type: Тип запроса (например, 'actor_partial', 'category' и т.д.).
    query_params: Словарь с параметрами запроса.
    '''
    db = settings.MONGO_CLIENT['ich_edit']
    collection = db['final_project_100125_Kseniia']

    collection.insert_one({
        'query': {
            'type': query_type,
            'params': query_params
        },
        'timestamp': datetime.utcnow()
    })


def format_mongo_logs(logs: list[dict]) -> str:
    '''
    Форматирует список логов из MongoDB в табличное представление.
    logs: Список документов из MongoDB с логами запросов.
    return: Строка с форматированной таблицей логов.
    '''
    table = []
    for entry in logs:
        query_info = entry.get('query', {})
        details = query_info.copy()
        query_type = details.pop('type', '—')
        timestamp = entry.get('timestamp')
        time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else '—'
        table.append([query_type, details, time_str])

    headers = ['Тип запроса', 'Детали запроса', 'Время']
    return tabulate(table, headers=headers, tablefmt='fancy_grid', stralign='left')


def format_actor_frequency(freq_list: list[tuple[str, int]]) -> str:
    '''
    Форматирует статистику по частоте поисковых запросов актёров в таблицу.
    freq_list: Список кортежей (актёр, количество запросов).
    return: Строка с форматированной таблицей частоты запросов.
    '''
    table = [[actor, count] for actor, count in freq_list]
    headers = ['Актёр (часть имени)', 'Количество запросов']
    return tabulate(table, headers=headers, tablefmt='fancy_grid', stralign='left')
