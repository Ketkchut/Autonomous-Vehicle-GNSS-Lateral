#!/usr/bin/env python3
import serial
import pynmea2
import utm
import csv
import rospy                                 
from std_msgs.msg import Float64MultiArray     

class main(object):
    
    def __init__(self):
        
        # GNSS Function
        self.start = 0
        self.raw_lat = 0.0
        self.raw_lng = 0.0
        self.time_hr = 0.0
        self.time_min = 0.0
        self.time_sec = 0.0
        self.quality = 0 
        self.time_start = 0.0
        self.time_operate = 0.0

        #StreamingMovingAverage Funtion
        self.window_size = 1       
        self.lat_buffer = []
        self.sum_lat = 0.0
        self.latitude = 0.0
        self.lng_buffer = []
        self.sum_lng = 0.0
        self.longitude = 0.0

        #UTMconvert Function
        self.utm_frame = []
        self.x_east = 0.0
        self.y_north = 0.0
        self.utm_position = []

        # CreateCSV Function
        self.value = []
        self.name = 'Data Column Name'
        self.column = 0
        self.csv_name = 0
        self.Data = []

        self.Rt_xy_pub = rospy.Publisher('Realtime_XY',Float64MultiArray,queue_size=10)    
        self.Time_lat_lon_Pub = rospy.Publisher('Time_Lat_Lon',Float64MultiArray,queue_size=10)      
       
        while True:
            self.GNSS()

    def GNSS(self):
        GNSS_frame = sercfg.readline()
        GNSS_buffer = GNSS_frame.split(b",")

        if GNSS_buffer[0] == b"$GNGGA":
            # print(GNSS_buffer)
            newmsg=pynmea2.parse(GNSS_frame.decode("utf-8"))
            self.raw_lat = newmsg.latitude
            self.raw_lng = newmsg.longitude
            self.time_hr = newmsg.timestamp.hour
            self.time_min = newmsg.timestamp.minute
            self.time_sec = newmsg.timestamp.second + newmsg.timestamp.microsecond/1000000
            self.quality = newmsg.gps_qual
                    
            if (self.quality == 4)or(self.quality == 5):
                self.StreamingMovingAverage()
                self.UTMconvert()
                if (self.latitude > 0.0)&(self.longitude > 0.0)&(self.x_east > 0.0)&(self.y_north > 0.0):
                    
                    if self.start == 0:
                        self.time_start = (self.time_min*60) + self.time_sec
                        self.start = 1
                    
                    if self.start == 1:
                        self.time_operate = round((self.time_min*60) + self.time_sec - self.time_start,2)
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

        self.utm_frame = utm.from_latlon(self.latitude,self.longitude)
        self.x_east = self.utm_frame[0]
        self.y_north = self.utm_frame[1]
        self.utm_position = self.x_east,self.y_north        
   
    def Talker(self):
    
        rospy.loginfo("Localization Nodes")
        Realtime_xy = Float64MultiArray()           
        Realtime_xy.data = [self.time_operate ,self.x_east,self.y_north]
        self.Rt_xy_pub.publish(Realtime_xy)           
        rospy.loginfo('Publishing RT XY : %s',Realtime_xy.data)               

        Time_lat_lon = Float64MultiArray()
        Time_lat_lon.data = [self.time_hr ,self.time_min ,self.time_sec ,self.latitude ,self.longitude ,self.raw_lat ,self.raw_lng]
        self.Time_lat_lon_Pub.publish(Time_lat_lon)
        rospy.loginfo('Pubilshing Times Lat/Lon : %s',Time_lat_lon.data) 
            
    def CreateCSV(self):

        self.value = self.time_operate , self.x_east , self.y_north , self.latitude , self.longitude
        self.name = 'time_operate,self.x_east,self.y_north,self.latitude,self.longitude'

        if self.time_operate <= 40 :

            name = 'test.csv'     #change name csv
            
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

        if self.time_operate > 40 :
            print("Stop...")            

if __name__ == '__main__':

    port = "/dev/ttyUSB4"
    
    sercfg = serial.Serial(port ,baudrate = 115200)

    rospy.init_node('Localization',anonymous=True)  
    try:
        cls = main()                       
    except rospy.ROSInterruptException:
        pass                                      