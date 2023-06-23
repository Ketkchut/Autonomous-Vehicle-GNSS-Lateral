##############################################################################

## Description :  This codes is for test two USB2CAN module commuincation
##                one as sender and the other as receiver.
##                sender send  '0,1,2,3,4,5,6'
 
## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.11.30

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                SYstem of RPI       ----------------------  2019-09-26-raspbian-buster-full.img
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)
## Toinstall dependencies:
## sudo pip install python-can


###############################################################################


# import os
# import can

# os.system('sudo ip link set can0 type can bitrate 2500000')
# os.system('sudo ifconfig can0 up')

# can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

# while True:
#     msg = can0.recv(30.0)
#     print (msg)
#     if msg is None:
#         print('No message was received')
    
       
# os.system('sudo ifconfig can0 down')

###############################################################################

# import os
# import can
# import time

# os.system('sudo ifconfig can0 down')
# os.system('sudo ip link set can0 type can bitrate 1000000')
# os.system('sudo ifconfig can0 up')

# can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
# rec_count = 0
# while True:
#     msg = can0.recv(1)
#     print (msg)
#     if msg is None:
#         print('No message was received')
#     else:
#         print(f'Received frame: \n{msg}\n')

# os.system('sudo ifconfig can0 down')

####################################################################

# import os
# import can
# import time

# os.system('sudo ifconfig can0 down')
# os.system('sudo ip link set can0 type can bitrate 1000000')
# os.system('sudo ifconfig can0 up')

# can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
# rec_count = 0
# while True:
#     msg = can0.recv(2.0)
#     print (msg)
#     if msg is None:
#         print('No message was received')
#     else:
#         if (msg.arbitration_id == 0x05800001):
#             rec_count = rec_count + 1
#         else:
#             while True:
#                 print("Get error arbitration_id!!!!!!!!!!!!!!!!!!")
#                 print(msg.arbitration_id)
#                 print("Currecnt rec count:", rec_count)
#                 time.sleep(1)
#     print("Currecnt rec count:", rec_count)
       
# os.system('sudo ifconfig can0 down')
####################################################################################

# import can
# from time import sleep


# def main():
#     can0 = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=250000)

#     try:
#         while True:

#             msg = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00], is_extended_id=False)
#             try:
#                 can0.send(msg)
#                 print("message sent on {}".format(can0.channel_info))
#             except can.CanError:
#                 print("message not sent!")

#             msg = can0.recv(None)
#             try:

#                 if msg.arbitration_id == 0x05800001:
#                     print(msg)

#                 if msg.arbitration_id == 0x07000001:
#                     print(msg)

#                 if msg.arbitration_id == 0x06000001:
#                     print(msg)

#             except AttributeError:
#                 print("Nothing received this time")

#             sleep(0.2)

#     except KeyboardInterrupt:
#         print("Program Exited")
#     except can.CanError:
#         print("Message NOT sent")

#     can0.shutdown()


#     if __name__ == '__main__':
#         main()