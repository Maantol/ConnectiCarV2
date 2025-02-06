import unittest
from serial_handler import SerialHandler
from influx_db_handler import InfluxDBHandler

class ConnectiCarUnitTests(unittest.TestCase):
    
    def test_signal_strength_type(self):
        serial = SerialHandler()
        signal_strength = serial.read_signal_strength_data()
        self.assertIsInstance(signal_strength, int)
    
    def test_sending_command(self):
        serial = SerialHandler()
        at_ok = serial.send_command_to_serial("AT", return_output=True)
        self.assertIn("OK", at_ok)
    
    def test_sim_status(self):
        serial = SerialHandler()
        cpin = serial.send_command_to_serial("AT+CPIN?", return_output=True)
        self.assertIn("READY", cpin)

    def test_influx_signal_strength_query(self):
        influx = InfluxDBHandler()
        query = f'from(bucket:"{influx.bucket}")\
        |> range(start: -10m)\
        |> filter(fn:(r) => r._measurement == "signal_strength")\
        |> filter(fn:(r) => r._field == "signal_strength")\
        |> last()'
        signal_strength = influx.read_and_write_signal_strength_data()
        result = influx.query_api.query(org=influx.org, query=query)
        for table in result:
            for record in table.records:
                query_result = record.get_value()
        self.assertEqual(signal_strength, query_result)



if __name__ == '__main__':
    unittest.main()
