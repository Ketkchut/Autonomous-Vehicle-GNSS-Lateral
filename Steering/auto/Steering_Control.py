#!/usr/bin/env python3
import rospy                                 
from std_msgs.msg import Float64MultiArray,Float64    
import os
import time
import can

class main(object):         

    def __init__(self):                     

        #Steering_Angle_Want_callback function    
        self.yaw_control = 0.0                                
                             
        #Control_sent_can function  
        self.angle = 0.0
        self.elec_angle_dec = 0.0
        self.elec_angle_hex = 0.0
        self.DATA_Hh = 0.0
        self.DATA_Hl = 0.0
        self.DATA_Lh = 0.0
        self.DATA_Ll = 0.0
        self.msg_sent = None
        
        rospy.Subscriber("Steering_Angle_Want",Float64,self.Steering_Angle_Want_callback)    
        rospy.spin()                         

    def Steering_Angle_Want_callback(self,msg):        
    
        self.yaw_control = msg.data                   

        self.angle = self.yaw_control

        self.elec_angle_dec = self.angle*27

        self.elec_angle_hex = ('{:0>8X}'.format(int(self.elec_angle_dec) & (2**32-1)))

        self.DATA_Hh = ((int(self.elec_angle_hex[0:2],16)))
        self.DATA_Hl = ((int(self.elec_angle_hex[2:4],16)))
        self.DATA_Lh = ((int(self.elec_angle_hex[4:6],16)))
        self.DATA_Ll = ((int(self.elec_angle_hex[6:8],16)))

        self.msg_sent = can.Message(arbitration_id=0x06000001, data=[0x23,0x02,0x20,0x01,(self.DATA_Lh),(self.DATA_Ll),(self.DATA_Hh),(self.DATA_Hl)])
        can0.send(self.msg_sent)
        print(self.yaw_control)

if __name__ == '__main__':

    rospy.init_node('Steering_Control',anonymous=True)

    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 250000')
    os.system("sudo ifconfig can0 txqueuelen 250000")
    os.system('sudo ifconfig can0 up')
    
    print(os.name)

    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
    msg_init = can.Message( arbitration_id=0x06000001, data= [0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])

    can0.send(msg_init)
    print("Message sent on Enable state data: {}".format(msg_init))   

    try:
        my_subs = main()             
    except rospy.ROSInterruptException:
        pass                                             