import can_reader
import time
from mqtt_publisher import MQTTMessage, publish_mqtt, publish_mqtt_simple
from serial_handler import SerialHandler


def test():
    serial_handler = SerialHandler()
    try:
        """
        serial.send_command_to_serial("AT+QGPS=1")  # turn on GPS
        print("Waiting 2 minutes for GPS.")
        time.sleep(120)
        """
        i = 0 #index for looping through gpsmockdata
        while True:
            mqtt_message = MQTTMessage()
            # GPS JSON simulation...
            gps_data = serial_handler.read_gps_json_object_from_array(index=i)
            if gps_data:
                timestamp = gps_data["utc"]
                latitude = gps_data["latitude"]
                longitude = gps_data["longitude"]
                speed = gps_data["speed"]
                date = gps_data["date"]
                mqtt_message.add_gps_data(timestamp, latitude, longitude, speed, date)
                i += 1
            #Hardcoded index reset length, since mockdata is 7 objects long, checking length dynamically is too much effort for this purpose :D
            if i >= 7:
                i = 0
            # CANDUMP JSON sim
            message = next(can_reader.read_from_json(), None) #picks random message...
            if message:  # Data from can_dump.json file
                mqtt_message.add_can_data(message)  # Add data to  message
                # TEST PRINT
                #print(f"CAN data (JSON format): {message}")
        
            # Convert to JSON format
            json_message = mqtt_message.to_json()
            #TEST PRINT
            print(f"\nUpdated message JSON with can, signal & gps: {json_message} \n")  
            #TODO: logic for publishing instead of printing... (add topic+subtopic?)
            #publish_mqtt(json_message) ?
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")
    # finally:
        # serial.send_command_to_serial("AT+QGPSEND")  # turn off GPS
        # print("GPS connection close")

def test_no_generator():
    serial_handler = SerialHandler()
    mqtt_message = MQTTMessage()
    try:
        i = 0
        while True:
            signal_strength = serial_handler.read_random_signal_strength()
            mqtt_message.add_signal_strength(signal_strength)
            gps_data = serial_handler.read_gps_json_object_from_array(index=i)
            mqtt_message.add_gps_data(gps_data["utc"], gps_data["latitude"], gps_data["longitude"], gps_data["speed"], gps_data["date"])
            can_data = can_reader.read_object_from_json(index=i)
            mqtt_message.add_can_data(can_data)
            print(f"Message: {mqtt_message.to_json()}")
            publish_mqtt(mqtt_message.to_json())
            i = i + 1
            
    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")


def main():
    #serial_handler = SerialHandler()
    #mqtt_message = MQTTMessage()
    try:
        while True:
            #signal_strength = serial_handler.read_signal_strength_data()
            #mqtt_message.add_signal_strength(signal_strength)
            #gps_data = serial_handler.read_gps_data()
            #mqtt_message.add_gps_data(gps_data["utc"], gps_data["latitude"], gps_data["longitude"], gps_data["speed"], gps_data["date"])
            data = can_reader.read()
            if data is None:
                continue
            for message in data:
                publish_mqtt_simple(message)
                print(f"CAN data: {message}")
            
    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")


if __name__ == "__main__":
    #main()
    test()