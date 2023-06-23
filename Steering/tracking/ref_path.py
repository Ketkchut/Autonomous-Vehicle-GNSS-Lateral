import matplotlib.pyplot as plt
import pandas as pd

x = []
y = []

# data = open('/home/autonomous/car_ws/src/autonomous_v/src/tracking/ref1_10_round_1.csv' , 'r')
ref_utm ='/home/autonomous/Desktop/raptor_project-master/raptor_project-master/tracking_path/refLinear_utm.csv'       #utm = xnorth,yeast  'copy path'

with open (ref_utm ) as f:
    ref_dataU = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')
    
ref_xNorth = ref_dataU.x
ref_yEast = ref_dataU.y

# for line in data:
#     lines = [i for i in line.split()]
#     x.append(float(lines[2]))
#     y.append(float(lines[3]))

print(ref_xNorth,ref_yEast)
plt.plot(ref_xNorth,ref_yEast)
plt.title('reference data test for tacking')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.show()

