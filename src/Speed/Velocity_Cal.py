from math import radians, cos, sin, asin, sqrt, atan2, degrees
import serial
import pynmea2
import csv

port = "COM6"     #port usb that connect rover in your computer
ser = serial.Serial(port, baudrate = 115200)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    d = c*r # Distance in km
    return round((d*1000),2) #Distance in m 


def calc_velocity(dist, time_start, time_end):

    s_now = time_end.second
    ms_now = (time_end.microsecond)/1000000
    s_now = s_now + ms_now
    
    s_prev = time_start.second
    ms_prev = (time_start.microsecond)/1000000
    s_prev = s_prev + ms_prev
    
    # print(s_prev,s_now ,"dif time = ",s_now-s_prev)

    return dist / (s_now - s_prev) if time_end > time_start else 0
    

def CreateCSV(lon1, lat1, lon2, lat2,dist, time_start, time_end, speed):
    
    s_now = time_end.second
    ms_now = (time_end.microsecond)/1000000
    s_now = s_now + ms_now
    
    s_prev = time_start.second
    ms_prev = (time_start.microsecond)/1000000
    s_prev = s_prev + ms_prev
    
    # buffer = lon1, lat1, lon2, lat2,dist, s_prev, s_now, time_end, speed, speed*3.6
    
    buffer = dist, s_prev, s_now, time_end, speed, speed*3.6
    
    print(round(buffer[8],2)," m/s || " , round(buffer[9],2)," km/hr ")

    
    with open('value_205_cut.csv', 'a',newline='') as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow(buffer)  
        
prev_data = None

while 1:
    line = ser.readline().decode('UTF-8')
    splitline = line.split(',')
    # print(splitline)
    if splitline[0] == '$GNGGA':
        msg = line
        data = pynmea2.parse(msg)
        if prev_data is not None:
            distance = haversine(data.longitude, data.latitude, prev_data.longitude, prev_data.latitude)
            Speed = float(calc_velocity(dist=distance, time_start=prev_data.timestamp ,time_end=data.timestamp))
            # print('distance', distance)
            # print('speed', round(Speed,3))
            CreateCSV(
                lon1=data.longitude,
                lat1=data.latitude,
                lon2=prev_data.longitude,
                lat2=prev_data.latitude,
                dist=distance,
                time_start=prev_data.timestamp,
                time_end=data.timestamp,
                speed=Speed
            )
            
        prev_data = data