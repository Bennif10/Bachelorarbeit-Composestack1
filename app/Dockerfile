FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

# Kopiere die requirements.txt in den Container
COPY requirements.txt /app/requirements.txt

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Kopiere deinen Quellcode in den Container
COPY . /app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]