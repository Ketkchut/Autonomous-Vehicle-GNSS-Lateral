import pandas as pd

quality = 0
count_quality = 0
count_fix = 0
count_float = 0
count_DGNSS = 0
count_other = 0

GGA = pd.read_csv('GGA_Frame_FootballField.csv')
for index, row in GGA.iterrows():
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
per_fix = (count_fix/Total)*100
per_float = (count_float/Total)*100
per_DGNSS = (count_DGNSS/Total)*100
per_other = (count_other/Total)*100

print('Sample = ',count_quality)        
print('RTK FIXED Quality = ',count_fix,' Sample')
print('RTK FLOAT Quality = ',count_float,' Sample')
print('RTK DGNSS Quality = ',count_DGNSS,' Sample')

if count_other > 0:
    print('Other Quality = ',count_other,' Sample')
    
print('Total Quality = ',Total,' Sample')

print('RTK FIXED Quality = ',round(per_fix,2), '%')
print('RTK float Quality = ',round(per_float,2), '%')
print('RTK DGNSS Quality = ',round(per_DGNSS,2), '%')

if count_other > 0:
    print('Other Quality = ',round(per_other,2), '%')
