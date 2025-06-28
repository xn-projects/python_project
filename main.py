'''
Главный модуль консольного приложения для поиска фильмов по базе данных Sakila.
Позволяет:
1. Выполнять различные типы поиска фильмов.
2. Просматривать статистику поисковых запросов.
3. Вести логирование запросов.
'''

import ui
import mysql_connector
import log_writer
import log_stats


def handle_pagination(results: list, start_index: int) -> bool:
    '''Отображает результаты и меню постраничного отображения данных.'''
    if results:
        ui.display_results(results, start_index=start_index)
        return ui.show_pagination_menu() == '1'
    print('Больше результатов нет.')
    return False


def handle_keyword_search() -> None:
    '''Обработка поиска по ключевому слову.'''
    keyword = ui.prompt_keyword()
    offset = 0
    while True:
        results = mysql_connector.search_by_keyword(keyword, offset)
        log_writer.log_query('keyword', {'keyword': keyword})
        if handle_pagination(results, offset):
            offset += 10
        else:
            break


def handle_genre_year_search() -> None:
    '''Обработка поиска по жанру и диапазону годов.'''
    genres, min_year, max_year = mysql_connector.get_genres_and_year_range()
    genre, year_from, year_to = ui.prompt_genre_and_years(genres, min_year, max_year)
    offset = 0
    while True:
        results = mysql_connector.search_by_genre_and_years(genre, year_from, year_to, offset)
        log_writer.log_query('genre_year', {
            'genre': genre,
            'year_from': year_from,
            'year_to': year_to
        })
        if handle_pagination(results, offset):
            offset += 10
        else:
            break


def handle_actor_search() -> None:
    '''Обработка поиска по имени актёра.'''
    first_name, last_name = ui.prompt_actor_name()
    offset = 0
    while True:
        results = mysql_connector.search_by_actor_name(first_name, last_name, offset)
        log_writer.log_query('actor_name', {
            'first_name': first_name,
            'last_name': last_name
        })
        if handle_pagination(results, offset):
            offset += 10
        else:
            break


def handle_length_search() -> None:
    '''Обработка поиска по длительности фильма.'''
    min_len_db, max_len_db = mysql_connector.get_length_range()
    print(f'\nДоступный диапазон длины фильмов: от {min_len_db} до {max_len_db} минут.')
    min_length, max_length = ui.length_prompt()

    if min_length < min_len_db or max_length > max_len_db:
        print('Ошибка: введённый диапазон вне допустимых значений.')
        return

    offset = 0
    while True:
        results = mysql_connector.search_by_length_range(min_length, max_length, offset)
        log_writer.log_query('length_range', {
            'min_length': min_length,
            'max_length': max_length
        })
        if handle_pagination(results, offset):
            offset += 10
        else:
            break


def handle_search_menu() -> None:
    '''Обработка выбора пользователем типа поиска.'''
    search_choice = ui.show_search_menu()
    if search_choice == '1':
        handle_keyword_search()
    elif search_choice == '2':
        handle_genre_year_search()
    elif search_choice == '3':
        handle_actor_search()
    elif search_choice == '4':
        handle_length_search()
    else:
        print('Некорректный выбор метода поиска.')


def handle_actor_frequency_stat() -> None:
    '''
    Запрашивает имя актёра у пользователя и выводит статистику частоты запросов.
    '''
    actor_name = input('Введите имя актёра для статистики запросов: ').strip()
    if not actor_name:
        print('Имя актёра не может быть пустым.')
        return

    count = log_stats.get_actor_query_frequency(actor_name)
    print(f'Количество запросов для актёра "{actor_name}": {count}')


def handle_stat_menu() -> None:
    '''Обработка меню статистики запросов.'''
    stat_choice = ui.show_stat_menu()
    if stat_choice == '1':
        top = log_stats.get_top_queries()
        print('\nТоп-5 популярных запросов:')
        for query, count in top:
            print(f"{query}: {count}")
    elif stat_choice == '2':
        last = log_stats.get_last_queries()
        print('\nПоследние 5 запросов:')
        for query in last:
            print(query)
    elif stat_choice == '3':
        type_name = input('Введите тип запроса (keyword, genre_year, actor_name, length_range, rating): ').strip()
        filtered = log_stats.get_queries_by_type(type_name)
        print(f'\nЗапросы типа "{type_name}":')
        for query in filtered:
            print(query)
    elif stat_choice == '4':
        handle_actor_frequency_stat()
    else:
        print('Некорректный выбор.')


def main() -> None:
    '''Основная функция запуска программы.'''
    print('Добро пожаловать в систему поиска фильмов по базе данных Sakila.')

    while True:
        choice = ui.main_menu()
        if choice == '1':
            handle_search_menu()
        elif choice == '2':
            handle_stat_menu()
        elif choice == '0':
            if ui.confirm_exit():
                print('До свидания!')
                break


if __name__ == '__main__':
    main()
