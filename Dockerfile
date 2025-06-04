FROM python:3.12-slim

WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .
