import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

# Velocity Single Plot from lat/lon (lat/lon with out filter)

df = pd.read_csv("/Users/sorravee/Desktop/project/speed/Velocity_Openloop_Plot/forward_220465/value_84.csv")                     

time = df.time_operate
raw_speed = df.raw_speed
filter_speed = df.filter_speed


plt.plot(time,raw_speed,color='red',label='Raw')
plt.plot(time,filter_speed,color='blue',label='filter')
plt.xlabel("Time (second)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.show() 



