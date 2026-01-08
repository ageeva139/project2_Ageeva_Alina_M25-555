import json


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