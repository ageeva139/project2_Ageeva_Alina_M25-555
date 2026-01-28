import shlex

from .constants import FILE_PATH
from .core import create_table, drop_table, insert, list_tables, select
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def show_help():
    """Показываем справочную информацию"""

    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert <имя_таблицы> <значение1> <значение2> .. - добавить запись")
    print("<command> select <имя_таблицы> [столбец=значение] .. - выбрать записи")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run():
    """Основная функция запуска программы"""
    show_help()
    
    while True:
        user_input = input("Введите команду: ").strip()
        if not user_input:
            print("Введите команду")
            continue

        args = shlex.split(user_input)
        command = args[0].lower()

        if command == "exit": #выход
            print("Выход из программы...")
            break

        elif command == "help": #список доступных команд
            show_help()
    
        elif command == "create_table": #создать таблицу
            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}
            if len(args) < 3:
                    print("Ошибка: недостаточно аргументов")
                    show_help()
                    continue
            table_name = args[1]
            columns = args[2:] 
            new_metadata = create_table(metadata, table_name, columns)
            if new_metadata is not None:
                save_metadata(FILE_PATH, new_metadata)
                print(f"Таблица '{table_name}' успешно создана")

        elif command == "list_tables": #список таблиц
            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}
            tables = list_tables(metadata)
            if tables is None:
                print("Пока нет существующих таблиц... Создайте новую таблицу")
            else:
                print(", ".join(tables))
    
        elif command == "drop_table": #удалить таблицу

            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы")
                continue
            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)
            save_metadata(FILE_PATH, new_metadata)
            print(f"Таблица '{table_name}' успешно удалена")

        elif command == "insert": #добавить запись в таблицу
            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}
            if len(args) < 3:
                print("Ошибка: недостаточно аргументов")
                show_help()
                continue
            table_name = args[1]
            values = args[2:]
            new_data = insert(metadata, table_name, values)
            if new_data is not None:
                save_table_data(table_name, new_data)
                print(f"Запись успешно добавлена в таблицу '{table_name}'")
        
        elif command == "select": #выбрать записи из таблицы
            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}

            if len(args) < 2:
                print("Ошибка: укажите имя таблицы")
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f"Таблицы {table_name} не существует")
                continue

            schema = metadata[table_name]
            table_data = load_table_data(table_name)

            where_clause = None
            if len(args) >= 3:
                where_clause = {}
                has_error = False

                #проверка одного и более условия
                for item in args[2:]:
                    if "=" not in item:
                        print("Ошибка: условие должно быть в формате столбец=значение")
                        has_error = True
                        break

                    key, raw_value = item.split("=", 1)
                    key = key.strip()
                    raw_value = raw_value.strip()

                    if key not in schema:
                        print(f"Ошибка: столбца '{key}' нет в таблице '{table_name}'")
                        has_error = True
                        break

                    column_type = schema[key]

                    if column_type == "int":
                        try:
                            where_clause[key] = int(raw_value)
                        except ValueError:
                            print(f"Ошибка: значение '{raw_value}' не подходит",
                                   "для типа int (столбец {key})")
                            has_error = True
                            break

                    elif column_type == "bool":
                        value_lower = raw_value.lower()
                        if value_lower in ("true", "1", "yes"):
                            where_clause[key] = True
                        elif value_lower in ("false", "0", "no"):
                            where_clause[key] = False
                        else:
                            print(f"Ошибка: значение '{raw_value}' не подходит", 
                                  "для типа bool (столбец {key})")
                            has_error = True
                            break

                    elif column_type == "str":
                        where_clause[key] = raw_value

                    else:
                        print(f"Ошибка: неизвестный тип {column_type}",
                               "для столбца {key}")
                        has_error = True
                        break

                if has_error:
                    continue

            result = select(table_data, where_clause)

            if result == []:
                print("Подходящих записей не найдено")
            else:
                for row in result:
                    print(row)

        elif command: #неизвестная команда
            print(f"Неизвестная команда: {command}")
            show_help()

        else: #нет команды
            print("Введите команду")
