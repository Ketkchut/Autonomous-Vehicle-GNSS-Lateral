import time
from numpy import angle
import math  
import serial
import pynmea2
import utm 
import csv

#====== Port conection =============
port1 = "COM27"                                 #port usb that connect rover in your computer for gnss f9p
port2 = "COM17"                                 #port usb that connect steering rs232
ser = serial.Serial(port1, baudrate = 115200)    
ser2 = serial.Serial(
    port2, 
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
)
ser2.isOpen()
#======Param variable Constant  ==============
#WAYPOINTS_file = 'refLinear_utm.csv'            #put file record waypoint that reference for tracking 
L = 1.68                                        #m wheel base of vehicle
Kp = 54                                         #best tune in linear waypoint kp ki kd == 50 0.21 18
Ki = 0.16                                       #best tune in linear_Curve waypoint kp ki kd == 
Kd = 24                                                                                                                                                                                                                                                   #not tune
sum_error_cte=0
prev_error_cte=0
error_positive_negative=0
yaw_expect=0
yaw_control =0
#=====================================================================================================#
def select_axisTracking(y_east ):
    if y_east < 661494.88:              #tracking on north axis value-- // east axis tell error
        y_east_track = y_east +0.42
        x_north_track = x_north
    elif y_east >  661494.88:           #tracking on east axis value ++ // north axis tell error 
        x_north_track = x_north +0.42
        y_east_track  = y_east

    return x_north_track,y_east_track

def select_linearEquation(x_north,y_east):
    global a,b,c
    a1,b1,c1 =  -0.0015632756, -1, 663847.0633094484       # linear1 52m -0.0015632756107706199 -1 663847.0633094484
    a2,b2,c2 =  -0.1754903706, -1, 926407.5688121466       ##linear with Curve1 equation of Curve 6.918949 m  -0.1754903706433879 -1 926407.5688121466
    a3,b3,c3 =  -0.9479336077, -1 ,2092481.2061952758      ##linear with Curve2 equation of Curve 7.122931 m -0.9479336077039751 -1 2092481.2061952758
    a4,b4,c4 =  0.006923016, -1 ,1505006.8807523265        #linear2   distance4 is 23.908760 m on east-axis define y1509586.450772019, x661496.8112426052 //0.00692301632478863 -1 1505006.8807523265
    
     #cal CTE Condition to select linear Equation
    if x_north <= 1509653.4323676503 and x_north  >= 1509602.340385789 and y_east < 661494.6837220492:       #car on linear1 move on north to sourth
        a,b,c = a1,b1,c1
        #print("chose 1 linear a1b1c1")
                
        #     ##Curve1##  start min (1509602.0818160048, 661487.0682533941)  stop max (1509591.2600646394, 661487.3151340398) // left 
    elif x_north  <= 1509602.1929960449 and x_north >=1509591.2600646394 and y_east <  661494.6837220492:       #car on linear1 move on north to sourth
        a,b,c = a2,b2,c2
        #print("chose 2 linear a2b2c2")
               
            #     ##Curve2##  max n to s(1509586.3371194396, 661487.3273840717) // on east start (1509586.4012525694, 661494.7559586521)
    elif x_north  <= 1509593.9769328258  and y_east <= 661494.2937220492:       #car on linear1 move on north to sourth
        a,b,c = a3,b3,c3
        #print("chose 3 linear a3b3c3")      

    elif  y_east> 661494.2998645048 and y_east <= 661518.5924456262: 
        a,b,c = a4,b4,c4
        #print("chose 4 linear a4b4c4")       
    return a,b,c

def cte_current(x_car,y_car,A,B,c):
    acceprtable_error = 0
    #661462.5360375226  :left +20 |centor : 661442.5360375226 |right -20: 661422.5360375226 ///ให้ช่วงนี้ทั้งหมด เป็น error =0
    if y_car< 661494.8837220492:
        error_track = abs((A*x_car)+(B*y_car)+c)/math.sqrt(A**2+B**2)
        
        if error_track<=0.10 and error_track >=0:
             error_track = acceprtable_error
             cross_track_error = error_track
        elif error_track <=0 and error_track >= -0.10:
             error_track = acceprtable_error
             cross_track_error = error_track
        else:
            cross_track_error = error_track

    elif y_car >= 661495.29:
        error_track = abs((A*y_car)+(B*x_car)+c)/math.sqrt(A**2+B**2)
        if error_track<=0.10 and error_track >=0:
             error_track = acceprtable_error
             cross_track_error = error_track
        elif error_track <=0 and error_track >= -0.10:
             error_track = acceprtable_error
             cross_track_error = error_track
        else:
            cross_track_error = error_track


    return cross_track_error

def cte_positive_negative(x_north,y_east,error_cte):
    global error_positive_negative,cte_previous
    cte_previous = error_positive_negative
    if y_east< 661494.8837220492:   #line1 curve 2 3
    #661489.0820793596,2.000646527027915 max error left
    #661484.698672817,2.3731407447625616 max error right 
        if y_east >= 661486.9281903153 and  y_east <= 661489.9361700793 :      
            error_positive_negative = error_cte     # max 661489.0821927758
        elif y_east<= 661486.9181903153 and y_east >=  661483.0655856021:    
            error_positive_negative = (-1)*error_cte   #min 486  max 661484.8694737963,
       
    if y_east> 661494.2937220492:   #line4
        if x_north >= 1509586.42046655 and x_north <= 1509588.4626106732 :      
            error_positive_negative = error_cte     # max 1509588.4626106732,661514.4671315048
        elif x_north<= 1509586.41046655 and x_north >=  1509582.8302920405:    
            error_positive_negative = (-1)*error_cte   #min 1509582.8302920405,661525.0501996374
        

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

def steer_input(steer):
    out = ''
    angle = steer*27 #27 from degree angle *( 10000 rpm/360 degree )  กำหนดช่วงมุมเลี้ยว decimal min20,max300 to  [] degree
    angle_steer = angle  #degree of yaw 
    if angle == 'exit' :
        ser2.close()
        exit()
    else :
        data = ("acec21"+'{:0>8X}'.format(int(angle) & (2**32-1)))
        sumCheck = hex(sum(int(str(data[i:i+2]),base = 16) for i in range(0, len(data), 2)))[3:]
        ser2.write(bytearray.fromhex((data+sumCheck).lower()))
        # time.sleep(1)
        while ser2.inWaiting() > 0:
            output = ser2.read(1)
            out += str(output.hex())
        if out != '':
            print(out)

    return angle_steer

def Previous_state_yaw():
    
    return yaw_previous

def angle_controlMotor(x_north,y_east,cte_pos_neg,yaw_expect,yaw_prev):
    global yaw_control        #cte + left side yaw -   and cte - right side yaw +
    if y_east < 661494.88 and x_north > 1509600.9766701984: #track control on linear1
        if cte_pos_neg > 0.05 :
            yaw = abs(yaw_expect - yaw_prev)
            if yaw >= 0.25:
                yaw_control = yaw_expect
        elif cte_pos_neg < -0.05:
            yaw = abs(yaw_expect - yaw_prev)
            if yaw >= 0.25:
                yaw_control = yaw_expect

    return yaw_control



#==============================================================================
if __name__ == '__main__':
     #=============Serial position from rover =================================
    while True:
        data = ser.readline()                           #output = b'$GNGGA,173534.70,1339.04546,N,10029.60344,E,1,12,0.56,6.3,M,-27.8,M,,*63\r\n'
        gngga_data = data.split(b",")
        if gngga_data[0] == b"$GNGGA":
            newmsg=pynmea2.parse(data.decode("utf-8"))
            lat=newmsg.latitude                          #get data from gnss is latitude and longtitude
            lng=newmsg.longitude
            gps = lat,lng                               #lat 13.xx lng 100.49xx // 
            xy = utm.from_latlon(lat,lng)               #convert data lat lng to utm-xy 
            x_north = xy[1]                             #for 150xxx
            y_east = xy[0]                              #for track forward linear 661xxx
            utem_position = x_north,y_east              #forward move in x-axis north data is decease , check error on y-axis east
    #===========================================================================
    #==========Selection line Reference for tracking ===========================
            x_north_track,y_east_track = select_axisTracking(y_east )
            a,b,c = select_linearEquation(x_north_track,y_east_track)
    #=============define CTE ==========
            error_current = cte_current(x_north_track,y_east_track,a,b,c)
            cte_pos_neg = cte_positive_negative(x_north_track,y_east_track,error_current)

    # # store data previous
            cte_prev = Previous_state()
    #=========Cal yaw angle that expect from PID controller=============
            yaw_expect = pid_angle(cte_pos_neg,cte_prev)
            yaw_prev = Previous_state_yaw()
            yaw_controlSteering = angle_controlMotor(x_north_track,y_east_track,cte_pos_neg,yaw_expect,yaw_prev)
             
    #===========input data yaw angle (degree) for control Steering Motor=============
            
            steer_input(yaw_controlSteering)
            # if y_east_track <= 661494.20 and x_north_track <= 1509600.97:
            #         for yaw_controlSteering in range(0,140,15):
            #             steer_input(yaw_controlSteering)
            #             time.sleep(0.5)  
            # elif y_east_track >= 661494.20 and x_north_track <= 1509587.97:
            #      steer_input(yaw_controlSteering)
            #      print("drive on linear2")
                        
            # elif y_east_track >= 661494.30 and x_north_track <= 1509587.97:
            #     steer_input(yaw_controlSteering)
            #(1509586.2283661815, 661494.290787259) start linear 4  
            
             #======= For write data to file CSV ========================
            # Data1= cte_pos_neg,yaw_controlSteering
            # data_positioning1 =x_north_track,y_east_track
            # with open('2_center_CteYaw.csv', 'a', newline='') as f:  
            #     writer = csv.writer(f,delimiter=",")    
            #     writer.writerow(Data1) 
            # with open('2_center_latlng.csv', 'a', newline='') as f:  
            #     writer = csv.writer(f,delimiter=",")    
            #     writer.writerow(gps) 
            # with open('2_center_utm.csv', 'a', newline='') as f:  
            #     writer = csv.writer(f,delimiter=",")    
            #     writer.writerow(data_positioning1) 