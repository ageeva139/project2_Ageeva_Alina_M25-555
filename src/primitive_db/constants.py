import os

#абсолютный путь к директории, где находится constants.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#файл для хранения метаданных базы данных
FILE_PATH = os.path.join(BASE_DIR, "db_meta.json")

#директория для хранения данных таблиц
DATA_DIR = os.path.join(BASE_DIR, "data")