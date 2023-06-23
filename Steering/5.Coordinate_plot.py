import pandas as pd
import geopy.distance 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('default')
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec

df = pd.read_csv('Moving_filter/ref1_20_round_3.csv')

x_east = df.x_east
y_north = df.y_north
raw_x_east = df.raw_x_east
raw_y_north = df.raw_y_north

print(x_east,y_north)
plt.plot(raw_x_east,raw_y_north,color='red',label='Raw')
plt.plot(x_east,y_north,color='blue',label='Moving Average')
plt.legend()
plt.show() 

# utc = df.UTC
# time = df.UTC - df.UTC[0]
# raw_lat = df.raw_lat
# raw_lng = df.raw_lng
# raw_x_east = df.raw_x_east
# raw_y_north = df.raw_y_north
# lat = df.lat
# lng = df.lng
# x_east = df.x_east
# y_north = df.y_north

# plt.plot(raw_lng,raw_lat,color='blue',label='Raw')
# plt.plot(lng,lat,color='red',label='Moving Average')
# plt.legend()
# plt.show() 

# # Create 2x2 sub plots
# gs = gridspec.GridSpec(2, 2)
# pl.figure()
# pl.suptitle('Reference3 Moving Average Filter 10 Windows')
# ax = pl.subplot(gs[1, 0]) # row 0, col 0
# pl.plot(time,raw_lat, color='blue',mfc='pink',label='Raw')
# pl.plot(time,lat, color='red',mfc='pink',label='filter')
# pl.title("Latitude(Degree)")
# pl.xlabel("Time(second)")
# pl.ylabel("Latitude")
# plt.legend()

# ax = pl.subplot(gs[0, 0]) # row 0, col 1
# pl.plot(time,raw_lng, color='blue',mfc='pink',label='Raw')
# pl.plot(time,lng, color='red',mfc='pink',label='filter')
# pl.title("Longitude(Degree)")
# pl.xlabel("Time(second)")
# pl.ylabel("Longitude")
# plt.legend()

# ax = pl.subplot(gs[1, 1]) # row 1, col 0
# pl.plot(time,raw_x_east, color='blue',mfc='pink',label='Raw')
# pl.plot(time,x_east, color='red',mfc='pink',label='filter')
# pl.title("UTM East X(meter)")
# pl.xlabel("Time(second)")
# pl.ylabel("UTM X")
# plt.legend()

# ax = pl.subplot(gs[0, 1]) # row 1, col 1
# pl.plot(time,raw_y_north, color='blue',mfc='pink',label='Raw')
# pl.plot(time,y_north, color='red',mfc='pink',label='filter')
# pl.title("UTM North Y(meter)")
# pl.xlabel("Time(second)")
# pl.ylabel("UTM Y")
# plt.legend()

# plt.show()