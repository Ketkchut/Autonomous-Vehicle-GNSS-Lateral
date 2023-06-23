import time
import can
import os
# from panda import Panda

class main(object):

    def __init__(self):

        self.angle_want = 0
        self.elec_angle_dec = 0
        self.elec_angle_hex = 0

    def sent(self,msg):
        
        #print(".....................................")      #for easy reading in terminal
        self.angle_want = msg
        #print("Actual Angle = ",int(self.angle_want))

        self.elec_angle_dec = self.angle_want*27
        #print("Electrical angle (Dec) = ",self.elec_angle_dec)

        self.elec_angle_hex = ('{:0>8X}'.format(int(self.elec_angle_dec) & (2**32-1)))       #i = 45 = 45*27 = 1215, --> data = 000004BF(hex)
        #print('Electrical Angle (Hex) = ',self.elec_angle_hex)
    
        DATA_Hh = ((int(self.elec_angle_hex[0:2],16))) #0x00 #0xFF
        DATA_Hl = ((int(self.elec_angle_hex[2:4],16))) #0x00 #0xFF
        DATA_Lh = ((int(self.elec_angle_hex[4:6],16)))
        DATA_Ll = ((int(self.elec_angle_hex[6:8],16)))

        #print("Electrical Angle (Dec of 2 Byte Hex Data low) = : ",(DATA_Lh), (DATA_Ll), (DATA_Hh), (DATA_Hl))

        msg_sent = can.Message(arbitration_id=0x06000001, data=[0x23, 0x02, 0x20, 0x01, (DATA_Lh), (DATA_Ll), (DATA_Hh), (DATA_Hl)])
        #print("Message sent on data frame: ",(msg_sent))
        can0.send(msg_sent) 
        #time.sleep(1)

def cal_rec_angle():
    data_rec_angle = 0
    delta_data_rec = 0

    delta_data_rec = ((data_rec - data_rec_prev)*(360/1000))
    data_rec_angle = data_rec_angle + delta_data_rec
    print('receive angle = ',data_rec_angle)
          
if __name__ == '__main__':

    print(os.name)
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 250000')
    os.system("sudo ifconfig can0 txqueuelen 250000")
    os.system('sudo ifconfig can0 up')

    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
    msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
    can0.send(msg_init)
    time.sleep(1)
    print("Message sent on Enable state data: {}".format(msg_init))
    
    crl = main()

    angle_now = 390
    angle_max = 0
    angle_step = -10

    angle_receive = 0
    count = 0
    data_rec = 0
    data_rec_prev = 0 
    # delta_data_rec = 0 
    # data_rec_angle = 0 
    round = 1

    while True:

        msg_re = can0.recv()
        
        
        if (msg_re.arbitration_id == 117440513)&(angle_now <= angle_max)&(round > 0):           #For 70 ID = 117440513
            print("Angle_sent ,",angle_now,",","Receive ,",msg_re)
            crl.sent(angle_now)

            print(msg_re.data[0:2]) #bytearray(b'\x02\xd6')
            data_rec = int.from_bytes(msg_re.data[0:2], byteorder='big', signed=True)
            print('data receive = ',data_rec) 

            data_rec_prev = data_rec
            print('data previous = ',data_rec_prev) 

            if (data_rec < data_rec_prev):
                data_rec = data_rec + 1000
                cal_rec_angle()

            if (data_rec > data_rec_prev): 
                cal_rec_angle()
            
            angle_now = angle_now + angle_step
            
            if (angle_now >= angle_max):   
                round = round -1
                angle_now = 0 
            
        if round == 0:
            break