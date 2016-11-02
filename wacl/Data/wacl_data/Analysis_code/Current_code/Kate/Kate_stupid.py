# Using python to to integrate the MOS signal
from pylab import plot, ginput, show, axis
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from datetime import timedelta, datetime
from pandas import DataFrame, read_csv
import csv
# Data file from sensors - DAQfactory txt file
path2 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/'

cal_file = ['mos_data_081616_01.txt']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	f = "".join(path2)+i
#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(f)
	
print(data.TheTime[0])
data['Time'] = data['TheTime'].map(lambda x :datetime.strptime(x,'%m/%d/%y %H:%M:%S')	.strftime('%s'))	
print(data.Time[0])

#plot up the MOS voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
ax1.plot(data.index, data.Sensor_ave,color="green",linewidth=3)
ax1.set_ylabel("MOS voltage (V)")
ax1.set_xlabel("Time")


######################################
#select points on graph
print "Click at either end of range"
# The two represents how many points the code wants the user to select using the mouse.
pts = ginput(2) # it will wait for four clicks
print "The points selected are"
print pts[0][0]
print pts[0][1]
print pts[1][0]
print pts[1][1]


xmin = pts[0][0] # To set the minimum value for the x axis in next plot
xmax = pts[1][0] # To set the maximum value for the x axis in the next plot
   
#Zoom into area of interest using the ginput clicking.
Zoomfig = plt.figure("Zoom")
ax1 = Zoomfig.add_subplot(111)
ax1.scatter(data.index, data.Sensor_ave,color="green",linewidth=3)
ax1.set_xlim(xmin, xmax) 
ax1.set_ylabel("MOS voltage (V)")
ax1.set_xlabel("Time")
Zoomfig.show()


# for index, item in enumerate(arr):
#     if item => 100:
#         return index, item
print "Click at either end of peak"
# The two represents how many points the code wants the user to select using the mouse.
pts = ginput(2) # it will wait for four clicks
print "The points selected are"
print pts[0][0]
print pts[0][1]
print pts[1][0]
print pts[1][1]
minval = pts[0][0] # To set the minimum value for the x axis in next plot
maxval = pts[1][0] # To set the maximum value for the x axis in the next plot

minval = round(minval, 0)
maxval = round(maxval, 0)
print minval, maxval


data_copy = data.copy()
sliced = data_copy[(data_copy.index >= minval) & (data_copy.index <= maxval)]


plotpeak = plt.figure()
ax1 = plotpeak.add_subplot(111)
ax1.plot(sliced.Time, sliced.Sensor_ave)
plt.title('Graph of Individual Peak')
plt.xlabel('Time in Seconds')
plt.ylabel('MOS Measurement in Volts')
plt.fill(sliced.Time, sliced.Sensor_ave, 'r')

PeakArea = np.trapz(sliced.Sensor_ave, dx = 1.)
print('Peak Area = ', PeakArea)
# sliced = data[data.Time >= minval]
# slice = sliced[sliced.Time <= maxval]
plt.show()

# print('Peak Start Time = ', minval)
# print('Peak End Time = ', maxval)
# x= data.Time[minval]
# x = data.Time==x
# x=data.Time[minval]
# slice1 = data[data.Time==x]
# minindexval = lambda x : data[data.Time==x].index
# print indexval(minval)
# 
# print slice1
# y = data.Time[maxval]
# y = data.Time==y
# y = data.Time[maxval]
# slice2 = data[data.Time==y]
# maxindexval = lambda y : data[data.Time==y].index
# print indexval(maxval)


# print('Slice rows based on x values')
# slice = data.ix[range(minval,maxval)]
# print slice

# The area under the curve is found using the trapezoidal rule. dx is equal to the time between measurements - 0.1 seconds in this case
# PeakArea = np.trapz(output_array, dx = 0.1)

# A graph of the peak is then plotted, with its area also given
# plt.plot(time_array, output_array, 'k-')
# plt.title('Graph of Individual Peak')
# plt.xlabel('Time in Seconds')
# plt.ylabel('PID Measurement in Volts')
# plt.fill(x, y, 'r')
# plt.xlim(minval, maxval)
# plt.show()
# print('Peak Area = ', PeakArea)

	