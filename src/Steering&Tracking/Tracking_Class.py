import time
from numpy import angle
import math  
import serial
import pynmea2
import utm 
import csv
import can
import os

class main(object):
    
    def __init__(self) :
        
        # CreateCSV Function
        self.value = []
        self.name = 'Data Column Name'
        self.column = 0
        self.csv_name = 0
        self.Data = []
                
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
        
        #Select_Track Function
        
        self.Track = None
        self.linear = 0
        self.curve = 0
            
        self.reference = 0.0
        self.max_right = 0.0
        self.max_left = 0.0
        
        self.s = 0
        self.a,self.b,self.c    =  0,0,0
        self.aL,self.bL,self.cL    =  0,0,0
        self.aR,self.bR,self.cR    =  0,0,0
        
            #linear S-N
        self.SN1_start = 1509528.36280817
        self.SN1_stop  = 1509583.749          #/
        self.SN1_maxright = 661489.88
        self.SN1_maxleft = 661484.173410818
        self.SN1_ref = 661487.31726504
        self.aSN1,self.bSN1,self.cSN1 = -78.53077, -1, 53456668.62524 

        self.SN2_start = 1509583.7491
        self.SN2_stop  = 1509688.06490994          #/
        self.SN2_maxright = 661489.88
        self.SN2_maxleft = 661484.173410818
        self.SN2_ref = 661486.8775
        self.aSN2,self.bSN2,self.cSN2 = -272.2586713752698, -1, 181605145.8698626 
        
            #curve1 E-W
        self.curve1_s1_start = 1509688.065
        self.curve1_s1_stop = 1509694.17
        self.curve1_s1_maxright = 661488.735
        self.curve1_s1_maxleft = 661482.46       
        self.aL1,self.bL1,self.cL1 = -2.0882352939222786  , -1    , 2891024.6175178257
        self.a1,self.b1,self.c1    =  -3.7748691098637175   , -1    , 4006714.14565129
        self.aR1,self.bR1,self.cR1    =   -4.341614906864185 ,  -1     , 4381619.400890658
                 
        self.curve1_s2_start = 661489.72
        self.curve1_s2_stop = 661480.88
        self.curve1_s2_maxright = 1509700.31
        self.curve1_s2_maxleft = 1509694.17     
        self.aL2,self.bL2,self.cL2 = -0.5649350650366756   , -1    , 1883388.2652620187
        self.a2,self.b2,self.c2    =  -0.6870229007823532   , -1     , 1964150.5048217247 
        self.aR2,self.bR2,self.cR2    =  -0.7342465753199211 ,  -1     , 1995391.7124782377      
        
        self.curve1_s3_start = 661480.90
        self.curve1_s3_stop = 661478.34
        self.curve1_s3_maxright = 1509700.31
        self.curve1_s3_maxleft = 1509694.17     
        self.aL3,self.bL3,self.cL3 = -0.8039215686310316    ,-1     ,2041473.2727474666
        self.a3,self.b3,self.c3    =  -0.3460559796060786   ,-1     ,1738606.9283974625
        self.aR3,self.bR3,self.cR3    =  -0.10139165010069193 ,-1   ,1576768.6405376315    
        

        

                
        #cte_current Function
        self.acceprtable_error = 0
        self.distance = 0.0
        self.error_track = 0.0      
        self.cte = 0.0
        
        #pid angle function
        self.cte_prev = 0.0
        self.sum_error_cte = 0.0
        self.error_cte_prev = 0.0
        self.yaw_prev = 0.0
        self.yaw_expect = 0.0       
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.P = 0.0
        self.I = 0.0
        self.D = 0.0  
        
        #angle controlMotor function
        self.yaw_control = 0.0
        self.yaw = 0.0
        
        #Control_sent_can
        self.angle = 0.0
        self.elec_angle_dec = 0.0
        self.elec_angle_hex = 0.0
        self.DATA_Hh = 0.0
        self.DATA_Hl = 0.0
        self.DATA_Lh = 0.0
        self.DATA_Ll = 0.0
        self.msg_sent = None
        
        
        while True:
            self.GNSS()
            
            
    def GNSS(self):
        
        GNSS_frame = GNSS_ser.readline()
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
                self.StreamingMovingAverage()                                       #Filter Lat/lon
                self.UTMconvert()                                                   #Convert Lat/lon to XY
                
                if (self.latitude > 0.0)&(self.longitude > 0.0)&(self.x_east > 0.0)&(self.y_north > 0.0):
                    
                    if self.start == 0:
                        self.time_start = (self.time_min*60) + self.time_sec
                        self.start = 1 
                    
                    if self.start == 1:
                        self.time_operate = round((self.time_min*60) + self.time_sec - self.time_start,2)

                        self.Select_Track() 
                        
                        self.cte_current()
                        
                        self.pid_angle()
                
                        self.angle_controlMotor()
                         
                        # self.Control_sent_can()
                        print(round(self.x_east,2),'||' ,round(self.y_north,2),'||'  ,self.Track,'||' ,round(self.cte,2),'||' ,round(self.yaw_control,2))
                                
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
   
    def Select_Track(self):
        
        if (self.x_east <= self.SN1_maxright)&(self.x_east >= self.SN1_maxleft) & (self.y_north >= self.SN1_start)&(self.y_north <= self.SN1_stop):
            
            self.Track = 'linear_SN1'
            self.linear = 1
            self.curve = 0
            self.s = 0
            self.a = self.aSN1
            self.b = self.bSN1
            self.c = self.cSN1

            
            self.reference = self.SN1_ref
            self.max_right = self.SN1_maxright
            self.max_left = self.SN1_maxleft 
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 20

        if (self.x_east <= self.SN2_maxright)&(self.x_east >= self.SN2_maxleft) & (self.y_north >= self.SN2_start)&(self.y_north <= self.SN2_stop):
            
            self.Track = 'linear_SN2'
            self.linear = 1
            self.curve = 0
            self.s = 0
            self.a = self.aSN2
            self.b = self.bSN2
            self.c = self.cSN2
            
            self.reference = self.SN2_ref
            self.max_right = self.SN2_maxright
            self.max_left = self.SN2_maxleft 
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 20

        if (self.y_north >= self.curve1_s1_start) & (self.y_north <= self.curve1_s1_stop ) & (self.x_east <= self.curve1_s1_maxright)&(self.x_east >= self.curve1_s1_maxleft):
            
            self.Track = 'Curve1_Set1'
            self.linear = 0
            self.curve = 1
            
            self.s = 1
            self.a = self.a1
            self.b = self.b1
            self.c = self.c1
            
            self.aL = self.aL1
            self.bL = self.bL1
            self.cL = self.cL1
            
            self.aR = self.aR1
            self.bR = self.bR1
            self.cR = self.cR1
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 20
            
        if (self.y_north >= self.curve1_s2_maxleft)&(self.y_north <= self.curve1_s2_maxright) & (self.x_east <= self.curve1_s2_start)&(self.x_east >= self.curve1_s2_stop):
            
            self.Track = 'Curve1_Set2'
            self.linear = 0
            self.curve = 1
            
            self.s = 2
            self.a = self.a2
            self.b = self.b2
            self.c = self.c2
            
            self.aL = self.aL2
            self.bL = self.bL2
            self.cL = self.cL2
            
            self.aR = self.aR2
            self.bR = self.bR2
            self.cR = self.cR2
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 20
            
        if (self.x_east < self.curve1_s3_start)&(self.x_east > self.curve1_s3_stop) & (self.y_north >= self.curve1_s3_maxleft)&(self.y_north <= self.curve1_s3_maxright):
            
            self.Track = 'curve1_set3'
            self.linear = 0
            self.curve = 1
            
            self.s = 3
            self.a = self.a3
            self.b = self.b3
            self.c = self.c3
            
            self.aL = self.aL3
            self.bL = self.bL3 
            self.cL = self.cL3
            
            self.aR = self.aR3
            self.bR = self.bR3
            self.cR = self.cR3
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 20
            
        if (self.x_east <= self.curve1_s3_stop):
            self.Track = 'linear_EW'
            self.linear = 1
            self.curve = 0
 
    def cte_current(self):
        
            self.distance = abs(( self.a * self.x_east ) + ( self.b * self.y_north ) + self.c) / math.sqrt( self.a**2 + self.b**2 )
            
            if (self.linear == 1)&(self.curve == 0):  #for linear
                
                if(self.distance <= 0.15):
                    self.cte = self.acceprtable_error
                
                if(self.distance > 0.15):
                    if (self.x_east >= self.reference) & (self.x_east <= self.max_right):
                        self.cte = self.distance
                        
                    if (self.x_east < self.reference) & (self.x_east >= self.max_left):
                        self.cte = (-1)*self.distance   
                        
              
            if (self.linear == 0)&(self.curve == 1):    #for curve
                
                self.distance_L = abs(( self.aL * self.x_east ) + ( self.bL * self.y_north ) + self.cL) / math.sqrt( self.aL**2 + self.bL**2 )
                self.distance_R = abs(( self.aR * self.x_east ) + ( self.bR * self.y_north ) + self.cR) / math.sqrt( self.aR**2 + self.bR**2 )
                
                if(self.distance <= 0.15):
                    self.cte = self.acceprtable_error      
                    
                if(self.distance > 0.15):
                    if (self.distance_L >= self.distance_R):
                        self.cte = self.distance
                        
                    if (self.distance_R > self.distance_L):
                        self.cte = (-1)*self.distance           
        
    def pid_angle(self):
        
        self.yaw_prev = self.yaw_expect
        self.sum_error_cte += self.cte
        
        self.P = self.kp * self.cte
        self.I = self.ki * self.sum_error_cte
        self.D = self.kd * ((self.cte - self.cte_prev))
        
        self.yaw_expect = (-1)*(self.P + self.I + self.D)

    def angle_controlMotor(self):
        
            if self.cte > 0.15 : 
                self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                if self.yaw >= 0.25:
                    self.yaw_control = abs(self.yaw_expect)
                
            if self.cte < -0.15 :
                self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                if self.yaw >= 0.25:
                    self.yaw_control = -1*(self.yaw_expect)
                
    # def Control_sent_can(self):

    #     self.angle = self.yaw_control

    #     self.elec_angle_dec = self.angle*27

    #     self.elec_angle_hex = ('{:0>8X}'.format(int(self.elec_angle_dec) & (2**32-1)))

    #     self.DATA_Hh = ((int(self.elec_angle_hex[0:2],16)))
    #     self.DATA_Hl = ((int(self.elec_angle_hex[2:4],16)))
    #     self.DATA_Lh = ((int(self.elec_angle_hex[4:6],16)))
    #     self.DATA_Ll = ((int(self.elec_angle_hex[6:8],16)))

    #     self.msg_sent = can.Message(arbitration_id=0x06000001, data=[0x23,0x02,0x20,0x01,(self.DATA_Lh),(self.DATA_Ll),(self.DATA_Hh),(self.DATA_Hl)])
    #     can0.send(self.msg_sent)
    #     time.sleep(0.4)     
        
    def CreateCSV(self):

        self.value = self.time_operate , self.x_east , self.y_north , self.latitude , self.longitude 
        self.name = 'time_operate,self.raw_x_east,self.raw_y_north,self.x_east,self.y_north,self.latitude,self.longitude'
        
        self.csv_name = 'ref1_position_center.csv'
        
        if self.column == 0:

            for i in range(len(self.name.split(','))):
                    self.Data.append(self.name.split(',self.')[i])
            print(self.Data)
                
            with open(self.csv_name, 'a',newline='') as f:
                writer = csv.writer(f,delimiter=",")
                writer.writerow(self.Data) 
                self.column = 1    
            
        if self.column == 1:
            
            self.Data = self.value  
            print(self.Data)    
            
            with open(self.csv_name, 'a',newline='') as f:
                writer = csv.writer(f,delimiter=",")
                writer.writerow(self.Data) 
                self.column = 1                   
            
if __name__ == '__main__':
    
    GNSS_port = "COM6"
    GNSS_ser = serial.Serial(GNSS_port, baudrate = 115200)
    
    # os.system('sudo ifconfig can0 down')
    # os.system('sudo ip link set can0 type can bitrate 250000')
    # os.system("sudo ifconfig can0 txqueuelen 250000")
    # os.system('sudo ifconfig can0 up')
    
    # print(os.name)
    # can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
    # msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
    # can0.send(msg_init)
    # print("Message sent on Enable state data: {}".format(msg_init)) 
    
    try:
        cls = main()
    except KeyboardInterrupt:
        print("End program...")