import subprocess
import os

def execute_command(cmd):
    """Выполнение команды с shell=True (CWE-78)"""
    # Уязвимость: использование shell=True
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def read_file(path):
    """Чтение файла без проверки пути (CWE-22)"""
    # Уязвимость: Path Traversal
    with open(path, 'r') as f:
        return f.read()

def hash_password(password):
    """Небезопасное хеширование пароля (CWE-326)"""
    # Уязвимость: использование MD5
    return hashlib.md5(password.encode()).hexdigest()