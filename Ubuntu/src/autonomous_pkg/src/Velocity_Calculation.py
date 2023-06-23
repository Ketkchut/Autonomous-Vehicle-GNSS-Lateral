#!/usr/bin/env python3
import rospy                              
from std_msgs.msg import Float64MultiArray,Float64 
from math import radians, cos, sin, asin, sqrt, atan2, degrees
import csv 

class main(object):      

    def __init__(self):        

        #Speed_Setpoint_callback Funtion
        self.speed_sp = 0.0

        #Time_Lat_Lon_callback Funtion
        self.data = None
        self.time_hr = 0.0
        self.time_min = 0.0
        self.time_sec = 0.0                            
        self.lat = 0.0                        
        self.lon = 0.0
        self.raw_lat = 0.0                        
        self.raw_lon = 0.0
        self.prev_data = None
        self.time_start = 0.0

        #Time_Counter Funtion
        self.time_operate = 0.0

        #Haversine_raw Funtion
        self.now_lat = 0.0
        self.now_lon = 0.0
        self.prev_lat = 0.0
        self.prev_lon = 0.0
        self.dlat = 0.0
        self.dlon = 0.0
        self.distance_km_raw = 0.0
        self.distance_m_raw = 0.0    

        #Movingfilter_raw Function
        self.raw_speed_buffer = []
        self.sum_raw_speed = 0.0
        self.window_size = 20
        self.raw_speed_filter = 0.0

        #Calculate Function
        self.prev_sec = 0.0
        self.now_sec = 0.0
        self.raw_speedms = 0.0
        self.raw_speed = 0.0

        # CreateCSV Function
        self.value = ()
        self.name = 'Data Column Name'
        self.csv_name = 0
        self.Data = []

        self.Velocity_Pub = rospy.Publisher('Velocity',Float64MultiArray,queue_size=10) 
        rospy.Subscriber("Time_Lat_Lon",Float64MultiArray,self.Time_Lat_Lon_callback)
        rospy.Subscriber("Speed_Setpoint",Float64,self.Speed_Setpoint_callback)
        rospy.spin()
              
    def Speed_Setpoint_callback(self,msg):
        self.speed_sp = msg.data

    def Time_Lat_Lon_callback(self,msg):    #For Get Message from Localization Nodes

        self.data = msg.data
        self.time_hr = msg.data[0]
        self.time_min = msg.data[1]
        self.time_sec = msg.data[2]                             
        self.lat = msg.data[3]                         
        self.lon = msg.data[4]
        self.raw_lat = msg.data[5]                         
        self.raw_lon = msg.data[6]

        if self.prev_data is None:

            self.time_start = (self.data[1]*60) + self.data[2]

        if self.prev_data is not None:

            self.Time_Counter()
            self.Haversine_raw()
            self.Calculate()
            self.Talker()
            # self.CreateCSV() 
    
        self.prev_data = msg.data

    def Time_Counter(self):                 #For Count Time Operate

        self.time_operate = round(((self.data[1]*60) + self.data[2]) - self.time_start,2)

    def Haversine_raw(self):                #For Raw Latitude/Longitude

        self.now_lat = self.data[5]
        self.now_lon = self.data[6]

        self.prev_lat = self.prev_data[5]
        self.prev_lon = self.prev_data[6]

        self.now_lat, self.now_lon, self.prev_lat, self.prev_lon = map(radians,[self.now_lat, self.now_lon, self.prev_lat, self.prev_lon])

        self.dlat = self.prev_lat - self.now_lat
        self.dlon = self.prev_lon - self.now_lon

        a = sin(self.dlat/2)**2 + cos(self.now_lat) * cos(self.prev_lat) * sin(self.dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.

        self.distance_km_raw = c*r
        self.distance_m_raw = self.distance_km_raw*1000        

    def Movingfilter_raw(self):             #For Filter Speed after Calculate Function

        self.raw_speed_buffer.append(self.raw_speed)
        self.sum_raw_speed = self.sum_raw_speed + self.raw_speed

        if len(self.raw_speed_buffer) > self.window_size:
            self.sum_raw_speed = self.sum_raw_speed - self.raw_speed_buffer.pop(0)
            self.raw_speed_filter = float(self.sum_raw_speed)/len(self.raw_speed_buffer)
            self.raw_speed_filter = round(self.raw_speed_filter,2)

    def Calculate(self):                    #For Calculate Speed

        self.prev_sec = self.prev_data[2]
        self.now_sec = self.data[2]   

        if self.now_sec > self.prev_sec:

            self.raw_speedms = self.distance_m_raw / (self.now_sec - self.prev_sec)                         #Speed from Raw lat/lon
            self.raw_speed = round(self.raw_speedms*3.6 ,2)
            self.Movingfilter_raw()        

    def Talker(self):                       #For Publish Velocity Data

        Velocity = Float64MultiArray() 
        Velocity.data = [self.time_operate ,self.raw_speed_filter ,self.speed_sp]
        self.Velocity_Pub.publish(Velocity)
        rospy.loginfo('Publishing Velocity : %s',Velocity.data) 

    def CreateCSV(self):

        self.value = self.time_operate , self.raw_speed , self.raw_speed_filter
        self.name = 'time_operate, self.raw_speed, self.raw_speed_filter'

        if self.time_operate <= 40 :

            print("Recording..",self.time_operate ,"Sec. || R = ",self.raw_speed , "|| RF =",self.raw_speed_filter)

            name = 'test_f_100.csv'     #change name csv
            
            if self.csv_name == 0:

                for i in range(len(self.name.split(','))):
                    self.Data.append(self.name.split(', self.')[i])
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
    rospy.init_node('Velocity_Calculation',anonymous=True)  
    try:
        my_subs = main()                           
    except rospy.ROSInterruptException:
        pass                                         
