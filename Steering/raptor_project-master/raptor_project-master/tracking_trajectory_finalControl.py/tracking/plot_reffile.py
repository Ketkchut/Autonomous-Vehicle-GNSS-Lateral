import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


x1 = []
y1 = []
x2 = [] 
y2 =[]
FileData3 = 'refLinearCurve_latlng.csv'
with open (FileData3) as f:
    data_result1 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
x1 = data_result1.x
y1 = data_result1.y

FileData2 = 'ref_linear2_UTM.csv'
with open (FileData2) as f:
    data_result2 = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
x2 = data_result2.x
y2 = data_result2.y
#==== PLot two graph together
fig, axs = plt.subplots(2)
fig.suptitle('Reference trajectory linear1-LatLng')
axs[0].plot(x1,'b')  #, y1,'r'
axs[1].plot(y1,'r')   #, -y2,'r'

# plt.plot(x1,'r' ) #plot line 1
# plt.plot(y1,'b' ) #plot line2

# naming the x axis
plt.xlabel('Time (second)')
# naming the y axis
axs[0].set( ylabel='x-axis-North')
plt.ylabel('y - axis-East')
# giving a title to my graph
plt.title('Linear1 ')
 
# show a legend on the plot
plt.legend()
 
# function to show the plot
plt.show()
