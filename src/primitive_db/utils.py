import json
import os

from .constants import DATA_DIR


def load_metadata(filepath):
    #загружаем данные из json-файла
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return {}

def save_metadata(filepath, data):
    #сохраняем переданные данные в json-файл
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except FileNotFoundError:
        print(f"Данная директория {filepath} не найдена")

def load_table_data(table_name):
    #загружаем данные таблицы из json-файла
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return []

def save_table_data(table_name, data):
    #сохраняем данные таблицы в json-файл
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except FileNotFoundError:
        print(f"Данная директория {filepath} не найдена")