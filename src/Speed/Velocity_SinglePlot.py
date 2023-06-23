import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

# Velocity Single Plot from lat/lon (lat/lon with out filter)

# df = pd.read_csv("backward_240465/value_b_140.csv")   
# df = pd.read_csv("forward_220465/value_132.csv")      

df = pd.read_csv("test_f_180.csv")            

time = df.time_operate
raw_speed = df.raw_speed
filter_speed = df.filter_speed
raw_speed_filter = df.raw_speed_filter


plt.plot(time,raw_speed ,color='red',label='Raw')
plt.plot(time,filter_speed ,color='blue',label='filter')
plt.plot(time,raw_speed_filter ,color='green',label='filter')
plt.xlabel("Time (second)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.show() 



