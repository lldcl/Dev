"""Analysing files containing data from three clusters of 8 MOS sensors."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

# The path to the raw files
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
# The name of the MOS file to be analysed
#cal_file =['d160905_060841','d160905_091251']
cal_file=['d160919_101505']
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
	
	# filter out periods when isop changes rapidly (disopdt<0.1) and for 60 seconds afterwards
# 	nm_pts = 300./float(Time_avg[:-1])
# 	dVOCdt = pd.Series(np.absolute(mean_resampled.VOC.diff()),name='dVOCdt')
# 	dVOCdt_filt = pd.Series(0, index=dVOCdt.index,name='dVOCdt_filt')
# 	dVOC_ctr=0
# 	for dp in dVOCdt:
# 		if (dp>0.01):
# 			dVOCdt_filt[dVOC_ctr:int(dVOC_ctr+nm_pts)] = 1
# 		dVOC_ctr+=1
# 
# 	mean_resampled = pd.concat([mean_resampled,dVOCdt],axis=1,join_axes=[mean_resampled.index])
# 	mean_resampled = pd.concat([mean_resampled,dVOCdt_filt],axis=1,join_axes=[mean_resampled.index])
# 	mean_resampled = mean_resampled[mean_resampled.dVOCdt_filt == 0]
# 	
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


# Returns the initial date and time that the file began
print(data_concat.Time[0])
print(data_concat.Time[len(data_concat.Time)-1])

# Finding the median MOS signal
data_concat['Median_MOS1'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
data_concat['Median_MOS2'] = data_concat[['MOS1b_Av','MOS2b_Av','MOS3b_Av','MOS5b_Av','MOS7b_Av','MOS8b_Av']].median(axis=1)
data_concat['Median_MOS3'] = data_concat[['MOS1c_Av','MOS2c_Av','MOS3c_Av','MOS5c_Av','MOS7c_Av','MOS8c_Av']].median(axis=1)
##########################################################################################

median = ['Median_MOS1', 'Median_MOS2','Median_MOS3']
numbers = [1,2,3,4]
color = ["blue","green","purple","orange"]
median_plot = plt.figure()

for i,n,p in zip(median,numbers, color):
	ax1 = median_plot.add_subplot(111)
	# ax2 = ax1.twinx()
	ax1.plot(data_concat.Time, data_concat[i], color=p, label=i)
	ax1.set_xlabel("Time")
	ax1.set_ylabel("MOS median (V)",size=18)
	# ax2.plot(data_concat.Time, data_concat.VOC, color="k")
	# ax2.set_ylabel("VOC conc (ppm)",size=18)
	ax1.legend()
	ax1.tick_params(labelsize=20)
plt.show()	