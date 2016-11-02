"""VOC MOS data file reader/plotter to look at individual files run with the dilute VOC mix.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160401_02']

for i in cal_file:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i

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
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
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
data_concat = data_concat.set_index(newindex)

VOC = plt.figure()
ax1 = VOC.add_subplot(4,1,1)
ax5 = ax1.twinx()
ax2 = VOC.add_subplot(4,1,2)
ax6 = ax2.twinx()
ax3 = VOC.add_subplot(4,1,3)
ax4 = VOC.add_subplot(4,1,4)

ax1.plot(data_concat.index, data_concat.MOSar3, color = "tomato")
ax1.set_ylabel("MOSar3 (V)")
ax2.plot(data_concat.index, data_concat.MOSar7, color = "mediumslateblue")
ax2.plot(data_concat.index, data_concat.MOSar2, color = "chocolate", label="MOSar2")
ax2.set_ylabel("MOSar7 and MOSar2 (V)")

ax3.plot(data_concat.index, data_concat.Temp*100, color = "red")
ax3.set_ylabel("Temperature (oC)")
ax4.plot(data_concat.index, data_concat.RH1, color = "blue")
ax4.plot(data_concat.index, data_concat.VS, color = "k")
ax4.set_ylabel("RH (%)")
ax5.plot(data_concat.index, data_concat.SO2*1000, color = "silver")
ax6.plot(data_concat.index, data_concat.NO2*1000, color = "silver")
ax5.set_ylabel("VOC (ppb)")
ax6.set_ylabel("VOC (ppb)")

arfig = plt.figure()
ax1 = arfig.add_subplot(211)
ax2 = arfig.add_subplot(212)

ax1.plot(data_concat.index, data_concat.MOS1, color = "skyblue", label="MOS1")
ax1.plot(data_concat.index, data_concat.MOS2, color = "darksage", label="MOS2")
ax2.plot(data_concat.index, data_concat.MOSar4, color = "blueviolet", label="MOSar8")
ax2.plot(data_concat.index, data_concat.MOSar5, color = "darkcyan", label="MOSar5")
ax2.plot(data_concat.index, data_concat.MOSar8, color = "gray",label="MOSar4")	
ax2.plot(data_concat.index, data_concat.MOSar6, color = "orange", label="MOSar6")
ax2.plot(data_concat.index, data_concat.MOSar1, color = "darkgreen", label="MOSar1")


ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
plt.show()