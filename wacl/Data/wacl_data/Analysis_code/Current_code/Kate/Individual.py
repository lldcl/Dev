"""Analysing files containing data from three clusters of 8 MOS sensors, but looking at the individual sensors too for the ambient conditions."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText
import matplotlib.dates as mdates

# The path to the raw files
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
# The name of the MOS file to be analysed
#cal_file=['d160902_195530','d160903_053742','d160903_151955','d160904_010207','d160904_104419','d160904_202630','d160905_060841',]
#cal_file=['d160928_103119','d160928_161841','d160929_074207','d160929_093719','d160929_143317','d160929_143317','d161003_084630','d161003_180949','d161006_114307']
cal_file = ['d161027_172220']
#cal_file =['d160930_140157']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	folder = list(i)[1:5]
	f = '20'+"".join(folder)+"/"+i

#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)
	

# 	convert daqfac time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')

	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset
# Ten second averaging of the raw data
	Time_avg = '10S'
# Make a new copy of the data called mean_resampled 
	mean_resampled = data.copy(deep=True)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
#Set the index to be the time column, when you do this it drops the index, even though it is set to False.
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)
	
# If there are more than files the data_concat function will join them together.
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

#find all MOSs in file
# sub = 'MOS'
# MOSs = [s for s in data.columns if sub in s]
MOSs = ['MOS1_Av', 'MOS2_Av', 'MOS3_Av', 'MOS4_Av', 'MOS5_Av', 'MOS6_Av', 'MOS7_Av', 'MOS8_Av', 'MOS1b_Av', 'MOS2b_Av', 'MOS3b_Av', 'MOS4b_Av', 'MOS5b_Av', 'MOS6b_Av', 'MOS7b_Av', 'MOS8b_Av', 'MOS1c_Av', 'MOS2c_Av', 'MOS3c_Av', 'MOS4c_Av', 'MOS5c_Av', 'MOS6c_Av', 'MOS7c_Av', 'MOS8c_Av']

data_concat['Median_MOS'] = data_concat[MOSs].median(axis=1)

overall = plt.figure()
for z in MOSs:
	ax1 = overall.add_subplot(111)
	ax1.plot(data_concat.Time, data_concat[z], linewidth=2)
	ax1.plot(data_concat.Time, data_concat.Median_MOS, color='k', linewidth=3)
	ax1.set_ylabel("MOS signal (V)", size=18)
	ax1.set_xlabel("Time",size=18)
overall.show()	

data_concat['Q1_MOS'] = np.percentile(data_concat[MOSs],25,axis=1)
data_concat['Q3_MOS'] = np.percentile(data_concat[MOSs],75,axis=1)
data_concat['Median_MOS1'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
data_concat['Median_MOS2'] = data_concat[['MOS1b_Av','MOS2b_Av','MOS3b_Av','MOS5b_Av','MOS7b_Av','MOS8b_Av']].median(axis=1)
data_concat['Median_MOS3'] = data_concat[['MOS1c_Av','MOS2c_Av','MOS3c_Av','MOS5c_Av','MOS7c_Av','MOS8c_Av']].median(axis=1)
average = plt.figure()	
ax1 = average.add_subplot(111)
ax1.plot(data_concat.Time, data_concat.Median_MOS, color="red", linewidth=3, label="Median for all")
ax1.plot(data_concat.Time, data_concat.Q1_MOS, color="grey", label="25th percentile")
ax1.plot(data_concat.Time, data_concat.Q3_MOS, color="grey", label="75th percentile")
ax1.plot(data_concat.Time, data_concat.Median_MOS1, color="blue", label="MOS1_median")
ax1.plot(data_concat.Time, data_concat.Median_MOS2, color="purple",label="MOS2_median")
ax1.plot(data_concat.Time, data_concat.Median_MOS3, color="teal",label="MOS3_median")
ax1.set_ylabel("MOS signal (V)", size=18)
ax1.set_xlabel("Time",size=18)
plt.title(cal_file)
plt.legend()
#average.show()

# colors = ['green','green','green','green','green','green','green','green','blue','blue','blue','blue','blue','blue','blue','blue','red','red','red','red','red','red','red','red']
# # Delta median
# difference = plt.figure("delta")
# for x,p in zip(MOSs,colors):
# 	delta = data_concat[x] - data_concat.Median_MOS
# 	y= data_concat.Median_MOS - data_concat.Median_MOS
# 	ax = difference.add_subplot(111)
# 	ax.plot(data_concat.Time, delta, color = p)
# 	ax.plot( data_concat.Time, y, color="k",linewidth=5)
# 	ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))   #to get a tick every 15 minutes
# 	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) 
# 	plt.legend()
# 	plt.title( "Differnce of the individual sensors from the median")
# difference.show()

biology = ['MOS1_Av', 'MOS2_Av', 'MOS3_Av', 'MOS4_Av', 'MOS5_Av', 'MOS6_Av', 'MOS7_Av', 'MOS8_Av']
aircraft1 = ['MOS1b_Av', 'MOS2b_Av', 'MOS3b_Av', 'MOS4b_Av', 'MOS5b_Av', 'MOS6b_Av', 'MOS7b_Av', 'MOS8b_Av']	
aircraft2 = ['MOS1c_Av', 'MOS2c_Av', 'MOS3c_Av', 'MOS4c_Av', 'MOS5c_Av', 'MOS6c_Av', 'MOS7c_Av', 'MOS8c_Av']

cluster = plt.figure("delta")
for x,y,z in zip(biology,aircraft1,aircraft2):
	bio_diff = data_concat[x] - data_concat.Median_MOS
	air1_diff = data_concat[y] - data_concat.Median_MOS
	air2_diff = data_concat[z] - data_concat.Median_MOS
	q= data_concat.Median_MOS - data_concat.Median_MOS
	ax = cluster.add_subplot(111)
	ax.plot(data_concat.Time, bio_diff, color= "red", label="Biology, last in line")
	ax.plot(data_concat.Time, air1_diff, color= "blue",label="Aircraft1, first in line")
	ax.plot(data_concat.Time, air2_diff, color= "green",label="Aircraft2, second in line")
	ax.plot( data_concat.Time, q, color="k",linewidth=5)
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))   #to get a tick every 15 minutes
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) 
	plt.legend()
	plt.title( "Sensors colour coded by cluster")
#cluster.show()

variables= plt.figure()
ax1 = variables.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Median_MOS, color="k")
ax2.plot(data_concat.Time, data_concat.LM65T1_Av, color="red", label="Temp")
plt.legend()

RH = plt.figure()
ax1 = RH.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Median_MOS, color="k")
ax2.plot(data_concat.Time, data_concat.HIH1_Av, color="blue", label="Humidity")
plt.legend()


plt.show()