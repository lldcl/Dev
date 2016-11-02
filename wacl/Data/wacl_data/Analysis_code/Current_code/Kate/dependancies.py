"""Use to determine temperature and RH for background files."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# Takes the file name and extracts the date then sticks this on the front to make the file path. 
# File with the isoprene in to plot the isoprene sensitivity.
cal_file = ['d20160224_01','d20160225_02','d20160225_03','d20160226_01','d20160226_02']

for i in cal_file:
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

	Total_VOC = 1040.	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100.	#sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)

	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
	VOC_mr = pd.Series(dil_fac*Total_VOC,name='VOC_mr')
	data = pd.concat([data,VOC_mr],axis=1)

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

	#filter out periods when isop changes rapidly (disopdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	disopdt = pd.Series(np.absolute(mean_resampled.VOC_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>1.):
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

T3 = pd.datetime(2015,01,01,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])


rawfig = plt.figure("Comparing raw data with variables")
ax1 = rawfig.add_subplot(5,1,1)
ax2 = rawfig.add_subplot(5,1,2)
ax3 = rawfig.add_subplot(5,1,3)
ax4 = rawfig.add_subplot(5,1,4)
ax5 = rawfig.add_subplot(5,1,5)

ax1.plot(data_concat.dt, data_concat.MOS1,color='darkorchid',marker='o')
ax2.plot(data_concat.dt, data_concat.MOS2,color='teal',marker='o')
ax3.plot(data_concat.dt, data_concat.RH1, color='royalblue', linewidth =3)
ax4.plot(data_concat.dt, data_concat.Temp*100, color='firebrick', linewidth = 3)
ax4.plot(data_concat.dt, data_concat.Temp2*100, color='k', linewidth = 3)
ax5.plot(data_concat.dt, data_concat.VS, color = 'darkviolet', linewidth = 3)

ax4.set_ylabel("Temperature")
ax1.set_ylabel("MOS1 (V)")
ax2.set_ylabel("MOS2 (V)")
ax2.set_ylabel("RH")
ax5.set_ylabel(" Supply voltage (V)")


#Plotting the MOS signal against the temperature and running a linear regression on the data
tempfig = plt.figure("Temeperature vs MOS")

ax1 = tempfig.add_subplot(2,1,1)
ax2 = tempfig.add_subplot(2,1,2)

ax1.scatter(data_concat.Temp*100, data_concat.MOS1, color="darkorchid")
ax2.scatter(data_concat.Temp*100, data_concat.MOS2, color="teal")
ax1.set_ylabel("MOS1 (V)")
ax2.set_ylabel("MOS2 (V)")
ax1.set_xlabel("Temperature (C)")
ax2.set_xlabel("Temperature (C)")
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(data_concat.Temp*100, data_concat.MOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(data_concat.Temp*100, data_concat.MOS2)
ax1.plot([np.min(data_concat.Temp*100), np.max(data_concat.Temp*100)], [(slope1*np.min(data_concat.Temp*100))+intercept1, (slope1*np.max(data_concat.Temp*100))+intercept1])
ax2.plot([np.min(data_concat.Temp*100), np.max(data_concat.Temp*100)], [(slope2*np.min(data_concat.Temp*100))+intercept2, (slope2*np.max(data_concat.Temp*100))+intercept2])
# Get the linear regression paramenters to have 3 sig figs.
slope1 = ("%.3g" %slope1)
intercept1 = ("%.3g" % (intercept1))
R21 = ("%.3g" % (R2value1))
slope2 = ("%.3g" %slope2)
intercept2 = ("%.3g" % (intercept2))
R22 = ("%.3g" % (R2value2))
print(slope1)
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text((np.min(data_concat.Temp*100))*1.0001, np.max(data_concat.MOS1)*0.999 ,'y = ' +str(slope1)+'x +' +str(intercept1), style='italic', fontsize = 15) 
ax1.text((np.min(data_concat.Temp*100))*1.0001, np.max(data_concat.MOS1)*0.87, '$R^2 value$ = '+str(R21), style = 'italic', fontsize=15)
ax2.text((np.min(data_concat.Temp*100))*1.0001, np.max(data_concat.MOS2)*0.999 ,'y = ' +str(slope2)+'x +' +str(intercept2), style='italic', fontsize = 15) 
ax2.text((np.min(data_concat.Temp*100))*1.0001, np.max(data_concat.MOS2)*0.875, '$R^2 value$ = '+str(R22), style = 'italic', fontsize=15)


# Plotting up the MOS signal against the RH.
RHfig = plt.figure("RH vs MOS")
ax1 = RHfig.add_subplot(2,1,1)
ax2 = RHfig.add_subplot(2,1,2)

ax1.scatter( data_concat.RH1, data_concat.MOS1, color="darkorchid")
ax2.scatter( data_concat.RH1, data_concat.MOS2, color="teal")
ax1.set_ylabel("MOS1 (V)")
ax2.set_ylabel("MOS2 (V)")
ax1.set_xlabel("RH (%)")
ax2.set_xlabel("RH (%)")

slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(data_concat.RH1, data_concat.MOS1)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(data_concat.RH1, data_concat.MOS2)
ax1.plot([np.min(data_concat.RH1), np.max(data_concat.RH1)], [(slope3*np.min(data_concat.RH1))+intercept3, (slope3*np.max(data_concat.RH1))+intercept3])
ax2.plot([np.min(data_concat.RH1), np.max(data_concat.RH1)], [(slope4*np.min(data_concat.RH1))+intercept4, (slope4*np.max(data_concat.RH1))+intercept4])
# Get the linear regression paramenters to have 3 sig figs.
slope3 = ("%.3g" %slope3)
intercept3 = ("%.3g" % (intercept3))
R23 = ("%.3g" % (R2value3))
slope4 = ("%.3g" %slope4)
intercept4 = ("%.3g" % (intercept4))
R24 = ("%.3g" % (R2value4))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(np.min(data_concat.RH1)*1.51, np.max(data_concat.MOS1)*0.999,'y = ' +str(slope3)+'x +' +str(intercept3), style='italic', fontsize = 15) 
ax1.text(np.min(data_concat.RH1)*1.51, np.max(data_concat.MOS1)*0.8, '$R^2 value$ = '+str(R23), style = 'italic', fontsize=15)
ax2.text(np.min(data_concat.RH1)*1.51, np.max(data_concat.MOS2)*0.999,'y = ' +str(slope4)+'x +' +str(intercept4), style='italic', fontsize = 15) 
ax2.text(np.min(data_concat.RH1)*1.51, np.max(data_concat.MOS2)*0.8, '$R^2 value$ = '+str(R24), style = 'italic', fontsize=15)

RH = data_concat[data_concat.RH1 > 40]
RH = RH[RH.RH1 < 50]

WATER = plt.figure("Comparing data with variables, once the HIGH AND LOW RH has been fitered out")
ax1 = WATER.add_subplot(5,1,1)
ax2 = WATER.add_subplot(5,1,2)
ax3 = WATER.add_subplot(5,1,3)
ax4 = WATER.add_subplot(5,1,4)
ax5 = WATER.add_subplot(5,1,5)

ax1.plot(RH.dt, RH.MOS1,color='darkorchid',marker='o')
ax2.plot(RH.dt, RH.MOS2,color='teal',marker='o')
ax3.plot(RH.dt, RH.RH1, color='royalblue', linewidth =3)
ax4.plot(RH.dt, RH.Temp*100, color='firebrick', linewidth = 3)
ax4.plot(RH.dt, RH.Temp2*100, color='k', linewidth = 3)
ax5.plot(RH.dt, RH.VS, color = 'darkviolet', linewidth = 3)

ax4.set_ylabel("Temperature")
ax1.set_ylabel("MOS1 (V)")
ax2.set_ylabel("MOS2 (V)")
ax2.set_ylabel("RH")
ax5.set_ylabel(" Supply voltage (V)")


# Plotting up the MOS signal against the filtered RH
figure5 = plt.figure("Filtered RH vs MOS")
ax1 = figure5.add_subplot(2,1,1)
ax2 = figure5.add_subplot(2,1,2)

ax1.scatter( RH.RH1, RH.MOS1, color="forestgreen")
ax2.scatter( RH.RH1, RH.MOS2, color="royalblue")
ax1.set_ylabel("MOS1 (V)")
ax2.set_ylabel("MOS2 (V)")
ax1.set_xlabel("Filtered RH (%)")
ax2.set_xlabel("Filtered RH (%)")

slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(RH.RH1, RH.MOS1)
slope6, intercept6, R2value6, p_value6, st_err6 = stats.linregress(RH.RH1, RH.MOS2)
ax1.plot([np.min(RH.RH1), np.max(RH.RH1)], [(slope5*np.min(RH.RH1))+intercept5, (slope5*np.max(RH.RH1))+intercept5])
ax2.plot([np.min(RH.RH1), np.max(RH.RH1)], [(slope6*np.min(RH.RH1))+intercept6, (slope6*np.max(RH.RH1))+intercept6])
# Get the linear regression paramenters to have 3 sig figs.
slope5 = ("%.3g" %slope5)
intercept5 = ("%.3g" % (intercept5))
R25 = ("%.3g" % (R2value5))
slope6 = ("%.3g" %slope6)
intercept6 = ("%.3g" % (intercept6))
R26 = ("%.3g" % (R2value6))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(np.min(RH.RH1)*1.0001, 1,'y = ' +str(slope5)+'x +' +str(intercept5), style='italic', fontsize = 15) 
ax1.text(np.min(RH.RH1)*1.0001, 0.95, '$R^2 value$ = '+str(R25), style = 'italic', fontsize=15)
ax2.text(np.min(RH.RH1)*1.0001, 1,'y = ' +str(slope6)+'x +' +str(intercept6), style='italic', fontsize = 15) 
ax2.text(np.min(RH.RH1)*1.0001, 0.95, '$R^2 value$ = '+str(R26), style = 'italic', fontsize=15)

plt.show()