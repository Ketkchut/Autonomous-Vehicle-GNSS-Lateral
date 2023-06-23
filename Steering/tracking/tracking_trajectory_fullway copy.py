import time
from numpy import angle
import math  
import serial
import pynmea2
import utm 
import csv 
import pandas as pd 
import numpy as np
import can
import os 

#====== Port conection =============
port1 = "COM38"                                 #port usb that connect rover in your computer for gnss f9p
# port2 = "COM17"                                 #port usb that connect steering rs232
ser = serial.Serial(port1, baudrate = 115200)    
# ser2 = serial.Serial(
#     port2, 
#     baudrate = 115200,
#     parity = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     bytesize = serial.EIGHTBITS
# )
# ser2.isOpen()

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
Ki = 0.18                                       #best tune in linear_Curve waypoint kp ki kd == 
Kd = 18                                                                                                                                                                                                                                                   #not tune
sum_error_cte=0
prev_error_cte=0
error_positive_negative=0
yaw_expect=0
yaw_control =0
#=====================================================================================================#
def cte_current(x_car,y_car,A,B,C):
    cross_track_error = abs((A*x_car)+(B*y_car)+C)/math.sqrt(A**2+B**2)

    return cross_track_error

def cte_positive_negative(y_east,error_cte):
    r = y_east
   #======== Linear North to East =========== move forward on north 150xxx decrease //cte on 661xxx
    global error_positive_negative,cte_previous
    cte_previous = error_positive_negative
    if y_east >= 661486.90607257 and  y_east <= 661488.9361700793 :      #cte range 0.77m -1.226195m
        error_positive_negative = error_cte
    elif y_east<= 661486.7770239009 and y_east >=  661485.0655856021:    #cte 0.85m - -1.283984 m
        error_positive_negative = (-1)*error_cte
    # else:
    #     error_positive_negative = error_cte
    # !! Curve !!
        #======== Linear2 North to east =========== move forward on north 150xxx cte on 661xxx
    if y_east >= 661486.90607257 and  y_east <= 661488.9361700793 :      #cte range 0.77m -1.226195m
        error_positive_negative = error_cte
    elif y_east<= 661486.7770239009 and y_east >=  661485.0655856021:    #cte 0.85m - -1.283984 m
        error_positive_negative = (-1)*error_cte
        #======== Linear3 North to east ===========
    if y_east >= 661486.90607257 and  y_east <= 661488.9361700793 :      #cte range 0.77m -1.226195m
        error_positive_negative = error_cte
    elif y_east<= 661486.7770239009 and y_east >=  661485.0655856021:    #cte 0.85m - -1.283984 m
        error_positive_negative = (-1)*error_cte
    #!!! Curve to linear !!!

    #======== Linear4 west to east =========== move forward on east 660xx increase // cte with north sourth 150xxx
    if y_east >= 1509586.6563329294 and  y_east <= 1509588.8436516593 :      #cte+ range 0.77m -1.226195m
        error_positive_negative = error_cte
    elif y_east<= 1509586.3165312603 and y_east >=  1509584.0089640797:    #cte- 0.85m - -1.283984 m
        error_positive_negative = (-1)*error_cte
        
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
    if cte_pos_neg > 0.15 :
        yaw = abs(yaw_expect - yaw_prev)
        if yaw >= 0.25:
            yaw_control = yaw_expect
       

    elif cte_pos_neg < -0.15:
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
            utem_position = x_north,y_east              #forward move in x-axis north 1509602 data is decease , check error on y-axis east 661487
    #===========================================================================
            # start_time = time.time()                    #บอกเวลา
            # print("time : ", (time.time()-start_time)*1000) #unit = millisecond ไว้บอกเวลาที่ใช้ไปทั้งหมด
    #=== import file path reference to compute====================
            a1,b1,c1 =  0.000731821795835581, -1, 660382.6150047198       # linear1 104.397028m 0.000731821795835581 -1 660382.6150047198
            a2,b2,c2 =  -0.37916030535783524, -1, 1233901.5788868917      # linear with Curve1 equation of Curve 5.604014 m  -0.37916030535783524 -1 1233901.5788868917
            a3,b3,c3 =  -2.0719753086850683, -1, 3789536.8208008595       # linear with Curve2 equation of Curve 5.590628 m -2.0719753086850683 -1 3789536.8208008595
            a4,b4,c4 =  -0.07250141061811229, -1, 1557656.7802278912      # linear2 distance 4 is 44.778426 m on east-axis define start y1509698.767, x661476.9674//-0.07250141061811229 -1 1557656.7802278912
    # #cal CTE Condition to select linear Equation
            if x_north <= 1509653.4323676503 and x_north  >= 1509602.340385789:       #car on linear1 move on north to sourth
                error_current1 = cte_current(x_north,y_east,a1,b1,c1)
                cte_pos_neg = cte_positive_negative(y_east,error_current1)    #data can tell cte + -
    
                ##curve1##  start curve: [343] 1509689.415, 661487.2793 // stop curve:(max left) [362] 1509694.655, 661485.2925
            if x_north  <= 1509689.415 and x_north >= 1509694.655  :       #car on linear1 move on north to sourth
                error_current2 = cte_current(x_north,y_east,a2,b2,c2)
                cte_pos_neg = cte_positive_negative(y_east,error_current2)
                
                ##Curve2##  max n to s(1509586.3371194396, 661487.3273840717) // on east start (1509586.4012525694, 661494.7559586521)
                ##Curve2##  start curve2 [369] 1509695.99, 661484.0059 // stop curve 2 [388] 1509698.42, 661478.971
            
            if x_north  <= 1509689.415 and x_north >= 1509695.99 and y_east <= 661478.971:       #car on linear1 move on north to sourth
                error_current3 = cte_current(x_north,y_east,a3,b3,c3)
                cte_pos_neg = cte_positive_negative(y_east,error_current3)
                
                #start linear2 (y1509698.767, x661476.9674) //stop linear2  (y1509702.005, x661432.3062)
            if y_east <= 661478.971:         # if >y  car that on y_east linear2 forward west to east
                error_current4 = cte_current(x_north,y_east,a4,b4,c4)
                cte_pos_neg = cte_positive_negative(y_east,error_current4)
                
    # # store data previous
            cte_prev = Previous_state()
    # #Cal yaw angle that expect from PID controller
            yaw_expect = pid_angle(cte_pos_neg,cte_prev)
            yaw_prev = Previous_state_yaw()
            yaw_controlSteering = angle_controlMotor(cte_pos_neg,yaw_expect,yaw_prev)
            #print(cte_pos_neg,yaw_controlSteering)

            #======= For write data to file CSV ========================
            test_see = cte_pos_neg,yaw_controlSteering
            with open('see_dataPrint.csv', 'a', newline='') as f:  
                writer = csv.writer(f,delimiter=",")    
                writer.writerow(test_see) 

    # #===========input data yaw angle (degree) for control Steering Motor=============
            
            Control(yaw_controlSteering)
            

           