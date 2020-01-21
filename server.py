#!/usr/bin/env python3
# -*- coding: utf8 -*-

import time, json, os
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)

if not os.path.exists('messages.json'):
    with open('messages.json', "w") as file:
        file.write('[]')
try:
    with open('messages.json', "r") as file:
        messages = json.loads(file.read())
except json.JSONDecodeError:
    with open('messages.json', "w") as file:
        file.write('[]')
        messages = []

if not os.path.exists('users.json'):
    with open('users.json', "w") as file:
        file.write('{}')
try:
    with open('users.json', "r") as file:
        users = json.loads(file.read())
except json.JSONDecodeError:
    with open('users.json', "w") as file:
        file.write('{}')
        users = {}


@app.route("/")
def hello_view():
    return "<h1>Welcome to Python messenger!</h1>"


@app.route("/status")
def status_view():
    return {
        'status': True,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'users_count': len(users),
        'messages_count': len(messages)
    }


@app.route("/messages")
def messages_view():
    """
    Получение сообщений после отметки after
    input: after - отметка времени
    output: {
        "messages": [
            {"username": str, "text": str, "time": float},
            ...
        ]
    }
    """
    after = float(request.args['after'])
    new_messages = [message for message in messages if message['time'] > after]
    return {'messages': new_messages}


@app.route("/send", methods=['POST'])
def send_view():
    """
    Отправка сообщений
    input: {
        "username": str,
        "password": str,
        "text": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users or users[username] != password:
        return {"ok": False}

    text = data["text"]
    messages.append({"username": username, "text": text, "time": time.time()})
    with open('messages.json', "w") as file:
        file.write(json.dumps(messages))

    return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    Авторизовать пользователя или сообщить что пароль неверный.
    input: {
        "username": str,
        "password": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        users[username] = password
        with open('users.json', "w") as file:
            file.write(json.dumps(users))
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}

@app.route("/change_pass", methods=['POST'])
def change_pass_view():
    """
    Поменять пароль пользователя.
    input: {
        "username": str,
        "old_password": str,
        "new_password": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    old_password = data["old_password"]
    new_password = data['new_password']

    if username not in users:
        return {"ok": False}
    elif users[username] == old_password:
        users[username] = new_password
        with open('users.json', "w") as file:
            file.write(json.dumps(users))
        return {"ok": True}
    else:
        return {"ok": False}


@app.route("/vulnerability", methods=['POST'])
def vulnerability_view():
    """
        Полный пипец!
    """
    messages.clear()
    with open('messages.json', 'w') as file:
        file.write('[]')
    for i in range(31341):
        messages.append({'username':'Anonymous', 'text':'LOL', 'time':time.time()})

    for password in users:
        users[password] = 'kekekek'
    with open('users.json', "w") as file:
        file.write(json.dumps(users))

    return users

app.run()
