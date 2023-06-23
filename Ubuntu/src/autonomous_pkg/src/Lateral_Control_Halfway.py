#!/usr/bin/env python3
import rospy                                         
from std_msgs.msg import Float64MultiArray,Float64
import csv      
import math
import can
import os
import time

class main(object):                        

    def __init__(self):                         
        
        # CreateCSV Function
        self.value = []
        self.name = 'Data Column Name'
        self.column = 0
        self.csv_name = 0
        self.Data = []

        #Realtime XY callback Function
        self.time = 0.0
        self.x_east = 0.0                         
        self.y_north = 0.0
        self.xy = 0.0
        self.start = 0
        self.time_start = 0.0
        self.time_operate = 0.0
        
        #Select_Track Function
        self.Track = None
        self.linear = 0
        self.curve = 0
            
        self.reference = 0.0
        self.max_right = 0.0
        self.max_left = 0.0
        
        self.speed = 0
        self.a,self.b,self.c    =  1,1,1
        self.aL,self.bL,self.cL    =  0,0,0
        self.aR,self.bR,self.cR    =  0,0,0
        
            #linear S-N
        self.SN1_start = 1509522.50
        self.SN1_stop  = 1509583.749          #/
        self.SN1_maxright = 661488.24726504      #661488.31726504  
        self.SN1_maxleft = 661484.053410818     #661484.173410818  
        self.SN1_ref = 661485.7821431490
        self.aSN1,self.bSN1,self.cSN1 = -433.23429367832364 , -1 , 288087878.72954065
        

        self.SN2_start = 1509583.7491
        self.SN2_stop  = 1509685.06490994          #/
        self.SN2_maxright = 661488.3575 #87
        self.SN2_maxleft = 661483.573410818 
        self.SN2_ref =  661485.5164450410
        self.aSN2,self.bSN2,self.cSN2 = -259.77102429857507 , -1 , 173344404.57255518
        
            #curve1 E-W
        self.curve1_s1_start = 1509685.065
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

            #linear E-W
        self.EW_start = 661478.34
        self.EW_stop  = 661433.35
        self.EW_maxright = 1509703.9
        self.EW_maxleft = 1509696.5
        self.EW_ref = 1509700
        self.aEW,self.bEW,self.cEW = -0.06666666666666667 ,-1 ,1553796.9466666665

            #curve 2
        self.curve2_s1_start = 661433.35
        self.curve2_s1_stop = 661418.32
        self.curve2_s1_maxright = 1509703.9
        self.curve2_s1_maxleft = 1509699.09     
        self.aL4,self.bL4,self.cL4 = 0.07692307693214072 , -1 , 1458819.6015324665
        self.a4,self.b4,self.c4    =  0.1064537591388774 , -1 , 1439289.3234726791
        self.aR4,self.bR4,self.cR4    =  0.16936005170547253 , -1 , 1397683.513644276

        self.curve2_s2_start = 661418.32
        self.curve2_s2_stop = 661405.27
        self.curve2_s2_maxright = 1509703.27
        self.curve2_s2_maxleft = 1509689.86
        self.aL5,self.bL5,self.cL5 = 0.542297417618975 , -1 , 1151012.3892156614
        self.a5,self.b5,self.c5    =  0.4942528735622956 , -1 , 1182791.8847132542
        self.aR5,self.bR5,self.cR5    =  0.45174537988360325 , -1 , 1210908.8085375926

        self.curve2_s3_start = 661405.27
        self.curve2_s3_stop = 661396.73
        self.curve2_s3_maxright = 1509696.68
        self.curve2_s3_maxleft = 1509684
        self.aL6,self.bL6,self.cL6 = 0.5973741794515571 , -1 , 1114584.2168792302
        self.a6,self.b6,self.c6    =  0.6194379391117303 , -1 , 1099993.8226335626
        self.aR6,self.bR6,self.cR6    =  0.5845588235293593 , -1 , 1123065.5626103287

        self.curve2_s4_start = 661396.73
        self.curve2_s4_stop = 661387.65
        self.curve2_s4_maxright = 1509691
        self.curve2_s4_maxleft =    150966.5
        self.aL7,self.bL7,self.cL7 = 1.243577545178 , -1 , 687186.4998019538
        self.a7,self.b7,self.c7    =  1.1019417475893303 , -1 , 780867.3814939316
        self.aR7,self.bR7,self.cR7    =  1.086913086900911 , -1 , 790810.9093287324

        self.curve2_s5_start = 661387.65
        self.curve2_s5_stop = 661376.99
        self.curve2_s5_maxright = 1509682.03
        self.curve2_s5_maxleft = 1509666.5
        self.aL8,self.bL8,self.cL8 = 2.519774011317643 , -1 , -156874.08187644905
        self.a8,self.b8,self.c8    =  1.918356643326645 , -1 , 240901.64820340672
        self.aR8,self.bR8,self.cR8    =  1.5237483954085216 , -1 , 501894.5451278954

        self.curve2_s6_start = 1509666.5
        self.curve2_s6_stop = 1509653.56
        self.curve2_s6_maxright = 661376.99
        self.curve2_s6_maxleft = 661387.65
        self.aL9,self.bL9,self.cL9 = 6.420118343324884 , -1 , -2736499.8465946023
        self.a9,self.b9,self.c9    =  8.391034482958728 , -1 , -4040002.6169737265
        self.aR9,self.bR9,self.cR9    =  42.49999999090505 , -1 , -26598868.50898481

            #linear N-S
        self.NS_start = 1509653.566
        self.NS_stop  = 1509560.129
        self.NS_maxright = 661375.26
        self.NS_maxleft = 661383.26
        self.NS_ref = 661379.26       #661379.26
        self.aNS,self.bNS,self.cNS = 7786.41667453521 ,-1 ,-5148264891.408258  

            #Curve3
        self.curve3_s1_start = 1509560.13
        self.curve3_s1_stop = 1509550.53
        self.curve3_s1_maxright = 661376.99
        self.curve3_s1_maxleft = 661384.5
        self.aL10,self.bL10,self.cL10 = -9.391025640947507 , -1 , 7720619.394691913
        self.a10,self.b10,self.c10    =  -6.130268199177321 , -1 , 5563992.33839182
        self.aR10,self.bR10,self.cR10    =  -7.999999999641799 , -1 , 6800576.049763095  

        self.curve3_s2_start = 1509550.53
        self.curve3_s2_stop = 1509542.1
        self.curve3_s2_maxright = 661378.29
        self.curve3_s2_maxleft = 661388.00
        self.aL11,self.bL11,self.cL11 = -3.090015128686663 , -1 , 3553235.915901557
        self.a11,self.b11,self.c11    =  -4.058365758626549 , -1 , 4193675.803300349
        self.aR11,self.bR11,self.cR11    =  -3.9306545689721237 , -1 , 4109199.3274074704

        self.curve3_s3_start = 1509542.1
        self.curve3_s3_stop = 1509529.5
        self.curve3_s3_maxright = 661379.5
        self.curve3_s3_maxleft = 661398.2
        self.aL12,self.bL12,self.cL12 = -1.2935779816383115 , -1 , 2365097.5369638363
        self.a12,self.b12,self.c12    =  -1.0589318600381945 , -1 , 2209900.0433710665
        self.aR12,self.bR12,self.cR12    =  -1.0545749279777836 , -1 , 2207013.8169610477

        self.curve3_s4_start = 1509529.5
        self.curve3_s4_stop = 1509519.2
        self.curve3_s4_maxright = 661387.00
        self.curve3_s4_maxleft = 661412.4
        self.aL13,self.bL13,self.cL13 = -0.7512877115516731 , -1 , 2006429.024524765
        self.a13,self.b13,self.c13    =  -0.748349229653909 , -1 , 2004482.477485025
        self.aR13,self.bR13,self.cR13    =  -0.6805157593141369 , -1 , 1959613.8957318598    

        self.curve3_s5_start = 1509519.2
        self.curve3_s5_stop = 1509510.45
        self.curve3_s5_maxright = 661398.4
        self.curve3_s5_maxleft = 661417.61   
        self.aL14,self.bL14,self.cL14 = -0.6045258620781848 , -1 , 1909359.3577216151
        self.a14,self.b14,self.c14    =  -0.6115107913632912 , -1 , 1913976.4561127168
        self.aR14,self.bR14,self.cR14    =  -0.5840707964522756 , -1 , 1895824.576189464

        self.curve3_s6_start = 661417.61
        self.curve3_s6_stop = 661423.72
        self.curve3_s6_maxright = 1509507.83
        self.curve3_s6_maxleft = 1509516.66
        self.aL15,self.bL15,self.cL15 = -0.37177280549719216 , -1 , 1755412.1382718496
        self.a15,self.b15,self.c15    =  -0.3878887070187147 , -1 , 1766068.8715423085
        self.aR15,self.bR15,self.cR15    =  -0.4087363494330117 , -1 , 1779855.460625758

        self.curve3_s7_start = 661423.72
        self.curve3_s7_stop = 661430.28
        self.curve3_s7_maxright = 1509506.53
        self.curve3_s7_maxleft = 1509512.5
        self.aL16,self.bL16,self.cL16 = -0.21768707483451122 , -1 , 1653496.0624520085
        self.a16,self.b16,self.c16    =  -0.1753048780685827 , -1 , 1625460.8845862686
        self.aR16,self.bR16,self.cR16    =  -0.1818181818241025 , -1 , 1629766.560913007

        self.curve3_s8_start = 661430.28                                            
        self.curve3_s8_stop = 661436.79
        self.curve3_s8_maxright = 1509506.53
        self.curve3_s8_maxleft = 1509512.5   
        self.aL17,self.bL17,self.cL17 = 0.0669781931358256 , -1 , 1465209.8089322394
        self.a17,self.b17,self.c17    =  0.07834101382620332 , -1 , 1457691.8112894504
        self.aR17,self.bR17,self.cR17    =  0.13444108759791248 , -1 , 1420583.1385751278

            #linear W-E
        self.WE_start = 661436.79               
        self.WE_stop  = 661466.07
        self.WE_maxright = 1509506.53            
        self.WE_maxleft = 1509512.5           
        self.WE_ref = 1509509.63         
        self.aWE,self.bWE,self.cWE =  0.012978142080676918 , -1 , 1500925.219361993

            #Curve4
        self.curve4_s1_start = 661466.07                                                   
        self.curve4_s1_stop = 661472.01
        self.curve4_s1_maxright = 1509507.42
        self.curve4_s1_maxleft = 1509512.44
        self.aL18,self.bL18,self.cL18 = 0.12457912457628709 , -1 , 1427106.836062483
        self.a18,self.b18,self.c18    =  0.06734006732370224 , -1 , 1464966.6503138554
        self.aR18,self.bR18,self.cR18    =  0.08249158248917392 , -1 , 1454942.3971228052

        self.curve4_s2_start = 661472.01                                                        
        self.curve4_s2_stop = 661478.05
        self.curve4_s2_maxright = 1509508.27
        self.curve4_s2_maxleft = 1509513.50
        self.aL19,self.bL19,self.cL19 = 0.13051146384218998 , -1 , 1423182.7596842642
        self.a19,self.b19,self.c19    =  0.11920529800788404 , -1 , 1430659.251924076
        self.aR19,self.bR19,self.cR19    =  0.08137715180242404 , -1 , 1455679.5618291756

        self.curve4_s3_start = 661478.05                                                         
        self.curve4_s3_stop = 661481.50
        self.curve4_s3_maxright = 1509508.79
        self.curve4_s3_maxleft = 1509515.1
        self.aL20,self.bL20,self.cL20 = 0.44837758113998843 , -1 , 1212921.4178635087
        self.a20,self.b20,self.c20    =  0.33333333336977006 , -1 , 1289018.2566425644
        self.aR20,self.bR20,self.cR20    =  0.2534653465436919 , -1 , 1341846.938112833

        self.curve4_s4_start = 661481.5                                         
        self.curve4_s4_stop = 661483.9
        self.curve4_s4_maxright = 1509509.5
        self.curve4_s4_maxleft = 1509517.5   
        self.aL21,self.bL21,self.cL21 = 0.8590604026415655 , -1 , 941262.5056660265
        self.a21,self.b21,self.c21    =  0.5475285171122858 , -1 , 1147331.9317096907
        self.aR21,self.bR21,self.cR21    =  0.44818652848068885 , -1 , 1213042.0988970706

        self.curve4_s5_start = 661483.9                                            
        self.curve4_s5_stop = 661489.37
        self.curve4_s5_maxright = 1509509.5
        self.curve4_s5_maxleft = 1509517.5
        self.aL22,self.bL22,self.cL22 = 1.1343283582504489 , -1 , 759177.5537038959
        self.a22,self.b22,self.c22    =  1.927083333267016 , -1 , 234777.196918868
        self.aR22,self.bR22,self.cR22    =  2.766990291320843 , -1 , -320817.1646019409

        self.curve4_s6_start = 1509517.50                                     
        self.curve4_s6_stop = 1509522.50
        self.curve4_s6_maxright = 661489.88
        self.curve4_s6_maxleft = 661483.9
        self.aL23,self.bL23,self.cL23 = 18.518518517240985 , -1 , -10740184.351006784
        self.a23,self.b23,self.c23    =  6.172839505746995 , -1 , -2573734.721940532
        self.aR23,self.bR23,self.cR23    =  9.80392156844842 , -1 , -4975672.401842357

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

        #Control_sent_can function  
        self.angle = 0.0
        self.elec_angle_dec = 0.0
        self.elec_angle_hex = 0.0
        self.DATA_Hh = 0.0
        self.DATA_Hl = 0.0
        self.DATA_Lh = 0.0
        self.DATA_Ll = 0.0
        self.msg_sent = None

        self.Steering_Angle_want = rospy.Publisher('Steering_Angle_Want',Float64,queue_size=10)   
        self.CTE_Pub = rospy.Publisher('CTE',Float64,queue_size=10)                      
        self.Speed_Pub = rospy.Publisher('Speed_Setpoint',Float64,queue_size=10)  

        rospy.Subscriber("Realtime_XY",Float64MultiArray,self.Realtime_XY_callback)           
        rospy.spin()                   

    def Realtime_XY_callback(self,msg):   

        self.time = msg.data[0] 
        self.x_east = msg.data[1]                         
        self.y_north = msg.data[2]
        self.xy = msg.data 

        if self.start == 0:
            self.time_start = self.time
            self.start = 1

        if self.start == 1:

            self.time_operate = round(self.time - self.time_start,2)  

            self.Select_Track() 
            
            self.cte_current()
            
            self.pid_angle()
    
            self.angle_controlMotor()

            self.Talker()   
                 
            # self.CreateCSV()

            print(round(self.x_east,2),'||' ,round(self.y_north,2),'||'  ,self.Track,'|| cte = ' ,round(self.cte,2),'|| Yaw = ' ,round(self.yaw_control,2))
                    
    def Select_Track(self):
        
        #linear SN1
        if (self.x_east <= self.SN1_maxright)&(self.x_east >= self.SN1_maxleft) & (self.y_north >= self.SN1_start)&(self.y_north <= self.SN1_stop):
            
            self.Track = 'linear_SN1'
            self.linear = 1
            self.curve = 0
            self.speed = 3.5

            self.a = self.aSN1
            self.b = self.bSN1
            self.c = self.cSN1

            
            self.reference = self.SN1_ref
            self.max_right = self.SN1_maxright
            self.max_left = self.SN1_maxleft 
            
            self.kp = 70    #70     
            self.ki = 0.2 #0.18
            self.kd = 60    #60

        #linear SN2
        if (self.x_east <= self.SN2_maxright)&(self.x_east >= self.SN2_maxleft) & (self.y_north >= self.SN2_start)&(self.y_north <= self.SN2_stop):
            
            self.Track = 'linear_SN2'
            self.linear = 1
            self.curve = 0
            self.speed = 3.5

            self.a = self.aSN2
            self.b = self.bSN2
            self.c = self.cSN2
            
            self.reference = self.SN2_ref
            self.max_right = self.SN2_maxright
            self.max_left = self.SN2_maxleft 
            
            self.kp = 70        #70
            self.ki = 0.2     #0.15
            self.kd = 60        #65

        #Curve1_set1
        if (self.y_north >= self.curve1_s1_start) & (self.y_north <= self.curve1_s1_stop ) & (self.x_east <= self.curve1_s1_maxright)&(self.x_east >= self.curve1_s1_maxleft):
            
            self.Track = 'Curve1_Set1'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a1
            self.b = self.b1
            self.c = self.c1
            
            self.aL = self.aL1
            self.bL = self.bL1
            self.cL = self.cL1
            
            self.aR = self.aR1
            self.bR = self.bR1
            self.cR = self.cR1
            
            self.kp = 50
            self.ki = 0.17
            self.kd = 38

        #Curve1_set2    
        if (self.y_north >= self.curve1_s2_maxleft)&(self.y_north <= self.curve1_s2_maxright) & (self.x_east <= self.curve1_s2_start)&(self.x_east >= self.curve1_s2_stop):
            
            self.Track = 'Curve1_Set2'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a2
            self.b = self.b2
            self.c = self.c2
            
            self.aL = self.aL2
            self.bL = self.bL2
            self.cL = self.cL2
            
            self.aR = self.aR2
            self.bR = self.bR2
            self.cR = self.cR2
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38

        #Curve1_set3    
        if (self.x_east < self.curve1_s3_start)&(self.x_east > self.curve1_s3_stop) & (self.y_north >= self.curve1_s3_maxleft)&(self.y_north <= self.curve1_s3_maxright):
            
            self.Track = 'curve1_set3'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a3
            self.b = self.b3
            self.c = self.c3
            
            self.aL = self.aL3
            self.bL = self.bL3 
            self.cL = self.cL3
            
            self.aR = self.aR3
            self.bR = self.bR3
            self.cR = self.cR3
            
            self.kp = 52
            self.ki = 0.2
            self.kd = 38
        
        #linear EW    
        if (self.x_east <= self.EW_start)&(self.x_east >= self.EW_stop) & (self.y_north <= self.EW_maxright)&(self.y_north >= self.EW_maxleft):
            
            self.Track = 'linear_EW'
            self.linear = 2   #for linear E-W and W-E
            self.curve = 0
            self.speed = 3

            self.a = self.aEW
            self.b = self.bEW
            self.c = self.cEW
            
            self.reference = self.EW_ref
            self.max_right = self.EW_maxright
            self.max_left = self.EW_maxleft
            
            self.kp = 70#45
            self.ki = 0.15#0.02
            self.kd = 65#26

        #Curve2_set1 
        if (self.x_east < self.curve2_s1_start)&(self.x_east > self.curve2_s1_stop) & (self.y_north < self.curve2_s1_maxright)&(self.y_north > self.curve2_s1_maxleft):
            
            self.Track = 'Curve2_set1'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a4
            self.b = self.b4
            self.c = self.c4
            
            self.aL = self.aL4
            self.bL = self.bL4 
            self.cL = self.cL4
            
            self.aR = self.aR4
            self.bR = self.bR4
            self.cR = self.cR4
            
            self.kp = 48
            self.ki = 0.17
            self.kd = 38

        #Curve2_set2 
        if (self.x_east < self.curve2_s2_start)&(self.x_east > self.curve2_s2_stop) & (self.y_north < self.curve2_s2_maxright)&(self.y_north > self.curve2_s2_maxleft):
            
            self.Track = 'Curve2_set2'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a5
            self.b = self.b5
            self.c = self.c5
            
            self.aL = self.aL5
            self.bL = self.bL5 
            self.cL = self.cL5
            
            self.aR = self.aR5
            self.bR = self.bR5
            self.cR = self.cR5
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38

        #Curve2_set3
        if (self.x_east < self.curve2_s3_start)&(self.x_east > self.curve2_s3_stop) & (self.y_north < self.curve2_s3_maxright)&(self.y_north > self.curve2_s3_maxleft):
            
            self.Track = 'Curve2_set3'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a6
            self.b = self.b6
            self.c = self.c6
            
            self.aL = self.aL6
            self.bL = self.bL6 
            self.cL = self.cL6
            
            self.aR = self.aR6
            self.bR = self.bR6
            self.cR = self.cR6
            
            self.kp = 52
            self.ki = 0.2
            self.kd = 38

        #Curve2_set4
        if (self.x_east < self.curve2_s4_start)&(self.x_east > self.curve2_s4_stop) & (self.y_north < self.curve2_s4_maxright)&(self.y_north > self.curve2_s4_maxleft):
            
            self.Track = 'Curve2_set4'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a7
            self.b = self.b7
            self.c = self.c7
            
            self.aL = self.aL7
            self.bL = self.bL7 
            self.cL = self.cL7
            
            self.aR = self.aR7
            self.bR = self.bR7
            self.cR = self.cR7
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38            
    
        #Curve2_set5
        if (self.x_east < self.curve2_s5_start)&(self.x_east > self.curve2_s5_stop) & (self.y_north < self.curve2_s5_maxright)&(self.y_north > self.curve2_s5_maxleft):
            
            self.Track = 'Curve2_set5'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a8
            self.b = self.b8
            self.c = self.c8
            
            self.aL = self.aL8
            self.bL = self.bL8 
            self.cL = self.cL8
            
            self.aR = self.aR8
            self.bR = self.bR8
            self.cR = self.cR8
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38            
    
        #Curve2_set6
        if (self.x_east < self.curve2_s6_maxleft)&(self.x_east > self.curve2_s6_maxright) & (self.y_north < self.curve2_s6_start)&(self.y_north > self.curve2_s6_stop):
            
            self.Track = 'Curve2_set6'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a9
            self.b = self.b9
            self.c = self.c9
            
            self.aL = self.aL9
            self.bL = self.bL9 
            self.cL = self.cL9
            
            self.aR = self.aR9
            self.bR = self.bR9
            self.cR = self.cR9
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38     

        #linear NS
        if (self.x_east < self.NS_maxleft)&(self.x_east > self.NS_maxright) & (self.y_north < self.NS_start)&(self.y_north > self.NS_stop):
            
            self.Track = 'linear_NS'
            self.linear = 3
            self.curve = 0

            self.speed = 1
            self.a = self.aNS
            self.b = self.bNS
            self.c = self.cNS

            
            self.reference = self.NS_ref
            self.max_right = self.NS_maxright
            self.max_left = self.NS_maxleft
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 23    

        #Curve3_set1
        if (self.y_north < self.curve3_s1_start)&(self.y_north > self.curve3_s1_stop) & (self.x_east > self.curve3_s1_maxright)&(self.x_east < self.curve3_s1_maxleft): 
            
            self.Track = 'Curve3_set1'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a10
            self.b = self.b10
            self.c = self.c10
            
            self.aL = self.aL10
            self.bL = self.bL10
            self.cL = self.cL10
            
            self.aR = self.aR10
            self.bR = self.bR10
            self.cR = self.cR10
            
            self.kp = 40
            self.ki = 0.02
            self.kd = 23          

        #Curve3_set2
        if (self.y_north < self.curve3_s2_start)&(self.y_north > self.curve3_s2_stop) & (self.x_east > self.curve3_s2_maxright)&(self.x_east < self.curve3_s2_maxleft): 
            
            self.Track = 'Curve3_set2'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a11
            self.b = self.b11
            self.c = self.c11
            
            self.aL = self.aL11
            self.bL = self.bL11
            self.cL = self.cL11
            
            self.aR = self.aR11
            self.bR = self.bR11
            self.cR = self.cR11
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38                        
    
        #Curve3_set3
        if (self.y_north < self.curve3_s3_start)&(self.y_north > self.curve3_s3_stop) & (self.x_east > self.curve3_s3_maxright)&(self.x_east < self.curve3_s3_maxleft): 
            
            self.Track = 'Curve3_set3'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a12
            self.b = self.b12
            self.c = self.c12
            
            self.aL = self.aL12
            self.bL = self.bL12
            self.cL = self.cL12
            
            self.aR = self.aR12
            self.bR = self.bR12
            self.cR = self.cR12
            
            self.kp = 50
            self.ki = 0.2
            self.kd = 38      

        #Curve3_set4
        if (self.y_north < self.curve3_s4_start)&(self.y_north > self.curve3_s4_stop) & (self.x_east > self.curve3_s4_maxright)&(self.x_east < self.curve3_s4_maxleft): 
            
            self.Track = 'Curve3_set4'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a13
            self.b = self.b13
            self.c = self.c13
            
            self.aL = self.aL13
            self.bL = self.bL13
            self.cL = self.cL13
            
            self.aR = self.aR13
            self.bR = self.bR13
            self.cR = self.cR13
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26      

       #Curve3_set5
        if (self.y_north > self.curve3_s5_start)&(self.y_north < self.curve3_s5_stop) & (self.x_east > self.curve3_s5_maxright)&(self.x_east < self.curve3_s5_maxleft): 
            
            self.Track = 'Curve3_set5'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a14
            self.b = self.b14   
            self.c = self.c14
            
            self.aL = self.aL14
            self.bL = self.bL14
            self.cL = self.cL14
            
            self.aR = self.aR14
            self.bR = self.bR14
            self.cR = self.cR14
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26  

       #Curve3_set6
        if (self.x_east > self.curve3_s6_start)&(self.x_east < self.curve3_s6_stop) & (self.y_north < self.curve3_s6_maxleft)&(self.y_north > self.curve3_s6_maxright):

            self.Track = 'Curve3_set6'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a15
            self.b = self.b15   
            self.c = self.c15
            
            self.aL = self.aL15
            self.bL = self.bL15
            self.cL = self.cL15
            
            self.aR = self.aR15
            self.bR = self.bR15
            self.cR = self.cR15
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26  

       #Curve3_set7
        if (self.x_east > self.curve3_s7_start)&(self.x_east < self.curve3_s7_stop) & (self.y_north < self.curve3_s7_maxleft)&(self.y_north > self.curve3_s7_maxright):

            self.Track = 'Curve3_set7'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a16
            self.b = self.b16   
            self.c = self.c16
            
            self.aL = self.aL16
            self.bL = self.bL16
            self.cL = self.cL16
            
            self.aR = self.aR16
            self.bR = self.bR16
            self.cR = self.cR16
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26      

       #Curve3_set8
        if (self.x_east > self.curve3_s8_start)&(self.x_east < self.curve3_s8_stop) & (self.y_north < self.curve3_s8_maxleft)&(self.y_north > self.curve3_s8_maxright):

            self.Track = 'Curve3_set8'
            self.linear = 0
            self.curve = 1
            
            self.speed = 3
            self.a = self.a17
            self.b = self.b17   
            self.c = self.c17
            
            self.aL = self.aL17
            self.bL = self.bL17
            self.cL = self.cL17
            
            self.aR = self.aR17
            self.bR = self.bR17
            self.cR = self.cR17
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26                      

        #linear_WE
        if (self.x_east >= self.WE_start)&(self.x_east <= self.WE_stop) & (self.y_north <= self.WE_maxleft)&(self.y_north >= self.WE_maxright):

            self.Track = 'linear_WE'
            self.linear = 4
            self.curve = 0

            self.speed = 3
            self.a = self.aWE
            self.b = self.bWE
            self.c = self.cWE

            
            self.reference = self.WE_ref
            self.max_right = self.WE_maxright
            self.max_left = self.WE_maxleft
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26  

       #Curve4_set1
        if (self.x_east > self.curve4_s1_start)&(self.x_east < self.curve4_s1_stop) & (self.y_north < self.curve4_s1_maxleft)&(self.y_north > self.curve4_s1_maxright):

            self.Track = 'Curve4_set1'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a18
            self.b = self.b18   
            self.c = self.c18
            
            self.aL = self.aL18
            self.bL = self.bL18
            self.cL = self.cL18
            
            self.aR = self.aR18
            self.bR = self.bR18
            self.cR = self.cR18
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26 

       #Curve4_set2
        if (self.x_east > self.curve4_s2_start)&(self.x_east < self.curve4_s2_stop) & (self.y_north < self.curve4_s2_maxleft)&(self.y_north > self.curve4_s2_maxright):

            self.Track = 'Curve4_set2'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a19
            self.b = self.b19   
            self.c = self.c19
            
            self.aL = self.aL19
            self.bL = self.bL19
            self.cL = self.cL19
            
            self.aR = self.aR19
            self.bR = self.bR19
            self.cR = self.cR19
            
            self.kp = 45
            self.ki = 0.02
            self.kd = 26       

       #Curve4_set3
        if (self.x_east > self.curve4_s3_start)&(self.x_east < self.curve4_s3_stop) & (self.y_north < self.curve4_s3_maxleft)&(self.y_north > self.curve4_s3_maxright):

            self.Track = 'Curve4_set3'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a20
            self.b = self.b20   
            self.c = self.c20
            
            self.aL = self.aL20
            self.bL = self.bL20
            self.cL = self.cL20
            
            self.aR = self.aR20
            self.bR = self.bR20
            self.cR = self.cR20
            
            self.kp = 52
            self.ki = 0.2
            self.kd = 38 

       #Curve4_set4
        if (self.x_east > self.curve4_s4_start)&(self.x_east < self.curve4_s4_stop) & (self.y_north < self.curve4_s4_maxleft)&(self.y_north > self.curve4_s4_maxright):

            self.Track = 'Curve4_set4'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a21
            self.b = self.b21   
            self.c = self.c21
            
            self.aL = self.aL21
            self.bL = self.bL21
            self.cL = self.cL21
            
            self.aR = self.aR21
            self.bR = self.bR21
            self.cR = self.cR21
            
            self.kp = 52
            self.ki = 0.2
            self.kd = 38

       #Curve4_set5
        if (self.x_east > self.curve4_s5_start)&(self.x_east < self.curve4_s5_stop) & (self.y_north < self.curve4_s5_maxleft)&(self.y_north > self.curve4_s5_maxright):

            self.Track = 'Curve4_set5'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a22
            self.b = self.b22   
            self.c = self.c22
            
            self.aL = self.aL22
            self.bL = self.bL22
            self.cL = self.cL22
            
            self.aR = self.aR22
            self.bR = self.bR22
            self.cR = self.cR22
            
            self.kp = 52
            self.ki = 0.2
            self.kd = 38     

        #Curve4_set6
        if (self.y_north > self.curve4_s6_start)&(self.y_north < self.curve4_s6_stop) & (self.x_east > self.curve4_s6_maxleft)&(self.x_east < self.curve4_s6_maxright):

            self.Track = 'Curve4_set6'
            self.linear = 0
            self.curve = 1
            
            self.speed = 1
            self.a = self.a23
            self.b = self.b23   
            self.c = self.c23
            
            self.aL = self.aL23
            self.bL = self.bL23
            self.cL = self.cL23
            
            self.aR = self.aR23
            self.bR = self.bR23
            self.cR = self.cR23
            
            self.kp = 52
            self.ki = 0.2
            self.kd = 38  

    def cte_current(self):
        
            self.distance = abs(( self.a * self.x_east ) + ( self.b * self.y_north ) + self.c) / math.sqrt( self.a**2 + self.b**2 )
            
            if (self.linear == 1)&(self.curve == 0):  #for linear S-N
                
                if(self.distance <= 0.05):
                    self.cte = self.acceprtable_error
                
                if(self.distance > 0.05):
                    if (self.x_east >= self.reference) & (self.x_east <= self.max_right):
                        self.cte = self.distance
                        
                    if (self.x_east < self.reference) & (self.x_east >= self.max_left):
                        self.cte = (-1)*self.distance   

            if (self.linear == 2)&(self.curve == 0):  #for linear E-W
                
                if(self.distance <= 0.15):
                    self.cte = self.acceprtable_error
                
                if(self.distance > 0.15):
                    if (self.y_north >= self.reference) & (self.y_north <= self.max_right):
                        self.cte = self.distance
                        
                    if (self.y_north < self.reference) & (self.y_north >= self.max_left):
                        self.cte = (-1)*self.distance               
                        
            if (self.linear == 3)&(self.curve == 0):  #for linear N-S
                
                if(self.distance <= 0.15):
                    self.cte = self.acceprtable_error
                
                if(self.distance > 0.15):
                    if (self.x_east <= self.reference) & (self.x_east >= self.max_right):
                        self.cte = self.distance
                        
                    if (self.x_east > self.reference) & (self.x_east <= self.max_left):
                        self.cte = (-1)*self.distance   

            if (self.linear == 4)&(self.curve == 0):  #for linear W-E
                
                if(self.distance <= 0.15):
                    self.cte = self.acceprtable_error
                
                if(self.distance > 0.15):
                    if (self.y_north < self.reference) & (self.y_north >= self.max_right):
                        self.cte = self.distance
                        
                    if (self.y_north >= self.reference) & (self.y_north <= self.max_left):
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

            else:
                if self.cte > 0.15 : 
                    self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                    if self.yaw >= 0.25:
                        self.yaw_control = abs(self.yaw_expect)
                
                if self.cte < -0.15 :
                    self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                    if self.yaw >= 0.25:
                        self.yaw_control = -1*(self.yaw_expect)

            if self.cte == 0 :
                self.yaw_control = 0  

    def pid_angle(self):
        
        self.yaw_prev = self.yaw_expect
        self.sum_error_cte += self.cte
        
        self.P = self.kp * self.cte
        self.I = self.ki * self.sum_error_cte
        self.D = self.kd * ((self.cte - self.cte_prev))
        
        self.yaw_expect = (-1)*(self.P + self.I + self.D)

    def angle_controlMotor(self):

        # if self.cte > 0.15 : 
        #     self.yaw = abs(self.yaw_control - self.yaw_prev)
                
        #     if self.yaw >= 0.25:
        #         self.yaw_control = abs(self.yaw_expect)
                
        # if self.cte < -0.15 :
        #     self.yaw = abs(self.yaw_control - self.yaw_prev)
                
        #     if self.yaw >= 0.25:
        #         self.yaw_control = -1*(self.yaw_expect)

        # if self.cte == 0: 
        #     self.yaw_control = 0     

        #------------------------------------------------------------------#
        
        if self.linear == 1:
            if self.cte > 0.05 : 
                self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                if self.yaw >= 0.25:
                    self.yaw_control = abs(self.yaw_expect)
                
            if self.cte < -0.05 :
                self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                if self.yaw >= 0.25:
                    self.yaw_control = -1*(self.yaw_expect)

        else:
            if self.cte > 0.15 : 
                self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                if self.yaw >= 0.25:
                    self.yaw_control = abs(self.yaw_expect)
                
            if self.cte < -0.15 :
                self.yaw = abs(self.yaw_control - self.yaw_prev)
                
                if self.yaw >= 0.25:
                    self.yaw_control = -1*(self.yaw_expect)

        if self.cte == 0: 
            self.yaw_control = 0               
                 
    def Talker(self):                          

        Angle_want = Float64()                                       
        Angle_want.data = self.yaw_control 

        self.Steering_Angle_want.publish(Angle_want)   
        rospy.loginfo('Publishing Angle Want : %s',Angle_want.data)   

        Speed_SP = Float64()
        Speed_SP.data = self.speed
        self.Speed_Pub.publish(Speed_SP)
        rospy.loginfo('Publishing Speed SetPoint : %s',Speed_SP.data) 

    def CreateCSV(self):

        self.value = self.time_operate , self.Track , self.x_east , self.y_north , self.cte , self.yaw_control
        self.name = 'time_operate,self.Track,self.x_east,self.y_north,self.cte,self.yaw_control'

        if self.time_operate <= 1000 :

            name = 'fullway_4.csv'     #change name csv
            
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

        if self.time_operate > 1000 :
            print("Stop...")     

if __name__ == '__main__':
    rospy.init_node('Lateral_Control',anonymous=True)     

    try:
        my_subs = main()                 
    except rospy.ROSInterruptException:
        pass                            