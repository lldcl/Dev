## Isoprene data ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats



path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201511/'

#filenames = ['d20151021_02','d20151021_03','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151022_03','d20151022_04','d20151023_01','d20151023_02','d20151023_03']
filenames = ['d20151103_02']
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
# Determining the isoprene concentration:
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

#filter out periods when RH changes rapidly (dRHdt<0.2)
# Creates a new dataframe which selects ALL the data when isoprene conc is lower than 1.
# The new data frame is called daa_lowIsop, and it is taking data from the data_concat dataframe,
# under the condition that isoprene is less than 1 ppb.
data_lowIsop = data_concat[data_concat.isop_mr <15]
data_highIsop = data_concat[data_concat.isop_mr >3]
#mean_dRHdt_filt
#concat_filename = str(path+'30sconcat_1021.csv')
#data_concat.to_csv(path_or_buf=concat_filename)

isoprene = plt.figure("Isoprene")
ax1 = isoprene.add_subplot(1,1,1)
ax1.plot(data.index, data.isop_mr, color="green", linewidth=2)
ax1.set_xlabel("Index")
ax1.set_ylabel("Isoprene / ppbv")

# Separating the high and low isoprene
isoplo = plt.figure("Low and high Isoprene")
ax1 = isoplo.add_subplot(2,1,1)
ax2 = isoplo.add_subplot(2,1,2)

ax1.plot(data_lowIsop.index, data_lowIsop.isop_mr, color="purple", linewidth=2)
ax2.plot(data_highIsop.index, data_highIsop.isop_mr, color="red", linewidth=2)
ax1.set_ylim(0.55, 0.6)
ax1.set_xlabel("Index")
ax1.set_ylabel("Isoprene / ppbv")
ax2.set_xlabel("Index")
ax2.set_ylabel("Isoprene / ppbv")


# Plotting isoprene with RH and PIDs
pidplot = plt.figure("PIDs")
ax1 = pidplot.add_subplot(3,1,1)
ax2 = pidplot.add_subplot(3,1,2)
ax3 = pidplot.add_subplot(3,1,3)
ax4 = ax2.twinx()

import matplotlib.cm as cm
# Changing the date time to a number between 0 and 1. 
c=data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
ax1.plot(data_lowIsop.index, data_lowIsop.isop_mr, color="blue", linewidth = 2)
#ax1.set_ylim(0.55, 0.6)
ax1.set_ylabel("Isoprene / ppbv")
ax1.set_xlabel("Time")
ax2.plot(data_lowIsop.index, data_lowIsop.pid4, color="red", linewidth = 2) 
ax2.set_ylabel("PID 4 / V")
ax4.plot(data_lowIsop.index, data_lowIsop.pid5, color="green", linewidth = 2)
ax4.set_ylabel("PID 5")
ax2.plot(data_lowIsop.index, data_lowIsop.pid6, color="purple", linewidth = 2)
ax3.scatter(data_lowIsop.index, data_lowIsop.RH, color=cm.jet(c), linewidth = 2)
ax3.set_ylabel("RH %")
ax3.set_xlabel("Time")



## Plot RH vs PID data for the low isoprene conc.
# To remove the values that aren't numbers, it gets rid of the NaN things.
data = data.dropna()
RHplot = plt.figure(" Colour coded by time")
#Create the three sub plots, so they all appear in the same window
ax1a = RHplot.add_subplot(3,1,1)
ax2a = RHplot.add_subplot(3,1,2)
ax3a = RHplot.add_subplot(3,1,3)
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):

# Creating the three respective scatter graphs. The 'o' command tells the code to plot with dots, not as a line graph.
ax1a.scatter(data_lowIsop.RH, data_lowIsop.pid4, color=cm.jet(c), linewidth=1)
ax2a.scatter(data_lowIsop.RH, data_lowIsop.pid5, color = cm.jet(c), linewidth=1)
ax3a.scatter(data_lowIsop.RH, data_lowIsop.pid6, color = cm.jet(c), linewidth=1)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1a.set_xlabel('RH (%)')
ax1a.set_ylabel('PID 4 /V')
ax1a.set_ylim(0.0596, 0.0603)
ax2a.set_xlabel('RH (%)')
ax2a.set_ylabel(' PID 5 /V')
ax2a.set_ylim(0.0550, 0.0560)
ax3a.set_xlabel('RH (%)')
ax3a.set_ylabel('PID 6 /V')
ax3a.set_ylim(0.0580, 0.0600)
# The linear regression of the data points.

# Linear regression using scipy. The function will return the following 5 parameters in that order.
slope1, intercept1, R2_value1, p_value1, st_err1 = stats.linregress(data_lowIsop.RH, data_lowIsop.pid4)
slope2, intercept2, R2_value2, p_value2, st_err2 = stats.linregress(data_lowIsop.RH, data_lowIsop.pid5)
slope3, intercept3, R2_value3, p_value3, st_err3 = stats.linregress(data_lowIsop.RH, data_lowIsop.pid6)
print ("Gradient pid 4:", slope1)
print ("R2 value pid 4:", R2_value1)
print ("Gradient pid 5:", slope2)
print ("R2 value pid 5:", R2_value2)
print ("Gradient pid 6:", slope3)
print ("R2 value pid 6:", R2_value3)

ax1a.plot([np.min(data_lowIsop.RH), np.max(data_lowIsop.RH)], [(slope1*np.min(data_lowIsop.RH))+intercept1, (slope1*np.max(data_lowIsop.RH))+intercept1])
ax2a.plot([np.min(data_lowIsop.RH), np.max(data_lowIsop.RH)], [(slope2*np.min(data_lowIsop.RH))+intercept2, (slope2*np.max(data_lowIsop.RH))+intercept2])
ax3a.plot([np.min(data_lowIsop.RH), np.max(data_lowIsop.RH)], [(slope3*np.min(data_lowIsop.RH))+intercept3, (slope3*np.max(data_lowIsop.RH))+intercept3])

## Plot RH vs PID data for the low isoprene conc.
# To remove the values that aren't numbers, it gets rid of the NaN things.
data = data.dropna()
RHplot = plt.figure(" Colour coded by Isoprene")
#Create the three sub plots, so they all appear in the same window
ax1a = RHplot.add_subplot(3,1,1)
ax2a = RHplot.add_subplot(3,1,2)
ax3a = RHplot.add_subplot(3,1,3)
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
import matplotlib.cm as cm
# Changing the date time to a number between 0 and 1. 
i = (data_lowIsop.isop_mr-np.min(data_lowIsop.isop_mr))/np.max(data_lowIsop.isop_mr-np.min(data_lowIsop.isop_mr))
# Creating the three respective scatter graphs. The 'o' command tells the code to plot with dots, not as a line graph.
ax1a.scatter(data_lowIsop.RH, data_lowIsop.pid4, color = cm.jet(i), linewidth=1)
ax2a.scatter(data_lowIsop.RH, data_lowIsop.pid5, color = cm.jet(i), linewidth=1)
ax3a.scatter(data_lowIsop.RH, data_lowIsop.pid6, color = cm.jet(i), linewidth=1)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1a.set_xlabel('RH (%)')
ax1a.set_ylabel('PID 4 /V')
ax1a.set_ylim(0.0596, 0.0603)
ax2a.set_xlabel('RH (%)')
ax2a.set_ylabel(' PID 5 /V')
ax2a.set_ylim(0.0550, 0.0560)
ax3a.set_xlabel('RH (%)')
ax3a.set_ylabel('PID 6 /V')
ax3a.set_ylim(0.0580, 0.0600)
# The linear regression of the data points.


## Checking the mass flow controllers ###
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
"""
#filter out periods when RH changes rapidly (dRHdt<0.2)
# Creates a new dataframe which selects ALL the data when isoprene conc is lower than 1.
# The new data frame is called daa_lowIsop, and it is taking data from the data_concat dataframe,
# under the condition that isoprene is less than 1 ppb.
data_oddisop = data_concat[ddata_concat.isop_mrdt !=0]
data_highIsop = data_concat[data_concat.isop_mr <1]"""


