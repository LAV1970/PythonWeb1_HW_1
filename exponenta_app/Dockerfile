FROM python:3.12
# Устанавливаем зависимости
RUN pip install prompt_toolkit

# Копируем файлы приложения в контейнер
COPY . /app
WORKDIR /app

# Команда для запуска вашего приложения
CMD ["python", "main.py"]