## De-trending the data.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats, signal

# The path to get the files
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201510/'
# The file/s I want to look at
filenames = ['d20151023_03']
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
# Determining isoprene concentration. Not relevant atm.
"""	isop_cyl = 1100.	#13.277	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1) """
	
	
# Time averaging over 10 seconds.
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
#mean_dRHdt_filt
#concat_filename = str(path+'30sconcat_1021.csv')
#data_concat.to_csv(path_or_buf=concat_filename)

###############################################
#plot up the pid voltages
# Create a figure instance
pidfig = plt.figure("PID voltage over time")
#Create the three subplots to appear in the same window
ax1 = pidfig.add_subplot(1,1,1)
# Secondary axis
ax2 = ax1.twinx()

colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Calculating RH from the voltage.
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
# Plotting the graph for PID 5.
ax1.plot(data_concat.index, data_concat.pid5, color="green", linewidth=3)
# Plotting the RH on the secondary axis.
ax2.plot(data_concat.index, RH, color="black", linewidth=2)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 5 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('RH')

############### Re plot the data after it has been detrended.
#plot up the pid voltages
# Create a figure instance
pidfig1 = plt.figure("PID voltage over time- detrended")
#Create the three subplots to appear in the same window
ax1a = pidfig1.add_subplot(2,1,1)
ax1a.plot(data_concat.index, data_concat.pid5, color="blue", label="Original", linewidth=3)
# Secondary axis
ax2a = ax1a.twinx()
#ax2a = pidfig1.add_subplot(2,1,1)
y = signal.detrend(data_concat.pid5)
ax2a.plot(data_concat.index, y, color="green", label="Detrended")

ax3a = pidfig1.add_subplot(2,1,1)
ax3a.plot(data_concat.index, data_concat.pid5 - y, color="red", label="mean")

ax1a.set_xlabel('Time')
ax2a.set_ylabel('detrended')
ax1a.set_ylabel('PID 5 / V')
plt.legend(bbox_to_anchor=(0.05,0.01), loc=3, borderaxespad=0.)

plt.show() 

### Make the pid vs RH graph
RH_plot = plt.figure()
ax1 = RH_plot.add_subplot(1,1,1)
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
colors = ["red", "blue", "green", "orange", "purple"]
# Making the scatter graphs
ax1.scatter(RH, y, color="purple", linewidth=1)
ax1.set_xlabel('RH %')
ax2a.set_ylabel('Detrended pid')

plt.show()

"""
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Calculating RH from the voltage.
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
pid5mean = np.mean(data_concat.pid5)
print ("mean:", pid5mean)
# Plotting the graph for PID 5.
ax1a.plot(data_concat.index, data_concat.pid5, color="blue", linewidth=3)
# Plotting the RH on the secondary axis.
#ax2a.plot(data_concat.index, RH, color="black", linewidth=2)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)

ax1a.set_xlabel('Time')
ax1a.set_ylabel('PID 5 /V')
#ax2a.set_xlabel('Time')
#ax2a.set_ylabel('RH')
detrend_pid5 = detrend(data_concat.pid5);
trend = data_concat.pid5 - detrend_pid5;
avedet = np.mean(detrend_pid5)
print (" trend:", avedet)
#scipy.signal.detrend(data_concat.pid5, axis=-1, type='constant', bp=0)
ax1a.plt(data_concat.index, trend, ':r')
ax2a.plt(data_concat.index, zeros(size(data_concat.index)), ':k')
plt.legend('Oringinal data','Trend','Detrended data','Mean of detrended data')
#(signal.detrend(data_concat.pid5, type=='linear', bp=0))
#(signal.detrend(data_concat.index, type=='linear', bp=0))
plt.show()

"""