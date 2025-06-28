FROM python:3.10-slim

# Installiere benötigte Tools (optional für Debug)
RUN apt-get update && apt-get install -y netcat curl openssl iputils-ping

# Arbeitsverzeichnis setzen
WORKDIR /app

# Projektdateien kopieren
COPY mqtt_client.py requirements.txt ca-root.pem ./

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Umgebungsvariablen setzen (können bei Bedarf durch docker run überschrieben werden)
ENV BROKER=iothub.magenta.at
ENV PORT=8883
ENV CA_FILE=/app/ca-root.pem
ENV ACCESS_TOKEN=dein_access_token_hier

# Standardkommando (für MQTT-Client)
CMD ["python", "mqtt_client.py"]
