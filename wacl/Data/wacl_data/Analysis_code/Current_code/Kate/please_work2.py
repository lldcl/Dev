"""Universal MOS data file reader/plotter to look at individual files
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'


#################################
# File with the VOCs in to plot the VOC sensitivity.
#cal_file = ['d20151210_07','d20151211_01','d20151211_02','d20151214_01','d20151215_01','d20151215_02','d20151216_01','d20151217_01','d20151218_02','d20151218_03']
# cal_file = ['d20160201_01','d20160201_02','d20160202_03','d20160203_01']
cal_file = ['d20160129_02','d20160201_01','d20160201_02','d20160202_03','d20160203_01']
#cal_file = ['d20160204_01','d20160205_02','d20160208_01']

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

	Total_VOC = 40000.	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100.	#sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)

	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
	VOC_mr = pd.Series(dil_fac*Total_VOC,name='VOC_mr')
	data = pd.concat([data,VOC_mr],axis=1)

	Time_avg = '30S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

	#filter out periods when VOC changes rapidly (dVOCdt<0.1) and for 60 seconds afterwards
	nm_pts =500./float(Time_avg[:-1])
	dVOCdt = pd.Series(np.absolute(mean_resampled.VOC_mr.diff()),name='dVOCdt')
	dVOCdt_filt = pd.Series(0, index=dVOCdt.index,name='dVOCdt_filt')
	dVOC_ctr=0
	for dp in dVOCdt:
		if (dp>0.01):
			dVOCdt_filt[dVOC_ctr:int(dVOC_ctr+nm_pts)] = 1
		dVOC_ctr+=1

# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

T3 = pd.datetime(2015,01,01,0)
# dt = pd.Series((data_concat.index - data_concat.index[0]),index=data_concat.index,name='dt')
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])


# Plotting up the raw data initially.
MOS1_cor = data_concat.MOS1	
MOS2_cor = data_concat.MOS2	
low_VOC = data_concat[data_concat.VOC_mr < 500]
cor1fig = plt.figure("Raw data ")

cor1ax = cor1fig.add_subplot(2,1,1)
cor2ax = cor1fig.add_subplot(2,1,2)
cor3 = cor1ax.twinx()
cor4 = cor2ax.twinx()

cor1ax.plot(low_VOC.dt,low_VOC.MOS1,color='b',marker='o')
cor3.plot(low_VOC.dt, low_VOC.VOC_mr, color='k')
cor2ax.plot(low_VOC.dt,low_VOC.MOS2,color='green',marker='o')
cor4.plot(low_VOC.dt, low_VOC.VOC_mr, color='k')

cor1ax.set_ylabel("MOS1 (V)")
cor2ax.set_ylabel("MOS2 (V)")
cor3.set_ylabel("Total VOC /ppb")
cor4.set_ylabel("Total VOC / ppb")


### Need to plot up the VOC sensitivity polts, with linear regression for each 50 ppb section.
# Finding the VOC sensitivity
# Bin the data into bins of 1ppb VOCrene, get an average for this data and then plot this.
#data_concat.VOC_mr = data_concat[data_concat.VOC_mr < 200]
# Sort the data out so that every 1%RH we take a mean. Essentially 'bin' the data in a similar way to a histogram.
bin1 = stats.binned_statistic(low_VOC.VOC_mr , low_VOC.MOS1, statistic='mean', bins= list(range(0, 500,20)))
bin2 = stats.binned_statistic(low_VOC.VOC_mr , low_VOC.MOS2, statistic='mean', bins= list(range(0, 500,20)))
bin3 = stats.binned_statistic(low_VOC.VOC_mr , low_VOC.VOC_mr, statistic='mean', bins= list(range(0, 500,20)))
# bin4 = stats.binned_statistic(low_VOC.MOS2 , low_VOC.VOC_mr, statistic='mean', bins=list(range(40,100,1)))

MOS1 = pd.Series(bin1[0])
MOS2 = pd.Series(bin2[0])
VOC = pd.Series(bin3[0])
# Just for the poster, as these bins didn't leave enough time to equilibriate
# bin1[0][10] = NaN
# bin2[0][10] = NaN
# bin3[0][10] = NaN
# bin1[0][12] = NaN
# bin2[0][12] = NaN
# bin3[0][12] = NaN
# bin1[0][18] = NaN
# bin2[0][18] = NaN
# bin3[0][18] = NaN

MOS1 = MOS1.dropna()
MOS2 = MOS2.dropna()
VOC = VOC.dropna()


# Plot the raw MOS data against [VOC] conc.
rawfig = plt.figure("Raw MOS vs [VOC]")

axa = rawfig.add_subplot(2,1,1)
axb = rawfig.add_subplot(2,1,2)

axa.scatter(VOC, MOS1,color='b',marker='o')
axb.scatter(VOC, MOS2,color='g',marker='o')

axa.set_ylabel("MOS1 (V)")
axb.set_ylabel("MOS2 (V)")
axa.set_xlabel("VOC (ppb)")
axb.set_xlabel("VOC (ppb)")


# ###############Find the different gradients of the VOC calibration.
# Create new data sets for each concentration

VOCsmall = VOC[VOC <= 100.]
MOS1small = MOS1[VOC <= 100]
MOS2small = MOS2[VOC <= 100]
VOC1 = VOC[VOC > 80.] 
MOS1big = MOS1[VOC > 80]
MOS2big = MOS2[VOC > 80]
# VOC1 = VOCbigger[VOCbigger.VOC_mr <= 800]


# Create the two subplots, one for each MOS.
gradientsMOS1 = plt.figure("MOS1")
ax1a = gradientsMOS1.add_subplot(1,1,1)

colors = ["red", "blue", "green", "orange", "purple"]

# Making the scatter graphs
ax1a.scatter(VOCsmall, MOS1small, color="red", linewidth=1)
ax1a.scatter(VOC1, MOS1big, color="blue", linewidth=1)

ax1a.set_xlabel('VOC concentration (ppb)',size =18)
ax1a.set_ylabel('MOS 1 signal (V)',size=18)

gradientsMOS2 = plt.figure("MOS2")
ax2a = gradientsMOS2.add_subplot(1,1,1)
ax2a.scatter(VOCsmall, MOS2small, color="green", linewidth=1)
ax2a.scatter(VOC1, MOS2big, color="purple", linewidth=1)

ax2a.set_xlabel('VOC concentration (ppb)',size=18)
ax2a.set_ylabel('MOS 2 signal (V)', size=18)


# Linear regression
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(VOCsmall, MOS1small)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(VOCsmall, MOS2small)
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(VOC1,  MOS1big)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(VOC1, MOS2big)

ax1a.plot([np.min(VOCsmall), np.max(VOCsmall)], [(slope1*np.min(VOCsmall))+intercept1, (slope1*np.max(VOCsmall))+intercept1], color="red")
ax2a.plot([np.min(VOCsmall), np.max(VOCsmall)], [(slope2*np.min(VOCsmall))+intercept2, (slope2*np.max(VOCsmall))+intercept2], color="green")

ax1a.plot([np.min(VOC1), np.max(VOC1)], [(slope3*np.min(VOC1))+intercept3, (slope3*np.max(VOC1))+intercept3],color="blue")
ax2a.plot([np.min(VOC1), np.max(VOC1)], [(slope4*np.min(VOC1))+intercept4, (slope4*np.max(VOC1))+intercept4], color="purple")

slope1 = ("%.3g" %slope1)
intercept1 = ("%.3g" %intercept1)
anchored_text1 = AnchoredText("MOS1 VOC < 100 ppb y= "+slope1+ "x + " +intercept1 , prop=dict(size=15, color="red"),loc=3)
ax1a.add_artist(anchored_text1)
slope3 = ("%.3g" %slope3)
intercept3 = ("%.3g" %intercept3)
anchored_text3 = AnchoredText("MOS1 VOC > 100 ppb y= "+slope3+ "x + " +intercept3 , prop=dict(size=15, color="blue"),loc=2)
ax1a.add_artist(anchored_text3)

slope2 = ("%.3g" %slope2)
intercept2 = ("%.3g" %intercept2)
anchored_text2 = AnchoredText("MOS2 VOC < 100 ppb y= "+slope2+ "x + " +intercept2 , prop=dict(size=15, color="green"),loc=3)
ax2a.add_artist(anchored_text2)
slope4 = ("%.3g" %slope4)
intercept4 = ("%.3g" %intercept4)
anchored_text4 = AnchoredText("MOS2 VOC > 100 ppb y= "+slope4+ "x + " +intercept4 , prop=dict(size=15, color="purple"),loc=2)
ax2a.add_artist(anchored_text4)
# plt.title("Overall VOC calibration for 1.5 %RH", size=20)

plt.show()

