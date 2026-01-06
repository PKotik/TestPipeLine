"""
Уязвимое Flask-приложение для демонстрации DevSecOps-пайплайна.
Намеренно содержит проблемы для обнаружения Trivy.
"""
import pickle
import subprocess
import yaml
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import sqlite3

app = Flask(__name__)
# CORS без ограничений (уязвимость)
CORS(app, resources={r"/*": {"origins": "*"}})

# Небезопасная десериализация (CWE-502)
notes_db = []

@app.route('/')
def home():
    """Главная страница с инъекцией шаблона (CWE-1336)"""
    name = request.args.get('name', 'Guest')
    # Уязвимость SSTI (Server-Side Template Injection)
    template = f"<h1>Welcome, {name}!</h1><p>This is a vulnerable app for security testing.</p>"
    return render_template_string(template)

@app.route('/notes', methods=['GET'])
def get_notes():
    """Получить все заметки"""
    return jsonify(notes_db)

@app.route('/notes', methods=['POST'])
def add_note():
    """Добавить заметку с небезопасной десериализацией"""
    data = request.get_json()
    
    if 'note' not in data:
        return jsonify({'error': 'No note provided'}), 400
    
    # Уязвимость: десериализация без валидации
    try:
        # Здесь может быть уязвимость, если данные придут в base64
        note_data = data.get('note')
        if isinstance(note_data, str) and note_data.startswith('gASV'):
            # Эмуляция десериализации pickle
            note = pickle.loads(bytes.fromhex(note_data[4:]))
        else:
            note = note_data
    except:
        note = note_data
    
    notes_db.append({
        'id': len(notes_db) + 1,
        'content': str(note),
        'timestamp': '2024-01-01'  # Фиксированная дата для простоты
    })
    
    return jsonify({'message': 'Note added', 'id': len(notes_db)}), 201

@app.route('/fetch')
def fetch_url():
    """Загрузить URL с отключенной проверкой SSL (CWE-295)"""
    url = request.args.get('url', 'https://example.com')
    
    # Уязвимость: отключение проверки SSL
    response = requests.get(url, verify=False, timeout=5)
    return jsonify({
        'url': url,
        'status': response.status_code,
        'content_length': len(response.text)
    })

@app.route('/calc')
def calculator():
    """Калькулятор с возможностью инъекции команд (CWE-78)"""
    expr = request.args.get('expr', '1+1')
    
    # Уязвимость: выполнение shell-команд
    try:
        # Опасный способ вычисления выражения
        result = eval(expr)  # CWE-94: Code Injection
    except Exception as e:
        result = f"Error: {str(e)}"
    
    return jsonify({'expression': expr, 'result': result})

@app.route('/config')
def show_config():
    """Показать конфигурацию с небезопасной загрузкой YAML (CWE-20)"""
    config_file = request.args.get('file', 'config.yaml')
    
    # Уязвимость: загрузка YAML без safe_load
    try:
        with open(config_file, 'r') as f:
            config = yaml.load(f)  # Опасный load вместо safe_load
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Уязвимость: запуск в production без WSGI
    app.run(
        host='0.0.0.0',  # CWE-1327: Binding to all interfaces
        port=5000,
        debug=True  # CWE-489: Debug mode enabled in production
    )