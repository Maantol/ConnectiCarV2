from serial_handler import SerialHandler
import logging
import sys

class TestingClient:
    
    def __init__(self):
        """Class designed to help with manual testing of commands and output. Will create a log file of everything.
        """
        self.logger = logging.getLogger()

    def perform_communications(self):
        self.set_logger()
        self.help()
        user_input = input("Please give the serial bus you want to use. Press ENTER if you wish to use /dev/ttyUSB2: ")
        if user_input:
            self.serial = SerialHandler(user_input)
            self.logger.info(f"Used serial bus is: {user_input}")
        else:
            self.serial = SerialHandler()
            self.logger.info("Using default serial bus (/dev/ttyUSB2)")

        try:
            while user_input.strip().lower() != "q":
                user_input = input("Please give the command to send: ")
                self.logger.info(f"Giving the command: {user_input}")
                output = self.serial.send_command_to_serial(user_input, return_output=True)
                self.logger.info(f"Received output: {output}")
        except KeyboardInterrupt:
            self.logger.info("User terminated the program by using KeyboardInterrupt.")
        finally:
            self.logger.info("Closing the application")
            

    def help(self):
        self.logger.info("To use this client, set the wanted serial bus by typing it out. If you do not wish to set it,"
                         "just press ENTER (it will be /dev/ttyUSB2 by default).\nAfter that, you can simply give the command"
                         "by typing it out.\n\nYou can quit the program by giving the character q as input.\n"
                         "Logs from the session will be saved to serial_comms.log in this directory. "
                         "(../ConnectiCar/RaspberryPiScripts/)")
    
    @staticmethod
    def set_logger():
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(message)s",
            handlers=[logging.FileHandler("serial_comms.log"), logging.StreamHandler(sys.stdout)],
            force=True  # any existing handlers attached to root logger will be closed
        )


if __name__ == "__main__":
    testing_client = TestingClient()
    testing_client.perform_communications()