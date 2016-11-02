"""Universal MOS data file reader/plotter to look at individual files run with the dilute VOC mix.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# Takes the file name and extracts the date then sticks this on the front to make the file path. 
# File with the isoprene in to plot the isoprene sensitivity.
cal_file = ['d20160218_02']

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

# Plot the raw MOS data against [VOC] conc.
rawfig = plt.figure("Raw MOS vs [VOC]")

axa = rawfig.add_subplot(2,1,1)
axb = rawfig.add_subplot(2,1,2)

import matplotlib.cm as cm
c = data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))

axa.scatter(data_concat.VOC_mr, data_concat.MOS1,color=cm.jet(c),marker='o')
axb.scatter(data_concat.VOC_mr, data_concat.MOS2,color=cm.jet(c),marker='o')

axa.set_ylabel("MOS1 (V)")
axb.set_ylabel("MOS2 (V)")
axa.set_xlabel("VOC (ppb)")
axb.set_xlabel("VOC (ppb)")

# Renaming the dataframe in order to work.
MOS1_cor = data_concat.MOS1*1000
MOS2_cor = data_concat.MOS2*1000

cor1fig = plt.figure("Comparing raw data with variables")

cor1ax = cor1fig.add_subplot(4,1,1)
cor2 = cor1ax.twinx()
cor5ax = cor1fig.add_subplot(4,1,2)
cor7 = cor5ax.twinx()
cor9ax = cor1fig.add_subplot(4,1,3)
cor11ax = cor1fig.add_subplot(4,1,4)

cor1ax.plot(data_concat.dt, data_concat.MOS1,color='darkorchid',marker='o')
cor2.plot(data_concat.dt, data_concat.VOC_mr, color='silver')
cor5ax.plot(data_concat.dt,data_concat.MOS2,color='teal',marker='o')
cor7.plot(data_concat.dt, data_concat.VOC_mr, color='silver')

cor9ax.plot(data_concat.dt, data_concat.RH1, color='royalblue', linewidth =3)
cor11ax.plot(data_concat.dt, data_concat.Temp*100, color='firebrick', linewidth = 3)

cor11ax.set_ylabel("Temperature")
cor1ax.set_ylabel("MOS1 (V)")
cor5ax.set_ylabel("MOS2 (V)")
cor9ax.set_ylabel("RH")
cor7.set_ylabel("Total VOC /ppb")


### Need to plot up the VOC sensitivity polts, with linear regression.
# Finding the VOC sensitivity
# Bin the data into bins of 1ppb isoprene, get an average for this data and then plot this.
# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 1 ppb of VOC sections, and take an average of the data.
bin1 = stats.binned_statistic(data_concat.VOC_mr, MOS1_cor, statistic='mean', bins=14, range=(0,14))
bin2 = stats.binned_statistic(data_concat.VOC_mr, MOS2_cor, statistic='mean', bins=14, range=(0,14))
bin3 = stats.binned_statistic(data_concat.VOC_mr, data_concat.VOC_mr, statistic='mean', bins=14, range=(0,14))
bin4 = stats.binned_statistic(data_concat.VOC_mr, MOS1_cor, statistic=stddev, bins=14, range=(0,14))
bin5 = stats.binned_statistic(data_concat.VOC_mr, MOS2_cor, statistic=stddev, bins=14, range=(0,14))
bin6 = stats.binned_statistic(data_concat.VOC_mr, data_concat.VOC_mr, statistic=stddev, bins=14, range=(0,14))
# Turn into pandas to get rid of NaNs.
MOS1_cor = pd.Series(bin1[0])
MOS2_cor = pd.Series(bin2[0])
VOC = pd.Series(bin3[0])
st1 = pd.Series(bin4[0])
st2 = pd.Series(bin5[0])
stIs = pd.Series(bin6[0])
# get rid of NaNs for both the data and the standard deviation.
MOS1_cor = MOS1_cor.dropna()
MOS2_cor = MOS2_cor.dropna()
VOC = VOC.dropna()
st1 = st1.dropna()
st2 = st2.dropna()
stIs = stIs.dropna()

VOCPLOT = plt.figure("VOC sensitivity")
ax1 = VOCPLOT.add_subplot(2,1,1)
ax2 = VOCPLOT.add_subplot(2,1,2)

ax1.scatter(VOC, MOS1_cor, color="g")
ax1.errorbar(VOC, MOS1_cor, xerr=stIs, yerr=st1, lw=1, fmt='o', color="g")
ax2.scatter(VOC, MOS2_cor, color="b")
ax2.errorbar(VOC, MOS2_cor, xerr=stIs, yerr=st2, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_ylabel("MOS2 signal / v")
ax1.set_xlabel("VOC / ppb")
ax2.set_xlabel("VOC / ppb")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(VOC, MOS1_cor)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(VOC, MOS2_cor)
ax1.plot([np.min(VOC), np.max(VOC)], [(slope3*np.min(VOC))+intercept3, (slope3*np.max(VOC))+intercept3])
ax2.plot([np.min(VOC), np.max(VOC)], [(slope4*np.min(VOC))+intercept4, (slope4*np.max(VOC))+intercept4])
# Get the linear regression paramenters to have 3 sig figs.
slope3 = ("%.3g" %slope3)
intercept3 = ("%.3g" % (intercept3))
R23 = ("%.3g" % (R2value3))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(1, np.max(MOS1_cor)*0.99 ,'y = ' +str(slope3)+'x +' +str(intercept3), style='italic', fontsize = 15) 
ax1.text(1,np.max(MOS1_cor)*0.90, '$R^2 value$ = '+str(R23), style = 'italic', fontsize=15)
#([0,14,850,890])


print ("Gradient of VOC vs MOS1", slope3)
print ("Intercept of VOC vsMOS1", intercept3)
print ("R2 of VOC vs MOS1", R2value3)
print ("Gradient of VOC vs MOS2", slope4)
print ("Intercept of VOC vs MOS2", intercept4)
print ("R2 of VOC vs MOS2", R2value4)
print ("Average RH", np.mean(data_concat.RH1))
print ("Average temp", np.mean(data_concat.Temp*100))


# ###############Find the different gradients of the VOC calibration.

# Create new data sets for each concentration
VOCsmall = data_concat[data_concat.VOC_mr <= 0.1]

VOCbigger = data_concat[data_concat.VOC_mr > 1.] 
VOC1 = VOCbigger[VOCbigger.VOC_mr <= 2]

VOCb = data_concat[data_concat.VOC_mr > 2]
VOC2 = VOCb[VOCb.VOC_mr <= 3 ]

VOCc = data_concat[data_concat.VOC_mr > 3]
VOC3 = VOCc[VOCc.VOC_mr <= 4 ]

VOCd = data_concat[data_concat.VOC_mr > 4]
VOC4 = VOCd[VOCd.VOC_mr <= 5 ]

VOCe = data_concat[data_concat.VOC_mr > 5]
VOC5 = VOCe[VOCe.VOC_mr <= 6 ]

VOCf = data_concat[data_concat.VOC_mr > 6]
VOC6 = VOCf[VOCf.VOC_mr <= 7]

VOCg = data_concat[data_concat.VOC_mr > 7]
VOC7 = VOCg[VOCg.VOC_mr <= 8 ]

VOCh = data_concat[data_concat.VOC_mr > 8]
VOC8 = VOCh[VOCh.VOC_mr <= 9 ]

VOCi = data_concat[data_concat.VOC_mr > 9]
VOC9 = VOCi[VOCi.VOC_mr <= 10 ]

# plot [VOC] = 0
zero = plt.figure("Zero ppb")
ax1 = zero.add_subplot(1,1,1)
ax2 = ax1.twinx()
ax1.scatter(VOCsmall.dt, VOCsmall.MOS1, color="green")
ax2.plot(VOCsmall.dt, VOCsmall.Temp*100, color="red")
ax1.set_ylabel("MOS1 (V)")
ax1.set_xlabel("Time")



# Linear regression; make a table in an Excel file with all the data in it. 

# Create the ten subplots, one for each ppb of MOS1.
# Filter each dataset to give a range that can be used to find a temp gradient.
MO1 = plt.figure("MOS1 0-1 ppb")
ax1b = MO1.add_subplot(1,1,1)
VOCx = VOCsmall[(VOCsmall.MOS1*1000)< 855]
VOCx = VOCx[(VOCx.Temp *100 )>27.0]
ax1b.scatter(VOCx.Temp*100, VOCx.MOS1*1000, color="red", linewidth=1)
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(VOCx.Temp*100, VOCx.MOS1*1000)
ax1b.plot([np.min(VOCx.Temp*100), np.max(VOCx.Temp*100)], [(slope1*np.min(VOCx.Temp*100))+intercept1, (slope1*np.max(VOCx.Temp*100))+intercept1])
print("MOS1 0 - 1 ppb temp slope",slope1)
print("Intercept value",intercept1)
ax1b.set_xlabel("Temperature ( degrees C)")
ax1b.set_ylabel(" MOS1 signal (mV)")
 
"""
MO2 = plt.figure("MOS1 1-2 ppb")
ax2b = MO2.add_subplot(1,1,1)
VOCy = VOC1[(VOC1.Temp)> 0.2585]
VOCy = VOCy[(VOCy.Temp) < 0.2615]
ax2b.scatter(VOCy.Temp*100, VOCy.MOS1*1000, color="blue", linewidth=1)
 
 
MO3 = plt.figure("MOS1 2-3 ppb")
ax2c = MO3.add_subplot(1,1,1)
VOCz = VOC2[(VOC2.Temp)> 0.274]
VOCz = VOCz[(VOCz.Temp) < 0.281]
ax2c.scatter(VOCz.Temp*100, VOCz.MOS1*1000, color="crimson", linewidth=1)
 
MO4 = plt.figure("MOS1 3-4 ppb")
ax2d = MO4.add_subplot(1,1,1)
VOCk = VOC3[(VOC3.Temp)> 0.275]
VOCk = VOCk[(VOCk.Temp) < 0.277]
ax2d.scatter(VOCk.Temp*100, VOCk.MOS1*1000, color="mediumseagreen", linewidth=1)

MO5 = plt.figure("MOS1 4-5 ppb")
ax2e = MO5.add_subplot(1,1,1)
VOCl = VOC4[(VOC4.Temp)> 0.266]
VOCl = VOCl[(VOCl.Temp) < 0.267]
ax2e.scatter(VOCl.Temp*100, VOCl.MOS1*1000, color="cornflowerblue", linewidth=1)

MO6 = plt.figure("MOS1 5-6 ppb")
ax2f = MO6.add_subplot(1,1,1)
VOCm = VOC5[(VOC5.Temp)> 0.2765]
VOCm = VOCm[(VOCm.Temp) < 0.2795]
ax2f.scatter(VOCm.Temp*100, VOCm.MOS1*1000, color="goldenrod", linewidth=1)

MO7 = plt.figure("MOS1 6-7 ppb")
ax2g = MO7.add_subplot(1,1,1)
VOCn = VOC6[(VOC6.Temp)> 0.256]
VOCn = VOCn[(VOCn.Temp) < 0.268]
ax2g.scatter(VOCn.Temp*100, VOCn.MOS1*1000, color="teal", linewidth=1)

MO8 = plt.figure("MOS1 7-8 ppb")
ax2h = MO8.add_subplot(1,1,1)
VOCo = VOC7[(VOC7.Temp)> 0.273]
VOCo = VOCo[(VOCo.Temp) < 0.28]
ax2h.scatter(VOCo.Temp*100, VOCo.MOS1*1000, color="blueviolet", linewidth=1)

MO9 = plt.figure("MOS1 8-9 ppb")
ax2i = MO9.add_subplot(1,1,1)
VOCp = VOC8[(VOC8.Temp)> 0.26]
VOCp = VOCp[(VOCp.Temp) < 0.262]
ax2i.scatter(VOCp.Temp*100, VOCp.MOS1*1000, color="hotpink", linewidth=1)"""

MO10 = plt.figure("MOS1 9-10 ppb")
ax2j = MO10.add_subplot(1,1,1)
VOCq = VOC9[(VOC9.Temp)> 0.271]
VOCq = VOCq[(VOCq.Temp) < 0.279]
ax2j.scatter(VOCq.Temp*100, VOCq.MOS1*1000, color="dodgerblue", linewidth=1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(VOCq.Temp*100, VOCq.MOS1*1000)
ax2j.plot([np.min(VOCq.Temp*100), np.max(VOCq.Temp*100)], [(slope2*np.min(VOCq.Temp*100))+intercept2, (slope2*np.max(VOCq.Temp*100))+intercept2])
print("MOS1 9 - 10 ppb temp slope", slope2)
print("Intercept", intercept2)
ax2j.set_xlabel("Temperature ( degrees C)")
ax2j.set_ylabel(" MOS1 signal (mV)")

# Plot the temperature corrected data, remember that the MOS data is reported in mV above.
MOS_temp = data_concat.MOS1*1000 - ((15.292599034255193)*data_concat.Temp*100)

# Filter out data where VS < 4.86806.
tempfig = plt.figure("Corrected for temperature")

ax1 = tempfig.add_subplot(4,1,1)
ax2 = ax1.twinx()
ax3 = tempfig.add_subplot(4,1,2)
ax4 = ax3.twinx()
ax5 = tempfig.add_subplot(4,1,3)
ax6 = tempfig.add_subplot(4,1,4)

ax1.plot(data_concat.dt, data_concat.MOS1*1000, color='darkorchid',marker='o')
ax2.plot(data_concat.dt, data_concat.VOC_mr, color='silver')
ax3.plot(data_concat.dt, MOS_temp, color='cyan',marker='o')
ax4.plot(data_concat.dt, data_concat.VOC_mr, color='silver')

ax5.plot(data_concat.dt, data_concat.Temp*100, color='red')
ax6.plot(data_concat.dt, data_concat.VS, color='deepskyblue')

#Labelling
ax1.set_ylabel("Raw MOS1 (V)")
ax2.set_ylabel("VOC (ppb)")
ax3.set_ylabel("Corrected MOS1 (V)")
ax5.set_ylabel("Temperature")
ax6.set_ylabel("RH")


# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 0.5 ppb of VOC sections, and take an average of the data.
bin7 = stats.binned_statistic(data_concat.VOC_mr, MOS_temp, statistic='mean', bins=28, range=(0,14))
bin8 = stats.binned_statistic(data_concat.VOC_mr, data_concat.VOC_mr, statistic='mean', bins=28, range=(0,14))
bin9 = stats.binned_statistic(data_concat.VOC_mr, MOS_temp, statistic = stddev, bins=28, range=(0,14))
bin10 = stats.binned_statistic(data_concat.VOC_mr, data_concat.VOC_mr, statistic = stddev, bins=28, range=(0,14))
# Turn into pandas to get rid of NaNs.
MOS_temp = pd.Series(bin7[0])
VOC_temp = pd.Series(bin8[0])
st_MOS = pd.Series(bin9[0])
st_VOC = pd.Series(bin10[0])
# get rid of NaNs for both the data and the standard deviation.
MOS_temp = MOS_temp.dropna()
VOC_temp = VOC_temp.dropna()
st_MOS = st_MOS.dropna()
st_VOC = st_VOC.dropna()

VOCPLOT1 = plt.figure("VOC sensitivity with temp correction")
ax1 = VOCPLOT1.add_subplot(1,1,1)
 
ax1.scatter(VOC_temp, MOS_temp, color="indigo")
ax1.set_title("VOC sensitivity with temp correction")
ax1.errorbar(VOC_temp, MOS_temp, xerr = st_VOC, yerr = st_MOS, lw=1, fmt='o', color="indigo")
ax1.set_ylabel("Temp corrected MOS1 signal (V)")
ax1.set_xlabel("VOC (ppb)")
slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(VOC_temp, MOS_temp)
ax1.plot([np.min(VOC_temp), np.max(VOC_temp)], [(slope5*np.min(VOC_temp))+intercept5, (slope5*np.max(VOC_temp))+intercept5])
# Get the linear regression paramenters to have 3 sig figs.
slope5 = ("%.3g" %slope5)
intercept5 = ("%.3g" % (intercept5))
R2 = ("%.3g" % (R2value5))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(1, np.max(MOS_temp)*0.99,'y = ' +str(slope5) + 'x + ' +str(intercept5), style='italic', fontsize = 15) 
ax1.text(1, np.max(MOS_temp)*0.95, '$R^2 value =$ '+str(R2), style = 'italic', fontsize=15)
#ax1.axis([0,14,450,490])
print ("Gradient of VOC vs corrected MOS1", slope5)
print ("Intercept of VOC vs corrected MOS1", intercept5)
print ("R2 of VOC vs corrected MOS1", R2)

tempMOS1 = plt.figure("All MOS1 happenings")
ax1a = tempMOS1.add_subplot(10,1,1)
ax2a = tempMOS1.add_subplot(10,1,2)
ax3a = tempMOS1.add_subplot(10,1,3)
ax4a = tempMOS1.add_subplot(10,1,4)
ax5a = tempMOS1.add_subplot(10,1,5)
ax6a = tempMOS1.add_subplot(10,1,6)
ax7a = tempMOS1.add_subplot(10,1,7)
ax8a = tempMOS1.add_subplot(10,1,8)
ax9a = tempMOS1.add_subplot(10,1,9)
ax10a = tempMOS1.add_subplot(10,1,10)
# Making the scatter graphs
ax1a.scatter(VOCsmall.Temp*100, VOCsmall.MOS1*1000, color="red", linewidth=1)
ax2a.scatter(VOC1.Temp*100, VOC1.MOS1*1000, color="blue", linewidth=1)
ax3a.scatter(VOC2.Temp*100, VOC2.MOS1*1000, color="green", linewidth=1)
ax4a.scatter(VOC3.Temp*100, VOC3.MOS1*1000, color="orange", linewidth=1)
ax5a.scatter(VOC4.Temp*100, VOC4.MOS1*1000, color="purple", linewidth=1)
ax6a.scatter(VOC5.Temp*100, VOC5.MOS1*1000, color="k", linewidth=1)
ax7a.scatter(VOC6.Temp*100, VOC6.MOS1*1000, color="red", linewidth=1)
ax8a.scatter(VOC7.Temp*100, VOC7.MOS1*1000, color="blue", linewidth=1)
ax9a.scatter(VOC8.Temp*100, VOC8.MOS1*1000, color="green", linewidth=1)
ax10a.scatter(VOC9.Temp*100, VOC9.MOS1*1000, color="orange", linewidth=1)
ax1a.set_xlabel('Temperature (C)')
ax1a.set_ylabel('MOS 1 signal (mV)')

plt.show()
 

