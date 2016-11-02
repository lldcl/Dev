"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
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
cal_files = ['d20151111_02b']

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

	isop_cyl = 723. 	#ppbv
	mfchi_range = 2000. 	#sccm
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

data_concat = data_concat[data_concat.dRHdt_filt == 0]

data_concat.RH = (((data_concat.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
pid4 = data_concat.pid4*1000
pid5 = data_concat.pid5*1000

def stddev(dat):
	stanRH = np.std(dat)
# 	print "Standard deviation of RH", stanRH
	return stanRH


# Sort the data out so that every 1%RH we take a mean. Essentially 'bin' the data in a similar way to a histogram.
bin = stats.binned_statistic(data_concat.RH , pid4, statistic='mean', bins=list(range(20,100,1)))
bin1 = stats.binned_statistic(data_concat.RH , data_concat.RH, statistic='mean', bins=list(range(20,100,1)))
bin2 = stats.binned_statistic(data_concat.RH , pid5, statistic='mean', bins=list(range(20,100,1)))
bin3 = stats.binned_statistic(data_concat.RH, data_concat.RH, statistic=stddev, bins=list(range(20,100,1)))
bin4 = stats.binned_statistic(data_concat.RH, pid5, statistic=stddev, bins=list(range(20,100,1)))

# Tells the code to convert to pandas, as theen I can get rid of NaNs.
RH = pd.Series(bin1[0])
pid4 = pd.Series(bin[0])
pid5 = pd.Series(bin2[0])
stdRH = pd.Series(bin3[0])
stdpid5 = pd.Series(bin4[0])

RH = RH.dropna()
pid4 = pid4.dropna()
pid5 = pid5.dropna()
stdRH = stdRH.dropna()
stdpid5= stdpid5.dropna()




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

ax1.plot(data_concat.index, data_concat.pid4, color="red", linewidth=3)
ax2.plot(data_concat.index, data_concat.pid5, color="green", linewidth=3)
ax4.plot(data_concat.index, data_concat.RH, color="black", linewidth=2)
ax5.plot(data_concat.index, data_concat.RH, color="black", linewidth=2)

ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')


# Now the aim is to plot the RH against the PID voltages.
# Create a figure instance
RH_plot = plt.figure("PID 4 response to RH")
colors = ["red", "blue", "green", "orange", "purple"]
# Making the scatter graph
plt.plot(RH, pid4, "bo", linewidth=1, label="Binned data")
x = np.array(RH, dtype=float)
pid4 = np.array(pid4, dtype=float)

def func(x, a, b, c, d):
	return a*x**3 + b*x**2 + c*x + d
	
popt, pcov = curve_fit(func, x, pid4)
print "PID4 a= %s , b= %s , c = %s , d = %s" % (popt[0], popt[1], popt[2], popt[3])
xs = sym.Symbol('\lambda')
tex = sym.latex(func(xs,*popt)).replace('$', '')
plt.title(r'$f(\lambda)= %s$' %(tex), fontsize=16)
plt.plot(x, func(x, *popt), label="Fitted Curve")
plt.legend(loc='upper left')


# The calibration curve for PID5
RH_plot1 = plt.figure("PID 5 response to RH")
ax1 = RH_plot1.add_subplot(1,1,1)
colors = ["red", "blue", "green", "orange", "purple"]
# Making the scatter graph. Can change the appearance of the plot.
ax1.plot(RH, pid5, "go",markersize=7, linewidth=5, label="Binned data")
ax1.errorbar(RH, pid5, xerr=stdRH, yerr=stdpid5, lw=1, fmt='o')
ax1.set_xlabel("Relative Humidity (%)")
ax1.set_ylabel(" PID signal (mV)")
x = np.array(RH, dtype=float)
pid5 = np.array(pid5, dtype=float)

def func(x, a, b, c, d):
	return a*x**3 + b*x**2 + c*x + d
	
popt, pcov = curve_fit(func, x, pid5)
print "PID5 a= %s , b= %s , c = %s , d = %s" % (popt[0], popt[1], popt[2], popt[3])
xs = sym.Symbol('\lambda')
tex = sym.latex(func(xs,*popt)).replace('$', '')
#plt.title(r'$f(\lambda)= %s$' %(tex), fontsize=16)
#plt.title("RH Calibration curve", fontsize=16)
ax1.plot(x, func(x, *popt), label="Fitted Curve")
#plt.legend(loc='upper left')
plt.show()

