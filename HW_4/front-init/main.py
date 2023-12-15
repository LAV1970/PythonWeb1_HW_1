from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import json
from datetime import datetime
import threading
import os

app = Flask(__name__, static_url_path="/static")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
socketio = SocketIO(app)

# Путь к папке для сохранения данных
storage_dir = os.path.join(os.getcwd(), "storage")
os.makedirs(storage_dir, exist_ok=True)

# Путь к файлу для сохранения данных
data_file_path = os.path.join(storage_dir, "data.json")

# Загрузка данных из существующего файла
if os.path.exists(data_file_path):
    with open(data_file_path, "r") as json_file:
        messages_data = json.load(json_file)
else:
    messages_data = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/message")
def message():
    return render_template("message.html")


@app.route("/handle_post_message", methods=["POST"])
def handle_post_message():
    # Ваш код обработки POST-запроса
    return "Success"  # или возвращайте что-то еще в зависимости от вашей логики


@socketio.on("message_from_client")
def handle_message(message):
    username = message["username"]
    text = message["text"]

    # Здесь вы можете добавить логику для обработки сообщения

    # Создание ключа с использованием времени получения сообщения
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    key = timestamp[:-3]

    # Сохранение данных в словаре
    messages_data[key] = {"username": username, "message": text}

    # Оповещение клиентов через SocketIO
    response_message = {"username": username, "text": text, "timestamp": timestamp}
    socketio.emit("message_from_server", response_message)

    # Сохранение данных в JSON файл
    save_to_json(messages_data)


def save_to_json(data):
    with open(data_file_path, "w") as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False)
