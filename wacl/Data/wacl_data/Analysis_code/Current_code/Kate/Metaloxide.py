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

cal_files = ['d20151207_02','d20151207_03','d20151207_04','d20151207_05']

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

pid4 = data_concat.pid4*1000
pid5 = data_concat.pid5*1000
pid7 = data_concat.pid7*1000
pid8 = data_concat.pid8*1000
pid9 = data_concat.pid9*1000

#
pids = plt.figure(" PIDs on new system ")
ax1 = pids.add_subplot(5,1,1)
ax2 = pids.add_subplot(5,1,2)
ax3 = pids.add_subplot(5,1,3)
ax4 = pids.add_subplot(5,1,4)
ax5 = pids.add_subplot(5,1,5)

ax6 = ax1.twinx()
ax7 = ax2.twinx()
ax8 = ax3.twinx()
ax9 = ax4.twinx()
ax10 = ax5.twinx()
Temp = data_concat.Temp*100
RH = (((data_concat.RH1/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*Temp)

ax1.plot(data_concat.index, pid5, linewidth=3, color="g")
ax2.plot(data_concat.index, pid7, linewidth=3, color="r")
ax3.plot(data_concat.index, pid8, linewidth=3, color="y")
ax4.plot(data_concat.index, pid4, linewidth=3, color="b")
ax5.plot(data_concat.index, pid9, linewidth=3, color="m")
"""ax6.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax7.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax8.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax9.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax10.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")"""
ax6.plot(data_concat.index, RH, linewidth=3, color="k")
ax7.plot(data_concat.index, RH, linewidth=3, color="k")
ax8.plot(data_concat.index, RH, linewidth=3, color="k")
ax9.plot(data_concat.index, RH, linewidth=3, color="k")
ax10.plot(data_concat.index, RH, linewidth=3, color="k")
ax1.yaxis.set_ticks(np.arange(54, 55, 0.2))
ax2.yaxis.set_ticks(np.arange(55., 56., 0.2))
ax3.yaxis.set_ticks(np.arange(54., 56, 0.2))
ax4.yaxis.set_ticks(np.arange(55., 56., 0.2))
ax5.yaxis.set_ticks(np.arange(51., 53., 0.2))
ax5.set_xlabel("Index")
ax1.set_ylabel("PID 5 signal / V")
ax2.set_ylabel("PID 7 signal / V")
ax3.set_ylabel("PID 8 signal / V")
ax4.set_ylabel("PID 4 signal / V")
ax5.set_ylabel("PID 9 signal / V")
ax6.set_ylabel("Isoprene / ppb")
ax7.set_ylabel("Isoprene / ppb")
ax8.set_ylabel("Isoprene / ppb")
ax9.set_ylabel("Isoprene / ppb")
ax10.set_ylabel("Isoprene / ppb")

pidRH = plt.figure("PIDs and RH")
ax1 = pidRH.add_subplot(5,1,1)
ax2 = pidRH.add_subplot(5,1,2)
ax3 = pidRH.add_subplot(5,1,3)
ax4 = pidRH.add_subplot(5,1,4)
ax5 = pidRH.add_subplot(5,1,5)
ax1.plot(pid5, RH, linewidth=3, color="g")
ax2.plot(pid7, RH, linewidth=3, color="r")
ax3.plot(pid8, RH, linewidth=3, color="y")
ax4.plot(pid4, RH, linewidth=3, color="b")
ax5.plot(pid9, RH, linewidth=3, color="m")




metal = plt.figure("Metal oxide sensor signal")

ax1 = metal.add_subplot(2,1,1)
ax2 = metal.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()

#ax1.plot(mosdf.index, mosdf.MOS1, linewidth=3, color="g")
#ax2.plot(mosdf.index, mosdf.MOS2, linewidth=3, color="b")
#ax3.plot(mosdf.index, mosdf.isop_mr, linewidth=3, color="k")
#ax4.plot(mosdf.index, mosdf.isop_mr, linewidth=3, color="k")
ax1.plot(data_concat.index, data_concat.MOS1, linewidth=3, color="g")
ax2.plot(data_concat.index, data_concat.MOS2, linewidth=3, color="b")
ax3.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax4.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax1.set_xlabel("Index")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_xlabel("Index")
ax2.set_ylabel("MOS2 signal / V")
ax3.set_ylabel("Isoprene / ppb")
ax4.set_ylabel("Isoprene / ppb")

voltage = plt.figure("VS vs MOS signal")
ax1 = voltage.add_subplot(2,1,1)
ax2 = voltage.add_subplot(2,1,2)

ax1.plot(mosdf.VS, mosdf.MOS1, 'o', color="g")
ax2.plot(mosdf.VS, mosdf.MOS2, 'o', color="b")
ax1.set_xlabel("VS")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_xlabel("VS")
ax2.set_ylabel("MOS2 signal / V")
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(mosdf.VS, mosdf.MOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(mosdf.VS, mosdf.MOS2)
ax1.plot([np.min(mosdf.VS), np.max(mosdf.VS)], [(slope1*np.min(mosdf.VS))+intercept1, (slope1*np.max(mosdf.VS))+intercept1])
ax2.plot([np.min(mosdf.VS), np.max(mosdf.VS)], [(slope2*np.min(mosdf.VS))+intercept2, (slope2*np.max(mosdf.VS))+intercept2])
print ("Gradient MOS1:", slope1)
print ("Intercept MOS1:", intercept1)
print ("R2 value MOS1:", R2value1)
print ("Gradient MOS2:", slope2)
print ("Intercept MOS2:", intercept2)
print ("R2 value MOS2:", R2value2)


cMOS1 = data_concat.MOS1 - ((data_concat.VS *  slope1) + intercept1)
cMOS2 = data_concat.MOS2 - ((data_concat.VS *  slope2) + intercept2)
corrected = plt.figure("Correcting for VS")
ax1 = corrected.add_subplot(2,1,1)
ax2 = corrected.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
ax1.plot(data_concat.index, cMOS1, linewidth=3, color="m")
ax2.plot(data_concat.index, cMOS2, linewidth=3, color="r")
ax3.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax3.plot(data_concat.index, data_concat.VS, linewidth=3, color="y")
ax4.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="k")
ax4.plot(data_concat.index, data_concat.VS, linewidth=3, color="y")
ax1.set_xlabel("Index")
ax1.set_ylabel("Corrected MOS1 signal / V")
ax2.set_xlabel("Index")
ax2.set_ylabel("Corrected MOS2 signal / V")
ax3.set_ylabel("Isoprene / ppb")
ax4.set_ylabel("Isoprene / ppb")


plt.show()

