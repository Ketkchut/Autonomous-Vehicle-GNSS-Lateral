import pandas as pd 
import matplotlib.pyplot as plt 
import math
import numpy as np
import time 

FileData1 = 'trajectory_latlnglinear1.csv'
FileData2 = 'trajectory_UTMlinear1.csv'
FileData3 = 'result_CTElinear1AndYAW.csv'
x = []
y = []
with open (FileData3) as f:
    data_result = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
x = data_result.x
y = data_result.y

#ploting point 1 graph
plt.plot(y)
#name xy-axis
plt.xlabel('x-axis')
plt.ylabel('y-axis')
#giving title graph
plt.title('track latlng')

#====== Show graph ========
plt.show()
#==============================================
#==== PLot two graph together

# plt.plot(x1,y1, label = "line1") #plot line 1
# plt.plot(x2, y2, label = "line2") #plot line2

# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
# # giving a title to my graph
# plt.title('Two lines on same graph!')
 
# # show a legend on the plot
# plt.legend()
 
# # function to show the plot
# plt.show()

# #===== plot dash and point big======

# # plotting the points
# plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
#          marker='o', markerfacecolor='blue', markersize=12)
 
# # setting x and y axis range
# plt.ylim(1,8)
# plt.xlim(1,8)
 
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
 
# # giving a title to my graph
# plt.title('Some cool customizations!')
 
# # function to show the plot
# plt.show()

# #=================== Scatter plot * =============

# # plotting points as a scatter plot
# plt.scatter(x, y, label= "stars", color= "green",
#             marker= "*", s=30)
 
# # x-axis label
# plt.xlabel('x - axis')
# # frequency label
# plt.ylabel('y - axis')
# # plot title
# plt.title('My scatter plot!')
# # showing legend
# plt.legend()
 
# # function to show the plot
# plt.show()
# #=====================================
# #======= plot curve =====
# # setting the x - coordinates
# x = np.arange(0, 2*(np.pi), 0.1)
# # setting the corresponding y - coordinates
# y = np.sin(x)
 
# # plotting the points
# plt.plot(x, y)
 
# # function to show the plot
# plt.show()
#===================