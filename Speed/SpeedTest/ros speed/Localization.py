#!/usr/bin/env python3
import rospy                                 
from std_msgs.msg import Float64MultiArray     

def Talker():                              

    Rt_xy_pub = rospy.Publisher('Realtime_XY',Float64MultiArray,queue_size=10)    
    Time_lat_lon_Pub = rospy.Publisher('Time_Lat_Lon',Float64MultiArray,queue_size=10)     

    rate = rospy.Rate(1)                        

    while not rospy.is_shutdown():                 
        rospy.loginfo("Localization Nodes")            

        Realtime_xy = Float64MultiArray()           
        Realtime_x = 10.11111111                  
        Realtime_y = 22.22222222                      
        Realtime_xy.data = [Realtime_x,Realtime_y]     
        Rt_xy_pub.publish(Realtime_xy)           

        rospy.loginfo('Publishing RT XY : %s',Realtime_xy.data)               

        Time_lat_lon = Float64MultiArray()
        Time = 33.300
        Lat = 100.100
        Lon = 200.200
        Time_lat_lon.data = [Time,Lat,Lon]
        Time_lat_lon_Pub.publish(Time_lat_lon)

        rospy.loginfo('Pubilshing Times Lat/Lon : %s',Time_lat_lon.data)

        rate.sleep()                          


if __name__ == '__main__':
    rospy.init_node('Localization',anonymous=True)  
    try:
        Talker()                         
    except rospy.ROSInterruptException:
        pass                                      