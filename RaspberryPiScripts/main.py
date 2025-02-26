import time
import canreader
from influx_db_handler import InfluxDBHandler

def main():
    """Gets the signal strength data and GPS data continuously and sends it to influxDB.
    """
    influx_db_handler = InfluxDBHandler()
    try:
        # influx_db_handler.serial.send_command_to_serial("AT+QGPS=1")  # turn on GPS
        # print("Waiting 2 minutes for GPS.")
        # time.sleep(120)
        while True:
            canreader.read()
            influx_db_handler.read_and_write_signal_strength_data()
            time.sleep(3)
            # influx_db_handler.read_and_write_gps_data()
            # time.sleep(3)
    except KeyboardInterrupt:
        print("Code execution was interrupted by user.")
    # finally:
        # influx_db_handler.serial.send_command_to_serial("AT+QGPSEND")  # turn off GPS
        # print("GPS connection close")

if __name__ == "__main__":
    main()
            