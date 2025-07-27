FROM python:3.11-slim

WORKDIR /app

# requirements.txt staat in root
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# app.py en templates kopiëren naar container
COPY . /app

CMD ["python", "app.py"]
