### Determining a constant to use for a temperature correction.
"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# Takes the file name and extracts the date then sticks this on the front to make the file path.""" 
stat = 'Y'

#cal_files = ['d20151201_05','d20151203_07','d20151204_04','d20151207_05','d20151208_04','d20151209_02','d20151210_08','d20151211_03']
#cal_files = ['d20151201_01','d20151201_02','d20151201_03','d20151201_04','d20151201_05','d20151202_01','d20151203_04','d20151203_06','d20151203_07']
cal_files = ['d20160209_01']

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

	isop_cyl = 685.4822 	#ppbv
	mfchi_range = 2000. 	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100. #sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
	#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)  ### Use for the files before the third mfc was introduced
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)
	
	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	#filter out periods when isop changes rapidly (disopdt<0.1) and for 300 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	disopdt = pd.Series(np.absolute(mean_resampled.isop_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>0.1):
			disopdt_filt[disop_ctr:int(disop_ctr+nm_pts)] = 1
		disop_ctr+=1

	mean_resampled = pd.concat([mean_resampled,disopdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,disopdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.disopdt_filt == 0]
	
# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

dt = pd.Series((data_concat.index - data_concat.index[0]),index=data_concat.index,name='dt')
dt = dt.astype('timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])


Tempa = (data.Temp *100.)
#Tempb = (data.RH2 * 100)
RHa = (((data.RH1/data.VS)-0.16)/0.0062)/(1.0546-0.00216*Tempa)
#RHb = (((data.RH1/data.VS)-0.16)/0.0062)/(1.0546-0.00216*Tempb)


#Graph 1: Plotting up all the variables
MOS1 = plt.figure("All Variables with MOS1")
ax1 = MOS1.add_subplot(5,1,1)
ax2 = MOS1.add_subplot(5,1,2)
ax3 = MOS1.add_subplot(5,1,3)
ax4 = MOS1.add_subplot(5,1,4)
ax5 = MOS1.add_subplot(5,1,5)

ax1.plot(data_concat.index, data_concat.MOS1, linewidth=3, color="g", label="MOS1")
ax2.plot(data_concat.index, data_concat.RH1, linewidth=3, color="b", label="RH")
ax3.plot(data_concat.index, data_concat.Temp, linewidth=3, color="r", label="Temp")
ax4.plot(data_concat.index, data_concat.VS, color="k")
ax5.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax4.set_xlabel("Time")

# Graph 2: All variables for MOS2
#Graph 1: Plotting up all the variables
MOS1 = plt.figure("All Variables with MOS2")
ax1 = MOS1.add_subplot(5,1,1)
ax2 = MOS1.add_subplot(5,1,2)
ax3 = MOS1.add_subplot(5,1,3)
ax4 = MOS1.add_subplot(5,1,4)
ax5 = MOS1.add_subplot(5,1,5)

ax1.plot(data_concat.index, data_concat.MOS2, linewidth=3, color="g", label="MOS1")
ax2.plot(data_concat.index, data_concat.RH1, linewidth=3, color="b", label="RH")
ax3.plot(data_concat.index, data_concat.Temp, linewidth=3, color="r", label="Temp")
ax4.plot(data_concat.index, data_concat.VS, color="k")
ax5.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS2 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax4.set_xlabel("Time")
MOS2 = plt.figure("All Variables with MOS2")


###### Filtering out isoprene- use the data_concat dataframe. dt is the time since the start of the run.
Temp = (data_concat.Temp *100.)
#Temp2 = (data_concat.RH1 * 100)
RH = (((data_concat.RH1/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*Temp)
#RH2 = (((data_concat.RH1/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*Temp2)

# Plots
mosfig = plt.figure("MOS siganl" )
mos1ax = mosfig.add_subplot(2,1,1)
mos1ax.plot(data_concat.dt,data_concat.MOS1,color='b',marker='o')
mos1ax.set_ylabel("MOS1 (V)")
ax2 = mos1ax.twinx()
ax2.plot(data_concat.dt,data_concat.isop_mr,color='k')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
plt.ylabel("Isoprene")

mos1ax = mosfig.add_subplot(2,1,2)
mos1ax.plot(data_concat.dt,data_concat.MOS2,color='r',marker='o')
mos1ax.set_ylabel("MOS2 (V)")
ax2 = mos1ax.twinx()
ax2.plot(data_concat.dt,data_concat.isop_mr,color='k')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
plt.ylabel("Isoprene")


######### Graph 3: Plotting up all the variables when there is no isoprene
noI = data_concat[data_concat.isop_mr < 0.5]
Temp = noI.Temp*100
RH = noI.RH1
MOSnoI = plt.figure("Gradient for background drift")
mos1ax = MOSnoI.add_subplot(2,1,1)
mos2ax = MOSnoI.add_subplot(2,1,2)
ax3 = mos1ax.twinx()
ax4 = mos2ax.twinx()
mos1ax.plot(noI.dt, noI.MOS1, color='g',marker='o')
mos2ax.plot(noI.dt, noI.MOS2, color='m',marker='o')
ax3.plot(noI.dt, RH, color='b', linewidth=3)
ax3.plot(noI.dt, Temp, color='r', linewidth=3)
ax4.plot(noI.dt, RH, color='b', linewidth=3)
ax4.plot(noI.dt, Temp, color='r', linewidth=3)
mos1ax.set_ylabel("MOS1 (V)")
mos2ax.set_ylabel("MOS2 (V)")
ax3.set_ylabel("Relative humidity")
ax4.set_ylabel("Relative Humidity")

slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(noI.dt, noI.MOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(noI.dt, noI.MOS2)
mos1ax.plot([np.min(noI.dt), np.max(noI.dt)], [(slope1*np.min(noI.dt))+intercept1, (slope1*np.max(noI.dt))+intercept1])
mos2ax.plot([np.min(noI.dt), np.max(noI.dt)], [(slope2*np.min(noI.dt))+intercept2, (slope2*np.max(noI.dt))+intercept2])
print ("Gradient MOS1 background", slope1)
print ("Intercept MOS1", intercept1)
print ("R2 MOS1", R2value1)
print ("Gradient MOS2", slope2)
print ("Intercept MOS2", intercept2)
print ("R2 MOS2 background", R2value2)
print ("Average RH", np.mean(RH))
print ("Average temp", np.mean(Temp))

# Finding the RH sensitivity
RHplot = plt.figure("As RH increases, MOS signal...")
ax1 = RHplot.add_subplot(2,1,1)
ax2 = RHplot.add_subplot(2,1,2)
ax1.scatter(data_concat.RH1, data_concat.MOS1, color="g")
#ax1.errorbar(data_concat.RH1, data_concat.MOS1, xerr=stIs, yerr=st1, lw=1, fmt='o', color="g")
ax2.scatter(data_concat.RH1, data_concat.MOS2, color="b")
#ax2.errorbar(isop, back2, xerr=stIs, yerr=st2, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_ylabel("MOS2 signal / v")
ax1.set_xlabel("RH / %")
ax2.set_xlabel("RH / %")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(data_concat.RH1, data_concat.MOS1)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(data_concat.RH1, data_concat.MOS2)
ax1.plot([np.min(data_concat.RH1), np.max(data_concat.RH1)], [(slope3*np.min(data_concat.RH1))+intercept3, (slope3*np.max(data_concat.RH1))+intercept3])
ax2.plot([np.min(data_concat.RH1), np.max(data_concat.RH1)], [(slope4*np.min(data_concat.RH1))+intercept4, (slope4*np.max(data_concat.RH1))+intercept4])
print ("Gradient of RH vs MOS1", slope3)
print ("Intercept of RH vsMOS1", intercept3)
print ("R2 of RH vs MOS1", R2value3)
print ("Gradient of RH vs MOS2", slope4)
print ("Intercept of RH vs MOS2", intercept4)
print ("R2 of RH vs MOS2", R2value4)
plt.show()
"""#Correct for total "background"
back1 = data_concat.MOS1 - (slope1 * (data_concat.dt)+intercept1)
back2 = data_concat.MOS2 - (slope2 * (data_concat.dt)+intercept2)
index1 = plt.figure("Plot MOS over time with the background drift removed")
ax1 = index1.add_subplot(2,1,1)
ax2 = index1.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
ax1.plot(data_concat.dt, back1, color="g", marker='o')
ax2.plot(data_concat.dt, back2, color="b", marker='o')
ax3.plot(data_concat.dt, data_concat.isop_mr, color="k")
ax4.plot(data_concat.dt, data_concat.isop_mr, color="k")
ax1.set_ylabel("Corrected MOS1 signal / V")
ax1.set_xlabel("Index")
ax2.set_ylabel(" Corrected MOS2 signal / V")
ax2.set_xlabel("Index")


# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 0.25 ppb of isoprene sections
bin1 = stats.binned_statistic(data_concat.isop_mr, back1, statistic='mean', bins=60, range=(0,15))
bin2 = stats.binned_statistic(data_concat.isop_mr, back2, statistic='mean', bins=60, range=(0,15))
bin3 = stats.binned_statistic(data_concat.isop_mr, data_concat.isop_mr, statistic='mean', bins=60, range=(0,15))
bin4 = stats.binned_statistic(data_concat.isop_mr, back1, statistic=stddev, bins=60, range=(0,15))
bin5 = stats.binned_statistic(data_concat.isop_mr, back2, statistic=stddev, bins=60, range=(0,15))
bin6 = stats.binned_statistic(data_concat.isop_mr, data_concat.isop_mr, statistic=stddev, bins=60, range=(0,15))
# Turn into pandas to get rid of NaNs.
back1 = pd.Series(bin1[0])
back2 = pd.Series(bin2[0])
isop = pd.Series(bin3[0])
st1 = pd.Series(bin4[0])
st2 = pd.Series(bin5[0])
stIs = pd.Series(bin6[0])
# get rid of NaNs for both the data and the standard deviation.
back1 = back1.dropna()
back2 = back2.dropna()
isop = isop.dropna()
st1 = st1.dropna()
st2 = st2.dropna()
stIs = stIs.dropna()




signal1 = plt.figure("MOS signal when VS is large")
ax1 = signal1.add_subplot(2,1,1)
ax2 = signal1.add_subplot(2,1,2)
import matplotlib.cm as cm
c= data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
#ax1.scatter(filterVS.index, filterVS.MOS1, linewidth=3, color=cm.jet(c))
#ax2.scatter(filterVS.index, filterVS.MOS1, linewidth=3, color=cm.jet(c))
ax1.plot(filter.index, filter.MOS1, linewidth=3, color="g")
ax2.plot(filter.index, filter.MOS2, linewidth=3, color="b")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Index")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Index")

tempcal = plt.figure("Plotting temp against MOS signal")
ax1 = tempcal.add_subplot(2,1,1)
ax2 = tempcal.add_subplot(2,1,2)
import matplotlib.cm as cm
c= data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
ax1.scatter(temp, filterVS.MOS1, linewidth=3, color=cm.jet(c))
ax2.scatter(temp, filterVS.MOS2, linewidth=3, color=cm.jet(c))
ax1.scatter(temp, filterVS.MOS1, linewidth=3, color="g")
ax2.scatter(temp, filterVS.MOS2, linewidth=3, color="b")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Temperature / C")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Temperature / C")
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(temp, filterVS.MOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(temp, filterVS.MOS2)
ax1.plot([np.min(temp), np.max(temp)], [(slope1*np.min(temp))+intercept1, (slope1*np.max(temp))+intercept1])
ax2.plot([np.min(temp), np.max(temp)], [(slope2*np.min(temp))+intercept2, (slope2*np.max(temp))+intercept2])
print ("Gradient MOS1", slope1)
print ("Intercept MOS1", intercept1)
print ("R2 MOS1", R2value1)
print ("Gradient MOS2", slope2)
print ("Intercept MOS2", intercept2)
print ("R2 MOS2", R2value2)"""

"""
signal1 = plt.figure("MOS signal when VS is large")
ax1 = signal1.add_subplot(2,1,1)
ax2 = signal1.add_subplot(2,1,2)
import matplotlib.cm as cm
c= data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
#ax1.scatter(filterVS.index, filterVS.MOS1, linewidth=3, color=cm.jet(c))
#ax2.scatter(filterVS.index, filterVS.%MOS1, linewidth=3, color=cm.jet(c))
ax1.plot(bigVS.index, bigVS.MOS1, linewidth=3, color="g")
ax2.plot(bigVS.index, bigVS.MOS2, linewidth=3, color="b")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Index")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Index")

tempcal1 = plt.figure("Plotting temp against MOS signal when VS is large, and isoprene is zero")
ax1 = tempcal1.add_subplot(2,1,1)
ax2 = tempcal1.add_subplot(2,1,2)
import matplotlib.cm as cm
c= data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
ax1.scatter(temp, filterVS.MOS1, linewidth=3, color=cm.jet(c))
ax2.scatter(temp, filterVS.MOS2, linewidth=3, color=cm.jet(c))
ax1.scatter(temp1, bigVS.MOS1, linewidth=3, color="g")
ax2.scatter(temp1, bigVS.MOS2, linewidth=3, color="b")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Temperature / C")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Temperature / C")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(temp1, bigVS.MOS1)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(temp1, bigVS.MOS2)
ax1.plot([np.min(temp1), np.max(temp1)], [(slope3*np.min(temp1))+intercept3, (slope3*np.max(temp1))+intercept3])
ax2.plot([np.min(temp1), np.max(temp1)], [(slope4*np.min(temp1))+intercept4, (slope4*np.max(temp1))+intercept4])
print ("Gradient MOS1 big VS", slope3)
print ("Intercept MOS1", intercept3)
print ("R2 MOS1", R2value3)
print ("Gradient MOS2", slope4)
print ("Intercept MOS2", intercept4)
print ("R2 MOS2 big VS", R2value4)"""