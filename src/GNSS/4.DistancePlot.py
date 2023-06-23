import geopy.distance
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('liner_lat.csv')
Avg_lat = df["Lat"].mean()
Avg_lon = df['Lon'].mean()
Moving_Avg_Lat = df['Lat'].rolling(3).mean()

list = []
distance = []
for i, row in df.iterrows():
    list.append(row['Lat'])
    list.append(row['Lon'])

coordinate_list = []    
for n in range(len(list)):
    if n%2 == 0:
        ref_point = (Avg_lat[n],list[n+1])
        coordinate = (Moving_Avg_Lat[n],list[n+1])
        coordinate_list.append(coordinate)
        distance.append(((geopy.distance.distance(ref_point,coordinate).m))*100)

print(Moving_Avg_Lat)        
print(len(distance))

plt.plot(distance, color='blue',mfc='pink' ) 
#plt.xticks(range(0,len(distance)+1, 1)) #set the tick frequency on x-axis

plt.ylabel('Distance Error (cm.)') 
plt.xlabel('Sample') 
plt.title("Measure Accuracy (Example)") 
plt.show() 