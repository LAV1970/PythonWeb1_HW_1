from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("message_from_client")
def handle_message(message):
    username = message["username"]
    text = message["text"]

    # Здесь ты можешь добавить логику для обработки сообщения

    response_message = {"username": username, "text": text}
    socketio.emit("message_from_server", response_message)

    # Сохраняем данные в JSON файл
    data = {"username": username, "text": text}
    save_to_json(data)


def save_to_json(data):
    storage_dir = os.path.join(os.getcwd(), "storage")
    os.makedirs(storage_dir, exist_ok=True)

    file_path = os.path.join(storage_dir, "data.json")
    with open(file_path, "a") as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    socketio.run(app, debug=True)
