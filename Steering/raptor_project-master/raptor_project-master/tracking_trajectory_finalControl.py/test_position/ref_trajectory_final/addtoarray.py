
import pandas as pd
import csv 
ref_x =[]
ref_y = [] 
with open ('ref_linear1_latlng.csv') as f:
    map_df = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')

ref_x = map_df.x
ref_y = map_df.y

for i in range(300):
    lat_ref = int(ref_x)
    lng_ref = int(ref_y)
    data1 = lat_ref,lng_ref
    with open('arary_1.csv', 'a', newline='') as f:  
        writer = csv.writer(f,delimiter=",")    
        writer.writerow(data1) 