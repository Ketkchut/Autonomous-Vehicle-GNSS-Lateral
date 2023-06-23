import pandas as pd
import matplotlib.pyplot as plt
import math
from statistics import mean
import csv

curve = 2

# plt.scatter(661478.35       ,1509700.25       ,color='red'    ,label='Max left')
# plt.scatter(661478.35       ,1509698.39  ,color='black'  ,label='reference')
# plt.scatter(661478.35       ,1509696.56      ,color='red'    ,label='Max right')

# plt.scatter(661433.35       ,1509703.28       ,color='green'    ,label='Max left')
# plt.scatter(661433.35       ,1509701.39   ,color='green'  ,label='reference')
# plt.scatter(661433.35       ,1509699.09      ,color='green'    ,label='Max right')

#...................................................................Set1.........................................................................#
set = 1
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
s1_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s1_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2

df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
s1_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s1_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2

df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))
s1_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s1_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s1_maxleft_east     ,s1_maxleft_north       ,color='red'    ,label='Max left')
plt.scatter(s1_ref_east         ,s1_ref_north           ,color='black'  ,label='reference')
plt.scatter(s1_maxright_east    ,s1_maxright_north      ,color='red'    ,label='Max right')

print(s1_maxleft_east     ,s1_maxleft_north)
print(s1_ref_east         ,s1_ref_north)
print(s1_maxright_east    ,s1_maxright_north)


#...................................................................Set2.........................................................................#
set = 2
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
s2_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s2_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2

df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
s2_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s2_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2

df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))
s2_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s2_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s2_maxleft_east     ,s2_maxleft_north       ,color='red'    ,label='Max left')
plt.scatter(s2_ref_east         ,s2_ref_north           ,color='black'  ,label='reference')
plt.scatter(s2_maxright_east    ,s2_maxright_north      ,color='red'    ,label='Max right')


#...................................................................Set3.........................................................................#
set = 3
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
s3_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s3_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2

df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
s3_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s3_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2

df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))
s3_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s3_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s3_maxleft_east     ,s3_maxleft_north       ,color='red'    ,label='Max left')
plt.scatter(s3_ref_east         ,s3_ref_north           ,color='black'  ,label='reference')
plt.scatter(s3_maxright_east    ,s3_maxright_north      ,color='red'    ,label='Max right')

#...................................................................Set4.........................................................................#
set = 4
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
s4_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s4_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2

df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
s4_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s4_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2

df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))
s4_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s4_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s4_maxleft_east     ,s4_maxleft_north       ,color='red'    ,label='Max left')
plt.scatter(s4_ref_east         ,s4_ref_north           ,color='black'  ,label='reference')
plt.scatter(s4_maxright_east    ,s4_maxright_north      ,color='red'    ,label='Max right')


#...................................................................Set5.........................................................................#
set = 5
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
s5_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s5_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2

df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
s5_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s5_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2

df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))
s5_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s5_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s5_maxleft_east     ,s5_maxleft_north       ,color='red'    ,label='Max left')
plt.scatter(s5_ref_east         ,s5_ref_north           ,color='black'  ,label='reference')
plt.scatter(s5_maxright_east    ,s5_maxright_north      ,color='red'    ,label='Max right')

# plt.scatter(661375.266    ,1509653.566      ,color='green'    ,label='Max left')
# plt.scatter(661379.266        ,1509653.566           ,color='green'  ,label='reference')
# plt.scatter(661383.266    ,1509653.566      ,color='green'    ,label='Max right')

# plt.scatter(661375.266    ,1509560.566      ,color='red'    ,label='Max left')
# plt.scatter(661379.254        ,1509560.566           ,color='black'  ,label='reference')
# plt.scatter(661383.266    ,1509560.566      ,color='red'    ,label='Max right')







# plt.legend()
plt.title('Curve2(RAW)')
plt.show() 



#...................................................................CreateCSV.........................................................................#

# value = s8_maxleft_east, s8_maxleft_north, s8_minleft15_east, s8_minleft15_north, s8_ref_east, s8_ref_north, s8_minright15_east, s8_minright15_north, s8_maxright_east, s8_maxright_north
# name_column = 's8_maxleft_east, s8_maxleft_north, s8_minleft15_east, s8_minleft15_north, s8_ref_east, s8_ref_north, s8_minright15_east, s8_minright15_north, s8_maxright_east, s8_maxright_north'

# name = 'Curve4_set8.csv'

# csv_name = 0
# Data = []
# if csv_name == 0:

#     for i in range(len(name_column.split(' ,'))):
#             Data.append(name_column.split(' ,')[i])
#     print(Data)
        
#     with open(name, 'a',newline='') as f:
#         writer = csv.writer(f,delimiter=",")
#         writer.writerow(Data) 
#         csv_name = 1    
    
# if csv_name == 1:
    
#     Data = value  
#     print(Data)    
    
#     with open(name, 'a',newline='') as f:
#         writer = csv.writer(f,delimiter=",")
#         writer.writerow(Data) 
#         csv_name = 1


# print(s7_maxleft_east ,s7_maxleft_north ,s7_minleft15_east ,s7_minleft15_north ,s7_ref_east ,s7_ref_north ,s7_minright15_east ,s7_minright15_north ,s7_maxright_east ,s7_maxright_north)