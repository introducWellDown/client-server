import threading
import time
import random
import json

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

