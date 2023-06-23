import pandas as pd
import matplotlib.pyplot as plt

# Velocity Single Plot from lat/lon (lat/lon with out filter)

df = pd.read_csv('value_175.csv')                           #import data from csv file      #print(df)
value = 175                                                 #for plot

raw_speed_ms = df.speed_ms                                  #Define parameter that keep data of column name "speed_ms"
raw_speed_kmhr = df.speed_kmhr                              #Define parameter that keep data of column name "speed_kmhr"

window_size = 20                                            #Window size of Moving Average Filter (Can change)

speed_ms_buff = []                                          #Define buffer list to keep the raw speed value in Moving Average Calculation
sum_speed_ms = 0.0                                          #Define Variable to keep the speed sum in Moving Average Calculation
list_speed_ms = []                                          #Define list to keep the speed value after Moving Average Calculation


for i in range(len(raw_speed_ms)):                          #Moving Average For loop
    
    speed_ms_buff.append(raw_speed_ms[i])                   #Add raw speed to speed buffer : speed_buff = [ raw_speed_ms[0] , raw_speed_ms[1] , ...]
    
    sum_speed_ms = sum_speed_ms + raw_speed_ms[i]           #Sum the raw speed
    
    if len(speed_ms_buff) > window_size:                    #if length of speed buffer > window size wil cal the moving average
        
        sum_speed_ms = sum_speed_ms - speed_ms_buff.pop(0)  #minus Sum with Speed buff number0 and Pop the speed buff number0 
        
        speed_ms = float(sum_speed_ms)/len(speed_ms_buff)   #Moving Average Calculation
        
        list_speed_ms.append(speed_ms)                      #Add speed after pass Moving Average Calculation


for i in range(window_size):                                #length of list_speed_ms after pass filter will = raw_speed_ms - window size
    
    list_speed_ms.append(list_speed_ms[-1])                 #So will add the last speed to list_speed_ms to make the length = raw_speed_ms (for plot in same graph)


list_second = []                                            #Define list_second : X-axis is time(second)
second = 0.0                                                #Define variable to keep the second time of each speed value in list
for i in range(len(list_speed_ms)):                         #Loop for make the time second of each speed
    
    sec_step = 60/len(list_speed_ms)                        #second step assume that all speed data kept in 60 sec. 

    second = second + sec_step                              #Sum the second evert time of for loop
    
    list_second.append(second)                              #Add second to list_second : list_second = [second of speed point[0] , second of speed point[1]]
    
# print(len(list_speed_ms))                                 #...........length of data in X-axis must equal data in Y-xis...........#
# print(len(raw_speed_ms))                                  #........... if not qual cannot plot in same graph...........#
# print(len(list_second))                                   #...........length of data in X-axis must equal data in Y-xis...........#

plt.plot(list_second,raw_speed_ms,color='red',label='Raw')
plt.plot(list_second,list_speed_ms,color='blue',label='filter')
plt.title("Velocity of value = %d " %(value) )
plt.xlabel("Time (second)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.show() 

#ลองทำ km/hr ดู ถ้าติดตรงไหนก็ถามนะ