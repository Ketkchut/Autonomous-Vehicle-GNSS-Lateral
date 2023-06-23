import time

import can

from pynput import keyboard

can0 = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=250000)

def on_press(key):
    if key.char == 'a': #handles if key press is shift
        msg = can.Message(arbitration_id==0x06000001, data=[0x23, 0x0d, 0x20, 0x01, 0x00, 0x00, 0x00, 0x00],is_extended_id=False)
        try:
            can0.send(msg)
            print("Message sent on {}".format(cano.channel_info))
        except can.CanError:
            print("Message NOT sent")

    if key.char == 'b': #handles if key press is shift
        msg = can.Message(arbitration_id=0x06000001, data=[0x23, 0x02, 0x20, 0x01, 0x00, 0x00, 0x00, 0x00],is_extended_id=False)
        task.modify_data(msg)

def get_current_key_input():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

msg = can.Message(arbitration_id=0x06000001, data=[x23, 0x0d, 0x20, 0x01, 0x00, 0x00, 0x00, 0x00],is_extended_id=False)
try:
    task = can0.send_periodic(msg, 1)
    print("Message sen on {}".format(can0.channel_info))
except can.CanError:
    print("Message NOT sent")

get_current_key_input()