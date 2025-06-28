FROM python:3.10-slim

# Debug-Tools (optional)
RUN apt-get update && apt-get install -y netcat-openbsd curl openssl iputils-ping

# Arbeitsverzeichnis
WORKDIR /app

# Projektdateien kopieren
COPY mqtt_client.py requirements.txt ca-root.pem ./

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Umgebungsvariablen (können überschrieben werden)
ENV BROKER=iothub.magenta.at
ENV PORT=8883
ENV CA_FILE=/app/ca-root.pem
ENV ACCESS_TOKEN=dein_access_token_hier

# Start
CMD ["python", "mqtt_client.py"]
