from ast import If
from asyncore import write
from fileinput import filename
from re import X
from socket import if_nameindex, timeout
from tkinter import Y
import serial
import time
import pynmea2
import matplotlib.pyplot as plt
import math
import csv
import serial as sr
import time
import pandas as pd
#param variable
dt = 0.2 #5Hz or 0.2 second
port = "COM13"  
filename = 'record_linear1.csv'
ser = serial.Serial(port, baudrate = 115200)
x = []
y = []
while True:
        data = ser.readline()
        #print(data)
        #output = b'$GNGGA,173534.70,1339.04546,N,10029.60344,E,1,12,0.56,6.3,M,-27.8,M,,*63\r\n'
        i =0
        gngga_data = data.split(b",")
        file = open(filename,'w')
        # gngga_data[0] = b'$GNGGA'
        if gngga_data[0] == b"$GNGGA":
            
                newmsg=pynmea2.parse(data.decode("utf-8"))
                lat=newmsg.latitude
                lng=newmsg.longitude
                #gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
                gps = [lat,lng] 
                #write data to file csv
                file = open(filename,'a')
                file.write(str(gps) +"\n" )
                
                print(gps)        #show output lad = 13.0 and long = 100.0
                time.sleep(dt)  # sleep(second) 5Hz = 1/5=0.2sec

            
    
    

