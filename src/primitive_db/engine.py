def show_help():
    """Показываем справочную информацию"""
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def welcome():
    """Основная функция запуска программы"""
    print("Первая попытка запустить проект!")
    print("***")
    show_help()
    
    while True:
        command = input("Введите команду: ").strip().lower()
        
        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            show_help()
        elif command:
            print(f"Неизвестная команда: {command}")
        else:
            print("Введите команду")
