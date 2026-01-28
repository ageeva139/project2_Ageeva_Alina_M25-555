import shlex

from .constants import FILE_PATH
from .core import create_table, delete, drop_table, insert, list_tables, select, update
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def show_help():
    """Показываем справочную информацию"""

    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert <имя_таблицы> <значение1> <значение2> .. - добавить запись")
    print("<command> select <имя_таблицы> [столбец=значение] .. - выбрать записи")
    print("<command> delete <имя_таблицы> столбец=значение .. - удалить записи")
    print("<command> update <имя_таблицы> set столбец=значение ..")
    print("                 where столбец=значение .. - обновить записи")


    print("\nУсловия для команд select, delete, update:")
    print("  - формат: столбец=значение (без пробелов вокруг '=')")
    print("  - несколько условий разделяйте пробелом")
    print('  - если значение строковое, используйте кавычки: name="Иван Иванов"')

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def parse_conditions(schema, items):
    #разбираем список условий и превращаем в словари
    result = {}
    for item in items:
        if item.lower() == "and":
            continue

        if "=" not in item:
            print("Ошибка: условие должно быть в формате столбец=значение")
            return

        key, raw_value = item.split("=", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if key not in schema:
            print(f"Ошибка: столбца '{key}' нет в схеме таблицы")
            return

        column_type = schema[key]

        if column_type == "int":
            try:
                result[key] = int(raw_value)
            except ValueError:
                print(
                    f"Ошибка: значение '{raw_value}' не подходит "
                    f"для типа int (столбец {key})"
                )
                return

        elif column_type == "bool":
            if raw_value.lower() in ("true", "1", "yes"):
                result[key] = True
            elif raw_value.lower() in ("false", "0", "no"):
                result[key] = False
            else:
                print(
                    f"Ошибка: значение '{raw_value}' не подходит "
                    f"для типа bool (столбец {key})"
                )
                return

        elif column_type == "str":
            if raw_value == "":
                print("Ошибка: строковое значение не должно быть пустым")
                return
            result[key] = raw_value

        else:
            print(f"Ошибка: неизвестный тип {column_type} для столбца {key}")
            return

    return result

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
                where_clause = parse_conditions(schema, args[2:])
                if where_clause is None:
                    continue

            result = select(table_data, where_clause)

            if result == []:
                print("Подходящих записей не найдено")
            else:
                for row in result:
                    print(row)

        elif command == "delete": #удалить записи из таблицы
            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}

            if len(args) < 3:
                print("Ошибка: укажите имя таблицы и условия удаления")
                show_help()
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f"Таблицы {table_name} не существует")
                continue

            schema = metadata[table_name]
            table_data = load_table_data(table_name)

            where_clause = parse_conditions(schema, args[2:])
            if where_clause is None:
                continue

            new_data = delete(table_data, where_clause)
            deleted_count = len(table_data) - len(new_data)

            save_table_data(table_name, new_data)
            print(f"Удалено записей: {deleted_count}")

        elif command == "update": #обновить записи в таблице
            metadata = load_metadata(FILE_PATH)
            if metadata is None:
                metadata = {}

            if len(args) < 6:
                print("Ошибка: недостаточно аргументов")
                show_help()
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f"Таблицы {table_name} не существует")
                continue

            schema = metadata[table_name]
            table_data = load_table_data(table_name)

            args_lower = [x.lower() for x in args]
            if "set" not in args_lower or "where" not in args_lower:
                print("Ошибка: используйте формат update <таблица> set ... where ...")
                show_help()
                continue

            set_index = args_lower.index("set")
            where_index = args_lower.index("where")

            if set_index >= where_index:
                print("Ошибка: сначала должен быть set, затем where")
                show_help()
                continue

            set_items = args[set_index + 1:where_index]
            where_items = args[where_index + 1:]

            if set_items == [] or where_items == []:
                print("Ошибка: set и where не должны быть пустыми")
                show_help()
                continue

            set_clause = parse_conditions(schema, set_items)
            if set_clause is None:
                continue

            if "ID" in set_clause:
                print("Ошибка: нельзя изменять столбец ID")
                continue

            where_clause = parse_conditions(schema, where_items)
            if where_clause is None:
                continue

            matched = len(select(table_data, where_clause))
            new_data = update(table_data, set_clause, where_clause)

            save_table_data(table_name, new_data)
            print(f"Обновлено записей: {matched}")

        elif command: #неизвестная команда
            print(f"Неизвестная команда: {command}")
            show_help()

        else: #нет команды
            print("Введите команду")
