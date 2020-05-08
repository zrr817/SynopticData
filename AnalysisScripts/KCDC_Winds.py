#Basic data import tutorial
#Prerequisites: pandas and matplotlib packages

#Import packages and assign to variables
import pandas as pd
import csv
from matplotlib import pyplot as plt
import os
import glob

#Change working directory to where file is located
cwd = os.getcwd()
os.chdir("C:/Users/zrr81/Downloads/Climate Dev/Python/Synoptic Client Data")

#Read in file
#Need to split into 2 files due to Excel row limits
path = r'C:\Users\zrr81\Downloads\Climate Dev\Python\Synoptic Client Data'
all_files = glob.glob(path + "/*.csv")
li = []
#Read in files and merge into 1
for filename in all_files:
    data = pd.read_csv(filename, parse_dates = ['Date_Time'], index_col = ['Date_Time'])
    li.append(data)
df = pd.concat(li)

#Skip header rows
df = df.iloc[1:]

#Create tables with monthly mean & max wind speeds
#Ignore null values
wind = pd.DataFrame(df, columns = ['wind_speed'])
wind.dropna(how = 'any', inplace = True)
wind['wind_speed'] = wind['wind_speed'].astype(str).astype(float)
wind_m = wind.resample('M').mean()
wind_max = wind.resample('M').max()

#Limit to May-November
wind_m = wind_m[wind_m.index.month.isin([5,6,7,8,9,10])]
wind_max = wind_max[wind_max.index.month.isin([5,6,7,8,9,10])]

#Build the same mean and max tables for wind gusts
gust = pd.DataFrame(df, columns = ['wind_gust'])

#Drop all rows that don't contain a gust (inplace)
gust.dropna(how = 'any', inplace = True)
#Convert data types from objects to datetime and float
gust['wind_gust'] = gust['wind_gust'].astype(str).astype(float)
gust_m = gust.resample('M').mean()
gust_max = gust.resample('M').max()

#Limit to May-November
gust_m = gust_m[gust_m.index.month.isin([5,6,7,8,9,10])]
gust_max = gust_max[gust_max.index.month.isin([5,6,7,8,9,10])]

#Impose a catch that redefines any wind greater than the gust value as a gust
i = 0
"""for index, row in wind_max.iterrows():
    if wind_max[i] > gust_max[i]:
        gust_max[i] = wind_max[i]
    i += 1"""

#Follow the same process for peak wind
pk_wnd = pd.DataFrame(df, columns = ['peak_wind_speed'])
pk_wnd.dropna(how = 'any', inplace = True)
pk_wnd['peak_wind_speed'] = pk_wnd['peak_wind_speed'].astype(str).astype(float)
pk_wnd_m = pk_wnd.resample('M').mean()
pk_wnd_max = pk_wnd.resample('M').max()

#Limit to May-November
pk_wnd_m = pk_wnd_m[pk_wnd_m.index.month.isin([5,6,7,8,9,10])]
pk_wnd_max = pk_wnd_max[pk_wnd_max.index.month.isin([5,6,7,8,9,10])]
      
#Define iterated arrays
y_array = ['wind_speed', 'wind_gust', 'peak_wind_speed']
colors = ['red', 'blue', 'green']
j = 0

#Plot max wind speeds, gusts, and times
plt.figure(0)
for frame in [wind_m, gust_m, pk_wnd_m]:
    if j == 0:
        ax = frame.reset_index().plot(kind = 'line', x= 'Date_Time', y = y_array[j], legend = False, color = colors[j])
    else:
        frame.reset_index().plot(kind = 'line', x= 'Date_Time', y = y_array[j], legend = False, color = colors[j], ax = ax)
    j += 1

#Define plot specifiers
plt.xlabel("Date")
plt.ylabel("Wind Speed (m/s)")
plt.title("Average Summer (May-Nov) Wind Speeds at KCDC")
plt.legend(['Average Wind', 'Average Gust', 'Average Peak Wind'])
plt.savefig('KCDC_Avg_Winds.png')

#Build maximums graph
plt.figure(1)
k = 0
for frame in [wind_max, gust_max, pk_wnd_max]:
    if k == 0:
        ax = frame.reset_index().plot(kind = 'line', x= 'Date_Time', y = y_array[k], legend = False, color = colors[k])
    else:
        frame.reset_index().plot(kind = 'line', x= 'Date_Time', y = y_array[k], legend = False, color = colors[k], ax = ax)
    k += 1  

#Define plot specifiers
plt.xlabel("Date")
plt.ylabel("Wind Speed (m/s)")
plt.title("Maximum Summer (May-Nov) Wind Speeds at KCDC")
plt.legend(['Max Wind', 'Max Gust', 'Max Peak Wind'])
plt.savefig('KCDC_Max_Winds.png')

#Show plots
plt.show()