# Примитивная база данных
Простая база данных на Python. Реализует основные операции по управлению таблицами с сохранением метаданных в JSON-файл.

# Установка и запуск

## Требования
- Python 3.12 или выше
- Poetry (менеджер зависимостей)

## Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/ageeva139/project2_Ageeva_Alina_M25-555.git
cd project2_Ageeva_Alina_M25-555

# Установите зависимости
make install
# или
poetry install
```

## Запуск
```bash
make project
# или
poetry run project
```

# Доступные команды:

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... - создать таблицу

list_tables - показать список всех таблиц

drop_table <имя_таблицы> - удалить таблицу

exit - выйти из программы

help - справочная информация

# Пример использования команд
Введите команду: create_table students name:str age:int grade:str
Таблица 'students' успешно создана

Введите команду: create_table teachers full_name:str subject:str experience:int
Таблица 'teachers' успешно создана

Введите команду: list_tables
Существующие таблицы:
  - students
  - teachers

Введите команду: drop_table teachers
Таблица 'teachers' успешно удалена

Введите команду: list_tables
Существующие таблицы:
  - students

Введите команду: exit
Выход из программы...

# Демонстрация
https://asciinema.org/a/E1lA3rY5CQVbbilz
