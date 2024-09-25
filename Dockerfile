FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webhook_server.py .

ENV FLASK_APP=webhook_server.py
ENV FLASK_RUN_HOST=0.0.0.0

# CMD ["flask", "run"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "webhook_server:app"]
