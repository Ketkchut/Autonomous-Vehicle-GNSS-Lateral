import cantools
from can.message import Message
db = cantools.db.load_file('home/pond/git/pythoncan-examples/python-can-examples/resources/motohawk.dbc')

import can
can0 = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=250000)
while True:
    message = bus.recv()
    print(db.decode_message(message.arbitration_id, message.data))