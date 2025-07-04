'''
Module for connecting to a MySQL database and executing queries on the film_extended_view.
Contains functions to search films by various criteria and obtain statistics.
'''

def search_by_keyword(conn, keyword, offset=0, limit=10):
    '''
    Search films by keyword in the title.
    keyword: Keyword for searching (used with LIKE %keyword%).
    offset: Offset for pagination.
    limit: Number of records to return.
    return: List of films matching the query.
    '''

    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE UPPER(title) LIKE UPPER(%s) '
            'LIMIT %s OFFSET %s;'
        )
        cursor.execute(query, (f'%{keyword}%', limit, offset))
        return cursor.fetchall()


def get_genres_and_year_range(conn):
    '''
    Retrieves the list of unique genres and the range of release years.
    return: List of genres, minimum year, maximum year.
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


def search_by_genre_and_years(conn, genre, year_from, year_to,*, offset=0, limit=10):
    '''
    Search films by genre and release year range.
    genre: Film genre.
    year_from: Starting year.
    year_to: Ending year.
    offset: Offset for pagination.
    limit: Number of records to return.
    return: List of films matching the filter.
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


def search_by_actor_name_partial(conn, name_part, offset=0, limit=10):
    '''
    Search films by partial actor's first or last name.
    name_part: Fragment of the actor's first or last name.
    offset: Offset for pagination.
    limit: Number of records to return.
    return: List of films where actor matches the name fragment.
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


def get_length_range(conn):
    '''
    Get the minimum and maximum film length in the database.
    return: Minimum length, maximum length in minutes.
    '''

    with conn.cursor() as cursor:
        query = (
            'SELECT MIN(length) AS min_length, MAX(length) AS max_length '
            'FROM film_extended_view;'
        )
        cursor.execute(query)
        result = cursor.fetchone()
    return result['min_length'], result['max_length']


def search_by_length_range(conn, length_from: int, length_to: int, offset=0, limit=10):
    '''
    Search films by length range.
    length_from: Minimum film length (in minutes).
    length_to: Maximum film length (in minutes).
    offset: Offset for pagination.
    limit: Number of records to return.
    return: List of films matching the filter.
    '''

    with conn.cursor() as cursor:
        query = (
            'SELECT * FROM film_extended_view '
            'WHERE length BETWEEN %s AND %s '
            'LIMIT %s OFFSET %s;'
        )
        cursor.execute(query, (length_from, length_to, limit, offset))
        return cursor.fetchall()
