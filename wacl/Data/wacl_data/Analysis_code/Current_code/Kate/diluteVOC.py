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
#cal_file = ['d20160201_01','d20160201_02','d20160202_03','d20160203_01']
cal_file = ['d20151210_07','d20151211_01','d20151211_02','d20151214_01','d20151215_01','d20151215_02','d20151216_01','d20151217_01','d20151218_02','d20151218_03']

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

	Total_VOC = 1025.041	#ppbv The actual total VOC mixing ratio
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

#filter out periods when isop changes rapidly (dVOCdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	disopdt = pd.Series(np.absolute(mean_resampled.isop.diff()),name='disopdt')
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
c=data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))

axa.scatter(data_concat.VOC_mr, data_concat.MOS1,color=cm.jet(c),marker='o')
axb.scatter(data_concat.VOC_mr, data_concat.MOS2,color=cm.jet(c),marker='o')

axa.set_ylabel("MOS1 (V)")
axb.set_ylabel("MOS2 (V)")
axa.set_xlabel("VOC (ppb)")
axb.set_xlabel("VOC (ppb)")

# Renaming the dataframe in order to work.
MOS1_cor = data_concat.MOS1
MOS2_cor = data_concat.MOS2
data_concat.RH1 = mean_resampled.RH1

cor1fig = plt.figure("Comparing raw data with variables")
cor1ax = cor1fig.add_subplot(5,1,1)
cor2 = cor1ax.twinx()
cor5 = cor1fig.add_subplot(5,1,2)
cor7 = cor5.twinx()
cor9ax = cor1fig.add_subplot(5,1,3)
cor11ax = cor1fig.add_subplot(5,1,4)
cor13ax = cor1fig.add_subplot(5,1,5)

cor1ax.plot(data_concat.dt, data_concat.MOS1,color='darkorchid',marker='o')
cor2.plot(data_concat.dt, data_concat.VOC_mr, color='silver')

cor5.plot(data_concat.dt,data_concat.MOS2,color='teal',marker='o')
cor7.plot(data_concat.dt, data_concat.VOC_mr, color='silver')


cor9ax.plot(data_concat.dt, data_concat.RH1, color='royalblue', linewidth =3)
cor11ax.plot(data_concat.dt, data_concat.Temp*100, color='firebrick', linewidth = 3)
cor11ax.plot(data_concat.dt, data_concat.Temp2*100, color='k', linewidth = 3)
cor13ax.plot(data_concat.dt, data_concat.VS, color = 'darkviolet', linewidth = 3)

cor11ax.set_ylabel("Temperature")
cor1ax.set_ylabel("MOS1 (V)")
cor5.set_ylabel("MOS2 (V)")
cor9ax.set_ylabel("RH")
cor7.set_ylabel("Total VOC (ppb)")
cor13ax.set_ylabel(" Supply voltage (V)")



### Need to plot up the VOC sensitivity polts, with linear regression.
# Finding the VOC sensitivity
# Bin the data into bins of 1ppb isoprene, get an average for this data and then plot this.
#data_concat.VOC_mr = data_concat[data_concat.VOC_mr < 200]
# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 1 ppb of VOC sections, and take an average of the data.
bin1 = stats.binned_statistic(data_concat.VOC_mr, MOS1_cor, statistic='mean', bins=100, range=(0,100))
bin2 = stats.binned_statistic(data_concat.VOC_mr, MOS2_cor, statistic='mean', bins=100, range=(0,100))
bin3 = stats.binned_statistic(data_concat.VOC_mr, data_concat.VOC_mr, statistic='mean', bins=100, range=(0,100))
bin4 = stats.binned_statistic(data_concat.VOC_mr, MOS1_cor, statistic=stddev, bins=100, range=(0,100))
bin5 = stats.binned_statistic(data_concat.VOC_mr, MOS2_cor, statistic=stddev, bins=100, range=(0,100))
bin6 = stats.binned_statistic(data_concat.VOC_mr, data_concat.VOC_mr, statistic=stddev, bins=100, range=(0,100))
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

VOCPLOT = plt.figure("VOC sensitivity with the general background removed")
ax1 = VOCPLOT.add_subplot(2,1,1)
ax2 = VOCPLOT.add_subplot(2,1,2)

ax1.scatter(VOC, MOS1_cor, color="g")
ax1.errorbar(VOC, MOS1_cor, xerr=stIs, yerr=st1, lw=1, fmt='o', color="g")
ax2.scatter(VOC, MOS2_cor, color="b")
ax2.errorbar(VOC, MOS2_cor, xerr=stIs, yerr=st2, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS1 signal (V)", fontsize = 16)
ax2.set_ylabel("MOS2 signal (V)", fontsize = 16)
ax1.set_xlabel("VOC (ppb)", fontsize = 16)
ax2.set_xlabel("VOC (ppb)", fontsize = 16)
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(VOC, MOS1_cor)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(VOC, MOS2_cor)
ax1.plot([np.min(VOC), np.max(VOC)], [(slope3*np.min(VOC))+intercept3, (slope3*np.max(VOC))+intercept3])
ax2.plot([np.min(VOC), np.max(VOC)], [(slope4*np.min(VOC))+intercept4, (slope4*np.max(VOC))+intercept4])
print ("Gradient of VOC vs MOS1", slope3)
print ("Intercept of VOC vsMOS1", intercept3)
print ("R2 of VOC vs MOS1", R2value3)
print ("Gradient of VOC vs MOS2", slope4)
print ("Intercept of VOC vs MOS2", intercept4)
print ("R2 of VOC vs MOS2", R2value4)
print ("Average RH", np.mean(data_concat.RH1))
print ("Average temp", np.mean(data_concat.Temp*100))
# Get the linear regression paramenters to have 3 sig figs.
slope3 = ("%.3g" %slope3)
intercept3 = ("%.3g" % (intercept3))
R23 = ("%.3g" % (R2value3))
slope4 = ("%.3g" %slope4)
intercept4 = ("%.3g" % (intercept4))
R24 = ("%.3g" % (R2value4))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text((np.min(VOC))*1.0001, 0.89 ,'y = ' +str(slope3)+'x +' +str(intercept3), style='italic', fontsize = 15) 
ax1.text((np.min(VOC))*1.0001, 0.875, '$R^2 value$ = '+str(R23), style = 'italic', fontsize=15)
ax2.text((np.min(VOC))*1.0001, 0.92 ,'y = ' +str(slope4)+'x +' +str(intercept4), style='italic', fontsize = 15) 
ax2.text((np.min(VOC))*1.0001, 0.90, '$R^2 value$ = '+str(R24), style = 'italic', fontsize=15)


# Temperature plots


plt.show()




