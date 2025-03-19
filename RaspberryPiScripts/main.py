import can_reader
import time
from mqtt_publisher import MQTTMessage, publish_mqtt
from serial_handler import SerialHandler

def main():
    serial_handler = SerialHandler()

    try:
        can_reader.read_from_json()
        """
        serial.send_command_to_serial("AT+QGPS=1")  # turn on GPS
        print("Waiting 2 minutes for GPS.")
        time.sleep(120)
        """
        while True:
            mqtt_message = MQTTMessage()
            json_message = None

            #commented for testing with json
            """ # SIGNAL STRENGTH
            signal_strength = serial_handler.read_signal_strength_data()
            mqtt_message.add_signal_strength(signal_strength)

            # GPS DATA
            gps_data = serial_handler.read_gps_data()
            if gps_data:
                timestamp, latitude, longitude, speed, date = gps_data
                mqtt_message.add_gps_data(timestamp, latitude, longitude, speed, date) """
            
            # Json simulation...
            gps_data = serial_handler.read_json_data()
            if gps_data:
                for data in gps_data:
                    timestamp = data["utc"]
                    latitude = data["latitude"]
                    longitude = data["longitude"]
                    speed = data["speed"]
                    date = data["date"]
                mqtt_message.add_gps_data(timestamp, latitude, longitude, speed, date)
           
            # CANDUMP
            for message in can_reader.read_from_json():  # Data from canbus, .read() for actual connection
                mqtt_message.add_can_data(message)  # Add data to  message
                # TEST PRINT
                print(f"CAN data (JSON format): {message}")
            
            # Convert to JSON format
            json_message = mqtt_message.to_json()
            

            #TEST PRINT
            print(f"Updated message JSON with can, signal & gps: {json_message}") # TESTING WITH MAIN LOOP DOESN'T WORK, WAITS FOR GENERATORS TO FINISH -> ALWAYS OUTPUTS LAST MESSAGE




            # mqtt publishing...
            # publish_mqtt("connecticar-mqtt.2.rahtiapp.fi", "toyota", msg.to_json(), 443)

            time.sleep(1)  # Adjust the delay
    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")
    # finally:
        # serial.send_command_to_serial("AT+QGPSEND")  # turn off GPS
        # print("GPS connection close")

if __name__ == "__main__":
    main()
