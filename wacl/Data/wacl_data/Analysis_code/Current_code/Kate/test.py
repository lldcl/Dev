## Isoprene data- want to plot isoprene vs PID over very small changes in RH (70-72% RH) ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201510/'

filenames = ['d20151026_05','d20151027_01', 'd20151027_02', 'd20151027_03']
stat = 'Y'


for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

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
mean_resampled.RH = (((mean_resampled.RH/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)


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
data_RH = mean_resampled[mean_resampled.RH > 79]
data_RH1 = data_RH[data_RH.RH <80]

#data_highIsop = mean_resampled[mean_resampled.isop_mr <1]
#mean_dRHdt_filt
#concat_filename = str(path+'30sconcat_1021.csv')
#mean_resampled.to_csv(path_or_buf=concat_filename)
data = data.dropna()
RHcheck = plt.figure("RH check")
ax1 = RHcheck.add_subplot(1,1,1)
ax1.plot(data_RH1.index, data_RH1.RH, color="b", linewidth=2)
ax1.set_xlabel("Index")
ax1.set_ylabel("RH %")
ax2 = ax1.twinx()
ax2.plot(data_RH1.index, data_RH1.pid4, color = "r", linewidth=2, label="pid4")
ax2.plot(data_RH1.index, data_RH1.pid5, color = "g", linewidth=2, label="pid5")
plt.legend()

isopcheck = plt.figure("Isop check")
ax1 = isopcheck.add_subplot(1,1,1)
ax1.plot(data_RH1.index, data_RH1.isop_mr, color="green", linewidth=2)
ax1.set_xlabel("Index")
ax1.set_ylabel("Isop")

# For this data range, need to plot isoprene vs pid voltage.
import matplotlib.cm as cm
i = (data_RH1.RH-np.min(data_RH1.RH))/np.max(data_RH1.RH-np.min(data_RH1.RH))
pid4 = data_RH1.pid4*1000
pid5 = data_RH1.pid5*1000
pid6 = data_RH1.pid6*1000
data_RH1.isop_mra = data_RH1.isop_mr[:(len(data_RH1.isop_mr)-1000)]
data_RH1.RHa = data_RH1.RH[1000:]
pid4a = pid4[:(len(pid4)-1000)]
pid5a = pid5[:(len(pid5)-1000)]
pid6a = pid6[:(len(pid6)-1000)]
indexa = data_RH1.index[:(len(data_RH1.index)-1000)]

isoprene = plt.figure(" Over a selected RH range")
ax1 = isoprene.add_subplot(2,1,1)
ax2 = isoprene.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()

ax1.scatter(data_RH1.isop_mr, pid4, color=cm.jet(i), linewidth=3)
ax2.scatter(data_RH1.isop_mr, pid5, color=cm.jet(i), linewidth=3)
ax3.scatter(data_RH1.isop_mra, pid4a, color="b", linewidth=1)
ax4.scatter(data_RH1.isop_mra, pid5a, color="g", linewidth=1)

# Linear regression using scipy. The function will return the following 5 parameters in that order.
slope1, intercept1, R2_value1, p_value1, st_err1 = stats.linregress(data_RH1.isop_mr, pid4)
slope2, intercept2, R2_value2, p_value2, st_err2 = stats.linregress(data_RH1.isop_mr, pid5)
#slope1, intercept1, R2_value1, p_value1, st_err1 = stats.linregress(data_RH1.isop_mra, pid4a)
#slope2, intercept2, R2_value2, p_value2, st_err2 = stats.linregress(data_RH1.isop_mra, pid5a)


print ("Gradient pid 4:", slope1)
print ("R2 value pid 4:", R2_value1)
print ("Gradient pid 5:", slope2)
print ("R2 value pid 5:", R2_value2)
"""print ("Gradient pid 4a:", slope1)
print ("R2 value pid 4a:", R2_value1)
print ("Gradient pid 5a:", slope2)
print ("R2 value pid 5a:", R2_value2)"""


ax1.plot([np.min(data_RH1.isop_mr), np.max(data_RH1.isop_mr)], [(slope1*np.min(data_RH1.isop_mr))+intercept1, (slope1*np.max(data_RH1.isop_mr))+intercept1])
ax2.plot([np.min(data_RH1.isop_mr), np.max(data_RH1.isop_mr)], [(slope2*np.min(data_RH1.isop_mr))+intercept2, (slope2*np.max(data_RH1.isop_mr))+intercept2])
#ax3.plot([np.min(data_RH1.isop_mra), np.max(data_RH1.isop_mra)], [(slope1*np.min(data_RH1.isop_mra))+intercept1, (slope1*np.max(data_RH1.isop_mra))+intercept1])
#ax4.plot([np.min(data_RH1.isop_mra), np.max(data_RH1.isop_mra)], [(slope2*np.min(data_RH1.isop_mra))+intercept2, (slope2*np.max(data_RH1.isop_mra))+intercept2])


"""ax1.set_xlim(np.min(data_RH1.isop_mr )*0.9999, np.max(data_RH1.isop_mr)*1.0001)
ax1.set_ylim(np.min(pid4)*0.9999999, np.max(pid4)*1.000000001)
ax2.set_xlim(4.30, 4.31)
ax2.set_ylim(np.min(pid5)*0.99999999, np.max(pid5)*1.0000000001)
ax3.set_xlim(4.30, 4.31)
ax3.set_ylim(np.min(pid6)*0.9999999, np.max(pid6)*1.00000001)"""


ax1.set_xlabel("Isoprene / ppbv")
ax1.set_ylabel("PID 4 / mV")
ax2.set_xlabel("Isoprene / ppbv")
ax2.set_ylabel("PID 5 / mV")
ax3.set_xlabel("Isoprene / ppbv")
ax3.set_ylabel("PID 4a / mV")
ax4.set_xlabel("Isoprene / ppbv")
ax4.set_ylabel("PID 5a / mV")


plt.show()