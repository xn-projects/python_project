'''
Модуль ui содержит функции для взаимодействия с пользователем:
вывод меню, запрос данных и отображение результатов в консоли.
'''

import tabulate


def main_menu():
    '''Выводит главное меню и возвращает выбор пользователя.'''
    prompt = (
        '\n=== Главное меню ===\n'
        '1. Поиск фильмов\n'
        '2. Статистика запросов\n'
        '0. Выход\n\n'
        'Введите номер пункта меню (0–2): '
    )

    while True:
        choice = input(prompt).strip()
        if choice in ('0', '1', '2'):
            return choice
        print('Некорректный выбор. Попробуйте снова.')


def confirm_exit():
    '''Запрашивает у пользователя подтверждение выхода из программы.'''
    print('\nВы действительно хотите выйти?')
    print('0. Да, выйти')
    print('1. Нет, вернуться в главное меню')
    return input('Ваш выбор: ').strip()


def show_search_menu():
    '''Выводит меню поиска фильмов и возвращает выбор пользователя.'''
    print('\n=== Поиск фильмов ===')
    print('1. По ключевому слову')
    print('2. По жанру и диапазону годов')
    print('3. По актёру (имя и фамилия)')
    print('4. Поиск по длине фильма')
    return input('Выберите метод поиска: ').strip()


def show_pagination_menu():
    '''Выводит меню постраничного показа и возвращает выбор пользователя.'''
    print('\nПоказать следующие 10 фильмов?')
    print('1. Да')
    print('2. Нет, вернуться в меню')
    return input('Ваш выбор: ').strip()


def show_stat_menu():
    '''Выводит меню статистики и возвращает выбор пользователя.'''
    print('\n=== Статистика ===')
    print('1. Топ-5 популярных запросов')
    print('2. Последние 5 запросов')
    print('3. Поиск запросов по типу')
    print('4. Частота запросов по актёрам')
    return input('Выберите опцию: ').strip()


def prompt_keyword():
    '''Запрашивает у пользователя ключевое слово для поиска по названиям фильмов.'''
    return input('\nВведите ключевое слово для поиска в названиях фильмов: ').strip()


def prompt_actor_name():
    '''Запрашивает у пользователя имя и фамилию актёра для поиска.'''
    print('\nВведите данные актёра для поиска (можно оставить пустым):')
    first = input('Имя актёра: ').strip()
    last = input('Фамилия актёра: ').strip()
    return first, last


def prompt_genre_and_years(genres, min_year, max_year):
    '''Запрашивает у пользователя жанр и диапазон годов для поиска фильмов.'''
    print('\nЖанры в базе данных:')
    for genre in genres:
        print(f'- {genre}')
    print(f'Доступные года: от {min_year} до {max_year}')

    while True:
        genre = input('Введите жанр: ').strip()
        if genre not in genres:
            print('Некорректный жанр. Попробуйте снова.')
            continue
        break

    while True:
        try:
            year_from = int(input(f'Введите начальный год (от {min_year}): ').strip())
            year_to = input(f'Введите конечный год (до {max_year}, или оставьте пустым для одного года): ').strip()
            year_to = int(year_to) if year_to else year_from

            if (
                min_year <= year_from <= max_year
                and min_year <= year_to <= max_year
                and year_from <= year_to
            ):
                return genre, year_from, year_to
        except ValueError:
            pass
        print('Ошибка ввода. Попробуйте снова.')


def length_prompt():
    '''Запрашивает у пользователя минимальную и максимальную длину фильма.'''
    while True:
        try:
            min_length = int(input('Введите минимальную длину фильма (в минутах): ').strip())
            max_length = input('Введите максимальную длину фильма (в минутах, или оставьте пустым): ').strip()
            max_length = int(max_length) if max_length else min_length
            if 0 < min_length <= max_length:
                return min_length, max_length
        except ValueError:
            pass
        print('Некорректный ввод. Попробуйте снова.')


def display_results(results, start_index=1):
    '''
    Отображает результаты поиска в виде таблицы.
    results: Список словарей с информацией о фильмах.
    start_index: Номер, с которого начать нумерацию результатов.
    '''
    if not results:
        print('Результаты не найдены.')
        return

    table = []
    for i, row in enumerate(results, start=start_index):
        table.append(
            [
                i,
                row.get('title', ''),
                row.get('release_year', ''),
                row.get('category', ''),
                row.get('rating', ''),
                row.get('length', ''),
                row.get('actors', ''),
            ]
        )

    headers = ['№', 'Название', 'Год', 'Жанр', 'Рейтинг', 'Длительность', 'Актёры']
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))
