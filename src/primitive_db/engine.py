from .constants import FILE_PATH
from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def show_help():
    """Показываем справочную информацию"""
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. "
        "- создать таблицу"
        )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def welcome():
    """Основная функция запуска программы"""
    print("Первая попытка запустить проект!")
    print("***")
    show_help()
    
    while True:
        command_info = input("Введите команду: ").strip().lower().split()
        command = command_info[0]
        
        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            show_help()
        elif command == "create_table":
            metadata = load_metadata(FILE_PATH) 
            new_metadata = create_table(metadata, command_info[1], command_info[2:])
            save_metadata(FILE_PATH, new_metadata)
        elif command == "list_tables":
            metadata = load_metadata(FILE_PATH)
            tables = list_tables(metadata)
            if tables is None:
                print("Пока нет существующих таблиц... Создайте новую таблицу")
            print(", ".join(tables))
        elif command == "drop_table":
            metadata = load_metadata(FILE_PATH) 
            new_metadata = drop_table(metadata, command_info[1])
            save_metadata(FILE_PATH, new_metadata)
        elif command:
            print(f"Неизвестная команда: {command}")
        else:
            print("Введите команду")
