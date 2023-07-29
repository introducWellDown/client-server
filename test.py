import tkinter as tk
from tkinter import ttk
import threading
import requests

USERS_JSON_URL = "http://localhost:5000"  # Замените на URL вашего сервера
PAGE_SIZE = 50  # Количество записей, запрашиваемых с сервера за раз
MAX_USERS = 1000  # Общее количество пользователей на сервере (задайте реальное значение)

def load_users_from_server(page):
    try:
        response = requests.get(f"{USERS_JSON_URL}?page={page}&size={PAGE_SIZE}")
        response.raise_for_status()  # Это вызовет исключение для статусных кодов, отличных от 2xx
        data = response.json()
        print("Данные получены с сервера:", data)  # Добавьте эту строку, чтобы проверить формат данных
        return data
    except requests.exceptions.RequestException as e:
        print("Ошибка при получении данных с сервера:", e)
        return []

def create_column(count, names):
    for i in range(count):
        column_id = f"column_{i+1}"
        column_width = int(500 / count)

        columns.column(column_id, anchor=tk.CENTER, width=column_width)
        columns.heading(column_id, text=names[i])

def insert_data(data_list):
    for item in data_list:
        values = [item["id"], item["name"], item["pay"]]
        columns.insert('', 'end', values=values)

def on_scroll(event):
    global last_loaded_page

    # Получаем информацию о видимой части Treeview при прокрутке
    first_visible = int(event.y / 20)  # Предполагаем, что высота строки 20 (может потребоваться корректировка)
    last_visible = int((event.y + event.height) / 20) - 1

    # Проверяем, нужно ли загрузить новые данные
    current_page = (first_visible // PAGE_SIZE) + 1
    if current_page * PAGE_SIZE <= MAX_USERS and current_page != last_loaded_page:
        new_data = load_users_from_server(current_page)
        insert_data(new_data)
        last_loaded_page = current_page

root_window = tk.Tk()
root_window.title("client")
root_window.geometry("500x670")

style = ttk.Style().theme_use('clam')
columns = ttk.Treeview(root_window, column=("column_1", "column_2", "column_3"), show='headings', height=32)

scrollbar = ttk.Scrollbar(root_window, orient="vertical", command=columns.yview)
columns.configure(yscrollcommand=scrollbar.set)

columns.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

root_window.grid_columnconfigure(0, weight=1)

create_column(3, ["id", "name", "pay"])

current_page = 1
last_loaded_page = 0

# Загружаем первую порцию данных с сервера
data = load_users_from_server(current_page)
insert_data(data)
last_loaded_page = current_page

# Связываем событие прокрутки с обработчиком
columns.bind("<Configure>", on_scroll)

root_window.mainloop()


