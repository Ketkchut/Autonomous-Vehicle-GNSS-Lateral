import os
import time
import can

print(os.name)
os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 250000')
os.system("sudo ifconfig can0 txqueuelen 250000")
os.system('sudo ifconfig can0 up')

bustype = 'socketcan'
channel = 'can0'

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
can0.send(msg_init)

# time.sleep(2)
print("Message sent on Enable state data: {}".format(msg_init))


def steer_input(steer):
    # msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
    # can0.send(msg_init)
    # time.sleep(1)
    # print("Message sent on Enable state data: {}".format(msg_init.data[4:]))

    angle = int(steer)*27  
    print("Actual Angle = ",int(steer))
    print("Electrical angle (Dec) =",angle)

    data_sent = ('{:0>8X}'.format(int(angle) & (2**32-1)))       #i = 45 = 45*27 = 1215, --> data = 000004BF(hex)
    print('Electrical Angle (Hex) = ',data_sent)
    
    DATA_Hh = ((int(data_sent[0:2],16)))
    DATA_Hl = ((int(data_sent[2:4],16)))
    DATA_Lh = ((int(data_sent[4:6],16)))
    DATA_Ll = ((int(data_sent[6:8],16)))
    

    msg_sent = can.Message(arbitration_id=0x06000001, data=[0x23, 0x02, 0x20, 0x01, (DATA_Lh), (DATA_Ll), (DATA_Hh), (DATA_Hl)])
    print("Message sent on data frame: ",(msg_sent))
    can0.send(msg_sent) 
    # time.sleep(1)
    receive()

    #query()

def receive():

    msg_re = can0.recv()
    print("Message receive on data frame: ",(msg_re))

def query():
    msg_q = can.Message(arbitration_id=0x06000001, data=[0x40, 0x04, 0x21, 0x01, 0x00 ,0x00 ,0x00 , 0x00])
    print("Message Encoder Query sent : {}".format(msg_q))
    can0.send(msg_q)
    time.sleep(1)
    msg_q = can0.recv(1)
    print("Return Query Message = ",msg_q) 

# if __name__ == '__main__':
#     print("Hello")
#     for i in range(0,380,10):
#         steer_input(i)
#         time.sleep(1) 

def show(i):
    print('angle now = ',i)
    time.sleep(1)

def count_steering(count):
    for count in range (0, 1, 1):
        print('current count = ',count)   
         
        if count == 0:
            print("count = ",count)
            for i in range(0,110,10): #(0,-400,-40)
                steer_input(i)

                if i == 0:           #-360
                    count = 1
                show(i)
                    
        # if count == 1:
        #     print("count = ",count)
        #     for i in range(-200,0,40):  #(-400,0,40)
        #         steer_input(i)

        #         if i == -40:            #-40
        #             count = 2
        #         show(i)

        # if count == 2:
        #     print("count = ",count)
        #     for i in range(-40,200,40): #(-40,400,40)
        #         steer_input(i)

        #         if i == 160:            #360
        #             count = 3
        #         show(i)

        # if count == 3:
        #     print("count = ",count)
        #     for i in range(200,-40,-40):    #(400,-40,-40)
        #         steer_input(i)

        #         if i == 0:
        #             count = 4
        #         show(i)
    

if __name__ == '__main__':  
    # for count in range (0, 4, 1):
    count = 0     
    count_steering(count)


    
            # if (800 < data_rec < 1000 or 0 < data_rec < 200):
            #     count = count +1
            #     print('count = ',count)
            

            #     if (data_rec_prev < data_rec < 1000 or 0 < data_rec < data_rec_prev):
            #         count = count
            #         print('count = ',count)


            # if (data_rec > data_rec_prev):
            #     cal_rec_angle()
            
            # if (data_rec < data_rec_prev):
            #     data_rec = data_rec + 1000
            #     cal_rec_angle()