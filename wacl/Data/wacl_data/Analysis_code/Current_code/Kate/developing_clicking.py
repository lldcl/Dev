import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats



path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201510/'

filenames = ['d20151021_01','d20151021_02','d20151021_03','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151022_03','d20151022_04']
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
# Time average the data to irradicate a lot of the noise, without removing too many datapoints.
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
# This function identifies areas where the RH has changed really rapidly and eliminates them
# as this is unlikely to happen outside and we are just looking at the PID v at steady RHs.
dRHdt = pd.Series(np.absolute(data_concat.RH.diff()),name='dRHdt')
dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
nm_pts = 120./float(Time_avg[:-1])
dRH_ctr=0
for dp in dRHdt:
	if (dp>0.02):
		dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
	dRH_ctr+=1
# Telling the plot to stick the axis together in order to fit all the concatenated data on.
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
ax1 = pidfig.add_subplot(3,1,1)
ax2 = pidfig.add_subplot(3,1,2)
ax3 = pidfig.add_subplot(3,1,3)
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Upgraded to a better DAQfactory therefore the 4.96 value in the RH calculation has been changed to
# data_concat.VS, which is the voltage supply to the MFC.
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
ax1.plot(data_concat.index,data_concat.pid4, color="red",linewidth=3)
ax2.plot(data_concat.index, data_concat.pid5, color="green", linewidth=3)
ax3.plot(data_concat.index, data_concat.pid6, color="blue", linewidth=3)
ax4.plot(data_concat.index, RH, color="black", linewidth=2)
ax5.plot(data_concat.index, RH, color="black", linewidth=2)
ax6.plot(data_concat.index, RH, color="black", linewidth=2)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel('PID 6 / V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')
ax6.set_ylabel('RH %')

######
# data_concat.VS, which is the voltage supply to the MFC.
RH1 = (((data_concat.RH/4.95)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
ax1.plot(data_concat.index, RH1, color="red",linewidth=3)
ax4.plot(data_concat.index, RH, color="black", linewidth=2)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel('PID 6 / V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')
ax6.set_ylabel('RH %')

##################### trying to select a range in order for the slope of the drift to be determined#################
if (stat == 'Y'):
	#select points on graph
	print "Click at either end of range"
	# The two represents how many points the code wants the user to select using the mouse.
	[x,y] = ginput(2) 

	#slice df and calculate stats on selected range
	xmin = int(x[0][0])
	xmax = int(x[1][0])
	ymin = int(y[0][0])
	ymax = int(y[1][0])
	print " The selected time range is:", xmin,xmax
	df_xrange = data.iloc[xmin:xmax]
	print (" The selected RH range is")
	print ymin, ymax
	plt.close()
	pidfig = plt.figure()
	ax1 = pidfig.add_subplot(111)
	colors = ["red", "blue" , "green", "orange", "purple"]
	for n,c in zip(pids,colors):
		ax1.plot(RH,data_concat.pid4,color=c,linewidth=3)
	ax1.plot([xmin,xmin],[np.min(np.min(data_concat[pids]))*0.98,np.max(np.max(data_concat[pids]))*1.02],color='k',linewidth=3)
	ax1.plot([xmax,xmax],[np.min(np.min(data_concat[pids]))*0.98,np.max(np.max(data_concat[pids]))*1.02],color='k',linewidth=3)
	plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("PID / V")
	plt.xlabel("Index")
	
	rangefig = plt.figure()
	ctr = 1
	for p,c in zip(pids,colors):
		sfig = 'pax'+str(ctr)
		sfig = rangefig.add_subplot(len(pids),1,ctr)
		sfig.plot(df_xrange.TheTime,df_xrange[p],color=c)
		sfig.set_ylabel(p+' / V')
		sfig.set_xlabel("Time")
	
		print p
		print 'mean =',np.mean(df_xrange[p])
		print 'stddev =',np.std(df_xrange[p])
		ctr+=1
	rangefig.show()
#################################################