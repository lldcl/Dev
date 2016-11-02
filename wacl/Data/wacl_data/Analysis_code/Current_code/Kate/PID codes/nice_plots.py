"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

filenames = ['201510/d20151023_01b','201510/d20151023_02','201510/d20151023_03']

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

	isop_cyl = 723.		#ppbv
	mfchi_range = 2000.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	#mfcmid_range = 100. #sccm
	#mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
	dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)  ### Use for the files before the third mfc was introduced
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)
	
	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH = (mean_resampled.RH)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
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

#filter out periods when RH changes rapidly (dRHdt<0.2)
data_concat = data_concat[data_concat.dRHdt_filt == 0]

###############################################
###############################################
#plot up the pid voltages

# Create a figure instance
pidfig = plt.figure("PID voltage over time")
#Create the three subplots to appear in the same window
ax1 = pidfig.add_subplot(2,1,1)
ax2 = pidfig.add_subplot(2,1,2)

ax4 = ax1.twinx()
ax5 = ax2.twinx()

colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
ax1.plot(data_concat.index, data_concat.pid4, color="red",linewidth=3)
ax2.plot(data_concat.index, data_concat.pid5, color="green", linewidth=3)

ax4.plot(data_concat.index, RH, color="black", linewidth=2)
ax5.plot(data_concat.index, RH, color="black", linewidth=2)

ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')



# Now the aim is to plot the RH against the PID voltages.
# Create a figure instance
RH_plot = plt.figure("PID s response to RH")

# Create the two subplots
ax1a = RH_plot.add_subplot(2,1,1)
ax2a = RH_plot.add_subplot(2,1,2)

# data_concat RH will return the relative humidity as a voltage so this must be converted to a percentage.

colors = ["red", "blue", "green", "orange", "purple"]
pid4 = data_concat.pid4*1000
pid5 = data_concat.pid5*1000

# Making the scatter graphs
ax1a.scatter(RH, pid4, color="red", linewidth=1)
ax2a.scatter(RH, pid5, color="blue", linewidth=1)

# Labelling the axis for the plots.
ax1a.set_xlabel('RH %')
ax2a.set_xlabel('RH %')

ax1a.set_ylabel('PID 4 / mV')
ax2a.set_ylabel('PID 5 / mV') 


# Linear regression
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(RH, pid4)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(RH, pid5)

print ("Gradient PID 4:", slope1)
print ("R2 value pid 4:", R2value1)
print ("Gradient PID 5:", slope2)
print ("R2 value pid 5:", R2value2)
print ("intercept pid 4:", intercept1)
print ("intercept pid 5:", intercept2)


ax1a.plot([np.min(RH), np.max(RH)], [(slope1*np.min(RH))+intercept1, (slope1*np.max(RH))+intercept1])
ax2a.plot([np.min(RH), np.max(RH)], [(slope2*np.min(RH))+intercept2, (slope2*np.max(RH))+intercept2])

##### voltage supply versus pid voltage
VS = plt.figure("VS vs PID voltage")
ax1 = VS.add_subplot(2,1,1)
ax2 = VS.add_subplot(2,1,2)
ax1.scatter(data_concat.VS, pid4, color="red")
ax2.scatter(data_concat.VS, pid5, color="blue")

# Labelling the axis for the plots.
ax1.set_xlabel('Supply voltage / V')
ax2.set_xlabel('Supply voltage / V')
ax1.set_ylabel('PID 4 / mV')
ax2.set_ylabel('PID 5 / mV') 


# Linear regression
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(data_concat.VS, pid4)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(data_concat.VS, pid5)
ax1.plot([np.min(data_concat.VS), np.max(data_concat.VS)], [(slope3*np.min(data_concat.VS))+intercept3, (slope3*np.max(data_concat.VS))+intercept3])
ax2.plot([np.min(data_concat.VS), np.max(data_concat.VS)], [(slope4*np.min(data_concat.VS))+intercept4, (slope4*np.max(data_concat.VS))+intercept4])

plt.show()