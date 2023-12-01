# Використовуємо базовий образ Python
FROM python:3.8

# Копіюємо файли з GitHub у робочий каталог контейнера
WORKDIR /app
RUN git clone https://github.com/LAV1970/PythonWeb1_HW_1 .

# Запускаємо "Персонального помічника" при старті контейнера
CMD ["python", "/exponenta_app/main.py"]