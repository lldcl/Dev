# Using python to to integrate the MOS signal

from pandas import DataFrame, read_csv
from datetime import timedelta, datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
# Data file from sensors - DAQfactory txt file
path2 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/'

cal_file = ['mos_data_081616_02.txt']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	f = "".join(path2)+i
#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(f)
	

# 	convert daqfac time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')

	T1 = pd.datetime(1970,01,01,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset
# Ten second averaging of the raw data
# 	Time_avg = '0S'
# Make a new copy of the data called mean_resampled 
	mean_resampled = data.copy(deep=True)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
#Set the index to be the time column, when you do this it drops the index, even though it is set to False.
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
# 	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)	
# If there are more than files the data_concat function will join tem together.
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'
		
# Re-make and re-set the index to be the time column for the data_concat dataframe.
T3 = pd.datetime(2015,01,01,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('int')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)

#read file into dataframe

# Turn the time into a number:
new_time = pd.Series(pd.to_datetime(data_concat.TheTime.strftime('%s')))

# Reading the CSV file to find the starting time of the experiment - the second line is used as the first line is made up of the column headers
# The time values are then all multiplied by 86400 (no. seconds in a day) to give the time in seconds since starting the measurements
Seconds = pd.Series(data_concat.newtime - data_concat.newtime[0])
d = timedelta(days = np.float(StartTime))
st = datetime(1899, 12, 30)
date = datetime.strftime(st + d, '%H-%M-%S')
print('Time and Date of intial measurements = ', date)

# The new time data and the PID measurements are then written to a new CSV file. IF row was used to prevent blank lines between the data
with open('SecondsData.csv', 'wb') as SD:
    csv_writer = csv.writer(SD)
    rows = zip(Seconds, df.PIDReading)
    for row in rows:
            if row:
                csv_writer.writerow(row)

# A graph is then plotted of the amended time against the PID measurements so the peaks can be easily identified
x,y = np.loadtxt('C:\Users\VolcanoFGAM\My Documents\Python Testing\SecondsData.csv', delimiter = ',', unpack = True)
plt.plot(x,y,'r-')
plt.title('Graph of PID Measurements against Time in Seconds')
plt.xlabel('Time in Seconds')
plt.ylabel('PID Measurement in Volts')
plt.show()

# Identifying the time window in which a peak occurs, with minval being the start time and maxval being the end time. Total time is the retention time
peaknumber = input('Which peak is being measured?')
minval = input('Minimum x value =')
maxval = input('Maximum x value =')
print('Peak Number = ', peaknumber)
print('Peak Start Time = ', minval)
print('Peak End Time = ', maxval)
print('Retention Time = ', maxval - minval)

# Reading the test data from the CSV file
csv_file = open('C:\Users\VolcanoFGAM\My Documents\Python Testing\SecondsData.csv', 'rb')
reader = csv.reader(csv_file)

# Creating a time array which the selected time data will be written to and an output array which the corresponding PID data will be written to 
time_array = []
output_array = []

# Loop iterating over each row. If the time is between the given time window, it will be written to the time array. The corresponding PID data will be written to the output array
for row in reader:        
    if (float(row[0]) >= minval) and (float(row[0]) <= maxval):
        time_array.append(float(row[0]))
        output_array.append(float(row[1]))      

# The two arrays are then written to a new CSV file, so that the time data and output data are set out in two dinstinct columns
with open('PeakDataArray.csv', 'wb') as PDA:
    csv_writer = csv.writer(PDA)
    rows = zip(time_array, output_array)
    for row in rows:
        if row:
            csv_writer.writerow(row)

# The area under the curve is found using the trapezoidal rule. dx is equal to the time between measurements - 0.1 seconds in this case
PeakArea = np.trapz(output_array, dx = 0.1)

# A graph of the peak is then plotted, with its area also given
plt.plot(time_array, output_array, 'k-')
plt.title('Graph of Individual Peak')
plt.xlabel('Time in Seconds')
plt.ylabel('PID Measurement in Volts')
plt.fill(x, y, 'r')
plt.xlim(minval, maxval)
plt.show()
print('Peak Area = ', PeakArea)

# Appending the results data to the file, underneath the column headers
with open('C:\Users\VolcanoFGAM\My Documents\PID Peak Data\RoughPeakData.csv', 'ab') as fp:
    a = csv.writer(fp, delimiter = ',')
    data = [str(date), peaknumber, minval, maxval, maxval-minval, PeakArea]
    a.writerow(data)

# A data frame is created using pandas in order to add headers to the data    
Location2 = r'C:\Users\VolcanoFGAM\My Documents\PID Peak Data\RoughPeakData.csv'
df2 = read_csv(Location2, names = ['Date and Time', 'Peak Number', 'Start Time', 'End Time', 'Retention Time', 'Peak Area'], skiprows=(1))
print df2

# The data is then written to a CSV file along with the headers - written rather than appended as the data is appended when read to the data frame
with open('C:\Users\VolcanoFGAM\My Documents\PID Peak Data\PeakData.csv', 'wb') as f1:
    df2.to_csv(f1, header = True)
f1.close()
