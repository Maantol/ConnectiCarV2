import time
import canreader
from mqtt_publisher import MQTTMessage, publish_mqtt
from influx_db_handler import InfluxDBHandler
from serial_handler import SerialHandler

def main():
    """Gets the signal strength data and GPS data continuously and sends it to influxDB.
    """
    # influx_db_handler = InfluxDBHandler()
    serial_handler = SerialHandler()

    try:
        #canreader.read()
        """
        influx_db_handler.serial.send_command_to_serial("AT+QGPS=1")  # turn on GPS
        print("Waiting 2 minutes for GPS.")
        time.sleep(120)
        """
        while True:
            mqtt_message = MQTTMessage()
            # SIGNAL STRENGTH
            signal_strength = serial_handler.read_signal_strength_data()
            mqtt_message.add_signal_strength(signal_strength)
            print(f"Initial signal strength: {signal_strength}")

            # GPS DATA
            gps_data = serial_handler.read_gps_data()
            if gps_data:
                timestamp, latitude, longitude, speed, date = gps_data
                mqtt_message.add_gps_data(timestamp, latitude, longitude, speed, date)
           
            # CANDUMP
            for can_data in canreader.read():  # Data from canbus
                mqtt_message.add_can_data(can_data)  # Add data to  message
                # test message
                print(f"CAN data (JSON format): {json_message}")
                
            # Convert to JSON format
            json_message = mqtt_message.to_json()
            #TEST PRINT
            print(f"Updated message JSON with can, signal & gps: {json_message}")

            # mqtt publishing...
            # publish_mqtt("connecticar-mqtt.2.rahtiapp.fi", "toyota", msg.to_json(), 443)

            time.sleep(1)  # Adjust the delay
    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")
    # finally:
        # influx_db_handler.serial.send_command_to_serial("AT+QGPSEND")  # turn off GPS
        # print("GPS connection close")

    if __name__ == "__main__":
        main()
