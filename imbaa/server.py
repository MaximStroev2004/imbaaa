from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

messages_lock = threading.Lock()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

def save_message(text):
    with app.app_context():  # Устанавливаем контекст приложения
        message = Message(text=text)
        db.session.add(message)
        db.session.commit()

def load_messages():
    with app.app_context():  # Устанавливаем контекст приложения
        messages = Message.query.all()
        return [message.text for message in messages]

def handle_message(data):
    message_text = data.get('message')
    with messages_lock:
        save_message(message_text)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message_text = data.get('message')

    thread = threading.Thread(target=handle_message, args=(data,))
    thread.start()

    return jsonify({'message': 'Сообщение успешно получено и обработано', 'text': message_text})

@app.route('/messages', methods=['GET'])
def get_messages():
    with messages_lock:
        messages = load_messages()
        return jsonify({'messages': messages})

@app.route('/')
def index():
    messages = load_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    with app.app_context():  # Устанавливаем контекст приложения
        db.create_all()  # Создание всех таблиц в базе данных
    app.run(debug=True)
