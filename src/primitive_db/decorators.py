import time
from functools import wraps


def handle_db_errors(func):
    #декоратор для перехвата ошибок
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except FileNotFoundError:
            print("Ошибка: файл данных не найден.",
                  "Возможно, база данных не инициализирована.")
            return

        except KeyError as e:
            print(f"Ошибка: таблица или столбец {e} не найден.")
            return

        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return

        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return

    return wrapper

def confirm_action(action_name):
    #декоратор для удаления
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()
            if answer != "y":
                print("Операция отменена")
                return
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def log_time(func):
    #декоратор для учета времени выполнения функции
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция выполнилась за {end - start:.8f} секунд")
        return result

    return wrapper