import pandas as pd
import matplotlib.pyplot as plt
import math
from statistics import mean

df1 = pd.read_csv("Linear_NS/linear_NS_ref_1.csv")
df2 = pd.read_csv("Linear_NS/linear_NS_ref_2.csv")
df3 = pd.read_csv("Linear_NS/linear_NS_ref_3.csv")
df4 = pd.read_csv("Linear_NS/linear_NS_ref_4.csv")
# time = df1["time_operate"]
x_east = df4["x_east"]
y_north = df4["y_north"]
n = len(x_east)

print("Start = ",x_east[0],y_north[0])
print("Stop = ",x_east[n-1],y_north[n-1])

print(mean(x_east))
print(mean(y_north))
plt.plot(x_east,y_north)
plt.xlabel("UTM_X")
plt.ylabel("UTM_Y")
# # plt.legend()
plt.show() 





















