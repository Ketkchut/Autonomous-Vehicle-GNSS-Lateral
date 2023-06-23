import time
from numpy import angle
import math  
import serial
import pynmea2
import utm 
import csv
import can
import os

#====== Port conection =============
port1 = "COM28"                                 #port usb that connect rover in your computer for gnss f9p
# port2 = "COM17"                                 #port usb that connect steering rs232
ser = serial.Serial(port1, baudrate = 115200)    
# ser2 = serial.Serial(
#     port2, 
#     baudrate = 115200,
#     parity = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     bytesize = serial.EIGHTBITS
# )
# ser2.isOpen()\
    
os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 250000')
os.system("sudo ifconfig can0 txqueuelen 250000")
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
can0.send(msg_init)
# time.sleep(1)

print("Message sent on Enable state data: {}".format(msg_init)) 

#======Param variable ==============
WAYPOINTS_file = 'refLinear_utm.csv'            #put file record waypoint that reference for tracking 
L = 1.68                                        #m wheel base of vehicle
Kp = 52                                         #best tune in linear waypoint kp ki kd == 50 0.21 18
Ki = 0.21                                       #best tune in linear_Curve waypoint kp ki kd == 
Kd = 18                                                                                                                                                                                                                                                   #not tune
sum_error_cte=0
prev_error_cte=0
error_positive_negative=0
yaw_expect=0
yaw_control =0
#=====================================================================================================#
def cte_current(x_car,y_car,A,B,c):
    cross_track_error = abs((A*x_car)+(B*y_car)+c)/math.sqrt(A**2+B**2)
    return cross_track_error

def cte_positive_negative(y_east,error_cte):
    r = y_east
   
    global error_positive_negative,cte_previous
    cte_previous = error_positive_negative
    if y_east >= 661486.90607257 and  y_east <= 661488.9361700793 :      #cte range 0.77m -1.226195m
        error_positive_negative = error_cte
    elif y_east<= 661486.7770239009 and y_east >=  661485.0655856021:    #cte 0.85m - -1.283984 m
        error_positive_negative = (-1)*error_cte
    else:
        error_positive_negative = error_cte
    return error_positive_negative

def Previous_state():
    
    return cte_previous

def pid_angle(cte_p_n,cte_prev):
    global sum_error_cte
    global yaw_expect,prev_error_cte,yaw_previous
    yaw_previous = yaw_expect
    sum_error_cte += cte_p_n 
    #=============================                         #error range [-1.28,1.28] yaw output [-300,300] so gain [-234,234]
    P = Kp*cte_p_n
    I = Ki*sum_error_cte
    D = Kd*((cte_p_n-cte_prev))
    yaw_expect = -1*(P+D+I)
    
    
    return yaw_expect

def Control(self):
    
    # os.system('sudo ifconfig can0 down')
    # os.system('sudo ip link set can0 type can bitrate 250000')
    # os.system("sudo ifconfig can0 txqueuelen 250000")
    # os.system('sudo ifconfig can0 up')

    # self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
    # self.msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
    # self.can0.send(self.msg_init)
    # # time.sleep(1)

    # print("Message sent on Enable state data: {}".format(self.msg_init)) 
         
    while not self.can0.shutdown():
        print("Angle_sent: %s",self.agn)         
        self.Sent(self.agn)

def Sent(self,msg):                                       

    self.elec_angle_dec = self.agn*27
    # rospy.loginfo("Electrical angle (Dec) = ",self.elec_angle_dec)

    self.elec_angle_hex = ('{:0>8X}'.format(int(self.elec_angle_dec) & (2**32-1)))       #i = 45 = 45*27 = 1215, --> data = 000004BF(hex)
    #print('Electrical Angle (Hex) = ',self.elec_angle_hex)
    
    DATA_Hh = ((int(self.elec_angle_hex[0:2],16))) #0x00 #0xFF
    DATA_Hl = ((int(self.elec_angle_hex[2:4],16))) #0x00 #0xFF
    DATA_Lh = ((int(self.elec_angle_hex[4:6],16)))
    DATA_Ll = ((int(self.elec_angle_hex[6:8],16)))

    #print("Electrical Angle (Dec of 2 Byte Hex Data low) = : ",(DATA_Lh), (DATA_Ll), (DATA_Hh), (DATA_Hl))

    self.msg_sent = can.Message(arbitration_id=0x06000001, data=[0x23, 0x02, 0x20, 0x01, (DATA_Lh), (DATA_Ll), (DATA_Hh), (DATA_Hl)])
    print("Message sent on data frame: %s",self.msg_sent)
    self.can0.send(self.msg_sent)     

# def steer_input(steer):
#     out = ''
#     angle = steer*27 #27 from degree angle *( 10000 rpm/360 degree )  กำหนดช่วงมุมเลี้ยว decimal min20,max300 to  [] degree
#     if angle == 'exit' :
#         ser2.close()
#         exit()
#     else :
#         data = ("acec21"+'{:0>8X}'.format(int(angle) & (2**32-1)))
#         sumCheck = hex(sum(int(str(data[i:i+2]),base = 16) for i in range(0, len(data), 2)))[3:]
#         ser2.write(bytearray.fromhex((data+sumCheck).lower()))
#         # time.sleep(1)
#         while ser2.inWaiting() > 0:
#             output = ser2.read(1)
#             out += str(output.hex())
#         if out != '':
#             print(out)
 
def Previous_state_yaw():
    
    return yaw_previous

def angle_controlMotor(cte_pos_neg,yaw_expect,yaw_prev):
    global yaw_control 
    if cte_pos_neg > 0.05 :
        yaw = abs(yaw_expect - yaw_prev)
        if yaw >= 0.25:
            yaw_control = yaw_expect
       

    elif cte_pos_neg < -0.05:
        yaw = abs(yaw_expect - yaw_prev)
        if yaw >= 0.25:
            yaw_control = yaw_expect
       
    # else:
    #     yaw_control = 5 
                                       #cte + left side yaw -   and cte - right side yaw +
    return yaw_control

if __name__ == '__main__':
    #=============Serial position from rover =================================
    while True:
        data = ser.readline()                           #output = b'$GNGGA,173534.70,1339.04546,N,10029.60344,E,1,12,0.56,6.3,M,-27.8,M,,*63\r\n'
        gngga_data = data.split(b",")
        if gngga_data[0] == b"$GNGGA":
            newmsg=pynmea2.parse(data.decode("utf-8"))
            lat=newmsg.latitude                         #get data from gnss is latitude and longtitude
            lng=newmsg.longitude
            gps = lat,lng
            xy = utm.from_latlon(lat,lng)               #convert data lat lng to utm-xy 
            x_north = xy[1]                             #for check cte 
            y_east = xy[0]                              #for track forward linear
            utem_position = x_north,y_east              #forward move in x-axis north data is decease , check error on y-axis east
            x_North_track = x_north
            y_east_track = y_east +0.42
    #===========================================================================
            # start_time = time.time()                    #บอกเวลา
            # print("time : ", (time.time()-start_time)*1000) #unit = millisecond ไว้บอกเวลาที่ใช้ไปทั้งหมด
    #=== import file path reference to compute====================
            # a,b,c =  -0.004432,-1,668177.730316                     #receive param linear eqaution of path ref
            a,b,c = 0.000831,-1, 660233.630317                        #จาก CalFromCSV_new.py --> Linear equation
            # #cal CTE
            error_current = cte_current(x_North_track,y_east_track,a,b,c)
            cte_pos_neg = cte_positive_negative(y_east_track,error_current)    #data can tell cte + - 
    # # store data previous
            cte_prev = Previous_state()
    # #Cal yaw angle that expect from PID controller
            yaw_expect = pid_angle(cte_pos_neg,cte_prev)
            yaw_prev = Previous_state_yaw()
            yaw_controlSteering = angle_controlMotor(cte_pos_neg,yaw_expect,yaw_prev)
            #print(cte_pos_neg,yaw_controlSteering)

            #======= For write data to file CSV ========================
            #======= For write data to file CSV ========================
            Data1= cte_pos_neg,yaw_controlSteering
            data_positioning1 =x_North_track,y_east_track
            with open('center_CteYaw.csv', 'a', newline='') as f:  
                writer = csv.writer(f,delimiter=",")    
                writer.writerow(Data1) 
            with open('center_latlng.csv', 'a', newline='') as f:  
                writer = csv.writer(f,delimiter=",")    
                writer.writerow(gps) 
            with open('center_utm.csv', 'a', newline='') as f:  
                writer = csv.writer(f,delimiter=",")    
                writer.writerow(data_positioning1) 

    # #===========input data yaw angle (degree) for control Steering Motor=============
            
            Control(yaw_controlSteering)
            

           