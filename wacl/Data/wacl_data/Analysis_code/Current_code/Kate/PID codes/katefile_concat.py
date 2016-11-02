"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats



path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201511/'

#filenames = ['d20151021_01','d20151021_02','d20151021_03','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151022_03','d20151022_04','d20151023_01b','d20151023_02','d20151023_03']
#filenames = ['d20151026_05']
#filenames = ['d20151023_02', 'd20151023_03', 'd20151022_04']
filenames = ['d20151112_06']
#filenames = ['d20151021_01','d20151021_02','d20151021_03','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151022_03','d20151022_04']
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

	isop_cyl = 723.	#13.277	#ppbv
	mfchi_range = 2000.	#100.	#sccm
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
data_concat = data_concat.dropna()
#filter out periods when RH changes rapidly (dRHdt<0.2)
data_concat = data_concat[data_concat.dRHdt_filt == 0]
#mean_dRHdt_filt
#concat_filename = str(path+'30sconcat_1021.csv')
#data_concat.to_csv(path_or_buf=concat_filename)
# def reject_outliers(data_concat):
# The purpose of this is to filter out the outliers when the instrumentation was changed.
"""u = np.mean(data_concat.pid4)
s = np.std(data_concat.pid4)
ectr = 0
for e in data_concat.pid4:
	if (np.logical_or(e > u+1.2*s,e < u-1.2*s)):
		data_concat.pid4[ectr] = u
# 		print 'In loop',np.logical_or(e > u+s,e < u-s)
	ectr+=1"""

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

# plotting mfcloR
mfc = plt.figure("MFC lo")
ax1 = mfc.add_subplot(1,1,1)
ax1.plot(data_concat.index, data_concat.mfcloR, color="blue", linewidth=2)
ax1.set_xlabel('Index')
ax1.set_ylabel('MFC lo R')


# Now the aim is to plot the RH against the PID voltages.
# Create a figure instance
RH_plot = plt.figure("PID s response to RH")

# Colour coding the points according to time
import matplotlib.cm as cm
# Changing the date time to a number between 0 and 1. 
c=data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
# Create the three subplots
ax1a = RH_plot.add_subplot(3,1,1)
ax2a = RH_plot.add_subplot(3,1,2)
ax3a = RH_plot.add_subplot(3,1,3)

# data_concat RH will return the relative humidity as a voltage so this must be converted to a percentage.
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp*10)
colors = ["red", "blue", "green", "orange", "purple"]
data_concat.pid4 = data_concat.pid4*1000
data_concat.pid5 = data_concat.pid5*1000
data_concat.pid6 = data_concat.pid6*1000
# Making the scatter graphs
ax1a.scatter(RH, data_concat.pid4, color=cm.jet(c), linewidth=1)
ax2a.scatter(RH, data_concat.pid5, color=cm.jet(c), linewidth=1)
ax3a.scatter(RH, data_concat.pid6, color=cm.jet(c), linewidth=1)
"""ax1a.scatter(RH, data_concat.pid4, color="red", linewidth=1)
ax2a.scatter(RH, data_concat.pid5, color="b", linewidth=1)
#ax3a.scatter(RH, data_concat.pid6, color="green", linewidth=1)""" # Use if you dont want the colour coding by time
# Labelling the axis for the plots.
ax1a.set_xlabel('RH %')
ax2a.set_xlabel('RH %')
ax3a.set_xlabel('RH %')
ax1a.set_ylabel('PID 4 / mV')
ax2a.set_ylabel('PID 5 / mV') 
ax3a.set_ylabel('PID6 / mV')
# Axes limits to be 10% higher and lower than the largest and smallest points respectively
"""ax1a.set_ylim((np.min(data_concat.pid4)*0.99), np.max(data_concat.pid4)*1.01)
#ax2a.set_ylim(55.,56.)
ax2a.set_ylim(np.min(data_concat.pid5)*0.999), np.max(data_concat.pid5)*1.001)
ax3a.set_ylim((np.min(data_concat.pid6)*0.99), np.max(data_concat.pid6)*1.01)"""
# Linear regression
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(RH, data_concat.pid4)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(RH, data_concat.pid5)
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(RH, data_concat.pid6)
print ("Gradient PID 4:", slope1)
print ("R2 value pid 4:", R2value1)
print ("Gradient PID 5:", slope2)
print ("R2 value pid 5:", R2value2)
print ("intercept : ", intercept2)
print ("Gradient PID 6:", slope3)
print ("R2 value pid 6:", R2value3)

ax1a.plot([np.min(RH), np.max(RH)], [(slope1*np.min(RH))+intercept1, (slope1*np.max(RH))+intercept1])

ax2a.plot([np.min(RH), np.max(RH)], [(slope2*np.min(RH))+intercept2, (slope2*np.max(RH))+intercept2], color="k", linewidth=5, label =  'Equation: y= 3.64E-2 x + 52.7' )
plt.legend()
ax3a.plot([np.min(RH), np.max(RH)], [(slope3*np.min(RH))+intercept3, (slope3*np.max(RH))+intercept3])



# Just PID 5 as it behaves the best. 

pid5 = plt.figure("PID 5")
ax1b = pid5.add_subplot(1,1,1)
ax1b.scatter(RH, data_concat.pid5, color=cm.jet(c), linewidth=1, label = "Equation y= 0.04248x + 52.41")
plt.legend()
ax1b.set_xlabel('RH %')
ax1b.set_ylabel('PID 5 / mV')
slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(RH, data_concat.pid5)
ax1b.plot([np.min(RH), np.max(RH)], [(slope5*np.min(RH))+intercept5, (slope5*np.max(RH))+intercept5], color="purple", linewidth=5)
print ('Gradient :',slope5)
print ('R2 value', R2value5)
print ('Intercept',intercept5)
plt.show()

######## Looking at how the VS affects it.

RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
RH1 = (((data_concat.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
VS = plt.figure("Observing VS")

ax1 = VS.add_subplot(3,1,1)
ax2 = VS.add_subplot(3,1,2)
ax3 = VS.add_subplot(3,1,3)
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
    
ax1.plot(data_concat.index, data_concat.pid4, '-', color="red", label='PID',linewidth=3)
ax2.plot(data_concat.index, data_concat.pid5, '-', color="green", label='PID', linewidth=3)
ax3.plot(data_concat.index, data_concat.pid6, '-', color="orange", label='PID', linewidth=3)
ax4.plot(data_concat.index, RH, '-', color="purple", label='RH with VS', linewidth=2)
ax4.plot(data_concat.index, RH1, '-', color="blue", label='RH with constant', linewidth=2)
ax5.plot(data_concat.index, RH, '-', color="purple", label='RH with VS', linewidth=2)
ax5.plot(data_concat.index, RH1, '-', color="blue", label='RH with constant', linewidth=2)
ax6.plot(data_concat.index, RH, '-', color="purple", label='RH with VS', linewidth=2)
ax6.plot(data_concat.index, RH1, '-', color="blue", label='RH with constant', linewidth=2)
plt.legend(loc='upper left');
ax1.set_ylim((np.min(data_concat.pid4)*0.99), np.max(data_concat.pid4)*1.01)
ax2.set_ylim((np.min(data_concat.pid5)*0.99), np.max(data_concat.pid5)*1.01)
ax3.set_ylim((np.min(data_concat.pid6)*0.99), np.max(data_concat.pid6)*1.01)
ax1.set_xlim((np.min(data_concat.index)), np.max(data_concat.pid4))
ax2.set_xlim((np.min(data_concat.index)), np.max(data_concat.pid5))
ax3.set_xlim((np.min(data_concat.index)), np.max(data_concat.pid6))
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

plt.show()

"""#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(3,1,1)
rhax.plot(data_concat.index,data_concat.RH,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(3,1,2)
isopax.plot(data_concat.index,data_concat.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("Isop / ppbv")

varfig.show()"""

