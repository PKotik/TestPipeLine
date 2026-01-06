import sqlite3
import hashlib

def init_db():
    """Инициализация БД с потенциальными SQL-инъекциями"""
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
    # Создание таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            user_input TEXT  # Поле для демонстрации уязвимостей
        )
    ''')
    
    # Добавление тестовых данных с "уязвимым" вводом
    test_notes = [
        ("Test", "This is a test note", "'; DROP TABLE notes; --"),
        ("Admin", "Secret note", "<script>alert('xss')</script>"),
        ("User", "Normal note", "normal input")
    ]
    
    # Уязвимость: конкатенация строк вместо параметризованных запросов
    for title, content, user_input in test_notes:
        query = f"INSERT INTO notes (title, content, user_input) VALUES ('{title}', '{content}', '{user_input}')"
        cursor.execute(query)
    
    conn.commit()
    conn.close()

def search_notes(keyword):
    """Поиск заметок с SQL-инъекцией (CWE-89)"""
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: SQL-инъекция
    query = f"SELECT * FROM notes WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    
    return results