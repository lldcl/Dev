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

# Takes the file name and extracts the date then sticks this on the front to make the file path. 
stat = 'Y'

cal_files = ['d20151209_01','d20151209_02','d20151210_02','d20151210_03']
#cal_files = ['d20151201_01','d20151201_02','d20151201_03','d20151201_04','d20151201_05','d20151202_01','d20151203_04','d20151203_06','d20151203_07']

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
Tempb = (data.RH2 * 100)
RHa = (((data.RH1/data.VS)-0.16)/0.0062)/(1.0546-0.00216*Tempa)



MOS1 = plt.figure("All Variables with MOS1")
ax1 = MOS1.add_subplot(5,1,1)
ax2 = MOS1.add_subplot(5,1,2)
ax3 = MOS1.add_subplot(5,1,3)
ax4 = MOS1.add_subplot(5,1,4)
ax5 = MOS1.add_subplot(5,1,5)

ax1.plot(data.index, data.MOS1, linewidth=3, color="g", label="MOS1")
ax2.plot(data.index, RHa, linewidth=3, color="b", label="RH")
ax3.plot(data.index, Tempa, linewidth=3, color="r", label="Temp")
ax4.plot(data.index, data.VS, color="k")
ax5.plot(data.index, data.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax4.set_xlabel("Time")

# Graph 2: All variables for MOS2
MOS2 = plt.figure("All Variables with MOS2")
ax1 = MOS2.add_subplot(5,1,1)
ax2 = MOS2.add_subplot(5,1,2)
ax3 = MOS2.add_subplot(5,1,3)
ax4 = MOS2.add_subplot(5,1,4)
ax5 = MOS2.add_subplot(5,1,5)
ax6 = ax3.twinx()

ax1.plot(data.index, data.MOS2, linewidth=3, color="b", label="MOS2")
ax2.plot(data.index, RHa, linewidth=3, color="b", label="RH")
ax3.plot(data.index, Tempa, linewidth=3, color="r", label="Temp")
ax4.plot(data.index, data.VS, color="k")
ax5.plot(data.index, data.isop_mr, linewidth=3, color="m")
ax6.plot(data.index, Tempb, linewidth=3, color="k", label="Temp")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax5.set_xlabel("Time")
ax5.set_ylabel("Isoprene / ppb")

"""#Graph 1: Plotting up all the variables
MOS1 = plt.figure("All Variables with MOS1")
ax1 = MOS1.add_subplot(5,1,1)
ax2 = MOS1.add_subplot(5,1,2)
ax3 = MOS1.add_subplot(5,1,3)
ax4 = MOS1.add_subplot(5,1,4)
ax5 = MOS1.add_subplot(5,1,5)

ax1.plot(data_concat.dt, data_concat.MOS1, linewidth=3, color="g", label="MOS1")
ax2.plot(data_concat.dt, RH, linewidth=3, color="b", label="RH")
ax3.plot(data_concat.dt, Temp, linewidth=3, color="r", label="Temp")
ax4.plot(data_concat.dt, data_concat.VS, color="k")
ax5.plot(data_concat.dt, data_concat.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax5.set_xlabel("Time")
ax5.set_ylabel("Isoprene / ppb")

# Graph 2: All variables for MOS2
MOS2 = plt.figure("All Variables with MOS2")
ax1 = MOS2.add_subplot(5,1,1)
ax2 = MOS2.add_subplot(5,1,2)
ax3 = MOS2.add_subplot(5,1,3)
ax4 = MOS2.add_subplot(5,1,4)
ax5 = MOS2.add_subplot(5,1,5)
ax6 = ax3.twinx()

ax1.plot(data_concat.dt, data_concat.MOS2, linewidth=3, color="b", label="MOS2")
ax2.plot(data_concat.dt, RH, linewidth=3, color="b", label="RH")
ax3.plot(data_concat.dt, Temp, linewidth=3, color="r", label="Temp")
ax4.plot(data_concat.dt, data_concat.VS, color="k")
ax5.plot(data_concat.dt, data_concat.isop_mr, linewidth=3, color="m")
ax6.plot(data_concat.dt, Temp2, linewidth=3, color="k", label="Temp")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax5.set_xlabel("Time")
ax5.set_ylabel("Isoprene / ppb")"""

###### Filtering out isoprene
filter = data_concat[data_concat.isop_mr < 0.1] 
temp = filter.Temp*100
RHc = (((filter.RH1/filter.VS)-0.16)/0.0062)/(1.0546-0.00216*temp)

######### Graph 3: Plotting up all the variables when there is no isoprene
MOSi = plt.figure("All Variables with MOS1 isoprene = 0")
ax1 = MOSi.add_subplot(5,1,1)
ax2 = MOSi.add_subplot(5,1,2)
ax3 = MOSi.add_subplot(5,1,3)
ax4 = MOSi.add_subplot(5,1,4)
ax5 = MOSi.add_subplot(5,1,5)

ax1.plot(filter.dt, filter.MOS1, linewidth=3, color="g", label="MOS1")
ax2.plot(filter.dt, RHc, linewidth=3, color="b", label="RH")
ax3.plot(filter.dt, temp, linewidth=3, color="r", label="Temp")
ax4.plot(filter.dt, filter.VS, color="k")
ax5.plot(filter.dt, filter.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS1 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax4.set_xlabel("Time")

# As above but for MOS2 
MOSj = plt.figure("All Variables with MOS2 isoprene = 0")
ax1 = MOSj.add_subplot(5,1,1)
ax2 = MOSj.add_subplot(5,1,2)
ax3 = MOSj.add_subplot(5,1,3)
ax4 = MOSj.add_subplot(5,1,4)
ax5 = MOSj.add_subplot(5,1,5)

ax1.plot(filter.dt, filter.MOS2, linewidth=3, color="b", label="MOS1")
ax2.plot(filter.dt, RHc, linewidth=3, color="b", label="RH")
ax3.plot(filter.dt, temp, linewidth=3, color="r", label="Temp")
ax4.plot(filter.dt, filter.VS, color="k")
ax5.plot(filter.dt, filter.isop_mr, linewidth=3, color="m")
ax1.set_ylabel("MOS2 / V")
ax2.set_ylabel("RH / %")
ax3.set_ylabel("Temperature / C")
ax4.set_ylabel(" Supply voltage / V")
ax4.set_xlabel("Time")

# Graph 4: plot temp vs MOS for all data with no isoprene
kate = plt.figure("Temp 1 vs MOS")
ax1 = kate.add_subplot(2,1,1)
ax2 = kate.add_subplot(2,1,2)

ax1.scatter(temp, filter.MOS1, linewidth=3, color="m")
ax2.scatter(temp, filter.MOS2, linewidth=3, color="k")

ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Temperature / C")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Temperature / C")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(temp, filter.MOS1)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(temp, filter.MOS2)
ax1.plot([np.min(temp), np.max(temp)], [(slope3*np.min(temp))+intercept3, (slope3*np.max(temp))+intercept3])
ax2.plot([np.min(temp), np.max(temp)], [(slope4*np.min(temp))+intercept4, (slope4*np.max(temp))+intercept4])
print ("Gradient MOS1 no isoprene", slope3)
print ("Intercept MOS1", intercept3)
print ("R2 MOS1", R2value3)
print ("Gradient MOS2", slope4)
print ("Intercept MOS2", intercept4)
print ("R2 MOS2 no isoprene", R2value4)

######### Graph 5: Plotting the data with the temperature effect removed.

remove1 = data_concat.MOS1 - (slope3 * (data_concat.Temp))
remove2 = data_concat.MOS2 - (slope4 * (data_concat.Temp))


background = plt.figure("Data with temperature correction")
ax1 = background.add_subplot(2,1,1)
ax2 = background.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
ax1.plot(data_concat.dt, remove1, color="g")
ax2.plot(data_concat.dt, remove2, color="b")
ax3.plot(data_concat.dt, data_concat.isop_mr, color="k")
ax4.plot(data_concat.dt, data_concat.isop_mr, color="k")

# Graph 6: Plot the isoprene calibration
isop = plt.figure("Isoprene")
ax1 = isop.add_subplot(2,1,1)
ax2 = isop.add_subplot(2,1,2)
ax1.scatter( data_concat.isop_mr, remove1, color="g")
ax2.scatter( data_concat.isop_mr, remove2, color="b")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Isoprene / ppb")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Isoprene / ppb")





# Graph 7: plot Temperature 2 vs MOS for all data with no isoprene
Temp2 = filter.RH2 *100
Temperature2 = plt.figure("Temp 2 vs MOS")
ax1 = Temperature2.add_subplot(2,1,1)
ax2 = Temperature2.add_subplot(2,1,2)

ax1.scatter(Temp2, filter.MOS1, linewidth=3, color="m")
ax2.scatter(Temp2, filter.MOS2, linewidth=3, color="k")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Temperature / C")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Temperature / C")
slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(Temp2, filter.MOS1)
slope6, intercept6, R2value6, p_value6, st_err6 = stats.linregress(Temp2, filter.MOS2)
ax1.plot([np.min(Temp2), np.max(Temp2)], [(slope5*np.min(Temp2))+intercept5, (slope5*np.max(Temp2))+intercept5])
ax2.plot([np.min(Temp2), np.max(Temp2)], [(slope6*np.min(Temp2))+intercept6, (slope6*np.max(Temp2))+intercept6])
print ("Gradient Temp2 MOS1 no isoprene", slope5)
print ("Intercept MOS1", intercept5)
print ("R2 MOS1", R2value5)
print ("Gradient MOS2", slope6)
print ("Intercept MOS2", intercept6)
print ("R2 MOS2 Temp2 no isoprene", R2value6)

# Remove the temperature effect. 

remove3 = data_concat.MOS1 - (slope5 * (data_concat.Temp2))
remove4 = data_concat.MOS2 - (slope6 * (data_concat.Temp2))


temp22= plt.figure("Data with temperature 2 correction")
ax1 = temp22.add_subplot(2,1,1)
ax2 = temp22.add_subplot(2,1,2)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
ax1.plot(data_concat.dt, remove3, color="g")
ax2.plot(data_concat.dt, remove4, color="b")
ax3.plot(data_concat.dt, data_concat.isop_mr, color="k")
ax4.plot(data_concat.dt, data_concat.isop_mr, color="k")

# Plot the isoprene conc against the MOS signal

# Graph 6: Plot the isoprene calibration
isopT2 = plt.figure("Isoprene with temp2 corrected data")
ax1 = isopT2.add_subplot(2,1,1)
ax2 = isopT2.add_subplot(2,1,2)
ax1.scatter( data_concat.isop_mr, remove3, color="g")
ax2.scatter( data_concat.isop_mr, remove4, color="b")
ax1.set_ylabel("MOS1 signal / V")
ax1.set_xlabel("Isoprene / ppb")
ax2.set_ylabel("MOS2 signal / V")
ax2.set_xlabel("Isoprene / ppb")



plt.show()

