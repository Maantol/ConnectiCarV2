import time
import canreader
from mqtt_publisher import publish_mqtt
from mqtt_publisher import MQTTMessage
from influx_db_handler import InfluxDBHandler

def main():
    """Gets the signal strength data and GPS data continuously and sends it to influxDB.
    """
    influx_db_handler = InfluxDBHandler()
    try:
        canreader.read()
        """
        influx_db_handler.serial.send_command_to_serial("AT+QGPS=1")  # turn on GPS
        print("Waiting 2 minutes for GPS.")
        time.sleep(120)
        while True:
            msg = MQTTMessage()
            msg.add_signal_strength(serial_handler.get_signal_strength())
            msg.add_gps_data(*serial_handler.get_gps_data())
            msg.add_can_data(canreader.get_can_data())
            publish_mqtt("connecticar-mqtt.2.rahtiapp.fi", "toyota", msg.to_json(), 443)
        """
    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")
    # finally:
        # influx_db_handler.serial.send_command_to_serial("AT+QGPSEND")  # turn off GPS
        # print("GPS connection close")

if __name__ == "__main__":
    main()
            