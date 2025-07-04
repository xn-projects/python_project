'''
Module errors provides decorators and functions to log and display errors
consistently during program execution.
'''

from functools import wraps
from datetime import datetime
from display_utils import colorize

def log_error_to_file(message: str, filename: str = 'error.log') -> None:
    '''
    Logs an error message to a specified log file with a timestamp.
    Args:
        message (str): The error message to log.
        filename (str): The log file path. Defaults to 'error.log'.
    Returns:
        None
    '''

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')


def show_error(message: str) -> None:
    '''
    Prints an error message to the console, colorized in red.
    Args:
        message (str): The error message to display.
    Returns:
        None
    '''

    print(colorize(message, 'red'))


def log_error(display: bool = True):
    '''
    Decorator that wraps a function to log exceptions to a file and optionally
    display them in the console.
    Args:
        display (bool): If True, error messages are printed to the console.
                        Defaults to True.
    Returns:
        Callable: The wrapped function with error logging.
    '''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_error_to_file(str(e))
                if display:
                    show_error(f'Error: {e}')
                return None
        return wrapper
    return decorator
