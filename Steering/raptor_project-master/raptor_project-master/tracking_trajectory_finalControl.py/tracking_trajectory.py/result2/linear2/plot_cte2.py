import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

x1 = []
y1 = []
x2 = [] 
y2 =[]

#===========================Result ================================================================

FileData1 = '2_center_CteYaw.csv'
with open (FileData1) as f:
    data_result1 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
cte1 = data_result1.x[:240]
yaw1 = data_result1.y

FileData3 = '2_left_CteYaw.csv'
with open (FileData3) as f:
    data_result2 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
cte2 = data_result2.x[:240]
yaw2 = data_result2.y

FileData2 = '2_right_CteYaw.csv'
with open (FileData2) as f:
    data_result3 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
cte3 = data_result3.x[:240]
yaw3 = data_result3.y

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

fig, axs = plt.subplots(3)
fig.suptitle('Error of Tracking Trajectory2 ')
axs[0].plot(cte1,label="cte1")  #, y1,'r'
axs[1].plot(cte2,'g')   #, -y2,'r'
axs[2].plot(cte3,'y')   #, -y2,'r'
# naming the x axis
plt.xlabel('Time (second)')
# naming the y axis
axs[0].set( ylabel='CTE1_Center (Meter)')
axs[1].set( ylabel='CTE2_Left (Meter)')
plt.ylabel('CTE3_Right (Meter)')



#==================================================

#========================================================
# giving a title to my graph
# plt.title('Linear1 ')
 
# show a legend on the plot
plt.legend()
 
# function to show the plot
plt.show()
