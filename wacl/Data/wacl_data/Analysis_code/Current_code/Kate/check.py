import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats
import pandas as pd

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201511/'

filenames = ['d20151106_02']
stat = 'Y'


for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)#, skiprows=range(1,19071))
	#with open(path+f, 'r') as f:
	#    data.columns = f.readline().split(',')
	data=  data.drop(' OTHER ', axis = 1)
	#dT = seconds since file start
	dT = data.TheTime-data.TheTime[0]
	dT*=60.*60.*24.

	#convert daqfac time into real time pd.datetime object (into a time that python exists).
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	#find all pids in file
	sub = 'pid'
	pids = [s for s in data.columns if sub in s]
	
### Determining the isoprene concentration:
	isop_cyl = 723.	#13.277	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100. #sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	
	data = pd.concat([data,isop_mr],axis=1)
# Tells it to add the data file to data_concat. For the first file won't have data_concat. 
# So it comes up with a NameError and that triggers it to form data_concat. Therefore, for the next	
# file it will just add it to that. 	
	print 'data = ',data.shape
	try:
		data_concat = data_concat.append(data)
		print ' concatenating'
	except NameError:
		data_concat = data.copy(deep=True)
		print ' making data_concat'


### Time averaging the data
Time_avg = '10S'

mean_resampled = data_concat.copy(deep=True)
mean_resampled.RH = (mean_resampled.RH)
mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

# data.RH gives the relative humidity as a voltage, so need to turn this into a n absolute value:
mean_resampled.RH = (((mean_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)

import numpy as np
dRHdt = pd.Series(np.absolute(mean_resampled.RH.diff()),name='dRHdt')
dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
nm_pts = 120./float(Time_avg[:-1])
dRH_ctr=0
for dp in dRHdt:
	if (dp>0.02):
		dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
	dRH_ctr+=1

mean_resampled = pd.concat([mean_resampled,dRHdt],axis=1,join_axes=[mean_resampled.index])
mean_resampled = pd.concat([mean_resampled,dRHdt_filt],axis=1,join_axes=[mean_resampled.index])

# Select the data points for which RH= 70- 72%RH
# Creates a new dataframe which selects ALL the data when RH is lower than 72% and higher than 70%.
# The new data frame is called RHselect, and it is taking data from the mean_resampled dataframe,
# under the condition that RH is within this range.
data_RH = mean_resampled[mean_resampled]

check = plt.figure()
ax1 = check.add_subplot(1,1,1)
ax1.plt(data_RH.index , data_RH.pid4, color='k', linewidth=2)

plt.show()
