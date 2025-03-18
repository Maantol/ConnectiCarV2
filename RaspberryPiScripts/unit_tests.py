import unittest
from serial_handler import SerialHandler

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

if __name__ == '__main__':
    unittest.main()
