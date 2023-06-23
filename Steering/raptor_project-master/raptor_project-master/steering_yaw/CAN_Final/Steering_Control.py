#!/usr/bin/env python
import rospy                                 
from std_msgs.msg import Float64MultiArray,Float64 
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time
import can
import os   

class main(object):         

    def __init__(self):                    
        self.angle_want = 0
        self.angle_now = 0 
        self.angle_step = 0 

        
        # self.agw = 0.0                                
        # self.heading = 0.0                            
        # self.agn = 0.0 

          
                             
        self.Vehecle_Heading = rospy.Publisher('Vehicle_Heading',Float64,queue_size=10)      
        self.Steering_Angle_Now = rospy.Publisher('Steering_Angle_Now',Float64,queue_size=10) 
        
        rospy.Subscriber("Steering_Angle_Want",Float64,self.Steering_Angle_Want_callback)    

        rospy.spin()                         

    def Steering_Angle_Want_callback(self,msg):        
        rospy.loginfo("Steering Control Nodes")        
        rospy.loginfo('Subscribing Angle Want')         
        self.angle_want = msg.data                         
        if self.angle_want != 0:
            self.sent()                    

    def sent(self,msg):                                 

        # self.heading = -10.123                   
        # self.agn = 123.456 
        # self.step = 10 
        self.elec_angle_dec = 0
        self.elec_angle_hex = 0 
        
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
                   
        self.talker()    

    def talker(self):                      

        angle_want = Float64()                      
        angle_now = Float64()                    

        angle_want.data = self.angle_want                
        angle_now.data = self.angle_now               

        rospy.loginfo('Publishing Vehecle Heading : %s',angle_want.data)  
        rospy.loginfo('Publishing Angle Now : %s',angle_now.data)          

        self.Vehecle_Heading.publish(angle_want)       
        self.Steering_Angle_Now.publish(angle_now) 
        
#def Control(self):

if __name__ == '__main__':

    rospy.init_node('Steering_Control',anonymous=True) 

    try:
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
        
        #my_subs = main()

        self.angle_now = 0    #0
        self.angle_want = 110  #-430 = angle heading, angle want
        self.angle_step = 10  #-10          #+,-
        self.round = 1

        while True:

            msg_re = can0.recv()

            if (msg_re.arbitration_id == 117440513)&(self.angle_now <= self.angle_want)&(self.round > 0):           #&(round > 0) ,  counterclockwise direction (+)
                print("Angle_sent ,",self.angle_now,",","Receive ,",msg_re)
                my_subs.sent(self.angle_now)

                data_rec = int.from_bytes(msg_re.data[0:2], byteorder='big', signed=True)           #Data (hex) --> Data (Dec)
                print('data receive = ',data_rec) 
                
                self.angle_now = self.angle_now + self.angle_step

                if (self.angle_now >= self.angle_want):
                    self.round = self.round -1
                    self.angle_now = 0 
 

            if (msg_re.arbitration_id == 117440513)&(self.angle_now >= self.angle_want)&(self.round > 0):           #&(round > 0) ,For clockwise direction (-)
                print("Angle_sent ,",self.angle_now,",","Receive ,",msg_re)
                my_subs.sent(self.angle_now)

                data_rec = int.from_bytes(msg_re.data[0:2], byteorder='big', signed=True)           #Data (hex) --> Data (Dec)
                print('data receive = ',data_rec) 
                
                self.angle_now = self.angle_now + self.angle_step

                if (self.angle_now <= self.angle_want):
                    self.round = self.round -1
                    self.angle_now = 0 

            if self.round == 0:
                break
                     
    except rospy.ROSInterruptException:
        pass                                             