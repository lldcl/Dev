"""Universal pid data file reader/plotter to plot the pid voltage over time, then the 
pid voltage corrected for RH.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats
import sympy as sym
from scipy.optimize import curve_fit
from numpy import *


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# Takes the file name and extracts the date then sticks this on the front to make the file path. 
stat = 'Y'
#cal_files = ['d20151021_01','d20151021_02','d20151021_04','d20151021_05','d20151022_02','d20151023_01b','d20151023_02','d20151023_03']
cal_files = ['d20151112_06']

for i in cal_files:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i

#for f in filenames:
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
	

	Time_avg = '100S'

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

data_concat = data_concat[data_concat.dRHdt_filt == 0]

isop_cyl = 723. 	#ppbv
mfchi_range = 2000. 	#sccm
mfchi_sccm = data_concat.mfchiR*(mfchi_range/5.)
mfclo_range = 20.	#sccm
mfclo_sccm = data_concat.mfcloR*(mfclo_range/5.)
mfcmid_range = 100. #sccm
mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)  ### Use for the files before the third mfc was introduced
isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
data = pd.concat([data,isop_mr],axis=1)
	
RH = (((data_concat.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)

pid4 = data_concat.pid4*1000
pid5 = data_concat.pid5*1000
pid6 = data_concat.pid6*1000

#plot up the pid voltages over time (without the RH correction)
#Create a figure instance
pidfig = plt.figure()
#Create the three sub plots, so they all appear in the same window
ax1 = pidfig.add_subplot(3,1,1)
ax2 = pidfig.add_subplot(3,1,2)
ax3 = pidfig.add_subplot(3,1,3)
# I want the relative humidity to be plotted on the same graph as the PID voltages so must create 
# secondary axes for each graph.
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective graphs.
ax1.plot(data_concat.index, pid4, color = "red",linewidth=3)
ax2.plot(data_concat.index, pid5, color = "green", linewidth=3)
ax3.plot(data_concat.index, pid6, color = "blue", linewidth=3)
ax4.plot(data_concat.index, RH, color="black", linewidth=3)
ax5.plot(data_concat.index, RH, color="black", linewidth=3)
ax6.plot(data_concat.index, RH, color="black",linewidth=3)
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


# Trying to calibrate for RH
# Tell the program to get the data from the various columns then do the calculation on it
prepid = (0.0019709*(RH) + 54.1918)
cpid5 = pid5 - prepid


#plot up the pid voltages without the correction
#Create a figure instance
RHcorr = plt.figure()
ax1 = RHcorr.add_subplot(1,1,1)
ax1.plot(data_concat.index, prepid, color = "green", linewidth=3)
ax1.set_xlabel("Time")
ax1.set_ylabel("Predicted PID 5 signal / mV")


RHcorr1 = plt.figure()

ax2 = RHcorr1.add_subplot(1,1,1)
ax3 = ax2.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
ax2.plot(data_concat.index, cpid5, color="blue", linewidth=3)
ax2.set_ylabel("Remainder signal after the predicted was subtracted from actual")
ax3.plot(data_concat.index, isop_mr, "k")
plt.show()