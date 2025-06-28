FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY mqtt_client.py .
COPY ca-root.pem .
CMD ["python", "mqtt_client.py"]
