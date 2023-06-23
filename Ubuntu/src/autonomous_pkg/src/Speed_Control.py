#!/usr/bin/env python3
import rospy                                           #Import python for Ros
from std_msgs.msg import Float64 ,Float64MultiArray    #Import Standard Message type
import csv 
import time
class main (object):
    
    def __init__(self):

        #Direction_F_callback Function
        self.forward = 0.0

        #Direction_B_callback Function
        self.backward = 0.0

        #Direction_P_callback Function
        self.padel = 0.0

        #velocity_GNSS_callback Function
        self.Speed_time  = 0.0
        self.Speed_velocity = 0.0
        self.Speed_Setpoint = 0.0

        #Speederror_callback Function
        self.Speed_error = 0.0

        #Speederror_callback Function 
        self.Speed_adjust = 0.0

        #CreateCSV Function
        self.value = ()
        self.name = 'Data Column Name'
        self.csv_name = 0
        self.Data = []

        rospy.Subscriber("direction_F",Float64,self.Direction_F_callback)
        rospy.Subscriber("direction_B",Float64,self.Direction_B_callback)
        rospy.Subscriber("direction_P",Float64,self.Direction_P_callback)
        rospy.Subscriber("Speedadjust",Float64,self.Speedadjust_callback)
        rospy.Subscriber("Speederror",Float64,self.Speederror_callback)
        rospy.Subscriber("Velocity",Float64MultiArray,self.velocity_GNSS_callback)

        rospy.spin()
     
    def Direction_F_callback(self,msg):

        if msg.data >= 1000:
            self.forward = 1
        if msg.data < 1000:
            self.forward = 0  
    
    def Direction_B_callback(self,msg):

        if msg.data >= 1000:
            self.backward = 1
        if msg.data < 1000:
            self.backward = 0
     
    def Direction_P_callback(self,msg):

        if msg.data >= 1000:
            self.padel = 1

        if msg.data <=1000:
            self.padel= 0
        
    def velocity_GNSS_callback(self,msg):
        self.Speed_time  = msg.data[0]
        self.Speed_velocity = msg.data[1]
        self.Speed_Setpoint = msg.data[2]

        if self.Speed_time > 0.0:
            self.print()
            # self.CreateCSV()
    
    def Speederror_callback(self,msg):
        self.Speed_error = msg.data

    def Speedadjust_callback(self,msg):
        self.Speed_adjust = msg.data

    def print(self):

        print("Recording..", self.Speed_time ,"||",self.Speed_Setpoint,"||",self.Speed_velocity,"||",self.Speed_adjust,"||",self.Speed_error)

    def CreateCSV(self):

        self.value = self.Speed_time ,self.Speed_velocity ,self.Speed_Setpoint ,self.Speed_adjust ,self.Speed_error

        self.name = 'Speed_time,self.Speed_velocity,self.Speed_Setpoint,self.Speed_adjust,self.Speed_error'

        if self.Speed_time <= 1000 :

            print("Recording..", self.Speed_time ,"||",self.Speed_Setpoint,"||",self.Speed_velocity,"||",self.Speed_adjust,"||",self.Speed_error)

            name = 'speed_fullway_1.csv'     #change name csv
            
            if self.csv_name == 0:

                for i in range(len(self.name.split(','))):
                    self.Data.append(self.name.split(',self.')[i])
                # print(self.Data)

                with open(name, 'a',newline='') as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow(self.Data) 
                    self.csv_name = 1  

            if self.csv_name == 1:
            
                self.Data = self.value  
                # print(self.Data)    
        
                with open(name, 'a',newline='') as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow(self.Data) 
                    self.csv_name = 1                 

        if self.Speed_time > 1000 :
            print("Stop...") 
                   
if __name__ == '__main__':
    rospy.init_node('Speed_Control',anonymous=True)         #Create ROS Node "Speed Control"
    try:
        my_sub = main()         #When This Code Run Do The Talker Function 
        
    except rospy.ROSInterruptException:
        pass  
    #When This Code get Interrupt or Ctrl+c Stop Do The Function
    
    
    