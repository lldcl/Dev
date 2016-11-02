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

#cal_files = ['d20151130_01','d20151130_02','d20151201_01','d20151201_02','d20151201_03','d20151201_04','d20151201_05','d20151202_01','d20151202_02','d20151202_03','d20151203_04','d20151204_02']
#cal_files = ['d20151203_06','d20151203_07']
#cal_files = ['d20151201_01','d20151201_02','d20151201_03','d20151201_04','d20151202_01','d20151203_04','d20151203_06']
cal_files = ['d20151204_01','d20151204_02','d20151204_03']
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
	
	
	Time_avg = '30S'

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
	
#mosdf = pd.concat([data_concat.MOS1,data_concat.MOS2,data_concat.VS],axis=1)
#mosdf = mosdf.dropna()

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


"""temp_dep = plt.figure("Temperature variability")
VSdrop = data_concat[data_concat.VS > 0] 
VSdrop.Temp = VSdrop.Temp * 100
ax1 = temp_dep.add_subplot(2,1,1)
ax2 = temp_dep.add_subplot(2,1,2)
ax1.scatter(VSdrop.Temp, VSdrop.MOS1, linewidth=3, color="g")
ax2.scatter(VSdrop.Temp, VSdrop.MOS2, linewidth=3, color="b")
ax1.set_ylabel("MOS1")
ax1.set_xlabel("Temperature")
ax2.set_ylabel("MOS2")
ax2.set_xlabel("Temperature")
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(VSdrop.Temp, VSdrop.MOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(VSdrop.Temp, VSdrop.MOS2)
ax1.plot([np.min(VSdrop.Temp), np.max(VSdrop.Temp)], [(slope1*np.min(VSdrop.Temp))+intercept1, (slope1*np.max(VSdrop.Temp))+intercept1])
ax2.plot([np.min(VSdrop.Temp), np.max(VSdrop.Temp)], [(slope2*np.min(VSdrop.Temp))+intercept2, (slope2*np.max(VSdrop.Temp))+intercept2])
print ("Gradient MOS1", slope1)
print ("Intercept MOS1", intercept1)
print ("R2 MOS1", R2value1)
print ("Gradient MOS2", slope2)
print ("Intercept MOS2", intercept2)
print ("R2 MOS2", R2value2)"""

# Correct for temperature:
#cMOS1 = data_concat.MOS1 - (slope1*Temp)
#cMOS2 = data_concat.MOS2 - (slope2*Temp)


### USING THE TEMP CALIBRATION WHEN VS IS LARGE (THIS IS MORE NORMAL!!)
cMOS1 = data_concat.MOS1 - (0.012800835060743062*Temp)
cMOS2 = data_concat.MOS2 - (0.027147416054429718*Temp)
ctemp = plt.figure("Plotting MOS signal after it's been Temp corrected")
ax1 = ctemp.add_subplot(2,1,1)
ax2 = ctemp.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
ax1.plot(data_concat.index, cMOS1, linewidth=3, color="g")
ax2.plot(data_concat.index, cMOS2, linewidth=3, color="b")
ax1.set_ylabel("Temp corrected MOS1 / V")
ax2.set_ylabel("Temp corrected MOS2 / V")
ax2.set_xlabel("Index")
ax3.set_ylabel("RH")
ax4.set_ylabel("RH")
ax3.plot(data_concat.index, RH, color="k", linewidth=3)
ax4.plot(data_concat.index, RH, color="k", linewidth=3)

VS = plt.figure("Correcting for VS and temperature ")
cMOS1 = data_concat.MOS1 - (0.011997243330363418*Temp)
cMOS2 = data_concat.MOS2 - (0.026643594251207471*Temp)
cVSMOS1 = cMOS1 - (1.4729425035386565*data_concat.VS)
cVSMOS2 = cMOS2 - (1.7021668025853687*data_concat.VS)
ax1 = VS.add_subplot(2,1,1)
ax2 = VS.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
ax1.plot(data_concat.index, cVSMOS1, linewidth=3, color="g")
ax2.plot(data_concat.index, cVSMOS2, linewidth=3, color="b")
ax3.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="m")
ax4.plot(data_concat.index, data_concat.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("Corrected MOS1 / V")
ax2.set_ylabel("Corrected MOS2 / V")
ax2.set_xlabel("Index")

RH_dep = plt.figure("RH variability, with Temp and VS corrected data")
ax1 = RH_dep.add_subplot(2,1,1)
ax2 = RH_dep.add_subplot(2,1,2)
ax1.scatter(RH, cVSMOS1, linewidth=3, color="g")
ax2.scatter(RH, cVSMOS2, linewidth=3, color="b")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(RH, cVSMOS1)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(RH, cVSMOS2)
ax1.plot([np.min(RH), np.max(RH)], [(slope3*np.min(RH))+intercept3, (slope3*np.max(RH))+intercept3])
ax2.plot([np.min(RH), np.max(RH)],[(slope4*np.min(RH))+intercept4, (slope4*np.max(RH))+intercept4])
print ("Gradient temp MOS1", slope3)
print ("Intercept MOS1", intercept3)
print ("R2 MOS1", R2value3)
print ("Gradient temp MOS2", slope4)
print ("Intercept MOS2", intercept4)
print ("R2 MOS2", R2value4)

RHcorr1 = cVSMOS1 - (cVSMOS1 * -0.0058413790479651144)
RHcorr = plt.figure("RH correction")
ax1 = RHcorr.add_subplot(1,1,1)
ax1.plot(data_concat.index, RHcorr1, color="m")


import matplotlib.cm as cm
i= data_concat.Temp
i = (i-np.min(i))/np.max(i-np.min(i))
isoprene = plt.figure(" Isoprene sensitivity with Temp and VS corrected data")
ax1 = isoprene.add_subplot(2,1,1)
ax2 = isoprene.add_subplot(2,1,2)
ax1.scatter(data_concat.isop_mr, cVSMOS1, color=cm.jet(i))
ax2.scatter(data_concat.isop_mr, cVSMOS2, color="b")
ax1.set_xlabel("Isoprene / ppb")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_xlabel("Isoprene / ppb")
ax2.set_ylabel("MOS2 signal / V")

plt.show()


