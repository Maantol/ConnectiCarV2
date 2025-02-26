import can
import cantools
import datetime
import json
import logging
import os
import time
import cantools.database
import cantools.database.namedsignalvalue

_logger = logging.getLogger(__name__)

def create_message_entry(
    message: can.Message,
    db: cantools.database.can.Database,
    args: dict,
    filter_set: set,
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
    database = "toyota_rav4_hybrid_2017_pt_generated.dbc"
    interface = "socketcan"
    channel = "can0"
    delay = 0;

    _start = time.time()
    db = cantools.database.load_file(database)
    bus = can.Bus(channel=channel, interface=interface)

    try:
        while True:
            time.sleep(delay)
            message = bus.recv()
            db_message = db.get_message_by_frame_id(message.arbitration_id)
            print(f"Name: {db_message.name}")
            print(f"Data: {db.decode_message(message.arbitration_id, message.data)}")
            print(f"Encoded: {message}")
    except KeyboardInterrupt:
        _logger.info("Exiting...")
    except IndexError:
        _logger.info("End of data, exiting...")
    finally:
        _logger.info("Closing CAN bus...")
        bus.shutdown()
        _logger.info("Finalizing MQTT data transmissions...")
        _finish = time.time()
        _logger.warning(f"Took {_finish - _start} seconds to run.")
        _end = time.time()
        if _end - _finish > 30:
            _logger.warning(f"Ran {_end - _finish} seconds behind!")
    
if __name__ == "__main__":
    read()
            