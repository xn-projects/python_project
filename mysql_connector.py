'''
Модуль для подключения к базе данных MySQL и выполнения запросов к представлению film_extended_view.
Содержит функции для поиска фильмов по разным критериям и получения статистики.
'''

import pymysql
import tabulate

import settings
import ui

conn = pymysql.connect(**settings.DATABASE_MYSQL_W)

if conn.open:
    print('Подключение к MySQL успешно.')


def search_by_keyword(keyword, offset=0, limit=10):
    '''
    Поиск фильмов по ключевому слову в названии.
    keyword: Ключевое слово для поиска (будет применяться с LIKE %keyword%).
    offset: Смещение для постраничного отображения данных.
    limit: Количество возвращаемых записей.
    return: Список фильмов, соответствующих запросу.
    '''
    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE UPPER(title) LIKE UPPER(%s) '
            'LIMIT %s OFFSET %s;'
        )
        cursor.execute(query, (f'%{keyword}%', limit, offset))
        return cursor.fetchall()


def get_genres_and_year_range():
    '''
    Получает список уникальных жанров и диапазон лет выпуска фильмов.
    return: Cписок жанров, минимальный год, максимальный год.
    '''
    with conn.cursor() as cursor:
        cursor.execute('SELECT DISTINCT category FROM film_extended_view;')
        genres = [row['category'] for row in cursor.fetchall()]

        cursor.execute(
            'SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year '
            'FROM film_extended_view;'
        )
        result = cursor.fetchone()
        min_year, max_year = result['min_year'], result['max_year']

    return genres, min_year, max_year


def search_by_genre_and_years(genre, year_from, year_to, offset=0, limit=10):
    '''
    Поиск фильмов по жанру и диапазону годов выпуска.
    genre: Жанр фильма.
    year_from: Начальный год.
    year_to: Конечный год.
    offset: Смещение для постраничного отображения данных.
    limit: Количество возвращаемых записей.
    return: Список фильмов, соответствующих фильтру.
    '''
    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE LOWER(category) = LOWER(%s) '
            'AND release_year BETWEEN %s AND %s '
            'LIMIT %s OFFSET %s;'
        )
        cursor.execute(query, (genre, year_from, year_to, limit, offset))
        return cursor.fetchall()


def search_by_actor_name(first_name, last_name, offset=0, limit=10):
    '''
    Поиск фильмов по полному имени актёра.
    first_name: Имя актёра.
    last_name: Фамилия актёра.
    offset: Смещение для постраничного отображения данных.
    limit: Количество возвращаемых записей.
    return: Список фильмов, в которых участвует указанный актёр.
    '''
    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE UPPER(actors) LIKE UPPER(%s) '
            'LIMIT %s OFFSET %s;'
        )
        full_name = f'%{first_name} {last_name}%'
        cursor.execute(query, (full_name, limit, offset))
        return cursor.fetchall()


def search_by_actor_name_partial(name_part, offset=0, limit=10):
    '''
    Поиск фильмов по части имени или фамилии актёра.
    name_part: Фрагмент имени или фамилии актёра.
    offset: Смещение для постраничного отображения данных.
    limit: Количество возвращаемых записей.
    return: Список фильмов, где актёр соответствует части имени.
    '''
    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE UPPER(actors) LIKE UPPER(%s) '
            'LIMIT %s OFFSET %s;'
        )
        pattern = f'%{name_part}%'
        cursor.execute(query, (pattern, limit, offset))
        return cursor.fetchall()


def get_length_range():
    '''
    Получение минимальной и максимальной длительности фильмов в базе.
    return: Минимальная длина, максимальная длина в минутах.
    '''
    with conn.cursor() as cursor:
        query = (
            'SELECT MIN(length) AS min_length, MAX(length) AS max_length '
            'FROM film_extended_view;'
        )
        cursor.execute(query)
        result = cursor.fetchone()
    return result['min_length'], result['max_length']


def search_by_length_range(length_from: int, length_to: int, offset=0, limit=10):
    '''
    Поиск фильмов по диапазону длительности.
    length_from: Минимальная длительность фильма (в минутах).
    length_to: Максимальная длительность фильма (в минутах).
    offset: Смещение для постраничного отображения данных.
    limit: Количество возвращаемых записей.
    return: Список фильмов, соответствующих фильтру.
    '''
    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE length BETWEEN %s AND %s '
            'LIMIT %s OFFSET %s;'
        )
        cursor.execute(query, (length_from, length_to, limit, offset))
        return cursor.fetchall()
