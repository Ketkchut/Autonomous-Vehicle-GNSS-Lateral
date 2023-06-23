import cantools
from can.message import Message
db = cantools.db.load_file('home/pond/git/pythoncan-examples/python-can-examples/resources/motohawk.dbc')

#print a particular message in the dbc
msg = db.get_message_by_name('ExampleMessage')
msg_data = msg.encode({'Enable':1,'AverageRadius':1,'Temperature':251})

import can
can0 = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=250000)
msg = can.Message(arbitration_id=msg.frame_id, data=msg_data, is_extended_id=False)
try:
    can0.send(msg)
    print("Message sent on {}".format(can0.channel_info))
except can.CanError:
    print("Message NOT sent")