from math import sin, sqrt
import math
import csv
from turtle import distance
import pandas as pd
import numpy as np
import mathplotlib.pyplot as plt

#รียกค่าพิกัดจากไฟล์ csv

WAYPOINTS_file = 'xy.csv'
waypoints_file = WAYPOINTS_file
with open (waypoints_file) as f:
    waypoints = pd.read_table(f, sep = ',', header = 0, name = ['x','y'])
    waypoints_np = np.array(waypoints)
    #print(waypoints_np)

#นำค่าพิกัดสองจุดแรกมาใช้
#พิกัดจุดที่ 1
pointx1 = waypoints_np [0][0]
pointy1 = waypoints_np [0][1]
point1  = [pointx1,pointy1]
print(pointx1,pointy1)

#พิกัดจุดที่ 2
pointx2 = waypoints_np [1][0]
pointy2 = waypoints_np [1][1]
point2  = [pointx2,pointy2]
print(pointx2,pointy2)


plt.scatter(point1[0],point1[1])
plt.scatter(point2[0],point2[1])
plt.show()

#คำนวณหา CTE
#1) สมการหาระยะห่างระหว่างจุดสองจุด
distance = []
distance.append(math.sqrt((pointx1-pointx2)**2 + (pointy1-pointy2)**2))
print('value distance is %f' %distance[0])

#2) หาสมการเส้นตรงของจุด A ไป B โดยสมการ y = mx + c
#หาความชัน m
m = (pointy2-pointy1)/(pointx2-pointx1)
print("slop is %f" %m)

#หาค่า c จาก c = y-mx
c = pointy1 - (m*pointx2)
# print('c id %f' %c)

#สมการเส้นตรงจากจุด A ไป B
car_position = [lat,lng]
carx = car_position[0]
cary = car_position[1]
# print(car_position[0])
# print(car_position[1])
# print('position of carx is %f' %carx)

#กำหนด A = m , B = -1
A = m
B = -1

#หาระยะทางจากจุด ไปยังเส้นตรง โดยกำหนดจุดของรถ คือ (15,110)--> *กำหนดจุดขึ้นมาเองเพื่อทดสอบหา CTE* ซึ่งหาจากสมการ CTE = abs(Ax + By + C) / sqrt(A**2 + B**2)
CTE = abs(A*carx + B*cary + c) / sqrt(A**2 + B**2)
print('CTE is %f' %CTE)

#คำนวณค่า CTE หลายๆจุด --> 1)ส่วนที่ระบุตำแหน่งปัจจุบันของรถ (update state) เองได้, 2)นำค่าที่ได้ไปใช้ในการสร้าง PID Controller




