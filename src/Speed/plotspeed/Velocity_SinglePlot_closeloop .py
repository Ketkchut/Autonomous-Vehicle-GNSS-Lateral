import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
# Velocity Single Plot from lat/lon (lat/lon with out filter)

df_1 = pd.read_csv("plotspeed/testspeed_r_5km_1.csv")                     
time_1 = df_1.Speed_time
SpeedKmperhr_1 = df_1.Speed_velocity
Digitalpoten_1 = df_1.Speed_adjust
error_1 = df_1.Speed_error
timebuffer_1 = []
errorbuffer_1 = []
digitalpotenbuffer_1 = []
speedbuffer_1 = []

for i in range(len(time_1)):
    if  time_1[i] < 2455 :
        timebuffer_1.append(time_1[i])
        errorbuffer_1.append(error_1[i])
        digitalpotenbuffer_1.append(Digitalpoten_1[i])
        speedbuffer_1.append(SpeedKmperhr_1[i])

df_2 = pd.read_csv("plotspeed/testspeed_r_5km_2.csv")                     
time_2 = df_2.Speed_time
SpeedKmperhr_2 = df_2.Speed_velocity
Digitalpoten_2 = df_2.Speed_adjust
error_2 = df_2.Speed_error
timebuffer_2 = []
errorbuffer_2 = []
digitalpotenbuffer_2 = []
speedbuffer_2 = []

for i in range(len(time_2)):
    if time_2[i]< 2455:
        timebuffer_2.append(time_2[i])
        errorbuffer_2.append(error_2[i])
        digitalpotenbuffer_2.append(Digitalpoten_2[i])
        speedbuffer_2.append(SpeedKmperhr_2[i])

df_3 = pd.read_csv("plotspeed/testspeed_r_5km_3.csv")                     
time_3 = df_3.Speed_time
SpeedKmperhr_3 = df_3.Speed_velocity
Digitalpoten_3 = df_3.Speed_adjust
error_3 = df_3.Speed_error
timebuffer_3 = []
errorbuffer_3 = []
digitalpotenbuffer_3 = []
speedbuffer_3 = []

for i in range(len(time_1)):
    
    if time_1[i] < 2455:
        timebuffer_3.append(time_3[i])
        errorbuffer_3.append(error_3[i])
        digitalpotenbuffer_3.append(Digitalpoten_3[i])
        speedbuffer_3.append(SpeedKmperhr_3[i])

speedset = (5)


# plt.plot(time_1,speedset,color='green',label='speedsetpoint')
plt.plot(time_1,SpeedKmperhr_1,color='red',label='speed1')
# plt.plot(time_2,SpeedKmperhr_2,color='blue',label='speed2')
plt.plot(time_3,SpeedKmperhr_3,color='black',label='speed3')
plt.ylabel("Velocity (m/s)")

# plt.plot(timebuffer_1,errorbuffer_1,color='red',label='error1')
# plt.plot(timebuffer_2,errorbuffer_2,color='blue',label='error2')
# plt.plot(timebuffer_3,errorbuffer_3,color='black',label='error3')
# plt.ylabel("error ")

# plt.plot(timebuffer_1,digitalpotenbuffer_1,color='red',label='Digitalpoten1')
# plt.plot(timebuffer_2,digitalpotenbuffer_2,color='blue',label='Digitalpoten2')
# plt.plot(timebuffer_3,digitalpotenbuffer_3,color='black',label='Digitalpoten3')
# plt.ylabel("digitalpoten ")

plt.xlabel("TIme (sec)")
plt.legend()
plt.show() 



