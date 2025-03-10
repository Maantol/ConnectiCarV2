import json
import paho.mqtt.client as mqtt

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

def publish_mqtt(broker: str, topic: str, message: str, port: int = 1883):
    """
    Publishes a message to a given MQTT topic.
    
    :param broker: MQTT broker address
    :param topic: Topic to publish to
    :param message: Message to send
    :param port: Broker port (default is 1883)
    """
    client = mqtt.Client()
    client.tls_set("./certs/ca.crt")
    client.tls_insecure_set(True)
    client.connect(broker, port)
    print(f"Connected to MQTT broker {broker} on port {port}")
    client.publish(topic, message)
    print(f"Published message: {message} to topic {topic}")
    client.disconnect()

if __name__ == "__main__":
    publish_mqtt("connecticar-mqtt.2.rahtiapp.fi", "toyota", "Hello, MQTT!", 443)

 