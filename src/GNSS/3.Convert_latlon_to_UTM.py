import matplotlib.pyplot as plt
import pandas as pd
import utm

df = pd.read_csv("Reference2_NetworkRTK\latlon_Network01.csv")
df['utm'] = df.apply(lambda row: utm.from_latlon(*row), axis=1)
utm_cols = ['easting', 'northing', 'zone_number', 'zone_letter']
for n, col in enumerate(utm_cols):
    df[col] = df['utm'].apply(lambda location: location[n])
df = df.drop('utm', axis=1)

window = 3
df['MA3_easting'] = df['easting'].rolling(window).mean()
df['MA3_northing'] = df['northing'].rolling(window).mean()

window = 5
df['MA5_easting'] = df['easting'].rolling(window).mean()
df['MA5_northing'] = df['northing'].rolling(window).mean()

window = 10
df['MA10_easting'] = df['easting'].rolling(window).mean()
df['MA10_northing'] = df['northing'].rolling(window).mean()

df.dropna(inplace=True)
print(df)

# df = <class 'pandas.core.frame.DataFrame'>
#             Lat         Lon        easting      northing  zone_number zone_letter
# 0     13.650840  100.492999  661486.890639  1.509608e+06           47           P
# 1     13.650843  100.492998  661486.866620  1.509608e+06           47           P
# 2     13.650847  100.492998  661486.842493  1.509609e+06           47           P
# 3     13.650851  100.492998  661486.829177  1.509609e+06           47           P
# 4     13.650854  100.492998  661486.805042  1.509610e+06           47           P


plt.plot(df['MA3_easting'],df['MA3_northing'],color='orange',linestyle='dotted',lw=2,label='Moving Average 3 Windows')
plt.plot(df['MA5_easting'],df['MA5_northing'],color='blue',linestyle='dotted',lw=2,label='Moving Average 5 Windows')
plt.plot(df['MA10_easting'],df['MA10_northing'],color='black',linestyle='dotted',lw=2,label='Moving Average 10 Windows')
plt.scatter(df['easting'],df['northing'],color='green',label='Raw Data')

plt.ylabel('Northing') 
plt.xlabel('Easting') 
plt.title("X Y Coordinate Comparison (Raw Data and Data After Moving Average filter) ")
plt.legend()
plt.show()

# Initialise the subplot function using number of rows and columns
# figure, axis = plt.subplots(1,2)
# figure.suptitle('Convert Lat,Lng to X,Y')

# axis[0].plot(df['Lon'],df['Lat'])
# axis[0].set_title("Latitude and Longtitude")
# axis[0].set_xlabel("Longtitude")
# axis[0].set_ylabel("Latitude")

# axis[1].plot(df['easting'],df['northing'])
# axis[1].set_title("Easting_X and Northing_Y Coordinate")
# axis[1].set_xlabel("Easting")
# axis[1].set_ylabel("Northing")