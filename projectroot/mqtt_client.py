import paho.mqtt.client as mqtt
import time
import json
import os
import random
import math
from datetime import datetime
import logging

# Logging-Konfiguration
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s')

# Umgebungsvariablen laden
BROKER = os.getenv("BROKER", "iothub.magenta.at")
PORT = 8883
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CA_FILE = os.getenv("CA_FILE", "ca-root.pem")

# MQTT-Client initialisieren
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.tls_set(ca_certs=CA_FILE)

# MQTT-Callbacks definieren
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("MQTT Verbindung erfolgreich!")
    else:
        logging.warning(f"MQTT Verbindung fehlgeschlagen, Code: {rc}")

def on_disconnect(client, userdata, rc):
    logging.warning(f"MQTT Verbindung getrennt (rc={rc})")

def on_publish(client, userdata, mid):
    logging.debug(f"Nachricht veröffentlicht (mid={mid})")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Verbindungsversuch
try:
    logging.info(f"Zertifikat: {CA_FILE}")
    logging.info(f"Broker: {BROKER}:{PORT}")
    client.connect(BROKER, PORT, 60)
except Exception as e:
    logging.error(f"Verbindung fehlgeschlagen: {e}")
    exit(1)

client.loop_start()

# ThingsBoard-typisches Topic
topic = "v1/devices/me/telemetry"

# Initialwerte
temperatur = 25.0
vibration = 0.5
leistung = 50
drehzahl = 1500
betriebsminuten = 10000
letzte_wartung = datetime.now().strftime("%Y-%m-%d")
status = "betriebsbereit"

last_sent = {
    "temperatur": 0,
    "vibration": 0,
    "status": 0,
    "leistung": 0,
    "drehzahl": 0,
    "betriebsminuten": 0,
    "letzte_wartung": ""
}

intervals = {
    "temperatur": 300,
    "vibration": 30,
    "status": 3600,
    "leistung": 30,
    "drehzahl": 30,
    "betriebsminuten": 30
}

def ermittle_status(temp, vib, leist, rpm):
    if temp > 65 or vib > 3.5:
        return "stopped"
    elif leist > 30 and rpm > 1200:
        return "running"
    else:
        return "betriebsbereit"

# Hauptloop
while True:
    try:
        now = time.time()
        payload = {}

        if now - last_sent["temperatur"] >= intervals["temperatur"]:
            temperatur += random.uniform(-0.5, 0.7)
            temperatur = min(max(temperatur, 15), 80)
            payload["temperatur"] = round(temperatur, 1)
            last_sent["temperatur"] = now

        if now - last_sent["vibration"] >= intervals["vibration"]:
            vibration = round(random.uniform(0.1, 4.0), 2)
            payload["vibration"] = vibration
            last_sent["vibration"] = now

        if now - last_sent["leistung"] >= intervals["leistung"]:
            leistung = random.randint(25, 95)
            payload["motor_aktuelleLeistung"] = leistung
            last_sent["leistung"] = now

        if now - last_sent["drehzahl"] >= intervals["drehzahl"]:
            drehzahl = int(1500 + 200 * math.sin(now / 60) + random.uniform(-50, 50))
            payload["drehzahl"] = drehzahl
            last_sent["drehzahl"] = now

        if now - last_sent["betriebsminuten"] >= intervals["betriebsminuten"]:
            betriebsminuten += 0.5
            payload["motor_betriebsminutenGesamt"] = int(betriebsminuten)
            last_sent["betriebsminuten"] = now

            if betriebsminuten % 5000 < 1:
                letzte_wartung = datetime.now().strftime("%Y-%m-%d")

        if letzte_wartung != last_sent["letzte_wartung"]:
            payload["motor_letzteWartung"] = letzte_wartung
            last_sent["letzte_wartung"] = letzte_wartung

        neuer_status = ermittle_status(temperatur, vibration, leistung, drehzahl)
        if neuer_status != status or now - last_sent["status"] >= intervals["status"]:
            status = neuer_status
            payload["status"] = status
            last_sent["status"] = now

        if payload:
            # Verbindung prüfen vor dem Senden
            if not client.is_connected():
                logging.warning("MQTT Verbindung verloren, versuche Wiederverbindung...")
                try:
                    client.reconnect()
                    time.sleep(2)
                except Exception as e:
                    logging.error(f"Wiederverbindung fehlgeschlagen: {e}")
                    continue
                    
            result = client.publish(topic, json.dumps(payload), qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"Gesendet: {payload}")
            else:
                logging.error(f"Fehler beim Senden: {result.rc}")

        time.sleep(1)
        
    except KeyboardInterrupt:
        logging.info("Programm durch Benutzer beendet")
        break
    except Exception as e:
        logging.error(f"Unerwarteter Fehler: {e}")
        time.sleep(5)  # Kurze Pause bei Fehlern
        
# Sauberes Beenden
client.loop_stop()
client.disconnect()
logging.info("MQTT Client beendet")
