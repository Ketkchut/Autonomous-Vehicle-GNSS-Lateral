import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

x1 = []
y1 = []
x2 = [] 
y2 =[]
ref_latlng ='ref_linear1_latlng.csv' #gps= lat,lng
ref_utm ='ref_linear1_utm.csv'       #utm = xnorth,yeast
#================= Reference Trajectory =========================================================
with open (ref_latlng) as f:
    ref_data = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')   #gps = lat,lng  
    
ref_lat = ref_data.x[:240]
ref_lng = ref_data.y[:240]
with open (ref_utm ) as f:
    ref_dataU = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
ref_xNorth = ref_dataU.x[:240]
ref_yEast = ref_dataU.y[:240]
#===========================Result ================================================================
FileData1 = 'left_CteYaw.csv'
with open (FileData1) as f:
    data_result1 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
cte = data_result1.x[:240]
yaw = data_result1.y[:240]

FileData3 = 'left_utm.csv'
with open (FileData3) as f:
    data_result3 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
xNorth = data_result3.x[:240]
yEast = data_result3.y[:240]

FileData2 = 'left_latlng.csv'
with open (FileData2) as f:
    data_result2 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')  #gps = lat,lng  
    
lat = data_result2.x[:240]
lng = data_result2.y[:240]

#==== PLot ref 
# fig, axs = plt.subplots(2)
# fig.suptitle('Tracking Trajectory1 ')
# axs[0].plot(lat,'r')  #, y1,'r'
# axs[1].plot(lng,'g')   #, -y2,'r'

# # naming the x axis
# plt.xlabel('Time (second)')
# # naming the y axis
# axs[0].set( ylabel='Latitude (Degree)')
# plt.ylabel('Longitude (Degree)')

#=========Plot CTE / YAW ======================================

fig, axs = plt.subplots(2)
fig.suptitle('Error of Tracking Trajectory1 ')
axs[0].plot(cte,'r')  #, y1,'r'
axs[1].plot(yaw,'g')   #, -y2,'r'

# naming the x axis
plt.xlabel('Time (second)')
# naming the y axis
axs[0].set( ylabel='CTE_left (Meter)')
plt.ylabel('Yaw_left (Degree)')



#==================================================

#==== Plot Real Track with Ref Track [2,2] four graph =====
fig, axs = plt.subplots(2, 2)
fig.suptitle('Tracking Trajectory Line1 From left ')
axs[0, 0].plot(lat ,label="Tracking on Latitude")
axs[0, 0].plot(ref_lat ,label="Reference Latitude")
axs[0, 0].legend()
axs[0, 0].set_title(' Latitude (degree)')
axs[0, 1].plot(xNorth,label="Tracking on UTM North" )
axs[0, 1].plot(ref_xNorth,label="Reference UTM North" )
axs[0, 1].legend()
axs[0, 1].set_title('UTM North (meter)')
axs[1, 0].plot(lng,label="Tracking on Longitude" )
axs[1, 0].plot(ref_lng,label="Reference Longitude" )
axs[1, 0].legend()
axs[1, 1].plot(yEast,label="Tracking on UTM East" )
axs[1, 1].plot(ref_yEast,label="Reference UTM East" )
axs[1, 1].legend()

for ax in axs.flat:
    ax.set(xlabel='Time(second)')
axs[1,0].set( ylabel='Longitude(Degree)')
axs[1,1].set( ylabel='UTM East (meter)')

#Hide x labels and tick labels for top plots and y ticks for left plots.

#========================================================
# giving a title to my graph
# plt.title('Linear1 ')
 
# show a legend on the plot
# plt.legend()
 
# function to show the plot
plt.show()
