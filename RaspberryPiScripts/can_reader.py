import can
import cantools
import json
import logging
import time
import cantools.database
import cantools.database.namedsignalvalue
import config as cfg

_logger = logging.getLogger(__name__)
config = cfg.get_config()
database = config["can"]["database"]
interface = config["can"]["interface"]
channel = config["can"]["channel"]
delay = config["can"]["delay"]
db = cantools.database.load_file(database)
bus = can.Bus(channel=channel, interface=interface)

def create_message_entry(
    message: can.Message,
    db: cantools.database.can.Database
) -> dict:
    try:
        db_message = db.get_message_by_frame_id(message.arbitration_id)
        decoded = db.decode_message(message.arbitration_id, message.data)
        _logger.debug(f"{db_message.name}: {decoded}")

        try:
            return {
                "name": db_message.name,
                "timestamp": message.timestamp,
                "id": message.arbitration_id,
                "data": json.dumps(decoded),
                "raw": "0x" + message.data.hex(),
            }
        except TypeError:
            return {
                "name": db_message.name,
                "timestamp": message.timestamp,
                "id": message.arbitration_id,
                "data": f"{decoded}",
                "raw": "0x" + message.data.hex(),
            }
    except KeyError:
        return {
            "name": "Unknown",
            "timestamp": message.timestamp,
            "id": message.arbitration_id,
            "data": message.data.hex(),
            "raw": "0x" + message.data.hex(),
        }


def read():
    time.sleep(delay)
    message = bus.recv()
    # Decode & return CAN data
    return create_message_entry(message, db)
    
if __name__ == "__main__":
    read()
            