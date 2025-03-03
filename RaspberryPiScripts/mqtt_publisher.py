import paho.mqtt.client as mqtt

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
    client.publish(topic, message)
    client.disconnect()

if __name__ == "__main__":
    publish_mqtt("connecticar-mqtt.2.rahtiapp.fi", "toyota", "Hello, MQTT!", 443)

 