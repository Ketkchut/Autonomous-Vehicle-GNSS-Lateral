import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##########################################################  #NetworkRTK#  ##########################################################

per_fix = [0,0,0,0,0,0]
per_float = [0,0,0,0,0,0]
per_DGNSS = [0,0,0,0,0,0]
per_other = [0,0,0,0,0,0]

GGA1 = pd.read_csv('Reference2_NetworkRTK/GGA_Network01.csv')
GGA2 = pd.read_csv('Reference2_NetworkRTK/GGA_Network02.csv')
GGA3 = pd.read_csv('Reference2_NetworkRTK/GGA_Network03.csv')
GGA4 = pd.read_csv('Reference2_NetworkRTK/GGA_Network04.csv')
GGA5 = pd.read_csv('Reference2_NetworkRTK/GGA_Network05.csv')
GGA6 = pd.read_csv('Reference2_NetworkRTK/GGA_Network06.csv')

################################################  #Round1#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA1.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[0] = (count_fix/Total)*100
per_float[0] = (count_float/Total)*100
per_DGNSS[0] = (count_DGNSS/Total)*100
per_other[0] = (count_other/Total)*100

################################################  #Round2#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA2.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[1] = (count_fix/Total)*100
per_float[1] = (count_float/Total)*100
per_DGNSS[1] = (count_DGNSS/Total)*100
per_other[1] = (count_other/Total)*100

################################################  #Round3#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA3.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[2] = (count_fix/Total)*100
per_float[2] = (count_float/Total)*100
per_DGNSS[2] = (count_DGNSS/Total)*100
per_other[2] = (count_other/Total)*100

################################################  #Round4#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA4.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[3] = (count_fix/Total)*100
per_float[3] = (count_float/Total)*100
per_DGNSS[3] = (count_DGNSS/Total)*100
per_other[3] = (count_other/Total)*100

################################################  #Round5#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA5.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[4] = (count_fix/Total)*100
per_float[4] = (count_float/Total)*100
per_DGNSS[4] = (count_DGNSS/Total)*100
per_other[4] = (count_other/Total)*100

################################################  #Round6#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA6.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix + count_float +count_DGNSS + count_other
per_fix[5] = (count_fix/Total)*100
per_float[5] = (count_float/Total)*100
per_DGNSS[5] = (count_DGNSS/Total)*100
per_other[5] = (count_other/Total)*100

################################################  #visualize#  ################################################
print(per_fix)
print(per_float)
print(per_DGNSS)

plt.plot(np.array(per_fix),label='Percent FIXED (1 Boards)', lw=1.5, marker = '.',color='green')
for x,y in zip(np.arange(0,len(per_fix),1),np.array(per_fix)):

    label = "{:.2f}".format(y)

    if (x < 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,-15), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)
    if (x >= 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,15), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)          
   
plt.plot(np.array(per_float),label='Percent FLOAT (1 Boards)', lw=1.5, marker = '.',color='red')
for x,y in zip(np.arange(0,len(per_float),1),np.array(per_float)):

    label = "{:.2f}".format(y)

    if (x < 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)       
    if (x >= 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,-15), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)
        
# plt.plot(np.array(per_DGNSS),label='Percent DGNSS (2 Boards)', lw=1.5, marker = '.',color='black')
# for x,y in zip(np.arange(0,len(per_DGNSS),1),np.array(per_DGNSS)):

#     label = "{:.2f}".format(y)

#     plt.annotate(label, # this is the text
#                  (x,y), # these are the coordinates to position the label
#                  textcoords="offset points", # how to position the text
#                  xytext=(0,10), # distance from text to points (x,y)
#                  ha='center',# horizontal alignment can be left, right or center
#                  size=9) 
    
if count_other > 0:
    plt.plot(np.array(per_other),label='Percent Other (1 Boards)', lw=1, marker = 'o')
    print(per_other)

plt.xticks(np.arange(len(per_fix)), np.arange(1, len(per_fix)+1))
plt.ylim(-10,110)
plt.ylabel('Percent Accuracy %') 
plt.xlabel('Round') 
plt.title("Measuremant Accuracy for NetworkRTK (Aroud Soccer field)")
plt.legend()
#plt.show() 



##########################################################  #RTK#  ##########################################################

per_fix = [0,0,0,0,0,0]
per_float = [0,0,0,0,0,0]
per_DGNSS = [0,0,0,0,0,0]
per_other = [0,0,0,0,0,0]

GGA1 = pd.read_csv('Reference2_RTK/GGA_RTK01.csv')
GGA2 = pd.read_csv('Reference2_RTK/GGA_RTK02.csv')
GGA3 = pd.read_csv('Reference2_RTK/GGA_RTK03.csv')
GGA4 = pd.read_csv('Reference2_RTK/GGA_RTK04.csv')
GGA5 = pd.read_csv('Reference2_RTK/GGA_RTK05.csv')
GGA6 = pd.read_csv('Reference2_RTK/GGA_RTK06.csv')

################################################  #Round1#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA1.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[0] = (count_fix/Total)*100
per_float[0] = (count_float/Total)*100
per_DGNSS[0] = (count_DGNSS/Total)*100
per_other[0] = (count_other/Total)*100

################################################  #Round2#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA2.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[1] = (count_fix/Total)*100
per_float[1] = (count_float/Total)*100
per_DGNSS[1] = (count_DGNSS/Total)*100
per_other[1] = (count_other/Total)*100

################################################  #Round3#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA3.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[2] = (count_fix/Total)*100
per_float[2] = (count_float/Total)*100
per_DGNSS[2] = (count_DGNSS/Total)*100
per_other[2] = (count_other/Total)*100

################################################  #Round4#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA4.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[3] = (count_fix/Total)*100
per_float[3] = (count_float/Total)*100
per_DGNSS[3] = (count_DGNSS/Total)*100
per_other[3] = (count_other/Total)*100

################################################  #Round5#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA5.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix+count_float+count_DGNSS+count_other
per_fix[4] = (count_fix/Total)*100
per_float[4] = (count_float/Total)*100
per_DGNSS[4] = (count_DGNSS/Total)*100
per_other[4] = (count_other/Total)*100

################################################  #Round6#  ################################################
quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0
for index, row in GGA6.iterrows():
    #print('The quallity is {0}'.format(row['QUALITY']))
    
    quality =  int(format(row['QUALITY']))
    if quality > 0:
        count_quality = count_quality+1
    if quality == 4:
        count_fix = count_fix+1
    if quality == 5:
        count_float = count_float+1
    if quality == 2:
        count_DGNSS = count_DGNSS+1    
    if quality != 2 and quality != 4 and quality != 5:
        print(index,quality)
        count_other = count_other+1
Total = count_fix + count_float +count_DGNSS + count_other
per_fix[5] = (count_fix/Total)*100
per_float[5] = (count_float/Total)*100
per_DGNSS[5] = (count_DGNSS/Total)*100
per_other[5] = (count_other/Total)*100

################################################  #visualize#  ################################################
print(per_fix)
print(per_float)
print(per_DGNSS)

plt.plot(np.array(per_fix),label='Percent FIXED (2 Board)', lw=1.5, marker = '.',linestyle='--',color='green')
for x,y in zip(np.arange(0,len(per_fix),1),np.array(per_fix)):

    label = "{:.2f}".format(y)

    if (x < 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,-15), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)
    if (x >= 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,15), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)          
   
plt.plot(np.array(per_float),label='Percent FLOAT (2 Board)', lw=1.5, marker = '.',linestyle='--',color='red')
for x,y in zip(np.arange(0,len(per_float),1),np.array(per_float)):

    label = "{:.2f}".format(y)

    if (x < 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)       
    if (x >= 4):
        plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,-15), # distance from text to points (x,y)
                 ha='center',# horizontal alignment can be left, right or center
                 size=9)
        
# plt.plot(np.array(per_DGNSS),label='Percent DGNSS (1 Board)', lw=1.5, marker = '.',linestyle='--',color='black')
# for x,y in zip(np.arange(0,len(per_DGNSS),1),np.array(per_DGNSS)):

#     label = "{:.2f}".format(y)

#     plt.annotate(label, # this is the text
#                  (x,y), # these are the coordinates to position the label
#                  textcoords="offset points", # how to position the text
#                  xytext=(0,10), # distance from text to points (x,y)
#                  ha='center',# horizontal alignment can be left, right or center
#                  size=9) 
    
if count_other > 0:
    plt.plot(np.array(per_other),label='Percent Other (2 Board)', lw=1, marker = 'o',linestyle='--')
    print(per_other)

plt.xticks(np.arange(len(per_fix)), np.arange(1, len(per_fix)+1))
plt.ylim(-10,110)
plt.ylabel('Percent Accuracy %') 
plt.xlabel('Round') 
plt.title("Measuremant Quality Comparison (Aroud Soccer field)")
plt.legend()
plt.show() 