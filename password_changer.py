#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests

response = requests.get("http://127.0.0.1:5000/status")
print(response.text)

print("Введите имя:")
username = input()

print("Введите пароль:")
old_password = input()

print("Введите новый пароль")
new_password = input()

response = requests.post(
    "http://127.0.0.1:5000/change_pass",
    json={"username": username, "old_password": old_password, "new_password": new_password}
)
if not response.json()['ok']:
    print('Пользователь не найден или неверный пароль')
else:
    print('Пароль успешно обновлен')
exit()