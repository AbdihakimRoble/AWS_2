import random
import time
import json
import uuid
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from decimal import Decimal
import requests
import boto3

# === AWS IoT och DynamoDB konfiguration ===
AWS_REGION = 'eu-north-1'
IOT_ENDPOINT = 'a3aijxzs7glmgu-ats.iot.eu-north-1.amazonaws.com'
TOPIC = 'iot/weather'
TABLE_NAME = 'IoTWeatherData'

# === Certifikatvägar (direkt angivna) ===
ROOT_CA_PATH = 'C:/Users/Abdih/AWS/certs/AmazonRootCA1.pem'
CERTIFICATE_PATH = 'C:/Users/Abdih/AWS/certs/certificate.pem.crt'
PRIVATE_KEY_PATH = 'C:/Users/Abdih/AWS/certs/private.pem.key'

# === Initiera DynamoDB och MQTT-klient ===
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

mqtt_client = AWSIoTMQTTClient("sensor-" + str(uuid.uuid4()))
mqtt_client.configureEndpoint(IOT_ENDPOINT, 8883)
mqtt_client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Temperaturhämtning ===
def fetch_temperature_from_api():
    """Hämtar temperatur från SMHI:s öppna API."""
    url = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/52350/period/latest-hour/data.json"
    try:
        response = requests.get(url)
        data = response.json()
        temperature = data['value'][-1]['value']
        return temperature
    except Exception as error:
        logger.error(f"API Error: {error}")
        return generate_random_temperature()

def generate_random_temperature():
    """Returnerar en slumpad temperatur om API:t misslyckas."""
    return round(random.uniform(10.0, 40.0), 2)

# === Publicera till AWS IoT och spara till DynamoDB ===
def publish_data():
    retries = 3
    for attempt in range(retries):
        try:
            temperature = fetch_temperature_from_api()
            timestamp = int(time.time())
            payload = {
                'deviceId': 'sensor-01',
                'temperature': str(temperature),
                'timestamp': timestamp
            }

            # Publicera till AWS IoT
            mqtt_client.publish(TOPIC, json.dumps(payload), 1)

            # Spara i DynamoDB
            table.put_item(Item={
                'deviceId': 'sensor-01',
                'timestamp': timestamp,
                'temperature': Decimal(str(temperature))
            })

            logger.info(f"✅ Publicerad: {temperature}°C")
            return
        except Exception as error:
            logger.error(f"❌ Fel vid publicering: {error}")
            if attempt < retries - 1:
                logger.info("🔁 Försöker igen...")
                sleep(2)
            else:
                logger.error("⛔ Max antal försök uppnått.")

# === Anslut MQTT ===
def connect_mqtt():
    retries = 3
    for attempt in range(retries):
        try:
            mqtt_client.connect()
            logger.info("🔌 Ansluten till AWS IoT.")
            return
        except Exception as error:
            logger.error(f"⚠️ Anslutningsfel: {error}")
            if attempt < retries - 1:
                sleep(5)
            else:
                logger.error("⛔ Misslyckades att ansluta efter flera försök.")

# === Starta sensorn ===
def run_sensor():
    try:
        connect_mqtt()
        while True:
            publish_data()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("⛔ Sensor avbruten av användare.")
    finally:
        try:
            mqtt_client.disconnect()
            logger.info("🔌 Frånkopplad från AWS IoT.")
        except Exception as error:
            logger.error(f"❌ Frånkopplingsfel: {error}")

# === Kör programmet ===
if __name__ == "__main__":
    run_sensor()
