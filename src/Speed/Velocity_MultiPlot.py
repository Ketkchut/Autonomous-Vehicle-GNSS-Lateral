import pandas as pd
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
from statistics import mean

# Velocity Multiple Plot from lat/lon (lat/lon with out filter)      !! look Single plot before

df_1 = pd.read_csv('value_70.csv')
value_1 = 70

df_2 = pd.read_csv('value_115.csv')
value_2 = 115

df_3 = pd.read_csv('value_155.csv')
value_3 = 155

df_4 = pd.read_csv('value_185.csv')
value_4 = 185

window_size = 20

Mean = []

#................................................................ value1 ...........................................................#

raw_speed_ms = df_1.speed_ms
raw_speed_kmhr = df_1.speed_kmhr

speed_ms_buff = []
sum_speed_ms = 0.0
list_speed_ms = []
for i in range(len(raw_speed_ms)):
    speed_ms_buff.append(raw_speed_ms[i])
    sum_speed_ms = sum_speed_ms + raw_speed_ms[i]
    
    if len(speed_ms_buff) > window_size:
        sum_speed_ms = sum_speed_ms - speed_ms_buff.pop(0)
        speed_ms = float(sum_speed_ms)/len(speed_ms_buff)
        list_speed_ms.append(speed_ms)
        
for i in range(window_size):
    list_speed_ms.append(list_speed_ms[-1])

Mean.append(mean(list_speed_ms)) 

list_second = []
second = 0.0
for i in range(len(list_speed_ms)):
    sec_step = 60/len(list_speed_ms)
    second = second + sec_step
    list_second.append(second)
    
# Create 2x2 sub plots
gs = gridspec.GridSpec(2, 2)
pl.figure()
pl.suptitle('Velocity Calculation from Latitude/Longitude ')
ax = pl.subplot(gs[0, 0]) # row 0, col 0
pl.plot(list_second,raw_speed_ms,color='red',label='Raw')
pl.plot(list_second,list_speed_ms,color='blue',label='filter')
pl.title("Velocity when value = %d " %(value_1))
pl.xlabel("Time(second)")
pl.ylabel("Velocity (m/s)")
pl.legend()


#................................................................ value2 ...........................................................#

raw_speed_ms = df_2.speed_ms
raw_speed_kmhr = df_2.speed_kmhr

speed_ms_buff = []
sum_speed_ms = 0.0
list_speed_ms = []
for i in range(len(raw_speed_ms)):
    speed_ms_buff.append(raw_speed_ms[i])
    sum_speed_ms = sum_speed_ms + raw_speed_ms[i]
    
    if len(speed_ms_buff) > window_size:
        sum_speed_ms = sum_speed_ms - speed_ms_buff.pop(0)
        speed_ms = float(sum_speed_ms)/len(speed_ms_buff)
        list_speed_ms.append(speed_ms)

for i in range(window_size):
    list_speed_ms.append(list_speed_ms[-1])
    
Mean.append(mean(list_speed_ms)) 

list_second = []
second = 0.0
for i in range(len(list_speed_ms)):
    sec_step = 60/len(list_speed_ms)
    second = second + sec_step
    list_second.append(second)

ax = pl.subplot(gs[0, 1]) # row 0, col 1
pl.plot(list_second,raw_speed_ms,color='red',label='Raw')
pl.plot(list_second,list_speed_ms,color='blue',label='filter')
pl.title("Velocity when value = %d " %(value_2))
pl.xlabel("Time(second)")
pl.ylabel("Velocity (m/s)")
pl.legend()


#................................................................ value3 ...........................................................#

raw_speed_ms = df_3.speed_ms
raw_speed_kmhr = df_3.speed_kmhr

speed_ms_buff = []
sum_speed_ms = 0.0
list_speed_ms = []
for i in range(len(raw_speed_ms)):
    speed_ms_buff.append(raw_speed_ms[i])
    sum_speed_ms = sum_speed_ms + raw_speed_ms[i]
    
    if len(speed_ms_buff) > window_size:
        sum_speed_ms = sum_speed_ms - speed_ms_buff.pop(0)
        speed_ms = float(sum_speed_ms)/len(speed_ms_buff)
        list_speed_ms.append(speed_ms)  

for i in range(window_size):
    list_speed_ms.append(list_speed_ms[-1])
    
Mean.append(mean(list_speed_ms))        

list_second = []
second = 0.0
for i in range(len(list_speed_ms)):
    sec_step = 60/len(list_speed_ms)
    second = second + sec_step
    list_second.append(second)

ax = pl.subplot(gs[1, 0]) # row 1, col 0
pl.plot(list_second,raw_speed_ms,color='red',label='Raw')
pl.plot(list_second,list_speed_ms,color='blue',label='filter')
pl.title("Velocity when value = %d " %(value_3))
pl.xlabel("Time(second)")
pl.ylabel("Velocity (m/s)")
pl.legend()


#................................................................ value4 ...........................................................#

raw_speed_ms = df_4.speed_ms
raw_speed_kmhr = df_4.speed_kmhr

speed_ms_buff = []
sum_speed_ms = 0.0
list_speed_ms = []
for i in range(len(raw_speed_ms)):
    speed_ms_buff.append(raw_speed_ms[i])
    sum_speed_ms = sum_speed_ms + raw_speed_ms[i]
    
    if len(speed_ms_buff) > window_size:
        sum_speed_ms = sum_speed_ms - speed_ms_buff.pop(0)
        speed_ms = float(sum_speed_ms)/len(speed_ms_buff)
        list_speed_ms.append(speed_ms)

for i in range(window_size):
    list_speed_ms.append(list_speed_ms[-1])

Mean.append(mean(list_speed_ms))  

list_second = []
second = 0.0
for i in range(len(list_speed_ms)):
    sec_step = 60/len(list_speed_ms)
    second = second + sec_step
    list_second.append(second)

ax = pl.subplot(gs[1, 1]) # row 1, col 1
pl.plot(list_second,raw_speed_ms,color='red',label='Raw')
pl.plot(list_second,list_speed_ms,color='blue',label='filter')
pl.title("Velocity when value = %d " %(value_4))
pl.xlabel("Time(second)")
pl.ylabel("Velocity (m/s)")
pl.legend()
# pl.show()

print(Mean)