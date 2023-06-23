#!/usr/bin/env python3
import rospy                              
from std_msgs.msg import Float64MultiArray,Float64,String 

class main(object):      

    def __init__(self):                   
        
        self.time = 0.0
        self.lat = 0.0
        self.lon = 0.0
        self.v = 0.0

        self.Velocity_Pub = rospy.Publisher('Velocity_test',Float64,queue_size=10) 

        rospy.Subscriber("Time_Lat_Lon",Float64MultiArray,self.Time_Lat_Lon_callback)

        rospy.spin()
              

    def Time_Lat_Lon_callback(self,msg):    # change to cal               
        rospy.loginfo('Velocity Calculation Nodes')      

        rospy.loginfo('Subscribing Time Lat/Lon : %s',msg.data)
        self.time = msg.data[0]                             
        self.lat = msg.data[1]                         
        self.lon = msg.data[2]                 
        self.Calculate()                   

    def Calculate(self):                                 
        self.v = self.time + self.lat + self.lon
        self.Talker()                                 

    def Talker(self):          # publish                         

        Velocity_test = Float64()                       
        Velocity_test.data = self.v                        
        self.Velocity_Pub.publish(Velocity_test)               
        rospy.loginfo('Publishing Velocity_test : %s',Velocity_test.data) 


if __name__ == '__main__':
    rospy.init_node('Velocity_Calculation',anonymous=True)  
    try:
        my_subs = main()                           
    except rospy.ROSInterruptException:
        pass  