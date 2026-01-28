import shlex

from .constants import FILE_PATH
from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def show_help():
    """Показываем справочную информацию"""

    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run():
    """Основная функция запуска программы"""
    show_help()
    
    while True:
        user_input = input("Введите команду: ").strip()
        args = shlex.split(user_input)
        command = args[0].lower()

        if command == "exit": #выход
            print("Выход из программы...")
            break
        elif command == "help": #список доступных команд
            show_help()
        elif command == "create_table": #создать таблицу
            metadata = load_metadata(FILE_PATH)
            if len(args) < 3:
                    print("Ошибка: недостаточно аргументов")
                    show_help()
                    continue
            table_name = args[1]
            columns = args[2:] 
            new_metadata = create_table(metadata, table_name, columns)
            save_metadata(FILE_PATH, new_metadata)
            print(f"Таблица '{table_name}' успешно создана")
        elif command == "list_tables": #список таблиц
            metadata = load_metadata(FILE_PATH)
            tables = list_tables(metadata)
            if tables is None:
                print("Пока нет существующих таблиц... Создайте новую таблицу")
            print(", ".join(tables))
        elif command == "drop_table": #удалить таблицу
            metadata = load_metadata(FILE_PATH)
            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)
            save_metadata(FILE_PATH, new_metadata)
        elif command: #неизвестная команда
            print(f"Неизвестная команда: {command}")
            show_help()
        else: #нет команды
            print("Введите команду")
