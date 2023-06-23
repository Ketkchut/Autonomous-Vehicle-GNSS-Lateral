import pandas as pd
import matplotlib.pyplot as plt
import math
from statistics import mean
import csv

curve = 1

#...................................................................Set1.........................................................................#
set = 1
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
s1_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s1_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2


df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
s1_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s1_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2


df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
s1_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s1_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2


df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
s1_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s1_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2


df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))
s1_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s1_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s1_maxleft_east     ,s1_maxleft_north       ,color='red'    ,label='Max left')
# plt.scatter(s1_minleft15_east   ,s1_minleft15_north     ,color='blue'   ,label='Min left')
plt.scatter(s1_ref_east         ,s1_ref_north           ,color='black'  ,label='reference')
# plt.scatter(s1_minright15_east  ,s1_minright15_north    ,color='blue'   ,label='Min right')
plt.scatter(s1_maxright_east    ,s1_maxright_north      ,color='red'    ,label='Max right')


#...................................................................Set2.........................................................................#
set = 2
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))

s2_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s2_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2
s2_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s2_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2
s2_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s2_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2
s2_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s2_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2
s2_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s2_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s2_maxleft_east     ,s2_maxleft_north       ,color='red')
# plt.scatter(s2_minleft15_east   ,s2_minleft15_north     ,color='blue')
plt.scatter(s2_ref_east         ,s2_ref_north           ,color='black')
# plt.scatter(s2_minright15_east  ,s2_minright15_north    ,color='blue')
plt.scatter(s2_maxright_east    ,s2_maxright_north      ,color='red')


#...................................................................Set3.........................................................................#
set = 3
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))

s3_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s3_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2
s3_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s3_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2
s3_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s3_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2
s3_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s3_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2
s3_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s3_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s3_maxleft_east     ,s3_maxleft_north       ,color='red')
# plt.scatter(s3_minleft15_east   ,s3_minleft15_north     ,color='blue')
plt.scatter(s3_ref_east         ,s3_ref_north           ,color='black')
# plt.scatter(s3_minright15_east  ,s3_minright15_north    ,color='blue')
plt.scatter(s3_maxright_east    ,s3_maxright_north      ,color='red')


#...................................................................Set4.........................................................................#
set = 4
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))

s4_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s4_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2
s4_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s4_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2
s4_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s4_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2
s4_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s4_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2
s4_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s4_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s4_maxleft_east     ,s4_maxleft_north       ,color='red')
# plt.scatter(s4_minleft15_east   ,s4_minleft15_north     ,color='blue')
plt.scatter(s4_ref_east         ,s4_ref_north           ,color='black')
# plt.scatter(s4_minright15_east  ,s4_minright15_north    ,color='blue')
plt.scatter(s4_maxright_east    ,s4_maxright_north      ,color='red')


#...................................................................Set5.........................................................................#
set = 5
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))

s5_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s5_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2
s5_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s5_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2
s5_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s5_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2
s5_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s5_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2
s5_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s5_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s5_maxleft_east     ,s5_maxleft_north       ,color='red')
# plt.scatter(s5_minleft15_east   ,s5_minleft15_north     ,color='blue')
plt.scatter(s5_ref_east         ,s5_ref_north           ,color='black')
# plt.scatter(s5_minright15_east  ,s5_minright15_north    ,color='blue')
plt.scatter(s5_maxright_east    ,s5_maxright_north      ,color='red')


#...................................................................Set6.........................................................................#
set = 6
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))

s6_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s6_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2
s6_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s6_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2
s6_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s6_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2
s6_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s6_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2
s6_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s6_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s6_maxleft_east     ,s6_maxleft_north       ,color='red')
# plt.scatter(s6_minleft15_east   ,s6_minleft15_north     ,color='blue')
plt.scatter(s6_ref_east         ,s6_ref_north           ,color='black')
# plt.scatter(s6_minright15_east  ,s6_minright15_north    ,color='blue')
plt.scatter(s6_maxright_east    ,s6_maxright_north      ,color='red')


#...................................................................Set7.........................................................................#
set = 7
df_mxl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_1.csv" %(curve,set,curve,set))
df_mxl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXLEFT_2.csv" %(curve,set,curve,set))
df_mnl_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_1.csv" %(curve,set,curve,set))
df_mnl_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINLEFT15_2.csv" %(curve,set,curve,set))
df_ref_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_1.csv" %(curve,set,curve,set))
df_ref_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_REF_2.csv" %(curve,set,curve,set))
df_mnr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_1.csv" %(curve,set,curve,set))
df_mnr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MINRIGHT15_2.csv" %(curve,set,curve,set))
df_mxr_1 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_1.csv" %(curve,set,curve,set))
df_mxr_2 = pd.read_csv("Curve%d/Set%d/C%d_S%d_MAXRIGHT_2.csv" %(curve,set,curve,set))

s7_maxleft_east = ( mean(df_mxl_1['x_east']) + mean(df_mxl_2['x_east']) ) /2
s7_maxleft_north = ( mean(df_mxl_1['y_north']) + mean(df_mxl_2['y_north']) ) /2
s7_minleft15_east = ( mean(df_mnl_1['x_east']) + mean(df_mnl_2['x_east']) ) /2
s7_minleft15_north = ( mean(df_mnl_1['y_north']) + mean(df_mnl_2['y_north']) ) /2
s7_ref_east = ( mean(df_ref_1['x_east']) + mean(df_ref_2['x_east']) ) /2
s7_ref_north = ( mean(df_ref_1['y_north']) + mean(df_ref_2['y_north']) ) /2
s7_minright15_east = ( mean(df_mnr_1['x_east']) + mean(df_mnr_2['x_east']) ) /2
s7_minright15_north = ( mean(df_mnr_1['y_north']) + mean(df_mnr_2['y_north']) ) /2
s7_maxright_east = ( mean(df_mxr_1['x_east']) + mean(df_mxr_2['x_east']) ) /2
s7_maxright_north = ( mean(df_mxr_1['y_north']) + mean(df_mxr_2['y_north']) ) /2

plt.scatter(s7_maxleft_east     ,s7_maxleft_north       ,color='red')
# plt.scatter(s7_minleft15_east   ,s7_minleft15_north     ,color='blue')
plt.scatter(s7_ref_east         ,s7_ref_north           ,color='black')
# plt.scatter(s7_minright15_east  ,s7_minright15_north    ,color='blue')
plt.scatter(s7_maxright_east    ,s7_maxright_north      ,color='red')

plt.title('Curve1(Raw)')
plt.legend()
plt.show() 


#...................................................................CreateCSV.........................................................................#

# value = s7_maxleft_east ,s7_maxleft_north ,s7_minleft15_east ,s7_minleft15_north ,s7_ref_east ,s7_ref_north ,s7_minright15_east ,s7_minright15_north ,s7_maxright_east ,s7_maxright_north
# name_column = 's7_maxleft_east ,s7_maxleft_north ,s7_minleft15_east ,s7_minleft15_north ,s7_ref_east ,s7_ref_north ,s7_minright15_east ,s7_minright15_north ,s7_maxright_east ,s7_maxright_north'

# name = 'Curve1_set7.csv'

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


print(s7_maxleft_east ,s7_maxleft_north ,s7_minleft15_east ,s7_minleft15_north ,s7_ref_east ,s7_ref_north ,s7_minright15_east ,s7_minright15_north ,s7_maxright_east ,s7_maxright_north)