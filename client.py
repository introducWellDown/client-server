import tkinter as tk
from tkinter import ttk
import json
import threading
from server import modify_users


USERS_JSON_FILE = "users.json"

def load_users_from_json():
    try:
        with open(USERS_JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Список users  из JSON-файла
users = load_users_from_json()

# Создаем основное окно
root_window = tk.Tk()
root_window.title("client")
root_window.geometry("500x670")

# Задаём тему
style = ttk.Style().theme_use('clam')
# Создаем Treeview
columns = ttk.Treeview(root_window, column=("column_1", "column_2", "column_3"),
                       show='headings', height=32)  

# Создаем вертикальный скроллбар
scrollbar = ttk.Scrollbar(root_window, orient="vertical", command=columns.yview)
columns.configure(yscrollcommand=scrollbar.set)

# Размещаем Treeview и скроллбар на главном окне
columns.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Настраиваем упаковку столбцов для заполнения доступной ширины окна
root_window.grid_columnconfigure(0, weight=1)

# Определяем столбцы и заголовки
def create_column(count, names):
    for i in range(count):
        column_id = f"column_{i+1}"
        column_width = int(500 / count)

        columns.column(column_id, anchor=tk.CENTER, width=column_width)
        columns.heading(column_id, text=names[i])

# Вставляем данные в Treeview
def insert_data(data_list, keys):
    for item in data_list:
        values = [item[key] for key in keys]
        columns.insert('', 'end', values=values)

# Обновление данных Treeview из файла JSON с задержкой
def update_data():
    global users
    columns.delete(*columns.get_children())  # Очищаем таблицу
    users = load_users_from_json()  # Загружаем обновленные данные из файла
    insert_data(users, ["id", "name", "pay"])  # Вставляем обновленные данные в таблицу
    root_window.after(1000, update_data) 

# Запускаем фоновый процесс обновления данных и отображения скроллбара
def get_start():
   
    background_thread = threading.Thread(target=modify_users)  
    background_thread.daemon = True  # Фоновый поток завершится при завершении главного потока
    background_thread.start()

    # Запускаем обновление данных в интерфейсе
    update_data()

create_column(3, ["id", "name", "pay"])
insert_data(users, ["id", "name", "pay"])

get_start()

root_window.mainloop()