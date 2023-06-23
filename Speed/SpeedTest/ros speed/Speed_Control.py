#!/usr/bin/env python3
import rospy                                           #Import python for Ros
from std_msgs.msg import Float64 ,Float64MultiArray    #Import Standard Message type

class main (object):
    
    def __init__(self):
        self.forward = 0.0
        self.backward = 0.0
        self.padel = 0.0
        self.Speed_GNSS = 0.0
        rospy.Subscriber("direction_F",Float64,self.Direction_F_callback)
        rospy.Subscriber("direction_B",Float64,self.Direction_B_callback)
        rospy.Subscriber("direction_P",Float64,self.Direction_P_callback)
        rospy.Subscriber("SpeedGNSS",Float64,self.SpeedGNSS_callback)
         
        rospy.spin()
    
    def Direction_F_callback(self,msg):
        #self.forward = msg.data
        if msg.data >= 1000:
            self.forward = 1
        if msg.data <= 1000:
            self.forward = 0
       
    def Direction_B_callback(self,msg):
        #self.backward = msg.data
        if msg.data >= 1000:
            self.backward = 1
        if msg.data <= 1000:
            self.backward = 0
    
    def SpeedGNSS_callback(self,msg):
         self.Speed_GNSS = msg.data
        
    def Direction_P_callback(self,msg):
        #self.padel = msg.data
        if msg.data >= 1000:
            self.padel = 1
        if msg.data <= 1000:
            self.padel= 0
        self.talker()
        
    def talker(self):
         
        Input_Array = Float64MultiArray()
        
        Input_Array.data = [self.forward,self.backward,self.padel]
        rospy.loginfo("Car_Input_Dataframe")                        #Print The Order Array
        rospy.loginfo(Input_Array.data)                  #Print Data in Message  
                             
if __name__ == '__main__':
    rospy.init_node('Speed_Control_',anonymous=True)         #Create ROS Node "Speed Control"
    try:
        my_sub = main()         #When This Code Run Do The Talker Function 
        
    except rospy.ROSInterruptException:
        pass  
    #When This Code get Interrupt or Ctrl+c Stop Do The Function
    
    
    