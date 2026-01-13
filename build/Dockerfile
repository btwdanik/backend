FROM python:3.13-slim

WORKDIR /app

COPY build/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../src .

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8080", "main.py"]