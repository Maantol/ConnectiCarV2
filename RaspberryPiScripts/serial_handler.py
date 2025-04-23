import serial
import re
import json
import time
import config as cfg

class SerialHandler:
    
    def __init__(self, used_serial="/dev/ttyUSB2"):
        """This class is used to read data through the serial port.
        
        Args:
            used_serial (str, optional): Used serial bus, /dev/ttyUSB2 by default.
        
        try:
            self.s = serial.Serial(used_serial, 115200, timeout=1)
        except Exception as e:  # to be specified later on.
            print(e)
        """

    def read_signal_strength_data(self):
        """Reads signal strength data through the serial port.

        Returns:
            int: Received signal strength indication. Possible values are:
                 0      -113 dBm or less
                 1      -111 dBm
                 2–30   -109 dBm to -53 dBm
                 31     -51 dBm or greater  # best signal strength
                 99      Not known or not detectable
        """
        try:
            regex_pattern = re.compile(r"\+CSQ: (?P<strength>\d+)")
            output = self.send_command_to_serial("AT+CSQ", return_output=True)
            match = re.match(regex_pattern, output)
            if match:
                signal_strength = match.group('strength')
                return int(signal_strength)
        except Exception as e:
            print(f"Unknown error occurred. Caught exception: {e}")
            return -1

    def read_gps_data(self):
        """Reads wanted GPS values through the serial port.

        Returns:
            str: UTC time    (hhmmss.sss)
            str: latitude    (ddmm.mmmmN/S)
            str: longitude   (ddmm.mmmmE/W)
            str: speed, km/h (xxxx.x)
            str: date        (ddmmyy)
            
        """
        try:
            regex_pattern = re.compile(r"""
            \+QGPSLOC:            # Match prefix
            (?P<utc>\S+),         # Capture UTC timestamp
            (?P<latitude>\S+),    # Capture latitude
            (?P<longitude>\S+),   # Capture longitude
            \S+,                  # Skip redundant values
            \S+,                  # Skip redundant values
            \S+,                  # Skip redundant values
            \S+,                  # Skip redundant values
            (?P<speed>\S+),       # Capture speed
            \S+,                  # Skip redundant values
            (?P<date>\S+)         # Capture date
            """, re.VERBOSE)
            
            output = self.send_command_to_serial("AT+QGPSLOC=0", return_output=True)
            match = re.match(regex_pattern, output)
            if match:
                return match.group('utc'), match.group('latitude'), match.group('longitude'), match.group('speed'), match.group('date')
            elif "ERROR" in output:
                print(f"Error found in output: {output}")
        except Exception as e:
            print(e)

    def send_command_to_serial(self, command, return_output=False):
        """Sends given command via serial.

        Args:
            command (str): given command
            return_output (boolean, optional): If true, returns output
        Returns:
            string output
        """
        command = command + "\r\n"
        self.s.write(command.encode())
        if return_output:
            self.s.readline()  # Filter out the line containing the given command
            return self.s.readline().decode().strip()
        
    # reads next line from json file for simulation
    def read_gps_json_object_from_array(self, index=0):

        test_data_file = cfg.get_config()["simulation"]["gps_data"]

        try:
            with open(test_data_file, "r") as file:
                file_content = file.read()

                try:
                    data = json.loads(file_content)  
                    #print(f"loaded json data: {data}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    return   
            
            if index < len(data):
                return data[index]
            else:
                return None
    
        except Exception as e:
            print(f"Error loading test data from {test_data_file}: {e}")
            return {}
        
    # simulates random signal strength
    def read_random_signal_strength(self):
        return int(time.time()) % 32
        


