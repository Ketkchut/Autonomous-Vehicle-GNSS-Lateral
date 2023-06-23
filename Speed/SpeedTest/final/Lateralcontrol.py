#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64MultiArray,Float64
import time

class Mysubscriber(object):
    def __init__(self):
        
        self.x = 0.0
        self.y = 0.0
        self.x_ref = 0.0
        self.y_ref = 0.0
        self.agw = 0.0
        self.CTE = 0.0
        self.forward = 0.0
        self.backward = 0.0
        self.padel = 0.0
        self.Speed_GNSS = 0.0
        self.Speed_PID = 0.0
        
         #Calculate
        self.agn = 0            #0 angle want
        self.agw = 310          #-430 = angle heading, 
        self.ag_step = 10       #-10          #+,-

        
        self.Steering_Angle_want = rospy.Publisher('Steering_Angle_Want',Float64,queue_size=10)
        self.CTE_Pub = rospy.Publisher('CTE',Float64,queue_size=10)
        
        
        # rospy.Subscriber("Realtime_XY",Float64MultiArray,self.Realtime_XY_callback)
        rospy.Subscriber("direction_F",Float64,self.Direction_F_callback)
        rospy.Subscriber("direction_B",Float64,self.Direction_B_callback)
        rospy.Subscriber("direction_P",Float64,self.Direction_P_callback)
        rospy.Subscriber("SpeedGNSS",Float64,self.SpeedGNSS_callback)
        rospy.Subscriber("SpeedPID",Float64,self.SpeedPID_callback)
        
        rate = rospy.Rate(1)
        rospy.spin()
    
    # def Realtime_XY_callback(self,msg):
    #    # rospy.loginfo('Lateral Control Nodes')
    #     self.x = msg.data[0]
    #     self.y = msg.data[1]
    #     #rospy.loginfo('Subscribing Real Time XY')
    #     self.Calculation()
        
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
        
    def Direction_P_callback(self,msg):
        #self.padel = msg.data
        if msg.data >= 1000:
            self.padel = 1
        if msg.data <= 1000:
            self.padel= 0
        self.Input_Speed_Array()  
        
    def SpeedGNSS_callback(self,msg):
         self.Speed_GNSS = msg.data
    
    def SpeedPID_callback(self,msg):
         self.Speed_PID = msg.data
            
    def Input_Speed_Array(self):
         
        Input_Array = Float64MultiArray()
        
        Input_Array.data = [self.Speed_GNSS,self.forward,self.backward,self.padel,self.Speed_PID]
        rospy.loginfo("Car_Input_Dataframe")                        #Print The Order Array
        rospy.loginfo(Input_Array.data)                             #Print Data in Message  
                             
    # def Calculation(self):
  
    #     rospy.loginfo('Lateral Control Nodes')
    #     rospy.loginfo('Subscribing Real Time XY %s',self.xy) 
    #     self.CTE = 123 
        
    #     for self.agn in range(self.agn,self.agw,self.ag_step): #(0,-400,-40)
    #         self.Talker(self.agn)

    #         rospy.loginfo('angle now = %s',self.agn)
    #         time.sleep(1)
            
    def Talker(self):
        
        Angle_want = Float64()
        CTE_valve = Float64()
        
        Angle_want.data = self.agn
        CTE_valve.data = self.CTE
        
        self.Steering_Angle_want.publish(Angle_want)
        self.CTE_Pub.publish(CTE_valve)
        
        rospy.loginfo('Publishing Angle Want : %s',Angle_want.data)
        rospy.loginfo('Publishing CTE : %s',CTE_valve.data)
        
                
        
if __name__ == '__main__':
    rospy.init_node('Lateral_Control',anonymous=True)
    try:
        my_subs = Mysubscriber()
    except rospy.ROSInterruptException:
        pass