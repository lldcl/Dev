"""RH correction. 
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

cal_files = ['d20151204_02','d20151204_03','d20151204_04']
#cal_files = ['d20151208_03']

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
	
	

	Time_avg = '5S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (mean_resampled.RH1)
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

dRHdt = pd.Series(np.absolute(data_concat.RH1.diff()),name='dRHdt')
dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
nm_pts = 120./float(Time_avg[:-1])
dRH_ctr=0
for dp in dRHdt:
	if (dp>0.02):
		dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
	dRH_ctr+=1
	
mosdf = pd.concat([data_concat.MOS1,data_concat.MOS2,data_concat.VS],axis=1)
mosdf = mosdf.dropna()

data_concat = pd.concat([data_concat,dRHdt],axis=1,join_axes=[data_concat.index])
data_concat = pd.concat([data_concat,dRHdt_filt],axis=1,join_axes=[data_concat.index])

data_concat = data_concat[data_concat.dRHdt_filt == 0]

Temp = (data_concat.Temp *100.)
RH = (((data_concat.RH1/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*Temp)


MOS1 = plt.figure("All Variables with MOS1")
ax1 = MOS1.add_subplot(5,1,1)
ax2 = MOS1.add_subplot(5,1,2)
ax3 = MOS1.add_subplot(5,1,3)
ax4 = MOS1.add_subplot(5,1,4)
ax5 = MOS1.add_subplot(5,1,5)

ax1.plot(data_concat.index, data_concat.MOS1, linewidth=3, color="g", label="MOS1")
ax2.plot(data_concat.index, RH, linewidth=3, color="b", label="RH")
ax3.plot(data_concat.index, Temp, linewidth=3, color="r", label="Temp")
ax4.plot(data_concat.index, data_concat.VS, color="k")
ax5.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax4.set_xlabel("Time")


MOS2 = plt.figure("All Variables with MOS2")
ax1 = MOS2.add_subplot(5,1,1)
ax2 = MOS2.add_subplot(5,1,2)
ax3 = MOS2.add_subplot(5,1,3)
ax4 = MOS2.add_subplot(5,1,4)
ax5 = MOS2.add_subplot(5,1,5)

ax1.plot(data_concat.index, data_concat.MOS2, linewidth=3, color="m", label="MOS2")
ax2.plot(data_concat.index, RH, linewidth=3, color="b", label="RH")
ax3.plot(data_concat.index, Temp, linewidth=3, color="r", label="Temp")
ax4.plot(data_concat.index, data_concat.VS, color="k")
ax5.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax5.set_xlabel("Time")
ax5.set_ylabel("Isoprene / ppb")

RHcal = plt.figure("RH calibration")
ax1 = RHcal.add_subplot(2,1,1)
ax2 = RHcal.add_subplot(2,1,2)
ax1.scatter(RH, data_concat.MOS1, color="g")
ax2.scatter(RH, data_concat.MOS1, color="b")
ax1.set_ylabel("MOS1 Signal / V")
ax1.set_xlabel("RH / %")
ax2.set_ylabel("MOS2 Signal / V")
ax2.set_xlabel("RH / %")

Tempcal = plt.figure("Temp calibration")
ax1 = Tempcal.add_subplot(2,1,1)
ax2 = Tempcal.add_subplot(2,1,2)
ax1.scatter(Temp, data_concat.MOS1, color="g")
ax2.scatter(Temp, data_concat.MOS2, color="b")
ax1.set_ylabel("MOS1 Signal / V")
ax1.set_xlabel("Temp /C")
ax2.set_ylabel("MOS2 Signal / V")
ax2.set_xlabel("Temp /C")


# Constant temp data
flatT = data_concat[100:200]
noI = flatT[(flatT.isop_mr < 0.5)]
heat = (noI.Temp *100.)
RH = (((noI.RH1/noI.VS)-0.16)/0.0062)/(1.0546-0.00216*heat)

MOSa = plt.figure("Selecting data; MOS signal and temperature")
ax1 = MOSa.add_subplot(4,1,1)
ax2 = MOSa.add_subplot(4,1,2)
ax3 = MOSa.add_subplot(4,1,3)
ax4 = MOSa.add_subplot(4,1,4)


ax1.plot(noI.index, noI.MOS1, linewidth=3, color="g", label="MOS1")
ax2.plot(noI.index, heat, linewidth=3, color="r", label="Temp")
ax3.plot(noI.index, noI.MOS2, color="b")
ax4.plot(noI.index, heat, linewidth=3, color="r")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("Temp / C%")
ax3.set_ylabel("MOS2 / V")
ax4.set_ylabel("Temp / C")


Tempflat = plt.figure("Selecting data;temp sensitivity")
ax1 = Tempflat.add_subplot(2,1,1)
ax2 = Tempflat.add_subplot(2,1,2)
import matplotlib.cm as cm
c= data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))
ax1.scatter(heat, noI.MOS1, color=cm.jet(c))
ax2.scatter(heat, noI.MOS2, color=cm.jet(c))
ax1.set_ylabel("MOS1 Signal with no isoprene / V")
ax1.set_xlabel("Temp /C")
ax2.set_ylabel("MOS2 Signal with no isoprene / V")
ax2.set_xlabel("Temp /C")
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(heat, noI.MOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(heat, noI.MOS2)
ax1.plot([np.min(heat), np.max(heat)], [(slope1*np.min(heat))+intercept1, (slope1*np.max(heat))+intercept1])
ax2.plot([np.min(heat), np.max(heat)], [(slope2*np.min(heat))+intercept2, (slope2*np.max(heat))+intercept2])
print ("Gradient MOS1:", slope1)
print ("Intercept MOS1:", intercept1)
print ("R2 value MOS1:", R2value1)
print ("Gradient MOS2:", slope2)
print ("Intercept MOS2:", intercept2)
print ("R2 value MOS2:", R2value2)

plt.show()