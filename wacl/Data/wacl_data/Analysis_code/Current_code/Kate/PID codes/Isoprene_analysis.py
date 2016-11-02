## MFC ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201510/'

#filenames = ['d20151021_02','d20151021_03','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151022_03','d20151022_04','d20151023_01','d20151023_02','d20151023_03']
filenames = ['d20151027_01']
stat = 'Y'


for f in filenames:
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

	#find all pids in file
	sub = 'pid'
	pids = [s for s in data.columns if sub in s]

	
	
# Time averaging the data
	
Time_avg = '10S'

mean_resampled = data.copy(deep=True)
mean_resampled.RH = (mean_resampled.RH)
mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

# data.RH gives the relative humidity as a voltage, so need to turn this into a n absolute value:
mean_resampled.RH = (((mean_resampled.RH/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)

	
print 'mean_resampled shape = ',mean_resampled.shape
try:
	data_concat = data_concat.append(mean_resampled)
	print ' concatenating'
except NameError:
	data_concat = mean_resampled.copy(deep=True)
	print ' making data_concat'

dRHdt = pd.Series(np.absolute(data_concat.RH.diff()),name='dRHdt')
dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
nm_pts = 120./float(Time_avg[:-1])
dRH_ctr=0
for dp in dRHdt:
	if (dp>0.02):
		dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
	dRH_ctr+=1

data_concat = pd.concat([data_concat,dRHdt],axis=1,join_axes=[data_concat.index])
data_concat = pd.concat([data_concat,dRHdt_filt],axis=1,join_axes=[data_concat.index])

mfc = plt.figure("MFC")
# Determining the isoprene concentration:
isop_cyl = 723.	#13.277	#ppbv
mfchi_range = 2000.	#100.	#sccm
mfchi_sccm = data_concat.mfchiR*(mfchi_range/5.)
mfclo_range = 20.	#sccm
mfclo_sccm = data_concat.mfcloR*(mfclo_range/5.)
mfcmid_range = 100. #sccm
mfcmid_sccm = data_concat.mfcmidR*(mfcmid_range/5.)
dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
data = pd.concat([data,isop_mr],axis=1)
	
ax1 = mfc.add_subplot(4,1,1)
ax2 = mfc.add_subplot(4,1,2)
ax3 = mfc.add_subplot(4,1,3)
ax4 = mfc.add_subplot(4,1,4)
ax1.plot(data_concat.index, mfchi_sccm, color="green", linewidth=2)
ax2.plot(data_concat.index, mfclo_sccm, color="red", linewidth=2)
ax3.plot(data_concat.index, mfcmid_sccm, color="blue", linewidth=2)

total = (mfclo_sccm + mfchi_sccm + mfcmid_sccm)
ax4.plot(data_concat.index, total , color="purple", linewidth=2)
ax1.set_xlabel("Index")
ax1.set_ylabel("MFC high")
ax2.set_ylabel("MFC low")
ax3.set_ylabel("MFC med")
ax4.set_ylabel("MFC total")
plt.show()
