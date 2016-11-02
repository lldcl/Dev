"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201510/'
# Write the files that you want to concantenate here.
filenames = ['d20151021_01','d20151021_02','d20151021_03','d20151021_04','d20151021_06']


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

	isop_cyl = 1100.	#13.277	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH = (((mean_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*10.)
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

# concat_filename = str(path+'30sconcat_1021.csv')
# data_concat.to_csv(path_or_buf=concat_filename)

################################################
#plot up the pid voltages
pidfig = plt.figure()
ax1 = pidfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(data_concat.index,data_concat[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")
plt.show()

#plot up the pid voltages over time (without the RH correction)
#Create a figure instance
pidfig = plt.figure()
#Create the three sub plots, so they all appear in the same window
ax1 = pidfig.add_subplot(3,1,1)
ax2 = pidfig.add_subplot(3,1,2)
ax3 = pidfig.add_subplot(3,1,3)
# I want the relative humidity to be plotted on the same graph as the PID voltages so must create 
# secondary axes for each graph.
RH = (((data_concat.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective graphs.
ax1.plot(data_concat.TheTime, data_concat.pid4, color="red",linewidth=3)
ax2.plot(data_concat.TheTime, data_concat.pid5, color = "green", linewidth=3)
ax3.plot(data_concat.TheTime, data_concat.pid6, color = "blue", linewidth=3)
ax4.plot(data_concat.TheTime, RH, color="black", linewidth=3)
ax5.plot(data_concat.TheTime, RH, color="black", linewidth=3)
ax6.plot(data_concat.TheTime, RH, color="black",linewidth=3)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel('PID 6 /V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')
ax6.set_ylabel('RH %')
# Setting the title for the overall figure
pidfig.set_label('Uncalibrated PID data')

	
########################
# The second set of graphs plot the relative humidity (RH) against the PID voltages
# To remove the values that aren't numbers, it gets rid of the NaN things.
data = data_concat.dropna()
RHplot = plt.figure()
#Create the three sub plots, so they all appear in the same window
ax1a = RHplot.add_subplot(3,1,1)
ax2a = RHplot.add_subplot(3,1,2)
ax3a = RHplot.add_subplot(3,1,3)
# data.RH gives the relative humidity as a voltage, so need to turn this into a n absolute value:
RH = (((data.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data.Temp)
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective scatter graphs. The 'o' command tells the code to plot with dots, not as a line graph.
ax1a.plot(RH, data_concat.pid4, 'o', color="purple", linewidth=1)
ax2a.plot(RH, data_concat.pid5, 'o', color = "green", linewidth=1)
ax3a.plot(RH, data_concat.pid6, 'o', color = "blue", linewidth=1)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1a.set_xlabel('RH (%)')
ax1a.set_ylabel('PID 4 /V')
ax2a.set_xlabel('RH (%)')
ax2a.set_ylabel(' PID 5 /V')
ax3a.set_xlabel('RH (%)')
ax3a.set_ylabel('PID 6 /V')
# The linear regression of the data points.

# Linear regression using scipy. The function will return the following 5 parameters in that order.
slope1, intercept1, R2_value1, p_value1, st_err1 = stats.linregress(RH,data_concat.pid4)
slope2, intercept2, R2_value2, p_value2, st_err2 = stats.linregress(RH,data_concat.pid5)
slope3, intercept3, R2_value3, p_value3, st_err3 = stats.linregress(RH,data_concat.pid6)
print ("Gradient pid 4:", slope1)
print ("R2 value pid 4:", R2_value1)
print ("Gradient pid 5:", slope2)
print ("R2 value pid 5:", R2_value2)
print ("Gradient pid 6:", slope3)
print ("R2 value pid 6:", R2_value3)

ax1a.plot([np.min(RH), np.max(RH)], [(slope1*np.min(RH))+intercept1, (slope1*np.max(RH))+intercept1])
ax2a.plot([np.min(RH), np.max(RH)], [(slope2*np.min(RH))+intercept2, (slope2*np.max(RH))+intercept2])
ax3a.plot([np.min(RH), np.max(RH)], [(slope3*np.min(RH))+intercept3, (slope3*np.max(RH))+intercept3])

print ("Start time:", np.min(data_concat.TheTime))
print ("End time:", np.max(data_concat.TheTime))
print ("RH range:", (np.max(RH) - np.min(RH)))
print ("RH max:", np.max(RH))

plt.show()

"""#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(3,1,1)
rhax.plot(data_concat.index,data_concat.RH,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(3,1,2)
isopax.plot(data_concat.index,data_concat.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("Isop / ppbv")

varfig.show()

"""