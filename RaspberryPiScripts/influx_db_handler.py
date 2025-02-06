from serial_handler import SerialHandler
from influxdb_client import Point
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDBHandler:
    
    def __init__(self):
        """This class acts as an intermediate between the RaspberryPi and InfluxDB.
        Data is read from the RaspberryPi and sent to InfluxDB through this class.
        """
        self.url = "YOUR_URL_HERE"
        self.token = "YOUR_TOKEN_HERE"
        self.org = "YOUR_ORG_HERE"
        self.bucket = "YOUR_BUCKET_HERE"
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.serial = SerialHandler()
    
    def read_and_write_signal_strength_data(self):
        signal_strength = self.serial.read_signal_strength_data()
        if signal_strength != -1:
            point = Point('signal_strength').field('signal_strength', signal_strength)
            if point:
                self.write_api.write(bucket=self.bucket, org=self.org, record=point)
                return signal_strength  # used in unit_tests.py
        else:
            print("Error in getting signal strength.")

    def read_and_write_gps_data(self):
        utc_time, latitude, longitude, speed, date = self.serial.read_gps_data()
        point = (Point('gps_data')
                 .field('utc', utc_time)
                 .field('latitude', latitude)
                 .field('longitude', longitude)
                 .field('speed', speed)
                 .field('date', date))
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        print(f"Data written: {point}")
