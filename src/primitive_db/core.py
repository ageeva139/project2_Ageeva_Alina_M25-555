def create_table(metadata, table_name, columns):
    #слздаем новую таблицу
    if table_name in metadata:
        print(f"Таблица с именем '{table_name}' уже существует")
        return
    
    valid_types = {"int", "str", "bool"}

    columns = ["ID:int"] + columns

    columns_dict = {}

    for i, column in enumerate(columns):
        column = column.split(":")
        if column[1] not in valid_types:
            print(f"Некорректный тип {column[1]} для столбца {column[0]}\n")
            print(f"Допустимые типы: {', '.join(valid_types)}")
            return
        
        columns_dict[column[0]] = column[1]
    
    metadata[table_name] = columns_dict
    
    return metadata


def drop_table(metadata, table_name):
    #удаляем существующую таблицу
    if table_name not in metadata:
        print(f"Таблицы {table_name} не существует")
        return

    metadata.pop(table_name)

    return metadata


def list_tables(metadata):
    if metadata == {}:
        return None
    return list(metadata.keys())