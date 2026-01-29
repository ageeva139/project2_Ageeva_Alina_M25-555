from .decorators import confirm_action, handle_db_errors, log_time
from .utils import load_table_data


@handle_db_errors #декоратор
def create_table(metadata, table_name, columns):
    #слздаем новую таблицу
    if table_name in metadata:
        raise ValueError(f"Таблица с именем '{table_name}' уже существует")
    
    valid_types = {"int", "str", "bool"}

    columns = ["ID:int"] + columns

    columns_dict = {}

    for i, column in enumerate(columns):
        column = column.split(":")
        if column[1] not in valid_types:
            raise ValueError(
                f"Некорректный тип {column[1]} для столбца {column[0]}. "
                f"Допустимые типы: {', '.join(valid_types)}"
            )
        
        columns_dict[column[0]] = column[1]
    
    metadata[table_name] = columns_dict
    
    return metadata

@confirm_action("удаление таблицы")
@handle_db_errors #декоратор
def drop_table(metadata, table_name):
    #удаляем существующую таблицу
    if table_name not in metadata:
        raise KeyError(table_name)

    metadata.pop(table_name)

    return metadata


def list_tables(metadata):
    #список таблиц
    if metadata == {}:
        return None
    return list(metadata.keys())

@log_time #измерение времени
@handle_db_errors #декоратор
def insert(metadata, table_name, values):
    #добавление новой строки в таблицу
    if table_name not in metadata:
        raise KeyError(table_name)

    schema = metadata[table_name]

    #берем колонки в порядке создания, ID пропускаем
    columns = list(schema.keys())
    if "ID" in columns:
        columns.remove("ID")

    if len(values) != len(columns):
        raise ValueError("Количество значений не соответствует количеству столбцов")

    data = load_table_data(table_name)

    #генерируем новый ID
    max_id = 0
    for row in data:
        try:
            max_id = max(max_id, int(row.get("ID", 0)))
        except (TypeError, ValueError):
            continue
    new_id = max_id + 1

    new_row = {"ID": new_id}

    #заполняем столбцы
    for i, column_name in enumerate(columns):
        column_type = schema[column_name]
        raw_value = values[i]

        if column_type == "int":
            try:
                new_row[column_name] = int(raw_value)
            except ValueError:
                raise ValueError(
                    f"Значение '{raw_value}' не подходит "
                    f"для типа int (столбец {column_name})"
                )

        elif column_type == "bool":
            value_lower = str(raw_value).strip().lower()
            if value_lower in ("true", "1", "yes"):
                new_row[column_name] = True
            elif value_lower in ("false", "0", "no"):
                new_row[column_name] = False
            else:
                raise ValueError(
                    f"Значение '{raw_value}' не подходит "
                    f"для типа bool (столбец {column_name})"
                )

        elif column_type == "str":
            new_row[column_name] = str(raw_value)

        else:
            raise ValueError(
                f"Неизвестный тип {column_type} для столбца {column_name}"
            )

    data.append(new_row)

    return data

def select(table_data, where_clause=None):
    #выбираем записи из таблицы

    #если нет условия - возвращаем всю таблицу
    if where_clause is None:
        return table_data
    result = []
    for row in table_data:
        is_match = True

        #проверяем все условия
        for key, value in where_clause.items():
            if key not in row:
                is_match = False
                break
            if row[key] != value:
                is_match = False
                break

        if is_match:
            result.append(row)

    return result

def update(table_data, set_clause, where_clause):
    #обновляем записи в таблице

    #если нет условий - ничего не обновляем
    if where_clause is None or where_clause == {}:
        return table_data

    for row in table_data:
        is_match = True

        #ищем подходящие записи
        for key, value in where_clause.items():
            if key not in row:
                is_match = False
                break
            if row[key] != value:
                is_match = False
                break

        #обновляем поля
        if is_match:
            for key, value in set_clause.items():
                row[key] = value

    return table_data

@confirm_action("удаление записей")
def delete(table_data, where_clause):
    #удаляем записи из таблицы

    #если нет условий - ничего не удаляем
    if where_clause is None or where_clause == {}:
        return table_data

    new_data = []

    for row in table_data:
        is_match = True

        #ищем подходящие записи
        for key, value in where_clause.items():
            if key not in row:
                is_match = False
                break
            if row[key] != value:
                is_match = False
                break

        #если не совпало - оставляем запись
        if not is_match:
            new_data.append(row)

    return new_data
