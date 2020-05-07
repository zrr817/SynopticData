#Basic data import tutorial
#Prerequisites: pandas and matplotlib packages

#Import packages and assign to variables
import pandas as pd
import csv
from matplotlib import pyplot as plt
import os

#Change working directory to where file is located
cwd = os.getcwd()
os.chdir("C:/Users/zrr81/Downloads/Climate Dev/Python/Synoptic Client Data")

#Read in file
data = pd.read_csv('KCDC.2019-11-01.csv')

wind = pd.DataFrame(data, columns = ['wind_speed'])
#wind.pop(0)
wind.dropna(thresh=1)
#print(wind)

#Build wind gust and datetime DataFrame
gust = pd.DataFrame(data, columns = ['Date_Time', 'wind_gust'])
#Drop all rows that don't contain a gust (inplace)
gust.dropna(how = 'any', inplace = True)
#Drop unit/ header row
gust = gust.drop(gust.index[0])
#Convert data types from objects to datetime and float
gust['Date_Time'] = pd.to_datetime(gust['Date_Time'])
gust['wind_gust'] = gust['wind_gust'].astype(str).astype(float)
print(gust)
print(gust.dtypes)

#Inc. only Summer (May 1- November 1) in time series
#Create data frame
df = pd.DataFrame()
df['date'] = pd.date_range('5/1/1997', periods = 100000, freq = 'T')

#Create an array of years to loop through
years = range(1997, 2020, 1)

# Set index
df = df.set_index(df['date'])

#Select date range for each year
i = 1
a = '-05-01 00:00:00Z'
b = '-11-01 00:00:00Z'
while i<= len(years) :
    start = (str(years[i-1]) + a)
    end = (str(years[i-1]) + b)
    #print(df.loc[start: end])
    i+=1

#Plot max wind speeds, gusts, and times
ax = plt.gca()
gust.plot(kind = 'line' , x = 'Date_Time', y = 'wind_gust', color = 'red')
#plt.plot(zw.year, zw.population)
plt.legend(['Wind gusts'])
plt.xlabel("Date Time")
plt.ylabel("Wind Gust (m/s)")
plt.title("May-Nov Maximum Wind Gusts at KCDC")
plt.show()

