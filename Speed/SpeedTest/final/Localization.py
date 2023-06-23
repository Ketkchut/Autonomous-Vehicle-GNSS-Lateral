#!/usr/bin/env python3
import serial
import pynmea2
import utm
import csv
import rospy                                 
from std_msgs.msg import Float64MultiArray     

class main(object):
    
    def __init__(self):
        
        self.raw_lat = 0.0
        self.raw_lng = 0.0
        self.time = 0.0
        self.quality = 0
        
        self.window_size = 10
        self.lat_buffer = []
        self.sum_lat = 0.0
        
        self.lng_buffer = []
        self.sum_lng = 0.0
        
        self.latitude = 0.0
        self.longitude = 0.0
        
        self.Coordinate = []
        
        self.raw_x_east = 0.0
        self.raw_y_north = 0.0
        self.raw_xy = []
        
        self.x_east = 0.0
        self.y_north = 0.0
        self.xy = []

        self.Rt_xy_pub = rospy.Publisher('Realtime_XY',Float64MultiArray,queue_size=10)    
        self.Time_lat_lon_Pub = rospy.Publisher('Time_Lat_Lon',Float64MultiArray,queue_size=10)      
       
        while not rospy.is_shutdown():

            GNSS_frame = sercfg.readline()
            GNSS_buffer = GNSS_frame.split(b",")
            
            if GNSS_buffer[0] == b"$GNGGA":

                newmsg=pynmea2.parse(GNSS_frame.decode("utf-8"))
                self.raw_lat = newmsg.latitude
                self.raw_lng = newmsg.longitude

                self.time_hr = newmsg.timestamp.hour
                self.time_min = newmsg.timestamp.minute
                self.time_sec = newmsg.timestamp.second + newmsg.timestamp.microsecond/1000000

                self.quality =newmsg.gps_qual

                if (self.quality == 4)or(self.quality == 5):
            
                    self.StreamingMovingAverage()
                    self.UTMconvert()

                    if (self.latitude > 0.0)&(self.longitude > 0.0)&(self.x_east > 0.0)&(self.y_north > 0.0):

                        self.Talker()
                        # self.CreateCSV()
                            
    def StreamingMovingAverage(self):
        
        self.lat_buffer.append(self.raw_lat)
        self.sum_lat = self.sum_lat + self.raw_lat
        if len(self.lat_buffer) > self.window_size:
            self.sum_lat = self.sum_lat - self.lat_buffer.pop(0)
            self.latitude = float(self.sum_lat)/len(self.lat_buffer)

        self.lng_buffer.append(self.raw_lng)
        self.sum_lng = self.sum_lng + self.raw_lng
        if len(self.lng_buffer) > self.window_size:
            self.sum_lng = self.sum_lng - self.lng_buffer.pop(0)
            self.longitude = float(self.sum_lng)/len(self.lng_buffer)               
            
    def UTMconvert(self):

        self.raw_xy = utm.from_latlon(self.raw_lat,self.raw_lng)
        self.raw_x_east = self.raw_xy[0]
        self.raw_y_north = self.raw_xy[1]
        
        self.xy = utm.from_latlon(self.latitude,self.longitude)
        self.x_east = self.xy[0]
        self.y_north = self.xy[1]

    def Talker(self):
    
        rospy.loginfo("Localization Nodes")
        Realtime_xy = Float64MultiArray()           
        Realtime_xy.data = [self.x_east,self.y_north,self.raw_x_east,self.raw_y_north]
        self.Rt_xy_pub.publish(Realtime_xy)           
        rospy.loginfo('Publishing RT XY : %s',Realtime_xy.data)               

        Time_lat_lon = Float64MultiArray()
        Time_lat_lon.data = [self.time_hr ,self.time_min ,self.time_sec ,self.latitude ,self.longitude ,self.raw_lat ,self.raw_lng]
        self.Time_lat_lon_Pub.publish(Time_lat_lon)
        rospy.loginfo('Pubilshing Times Lat/Lon : %s',Time_lat_lon.data) 
             
    def CreateCSV(self):
        
        self.Coordinate = self.time , self.raw_lat , self.raw_lng , self.latitude , self.longitude , self.raw_x_east , self.raw_y_north , self.x_east , self.y_north
        print(self.Coordinate)
        with open('ref1_window5_1.csv', 'a',newline='') as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow(self.Coordinate)

           
if __name__ == '__main__':

    port = "/dev/ttyUSB0"
    sercfg = serial.Serial(port ,baudrate = 115200)

    rospy.init_node('Localization',anonymous=True)  
    try:
        cls = main()                       
    except rospy.ROSInterruptException:
        pass                                      