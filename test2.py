import threading
import time
import random
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# В этом скрипте происхрдит имитация работы сервера,который постоянно меняется.
# Добавляются новые пользователи,удаляются старые,меняются значения полей уже существующих пользователей 

# Создаем список имен пользователей для дальнейшей генерации полей в списке users
names = ["igor", "Koly", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"]

# Блокировка для синхронизации доступа к списку пользователей
lock = threading.Lock()

def is_unique_id(new_id):
    for user in users:
        if user['id'] == new_id:
            return False
    return True

def generate_unique_id():
    while True:
        new_id = random.randint(1, 1000)
        if is_unique_id(new_id):
            return new_id

USERS_JSON_FILE = "users.json"

def load_users_from_json():
    try:
        with open(USERS_JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users_to_json(users_data):
    with open(USERS_JSON_FILE, "w") as file:
        json.dump(users_data, file,indent=2)

# Заменяем список users на загрузку из JSON-файла
users = load_users_from_json()

def modify_users():
    global users

    while True:
        time.sleep(1)  

        with lock:
            # Вносим произвольные изменения в данные пользователей
            if users:
                user_to_change = random.choice(users)
                user_to_change["pay"] = random.choice([True, False])
                #print(f'Изменено значение у пользователя: id={user_to_change["id"]} в поле "Pay" на {user_to_change["pay"]}')

            # Произвольно удаляем пользователя
            if users:
                user_to_remove = random.choice(users)
                users.remove(user_to_remove)
                #print(f"Удален пользователь: {user_to_remove}")
                #for user in users:
                    #print(user)

            # Произвольно добавляем нового пользователя
            new_user = {"id": generate_unique_id(), "name": random.choice(names), "pay": random.choice([True, False])}
            users.append(new_user)
            #print(f"Добавлен новый пользователь: {new_user}")
            #for user in users:
                #print(user)

            # Сохраняем обновленные данные в JSON-файл
            save_users_to_json(users)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.lock = kwargs.pop("lock")
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            with self.lock:
                response = json.dumps(users).encode('utf-8')
                self.wfile.write(response)

def run_server(lock):
    server_address = ('localhost', 5000)
    httpd = HTTPServer(server_address, lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, lock=lock, **kwargs))
    httpd.serve_forever()

if __name__ == "__main__":
    # Запускаем сервер в отдельном потоке
    server_thread = threading.Thread(target=run_server, args=(lock,))
    server_thread.daemon = True
    server_thread.start()

    # Запускаем поток для модификации пользователей
    modify_users_thread = threading.Thread(target=modify_users)
    modify_users_thread.daemon = True
    modify_users_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # При остановке программы закрываем файл users.json
        save_users_to_json(users)
