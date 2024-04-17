import datetime
import csv
import os


def user_action(notebook): # Главное меню
    while True:
        print(
            '\nБлокнот заметок приветствует Вас!!\n1 - Просмотр всех заметок | 2 - Добавить заметку |'
            ' 3 - Изменить заметку | 4 - Удалить заметку | 5 - Поиск заметок по дате | 0 - Выйти из приложения\n')
        user_choice = input('Введите команду: ')
        if user_choice == '1':
            print_all_notes(notebook)
        elif user_choice == '2':
            add_new_note(notebook)
        elif user_choice == '3':
            edit_note(notebook)
        elif user_choice == '4':
            delete_note(notebook)
        elif user_choice == '5':
            search_notes_by_date(notebook)
        elif user_choice == '0':
            print('Гуд бай!')
            break
        else:
            print('Некорректный выбор действия! Повторите!')
            print()
            continue


def print_all_notes(file_path): # Вывод списка заметок на консоль
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)
        for row in reader:
            print(
                f"ID заметки: {row[0]}, Заголовок: {row[1]}, Дата/время создания: {row[3]},"
                f" Дата/время изменения: {row[4]}")
            print(f"Текст заметки: {row[2]}")
            print("-" * 80)


def add_new_note(file_path):  # добавление новой заметки
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        note_title = input('Введите заголовок заметки: ')
        note_content = input('Введите текст заметки: ')
        writer = csv.writer(file, delimiter=';')
        now = datetime.datetime.now()
        first_date = lust_date = now.strftime('%Y-%m-%d %H:%M:%S')
        note_id = get_next_id(file_path)
        if len(file_path) == 0:
            writer.writerow(
                ['ID Заметки', 'Заголовок заметки', 'Содержание заметки', 'Дата/время создания',
                 'Дата/время изменения'])
        writer.writerow([note_id, note_title, note_content, first_date, lust_date])
        print(f"Добавлена новая заметка! ID: {note_id}")
        print()


def get_next_id(file_path):  # Функция для получения следующего доступного ID
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next_id = sum(1 for row in reader)  # Количество строк в файле
    return next_id


def edit_note(file_path): # Редактирование заметки
    note_id = input("Введите ID заметки для редактирования: ")
    if not search_note_by_id(file_path, note_id):
        return
    temp_file_path = 'temp_notes.csv'

    with open(file_path, 'r', newline='', encoding='utf-8') as file, \
            open(temp_file_path, 'w', newline='', encoding='utf-8') as temp_file:
        reader = csv.reader(file, delimiter=';')
        writer = csv.writer(temp_file, delimiter=';')
        for row in reader:
            if row[0] == note_id:
                note_title = input("Введите новый заголовок: ")
                note_content = input("Введите новый текст заметки: ")
                now = datetime.datetime.now()
                row[1] = note_title
                row[2] = note_content
                row[4] = now.strftime('%Y-%m-%d %H:%M:%S')
                result = True
            writer.writerow(row)

    os.remove(file_path) # Заменяем исходный файл временным
    os.rename(temp_file_path, file_path)
    print(f"Заметка с ID {note_id} отредактирована!")


def delete_note(file_path):
    note_id = input("Введите ID заметки для удаления: ")
    if not search_note_by_id(file_path, note_id):
        return
    temp_file_path = 'temp_notes.csv'
    with open(file_path, 'r', newline='', encoding='utf-8') as file, \
            open(temp_file_path, 'w', newline='', encoding='utf-8') as temp_file:
        reader = csv.reader(file, delimiter=';')
        writer = csv.writer(temp_file, delimiter=';')
        for row in reader:
            if row[0] != note_id:
                writer.writerow(row)

    os.remove(file_name)
    os.rename(temp_file_path, file_name)
    print(f"Заметка с ID {note_id} удалена!")


def search_notes_by_date(file_path): # Выборка заметок по дате создания
    date_input = input("Введите дату в формате YYYY-MM-DD: ")
    try:
        target_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").strftime('%Y-%m-%d')
    except ValueError:
        print("Некорректный формат даты. Введите дату в формате YYYY-MM-DD.")
        return

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        found_notes = False
        for row in reader:
            if row[3].startswith(target_date):
                print(
                    f"ID заметки: {row[0]}, Заголовок: {row[1]}, Дата/время создания: {row[3]}, Дата/время изменения: {row[4]}")
                print(f"Текст заметки: {row[2]}")
                print("-" * 80)
                found_notes = True

        if not found_notes:
            print(f"Заметки, созданные {target_date}, не найдены.")


def search_note_by_id(file_path, note_id): # Проверка существования заметки с заданным ID
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)
        for row in reader:
            if row[0] == note_id:
                print(
                    f"ID заметки: {row[0]}, Заголовок: {row[1]}, Дата/время создания: {row[3]}, Дата/время изменения: {row[4]}")
                print(f"Текст заметки: {row[2]}")
                print("-" * 80)
                return True

        print(f"Заметки с ID {note_id} не существует!")
        return False


file_name = 'notes.csv'
try:
    with open(file_name, 'r') as notebook:
        pass
except FileNotFoundError:
    with open(file_name, 'w', newline='', encoding='utf-8') as notebook:
        writer = csv.writer(notebook, delimiter=';')
        writer.writerow(['ID Заметки', 'Заголовок заметки', 'Содержание заметки',
                         'Дата/время создания', 'Дата/время изменения'])
        notebook.flush()

user_action(file_name)
