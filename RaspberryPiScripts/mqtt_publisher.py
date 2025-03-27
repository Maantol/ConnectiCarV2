import json
import paho.mqtt.client as mqtt
import config as cfg

config: dict = cfg.get_config()
broker: str = config["mqtt"]["broker"]
topic: str = config["mqtt"]["topic"]
port: int = config["mqtt"]["port"]
certs_path: str = config["mqtt"]["certs_path"]

client = mqtt.Client()
client.tls_set(certs_path)
client.tls_insecure_set(True)
client.connect(broker, port)
print(f"Connected to MQTT broker {broker} on port {port}")

class MQTTMessage:
    """
    Class for creating a message to be sent to an MQTT broker.
    """
    def add_signal_strength(self, signal_strength):
        self.signal_strength = signal_strength

    def add_gps_data(self, timestamp, latitude, longitude, speed, date):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.date = date

    def add_can_data(self, can_data):
        self.can_data = can_data

    def to_json(self):
        return json.dumps(self.__dict__)
    
class SimpleMQTTMessage:
    """
    Class for creating a simple message to be sent to an MQTT broker.
    """
    def __init__(self, subtopic: str, message: str):
        self.subtopic = subtopic
        self.message = message

def publish_mqtt(subtopic: str, message: str):
    """
    Publishes a message to a configured MQTT topic.
    
    :param message: Message to send
    """
    client.publish(topic + subtopic, message)

def publish_mqtt_simple(mqtt_message: SimpleMQTTMessage):
    """
    Publishes a simple message to a configured MQTT topic.
    
    :param mqtt_message: SimpleMQTTMessage object
    """
    client.publish(topic + mqtt_message.subtopic, mqtt_message.message)

if __name__ == "__main__":
    publish_mqtt("Hello, MQTT!")

 