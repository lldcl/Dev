## Isoprene data- want to plot isoprene vs PID over very small changes in RH (70-72% RH) ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats
from RH_cal_fna import *

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# Takes the file name and extracts the date then sticks this on the front to make the file path. 
stat = 'Y'
cal_files = ['d20151103_03','d20151103_04']

#RH_cal_data = RH_cal_fn(path,'201510/d20151023_03','30S')

for i in cal_files:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i

# for f in filenames:
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
	isop_cyl = 723.	 #ppbv
	mfchi_range = 2000. 	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100. #sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
	#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)
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
#mean_resampled.RH = (((mean_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
mean_resampled.RH = (((mean_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)


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

isop_cyl = 723.	 #ppbv
mfchi_range = 2000. 	#sccm
mfchi_sccm = mean_resampled.mfchiR*(mfchi_range/5.)
mfclo_range = 20.	#sccm
mfclo_sccm = mean_resampled.mfcloR*(mfclo_range/5.)
mfcmid_range = 100. #sccm
mfcmid_sccm = mean_resampled.mfcmidR*(mfcmid_range/5.)
dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)
isop_mix = pd.Series(dil_fac*isop_cyl,name='isop_mr')
#data = pd.concat([data,isop_mr],axis=1)dil_fac
	
pid4 = mean_resampled.pid4*1000
pid5 = mean_resampled.pid5*1000
time = mean_resampled.index
RH = mean_resampled.RH

# Create a figure instance
pidfig = plt.figure("PID voltage over time")
#Create the three subplots to appear in the same window
ax1 = pidfig.add_subplot(2,1,1)
ax2 = pidfig.add_subplot(2,1,2)

ax4 = ax1.twinx()
ax5 = ax2.twinx()

colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
ax1.plot(time , pid4, color="red",linewidth=3)
ax2.plot(time, pid5, color="green", linewidth=3)

ax4.plot(time, RH, color="black", linewidth=2)
ax5.plot(time, RH, color="black", linewidth=2)

ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')

######## Now the aim is to plot the isoprene against the PID voltages.#########
# Create a figure instance
RHpid4 = RH_cal_data.loc['Slope (mV/%)',:].pid4
RHpid5 = RH_cal_data.loc['Slope (mV/%)',:].pid5
isop4 = pid4 - (RHpid4 * RH)
isop5 = pid5 - (RHpid5 * RH)

isop_plot = plt.figure("Isoprene")

# Create the two subplots
ax1a = isop_plot.add_subplot(2,1,1)
ax2a = isop_plot.add_subplot(2,1,2)

# data_concat RH will return the relative humidity as a voltage so this must be converted to a percentage.

colors = ["red", "blue", "green", "orange", "purple"]

# Making the scatter graphs
ax1a.scatter(isop_mix, isop4, color="red", linewidth=1)
ax2a.scatter(isop_mix, isop5, color="blue", linewidth=1)

# Labelling the axis for the plots.
ax1a.set_xlabel('Isoprene / ppb')
ax2a.set_xlabel('Isoprene / ppb')

ax1a.set_ylabel('PID 4 / mV')
ax2a.set_ylabel('PID 5 / mV') 
# Linear regression
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(isop_mix, isop4)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(isop_mix, isop5)

print ("Gradient PID 4:", slope1)
print ("R2 value pid 4:", R2value1)
print ("Gradient PID 5:", slope2)
print ("R2 value pid 5:", R2value2)
print ("intercept pid 4:", intercept1)
print ("intercept pid 5:", intercept2)


ax1a.plot([np.min(isop_mix), np.max(isop_mix)], [(slope1*np.min(isop_mix))+intercept1, (slope1*np.max(isop_mix))+intercept1])
ax2a.plot([np.min(isop_mix), np.max(isop_mix)], [(slope2*np.min(isop_mix))+intercept2, (slope2*np.max(isop_mix))+intercept2])

import matplotlib.cm as cm
c = time.dayofyear+(time.hour/24.)+(time.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
	
isop_plot1 = plt.figure("Isoprene over time")

# Create the two subplots
ax1b = isop_plot1.add_subplot(2,1,1)
ax2b = isop_plot1.add_subplot(2,1,2)

# Making the scatter graphs
ax1b.scatter(isop_mix, isop4, color=cm.jet(c), linewidth=1)
ax2b.scatter(isop_mix, isop5, color=cm.jet(c), linewidth=1)

# Labelling the axis for the plots.
ax1b.set_xlabel('Isoprene / ppb')
ax2b.set_xlabel('Isoprene / ppb')

ax1b.set_ylabel('PID 4 / mV')
ax2b.set_ylabel('PID 5 / mV') 	
	
corrPID = plt.figure("Corrected PID voltage over time")

ax1 = corrPID.add_subplot(2,1,1)
ax2 = corrPID.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()

ax1.plot(time, isop4, color='red', linewidth=1)
ax2.plot(time, isop5, color='blue', linewidth=1)
ax3.plot(time, isop_mix, color="k", linewidth=1)
ax4.plot(time, isop_mix, color="k", linewidth=1)
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 / mV')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 / mV')
ax3.set_ylabel('Isoprene / ppb')
ax4.set_ylabel('Isoprene / ppb')

plt.show()



### Using the slope to correct for RH. I want to use the slope of the RH calibration on a different file which contains isoprene as well. 

