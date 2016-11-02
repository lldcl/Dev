## Isoprene data- want to plot isoprene vs PID over very small changes in RH (70-72% RH) ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201510/'

filenames = ['d20151026_05','d20151027_02b','d20151027_03b','d20151028_01b','d20151028_02b','d20151028_03b','d20151029_02','d20151029_03b']
#filenames = ['d20151103_02','d20151103_03','d20151103_04']
#filenames = ['d20151023_03']
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
	#mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
	dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)
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

# Select the data points for which RH= 70- 72%RH
# Creates a new dataframe which selects ALL the data when RH is lower than 72% and higher than 70%.
# The new data frame is called RHselect, and it is taking data from the mean_resampled dataframe,
# under the condition that RH is within this range.
data_RH = mean_resampled[mean_resampled.RH >70]
data_RH1 = data_RH[data_RH.RH <80]

# Create a figure instance
pidfig = plt.figure("PID voltage over time")
#Create the three subplots to appear in the same window
ax1 = pidfig.add_subplot(2,1,1)
ax2 = pidfig.add_subplot(2,1,2)

ax4 = ax1.twinx()
ax5 = ax2.twinx()

colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
RH = data_RH1.RH
ax1.plot(data_RH1.index, data_RH1.pid4, color="red",linewidth=3)
ax2.plot(data_RH1.index, data_RH1.pid5, color="green", linewidth=3)

ax4.plot(data_RH1.index, RH, color="black", linewidth=2)
ax5.plot(data_RH1.index, RH, color="black", linewidth=2)

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
pid4 = data_RH1.pid4*1000
pid5 = data_RH1.pid5*1000

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

plt.show()
