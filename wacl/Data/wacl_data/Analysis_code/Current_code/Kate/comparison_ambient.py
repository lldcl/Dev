"""Ambient comparison MOS data file reader/plotter to look at individual files run with air outside WACL.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['ambientexp2_split_160727_145910']


for i in cal_file:
	folder = list(i)[18:22]
	f = '20'+"".join(folder)+'/DAQfactory_split_files/'+i

#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

	#dT = seconds since file start
	dT = data.TheTime-data.TheTime[0]
	dT*=60.*60.*24.

	#convert daqfac time into real time pd.datetime object
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)
	
# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

T3 = pd.datetime(2015,01,01,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('int')
#'timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex, drop=False)
Time = pd.Series(data_concat.index,name='Time', index=data_concat.index)
data_concat = pd.concat([data_concat,Time],axis=0)

print(data_concat.index[0])
# Find all the columns with MOS in the title for use in loops.
sub = 'MOS'
#MOS = [s for s in data_concat.columns if sub in s]
MOS=['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']

#plot up the MOS voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
	ax1.plot(data_concat.index,data_concat[n],color=c,linewidth=3)
	plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("MOS / V")
	plt.xlabel("Index")	
# Give it something to count through at the same time as the MOS, so it changes color.
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
#Use a counter to count through numbers in integers, beginning at one.
ctr=1
MOSloop = plt.figure("Raw MOS signal")
for n,c in zip(MOS,colors):
	ax = 'MOSraw'+str(ctr)
	ax = MOSloop.add_subplot(8,1,ctr)
	ax.scatter(data_concat.index, data_concat[n],color=c,linewidth=3)
	ax.set_xlim([data_concat.index[0], data_concat.index[len(data_concat.index)-1]])
	ax.set_ylabel(n +"/ V")
	ax.set_xlabel("Index")
	ctr+=1
MOSloop.show()

# The median MOS signal
data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']].median(axis=1)
median = plt.figure()
ax1 = median.add_subplot(111)
ax1.plot(data_concat.index, data_concat.Median_MOS_signal, color="green")
ax1.set_xlabel("Index",size =18)
ax1.set_ylabel('Median MOS signal (V)',size=18)
plt.title(cal_file, size=20)


### COZI data  ####
filename = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201606/logging_1min_160625_125853'
cozi = pd.read_csv(filename)

# Ozone - not sure wich one is for outside
ozone = plt.figure()
ax1 = ozone.add_subplot(111)
ax1.plot(cozi.TheTime, cozi.O3_1, label="O3_1", color="green")
ax1.plot(cozi.TheTime, cozi.O3_3, label="O3_3", color="blue")
ax1.plot(cozi.TheTime, cozi.O3_6, label="O3_6", color="black")
ax1.plot(cozi.TheTime, cozi.O3_7, label="O3_7", color="purple")
ax1.set_xlabel("Time")
ax1.set_ylabel("Ozone")
plt.legend()
plt.title("Ozone COZI data for June")

# Carbon monoxide, again there are a couple of traces for this.
COfig = plt.figure()
ax1 = COfig.add_subplot(111)
ax1.plot(cozi.TheTime, cozi.co, label="CO", color="green")
ax1.plot(cozi.TheTime, cozi.co_guest_conc, label="CO Guest", color="blue")
ax1.plot(cozi.TheTime, cozi.co_ta3000, label="CO ta3000", color="black")
ax1.set_xlabel("Time", size=18)
ax1.set_ylabel("Carbon monoxide", size=18)
plt.legend()
plt.title("Carbon monoxide COZI data for June")

# NOx plot
Noxfig = plt.figure()
ax1 = Noxfig.add_subplot(111)
ax1.plot(cozi.TheTime, cozi.NO, label="NO", color="green")
ax1.plot(cozi.TheTime, cozi.NO2, label="NO2", color="blue")
ax1.set_xlabel("Time", size=18)
ax1.set_ylabel("Carbon monoxide", size=18)
plt.legend()
plt.title("Carbon monoxide COZI data for June")
print(cozi.columns)


plt.show()









