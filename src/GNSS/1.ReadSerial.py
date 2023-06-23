import serial
import pynmea2
import utm
import csv
from math import radians, cos, sin, asin, sqrt, atan2, degrees

class main(object):
    
    def __init__(self):
        
        self.raw_lat = 0.0
        self.raw_lng = 0.0
        self.time = 0.0
        self.quality = 0
        
        self.window_size = 3
        self.lat_buffer = []
        self.sum_lat = 0.0
        
        self.lng_buffer = []
        self.sum_lng = 0.0
        
        self.latitude = 0.0
        self.longitude = 0.0
        
        self.raw_x_east = 0.0
        self.raw_y_north = 0.0
        self.raw_xy = []
        
        self.x_east = 0.0
        self.y_north = 0.0
        self.xy = []
        
        self.csv_name = 0
        self.Data = []
        
        self.start = 1
        
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
                if (self.latitude > 0.0)&(self.longitude > 0.0):
                    
                    if self.start == 1:
                        self.time_start = (self.time_min*60) + self.time_sec
                        self.start = 0  
                    
                    if self.start == 0:
                        self.time_operate = round((self.time_min*60) + self.time_sec - self.time_start,2)           
                        self.CreateCSV()
               
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

    def CreateCSV(self):

        self.value = self.time_operate , self.x_east , self.y_north , self.latitude , self.longitude
        self.name = 'time_operate,self.x_east,self.y_north,self.latitude,self.longitude'
        
        # name = 'C4_S7_MAXLEFT_1.csv'
        
        # name = 'C4_S7_REF_1.csv'
        
        name = 'Test.csv' 
        
        if self.time_operate <= 1000 :
            
            if self.csv_name == 0:

                for i in range(len(self.name.split(','))):
                        self.Data.append(self.name.split(',self.')[i])
                print(self.Data)
                    
                with open(name, 'a',newline='') as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow(self.Data) 
                    self.csv_name = 1    
                
            if self.csv_name == 1:
                
                self.Data = self.value  
                print(self.Data)    
                
                with open(name, 'a',newline='') as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow(self.Data) 
                    self.csv_name = 1
                    
        if self.time_operate > 1000 :
            print("Finished...")             
   
if __name__ == '__main__':
    
    port = "COM6"     #port usb that connect rover in your computer
    sercfg = serial.Serial(port, baudrate = 115200)
    try:
        cls = main()
    except KeyboardInterrupt:
        print("End program...")
    
    
        
        
    
    
    
    
