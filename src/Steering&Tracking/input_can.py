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
# import time

# #check system name, in linux will print 'posix' and in windows will print 'nt'
# print(os.name)

# #1)Set bitrate and setup CAN device
# os.system('sudo ip link set can0 type can bitrate 250000')
# os.system('sudo ifconfig can0 up')

# #2)Bind the socket to 'can0'
# can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# #3)Assembly data to send
# #                                0x123           0,1,2,3,4,5,6
# msg = can.Message(arbitration_id=0x06000001, data=[0x23, 0x0d, 0x20, 0x01, 0x00, 0x00, 0x00, 0x00])
# can0.send(msg)
# time.sleep(0.01)
# print (msg)

# msg = can.Message(arbitration_id=0x06000001, data=[0x23, 0x02, 0x20, 0x01, 0x03, 0xE7, 0x00, 0x00])

# #4)Send data
# can0.send(msg)
# time.sleep(0.01)
# print (msg) #NOTHING

# # #5)Receive data
# msg = can0.recv(5.0)

# print (msg) #NOTHING

# #6)Close CAN device
# os.system('sudo ifconfig can0 down')


#####################################################################
import os
import can
import time
from ast import literal_eval

#check system name, in linux will print 'posix' and in windows will print 'nt'
print(os.name)

os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 250000')
os.system("sudo ifconfig can0 txqueuelen 250000")
os.system('sudo ifconfig can0 up')
270

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
send_count = 0
recv_count = 0

msg = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])    # Enable
# print("msg = ",msg )
can0.send(msg)
time.sleep(1)
print("Message sent on Enable state data: {}".format(msg.data[4:])) #Message sent on Enable state data bytearray(b'\x00\x00\x00\x00')


# def steer_input(steer):
out = ''
angle = input(">>")       
angle = int(angle)*27 #27 from degree angle *( 10000 rpm/360 degree )  กำหนดช่วงมุมเลี้ยว decimal min20,max300 to  [] degree
                #define min steer 0, max steer 300 if decimal number 
                #งานที่เหลือคือ แมปค่าเลขฐานสิบนั้นให้เป็นองศา

print('angle = ',angle)
if angle > 0 : print('Motor run to counterclockwise')
else: angle < 0, print('Motor run clockwise')

if angle == 'exit' :
    os.system('sudo ifconfig can0 down')
    print('exit')
    exit()

else :
    data = ('{:0>8X}'.format(int(angle) & (2**32-1)))       #i = 45 = 45*27 = 1215, --> data = 000004BF(hex)
    print('pulse(hex) = ',data)
    # print(data[-2:])


    for i in range(0,len(data),2):
        # (hex(int(data[i:i+2],16))) 

        if (hex(int(data[0:2],16))):
            DATA_Hh = ((int(data[0:2],16)))
            # print('DATA_Hh = ',DATA_Hh)
                
        if (hex(int(data[2:4],16))):
            DATA_Hl = ((int(data[2:4],16)))
            # print('DATA_Hl = ',DATA_Hl)

        if  (hex(int(data[4:6],16))):
            DATA_Lh = ((int(data[4:6],16)))
            # print('DATA_Lh = ',DATA_Lh)

        else : (hex(int(data[6:8],16)))
        DATA_Ll = ((int(data[6:8],16)))
            # print('DATA_Ll = ',DATA_Ll)

    msg = can.Message(arbitration_id=0x06000001, data=[0x23, 0x02, 0x20, 0x01, (DATA_Lh), (DATA_Ll), (DATA_Hh), (DATA_Hl)])
    print('send msg: ',msg)
    can0.send(msg) 
    print('rec msg: ',(can0.recv(0.2)))
    time.sleep(1)

# if __name__ == '__main__':
# #     for i in range(0,300,10): #0,600,10 #range max2200
#     while True:
#         steer_input()
    
#         msg1 = can0.recv(1)
#         if msg1 is None:
#             print(f'No message was received: \n{msg1}\n')
#         else:
#             print(f'Received frame: \n{msg1}\n')
#         time.sleep(0.2)
