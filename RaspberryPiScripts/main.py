import can_reader
from mqtt_publisher import MQTTMessage, publish_mqtt
from serial_handler import SerialHandler

def main():
    serial_handler = SerialHandler()

    try:
        """
        serial.send_command_to_serial("AT+QGPS=1")  # turn on GPS
        print("Waiting 2 minutes for GPS.")
        time.sleep(120)
        """
        while True:
            mqtt_message = MQTTMessage()

            # SIGNAL STRENGTH
            signal_strength = serial_handler.read_signal_strength_data()
            mqtt_message.add_signal_strength(signal_strength)

            # GPS DATA
            gps_data = serial_handler.read_gps_data()
            mqtt_message.add_gps_data(*gps_data)

            # CAN DATA
            can_data = can_reader.read()
            mqtt_message.add_can_data(can_data)

            json_message = mqtt_message.to_json()
            print(f"JSON: {json_message}")
            publish_mqtt(json_message)

    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")
    # finally:
        # serial.send_command_to_serial("AT+QGPSEND")  # turn off GPS
        # print("GPS connection close")

    if __name__ == "__main__":
        main()
