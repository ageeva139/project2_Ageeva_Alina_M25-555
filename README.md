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

insert <имя_таблицы> <значение1> <значение2> ... - добавить запись

select <имя_таблицы> [столбец=значение] ... - выбрать записи (условия через пробел)

update <имя_таблицы> set столбец=значение ... where столбец=значение ... - обновить записи

delete <имя_таблицы> столбец=значение ... - удалить записи

exit - выйти из программы

help - справочная информация

# CRUD-операции
1. insert
Добавляет новую запись в таблицу. ID генерируется автоматически

Пример:
insert students "Иван Иванов" 20 "A"

2. select
Выводит записи таблицы. Можно указать условия (через пробел) в формате столбец=значение.

Примеры:
select students
select students age=20
select students grade="A"
select students age=20 grade="A"

3. update
Обновляет записи, найденные по where. Новые значения задаются после set.
Формат:
update <таблица> set <присваивания> where <условия>

Пример:
update students set grade="B" where name="Иван Иванов"

4. delete
Удаляет записи, подходящие под условия.

Пример:
delete students age=20
delete students name="Иван Иванов" grade="A"

# Пример использования команд
Введите команду: create_table students name:str age:int grade:str
Таблица 'students' успешно создана

Введите команду: insert students "Иван Иванов" 20 "A"
Запись успешно добавлена в таблицу 'students'

Введите команду: insert students "Петр Петров" 21 "A"
Запись успешно добавлена в таблицу 'students'

Введите команду: select students
(таблица с результатами)

Введите команду: select students grade="A"
(таблица с результатами)

Введите команду: update students set grade="B" where name="Иван Иванов"
Обновлено записей: 1

Введите команду: select students name="Иван Иванов"
(таблица с результатами)

Введите команду: delete students age=21
Удалено записей: 1

Введите команду: select students
(таблица с результатами)

Введите команду: exit
Выход из программы...

# Демонстрация CRUD-операций
Демонстрация основных функций (create_table, list_tables, drop_table):
https://asciinema.org/a/E1lA3rY5CQVbbilz

Демонстрация 
https://asciinema.org/a/K1u3YCgVfctO681W