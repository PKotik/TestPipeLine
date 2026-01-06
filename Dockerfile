# Использование устаревшего базового образа
FROM python:3.7-slim

# Работа от root (безопаснее создавать отдельного пользователя)
USER root

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ /app/src/
COPY config.yaml /app/

# Уязвимость: чувствительные данные в билде
ENV SECRET_KEY="insecure_secret_here"
ENV ADMIN_PASSWORD="admin123"

# Открытие всех портов
EXPOSE 5000 80 443

# Запуск от root
CMD ["python", "/app/src/app.py"]