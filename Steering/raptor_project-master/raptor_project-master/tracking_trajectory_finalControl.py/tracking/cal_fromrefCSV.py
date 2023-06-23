import time
from numpy import angle
import math  
import serial
import pynmea2
import utm 
import pandas as pd
import matplotlib.pyplot as plt   
import numpy as np  
import csv

# port1 = "COM36"                                 #port usb that connect rover in your computer for gnss f9p
# ser = serial.Serial(port1, baudrate = 115200)  
#from module_name import name1  //module_name คือชื่อ module ที่ต้องการ import เข้ามาใช้ ชื่อไฟล .py //name1 คือ ชื่อ funtion ที่อยู่ภายใน module นั้น เรียกกี่ตัวก็ได้
#============Param variable =====
WAYPOINTS_file_linear = 'refLinear_utm.csv'    #put file record waypoint that reference for tracking 
WAYPOINTS_file_linearCurve = 'refLinearCurve_utm.csv'    #y_east linear route forward, x_north calculate cte error from positoion y_east
L = 1.68          #m wheel base of vehicle


def calRef_toLinear():
    #=== load waypoint =============     # lat 13.650680 to utm east 661487.25   // lng  100.493001 to utm north 1509590.43
    n_pointStart =0
    n_pointStop = 88
    waypoints_file = WAYPOINTS_file_linear
    with open (waypoints_file,"r") as f:
        waypoints = pd.read_table(f, sep=',', header=0, names=['x','y'])
        waypoints_np = np.array(waypoints)
    #input waypoint reference 
    x_axiswaypoint_ylngNorth = waypoints.x     #run direct forward in axis
    y_axiswaypoint_xlatEast = waypoints.y
    #print(x_axiswaypoint_ylngNorth[88],x_axiswaypoint_ylngNorth[0])
    Dis = math.sqrt(( x_axiswaypoint_ylngNorth[n_pointStart]- x_axiswaypoint_ylngNorth[ n_pointStop])**2+(y_axiswaypoint_xlatEast[n_pointStart]-y_axiswaypoint_xlatEast[ n_pointStop])**2) #distance point start to stop
    print("value distance is %f" %Dis)  #56.56m
    #find linear equretion
    slop  = (y_axiswaypoint_xlatEast[ n_pointStop]-y_axiswaypoint_xlatEast[n_pointStart])/( x_axiswaypoint_ylngNorth[ n_pointStop]- x_axiswaypoint_ylngNorth[n_pointStart])#find slop of linear equation -147.302103
    print("slop is %f" %slop)
    # find C fo linear equation
    C  = y_axiswaypoint_xlatEast[n_pointStart]-slop* x_axiswaypoint_ylngNorth[n_pointStart]
    print("value C is %f"%C)
    A = slop
    B = -1
    return A,B,C

def calRef_LinearCurve():
     #=== load waypoint =============      # lat 13.650680 to utm east 661487.25   // lng  100.493001 to utm north 1509590.43
    n_pointStart_linear1 =0
    n_pointStop_linear1 = 425
    n_pointStart_Curve = 439
    n_pointStop_Curve = 492
    n_pointStart_CurfromLin = 495
    n_pointStop_CurfromLin = 30
    waypoints_file = WAYPOINTS_file_linearCurve
    with open (waypoints_file,"r") as f:
        waypoints = pd.read_table(f, sep=',', header=0, names=['x','y'])
        waypoints_np = np.array(waypoints)
    #input waypoint reference 
    x_axiswaypoint_ylngNorth = waypoints.x     #run direct forward in axis
    y_axiswaypoint_xlatEast = waypoints.y
    #==========Cal+===Linear===========================  1509653.4323676503,661487.058917912 //1509602.3403857893, 661487.1387887611
    # Dis1 = math.sqrt(( x_axiswaypoint_ylngNorth[n_pointStart_linear1]- x_axiswaypoint_ylngNorth[ n_pointStop_linear1])**2+(y_axiswaypoint_xlatEast[n_pointStart_linear1]-y_axiswaypoint_xlatEast[ n_pointStop_linear1])**2) #distance point start to stop
    Dis1 = math.sqrt((1509653.4323676503- 1509602.3403857893)**2+(661487.058917912-661487.1387887611)**2) #distance point start to stop
    print("value distance1 is %f" %Dis1)  #62.707530m => decrease 51.092044 m
        #find linear equretion
    #slop1  = (y_axiswaypoint_xlatEast[ n_pointStop_linear1]-y_axiswaypoint_xlatEast[n_pointStart_linear1])/( x_axiswaypoint_ylngNorth[ n_pointStop_linear1]- x_axiswaypoint_ylngNorth[n_pointStart_linear1])#find slop of linear equation -147.302103
    slop1  = (661487.1387887611-661487.058917912 )/( 1509602.3403857893- 1509653.4323676503)#find slop of linear equation -0.004138
    #print("slop1 is %f" %slop1)
        # find C fo linear equation
    #c1  = y_axiswaypoint_xlatEast[n_pointStart_linear1]-slop2* x_axiswaypoint_ylngNorth[n_pointStart_linear1]
    c1  =661487.058917912-slop1* 1509653.4323676503    #667734.571177
    #print("value C1 is %f"%c1)
    a1 = slop1
    b1 = -1
    # print("linear equation 1")
    # print(a1,b1,c1)            # -0.0015632756107706199 -1 663847.0633094484
    #=============================================
    #==========Cal+===Curve[1]===========================2 (1509600.7917398307, 661487.1663461719) start curve 
            #2 stop (1509593.9769328258, 661488.362279179)
    #Dis2 = math.sqrt(( x_axiswaypoint_ylngNorth[ n_pointStart_Curve]- x_axiswaypoint_ylngNorth[ n_pointStop_linear1])**2+(y_axiswaypoint_xlatEast[ n_pointStart_Curve]-y_axiswaypoint_xlatEast[ n_pointStop_linear1])**2) #distance point start to stop
    Dis2 = math.sqrt(( 1509600.7917398307- 1509593.9769328258)**2+(661487.1663461719-661488.362279179)**2) #distance point start to stop
    
    print("value distance2 is %f" %Dis2)  #3.344143m
        #find linear equretion
    #slop2  = (y_axiswaypoint_xlatEast[ n_pointStop_linear1]-y_axiswaypoint_xlatEast[n_pointStart_linear1])/( x_axiswaypoint_ylngNorth[ n_pointStop_linear1]- x_axiswaypoint_ylngNorth[n_pointStart_linear1])#find slop of linear equation -147.302103
    #print("slop is %f" %slop)
    slop2  = (661488.362279179- 661487.1663461719)/(1509593.9769328258- 1509600.7917398307)#find slop of linear equation 
    #print("slop is %f" %slop)
        # find C fo linear equation
    c2  =661487.1663461719-slop2* 1509600.7917398307
    #print("value C is %f"%c)
    a2 = slop2
    b2 = -1
    print(a2,b2,c2)  
    #==========Cal+===Curve[2]===========================   จบโค้งสองกำลังจะเส้นตรง #3 start curve2 (1509591.5631623606, 661488.6295672964)
            #3 stop curve 2  (1509586.3937104405, 661493.5298645048)
    #Dis2 = math.sqrt(( x_axiswaypoint_ylngNorth[ n_pointStart_Curve]- x_axiswaypoint_ylngNorth[ n_pointStop_linear1])**2+(y_axiswaypoint_xlatEast[ n_pointStart_Curve]-y_axiswaypoint_xlatEast[ n_pointStop_linear1])**2) #distance point start to stop
    Dis3 = math.sqrt((1509591.5631623606- 1509586.3937104405)**2+(661488.6295672964- 661493.5298645048)**2) #distance point start to stop
    
    print("value distance3 is %f" %Dis3)  #3.344143m
        #find linear equretion
    #slop2  = (y_axiswaypoint_xlatEast[ n_pointStop_linear1]-y_axiswaypoint_xlatEast[n_pointStart_linear1])/( x_axiswaypoint_ylngNorth[ n_pointStop_linear1]- x_axiswaypoint_ylngNorth[n_pointStart_linear1])#find slop of linear equation -147.302103
    #print("slop is %f" %slop)
    slop3  = ( 661493.5298645048- 661488.6295672964)/(1509586.3937104405- 1509591.5631623606)#find slop of linear equation -147.302103
    #print("slop is %f" %slop)
        # find C fo linear equation
    c3  =661488.6295672964-slop3* 1509591.5631623606
    #print("value C is %f"%c)
    a3 = slop3
    b3 = -1
    print(a3,b3,c3)  

    #==========Cal+===Curveto[Linear]===========================#4 start linear2 (y1509586.419246495, x661494.6837220492)
            #4 stop linear2  (y1509586.5847669786, x661518.5924456262)
    #Dis = math.sqrt(( x_axiswaypoint_ylngNorth[n_pointStart_linear1]- x_axiswaypoint_ylngNorth[ n_pointStop_linear1])**2+(y_axiswaypoint_xlatEast[n_pointStart_linear1]-y_axiswaypoint_xlatEast[ n_pointStop_linear1])**2) #distance point start to stop
    #print("value distance is %f" %Dis)  
    Dis4 = math.sqrt((661494.6837220492- 661518.5924456262)**2+(1509586.450772019-1509586.4924681296)**2) #distance point start to stop
    print("value distance4 is %f" %Dis4)  #29.615453m
        #find linear equretion
    #slop3  = (y_axiswaypoint_xlatEast[ n_pointStop_linear1]-y_axiswaypoint_xlatEast[n_pointStart_linear1])/( x_axiswaypoint_ylngNorth[ n_pointStop_linear1]- x_axiswaypoint_ylngNorth[n_pointStart_linear1])#find slop of linear equation -147.302103
    #print("slop is %f" %slop)
    slop4  = (1509586.5847669786-1509586.419246495)/(661518.5924456262- 661494.6837220492)#find slop of linear equation -147.302103
    #print("slop is %f" %slop)
        # find C fo linear equation
    #c3  = y_axiswaypoint_xlatEast[n_pointStart_linear1]-slop2* x_axiswaypoint_ylngNorth[n_pointStart_linear1]
    #print("value C is %f"%c)
    c4  = 1509586.419246495-slop4* 661494.6837220492
    #print("value C is %f"%c)
    a4 = slop4
    b4 = -1
    print(a4,b4,c4)  

    return a1,b1,c1,a2,b2,c2,a3,b3,c3
    
if __name__ == '__main__':
    #=============Serial position from rover =================================
    # while True:
    #     data = ser.readline()                           #output = b'$GNGGA,173534.70,1339.04546,N,10029.60344,E,1,12,0.56,6.3,M,-27.8,M,,*63\r\n'
    #     gngga_data = data.split(b",")
    #     if gngga_data[0] == b"$GNGGA":
    #         newmsg=pynmea2.parse(data.decode("utf-8"))
    #         lat=newmsg.latitude                         #get data from gnss is latitude and longtitude
    #         lng=newmsg.longitude
    #         gps = lat,lng
    #         xy = utm.from_latlon(lat,lng)               #convert data lat lng to utm-xy 
    #         x_north = xy[1]                             #for check cte 
    #         y_east = xy[0]                              #for track forward linear
    #         utem_position = x_north,y_east 
    #         print(utem_position)   
            #(1509590.5956462447, 661487.2110320957)  จุดสุดท้ายของเส้นตรง
            #(1509588.622825012, 661487.2231671072)  จุดเริ่มไปโค้ง
            #(1509587.3770549416, 661488.5290963219)  หน้ารถอยู่สิ้นสุดทางโค้ง
            # (1509586.648091768, 661489.9220040793) จีพีเอสอยู่ตรงเส้นสิ้นสุดทางโค้ง
            #(1509586.5209141802, 661490.2293215026) หน้ารถตั้งตรงกำลังจะวิ่งทางงตรงหลังจบโค้ง
            #(1509583.3647347316, 661519.6761136154) สิ้นสุดเส้นทาง
    #======Calculate Reference Waypoint trajectory ===================================
    A,B,C = calRef_toLinear()
            # lat 13.650680 to utm east 661487.25   // lng  100.493001 to utm north 1509590.43
            #เราวิ่งจาก noth ไป south ทำให้ค่า utm north 1509590.43 มีค่าลดลงไปเรื่อยๆ ซึ่งเราจะกำหนดให้มันเป็นแกน x แกนที่เราวิ่งอยู่
            # east คือค่าที่เกิดจากการวิ่งเอียงออกจากเส้นตรง ซึ่งจะมีค่าเป็นช่วง ส่วนนี้เราจะนำมาคิดเป็นค่าความคาดเคลื่อน 
            #  โดย ไปทางซ้าย ค่าeast จะเพิ่มขึ้น 86-88 ไปทางขวาค่า east จะลดลง 86-85
    calRef_LinearCurve()

                                                     #(1509602.3403857893, 661487.1387887611)  สิ้นสุดทางตรง เปลี่ยนจุดสิ้นสุด 
                                                        #(1509600.9763374685, 661487.2012736237) เริ่มโค้งหนึ่ง
                                                        # (1509600.222282086, 661487.5124468891) เริ่มเอียงซ้าย //  (1509597.629237676, 661488.6102853089) สูงสุดเอียงซ้าย
                                                        # เริ่มเอียงขวา (1509599.720252805, 661486.8303391305) // (1509595.146401635, 661486.6420957469) สูงสุดเอียงขวา
                                                        #(1509592.6520887874, 661488.8031838707)  จบโค้งหนึ่ง

                                                        # เอียงซ้ายเริ่ม  (1509591.6913381505, 661488.4845270686) // เอียงซ้ายสูงสุด (1509590.5525073276, 661492.1879846489)  
                                                        #เอียงขวาเริ่ม (1509591.0425845834, 661487.9295419285) // เอียงขวาสูงสุด  (1509587.0698270244, 661489.5407488741)
                                                        #(1509587.0942276441, 661493.5075239165)  จบโค้งสองกำลังจะเส้นตรง

                                                        #แกนตะวันออก(1509586.450772019, 661496.8112426052  เริ่มทางตรงแกนตะวันออก  track west to east value++
                                                        # เออเร้อแกนตะวันออก(1509586.6563329294, 661500.2539905524) รถเริ่มเอียงไปซ้าย cte+  //max cte (1509588.8436516593, 661511.1315476849)
                                                        # (1509586.3165312603, 661504.9622969673) รถเริ่มเอียงขวา แกนตะวันออก cte- // max cte- (1509584.0089640797, 661516.4986092591)
            #======= For write data to file CSV ========================

    #======= For write data to file CSV ========================
            # test_see1 = gps
            # with open('refLinearCurve_latlng.csv', 'a', newline='') as f:  
            #     writer = csv.writer(f,delimiter=",")    
            #     writer.writerow(test_see1) 

            # test_see2 = utem_position
            # with open('refLinearCurve_utm.csv', 'a', newline='') as f:  
            #     writer = csv.writer(f,delimiter=",")    
            #     writer.writerow(test_see2)