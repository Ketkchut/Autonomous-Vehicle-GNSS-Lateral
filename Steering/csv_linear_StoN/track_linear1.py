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
port1 = '/dev/ttyACM0'                                    #port usb that connect rover in your computer for gnss f9p
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
WAYPOINTS_file = '/home/pond/ros_ws/src/autonomous_pkg/src/tracking/CSV_linear_StoN/ref1_1.csv'  #put file record waypoint that reference for tracking 
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
  

def cte_current(x_car,y_car,A,B,c):
    acceprtable_error = 0
    #661462.5360375226  :left +20 |centor : 661442.5360375226 |right -20: 661422.5360375226 ///ให้ช่วงนี้ทั้งหมด เป็น error =0
    error_track = abs((A*x_car)+(B*y_car)+c)/math.sqrt(A**2+B**2)
    
    if y_car< 661494.6837220492:
        error_track = abs((A*x_car)+(B*y_car)+c)/math.sqrt(A**2+B**2)
        
        if error_track<=0.15 and error_track >=0:
             error_track = acceprtable_error
             cross_track_error = error_track
        elif error_track <=0 and error_track >= -0.15:
             error_track = acceprtable_error
             cross_track_error = error_track
        else:
            cross_track_error = error_track

    elif y_car >= 661494.00:
        error_track = abs((A*y_car)+(B*x_car)+c)/math.sqrt(A**2+B**2)
        if error_track<=0.15 and error_track >=0:
             error_track = acceprtable_error
             cross_track_error = error_track
        elif error_track <=0 and error_track >= -0.15:
             error_track = acceprtable_error
             cross_track_error = error_track
        else:
            cross_track_error = error_track


    return cross_track_error

def cte_positive_negative(y_east,error_cte):
    #661489.0820793596,2.000646527027915 max error left     661480.2636,661489.5472
    #661484.698672817,2.3731407447625616 max error right    661491.436,661489.6863
    global error_positive_negative,cte_previous
    cte_previous = error_positive_negative
    if y_east >= 661486.9281903153 and  y_east <= 661489.9361700793 :      
        error_positive_negative = error_cte     # max 661489.0821927758
    elif y_east<= 661486.9181903153 and y_east >=  661483.0655856021:    
        error_positive_negative = (-1)*error_cte   #min 486  max 661484.8694737963,
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

def Control():
    
    # os.system('sudo ifconfig can0 down')
    # os.system('sudo ip link set can0 type can bitrate 250000')
    # os.system("sudo ifconfig can0 txqueuelen 250000")
    # os.system('sudo ifconfig can0 up')

    # self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
    # self.msg_init = can.Message(arbitration_id=0x06000001, data=[0x23,0x0d,0x20,0x01,0x00,0x00,0x00,0x00])
    # self.can0.send(self.msg_init)
    # # time.sleep(1)

    # print("Message sent on Enable state data: {}".format(self.msg_init)) 
         
    while not can0.shutdown():
        print("Angle_sent: %s",yaw_expect)         
        Sent(yaw_expect)

def Sent(self,agn):                                       

    self.elec_angle_dec = agn*27
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
    can0.send(self.msg_sent)  

# def steer_input(steer):
    # out = ''
    # angle = steer*27 #27 from degree angle *( 10000 rpm/360 degree )  กำหนดช่วงมุมเลี้ยว decimal min20,max300 to  [] degree
    # if angle == 'exit' :
    #     ser2.close()
    #     exit()
    # else :
    #     data = ("acec21"+'{:0>8X}'.format(int(angle) & (2**32-1)))
    #     sumCheck = hex(sum(int(str(data[i:i+2]),base = 16) for i in range(0, len(data), 2)))[3:]
    #     ser2.write(bytearray.fromhex((data+sumCheck).lower()))
    #     # time.sleep(1)
    #     while ser2.inWaiting() > 0:
    #         output = ser2.read(1)
    #         out += str(output.hex())
    #     if out != '':
    #         print(out)
 
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
            utem_position = x_north,y_east              #forward move in x-axis north data is decease , check error on y-axis east
    #===========================================================================
            offset_y_east = y_east +0.42
            utm_position = x_north,offset_y_east
            # start_time = time.time()                    #บอกเวลา
            # print("time : ", (time.time()-start_time)*1000) #unit = millisecond ไว้บอกเวลาที่ใช้ไปทั้งหมด
    #=== import file path reference to compute====================
    # #cal CTE
            a,b,c =  a1,b1,c1 =  -0.0015632756, -1, 663847.0633094484 
           
            error_current = cte_current(x_north,offset_y_east,a,b,c)
            cte_pos_neg = cte_positive_negative(offset_y_east,error_current)
           
            
    # # store data previous
    #         cte_prev = Previous_state()
    # # #Cal yaw angle that expect from PID controller
    #         yaw_expect = pid_angle(cte_pos_neg,cte_prev)
    #         yaw_prev = Previous_state_yaw()
    #         yaw_controlSteering = angle_controlMotor(cte_pos_neg,yaw_expect,yaw_prev)
            #print(cte_pos_neg,yaw_controlSteering)
            # ( 661486.5360375226) จีพีเอสขวาของรถ รถตั้งตรงเส้นกึ่งกลาง ตรงกลาง  +0.42 เพื่อให้gps ค่าอยู่ตรงกลางรถ = 661486.9460375226
            # gps 661486.9281903153 ตั้งตรงเส้นกลางเลย
            #661487.0960375226  :left +0.15 |centor : 661486.9460375226 |right -0.15: 661486.7960375226 ///ให้ช่วงนี้ทั้งหมด เป็น error =0
            #======= For write data to file CSV ========================
            test_see = offset_y_east,cte_pos_neg
            with open('see_dataPrint.csv', 'a', newline='') as f:  
                writer = csv.writer(f,delimiter=",")    
                writer.writerow(test_see) 

    # #===========input data yaw angle (degree) for control Steering Motor=============
            
            #steer_input(yaw_controlSteering)
            

           