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
bin1 = stats.binned_statistic(low_VOC.MOS1 , low_VOC.VOC_mr, statistic='mean', bins= list(range(0, 500)))
bin2 = stats.binned_statistic(low_VOC.MOS2 , low_VOC.VOC_mr, statistic='mean', bins= list(range(0, 500)))
bin3 = stats.binned_statistic(low_VOC.VOC_mr , low_VOC.VOC_mr, statistic='mean', bins= list(range(0, 500)))
# bin4 = stats.binned_statistic(low_VOC.MOS2 , low_VOC.VOC_mr, statistic='mean', bins=list(range(40,100,1)))

MOS1 = pd.Series(bin1[0])
MOS2 = pd.Series(bin2[0])
VOC = pd.Series(bin3[0])

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

'''
# ###############Find the different gradients of the VOC calibration.
# Create new data sets for each concentration


VOCsmall = low_VOC[low_VOC.VOC_mr <= 20.]

VOCbigger = low_VOC[low_VOC.VOC_mr > 100.] 
VOC1 = VOCbigger[VOCbigger.VOC_mr <= 800]


# VOCb = data_concat[data_concat.VOC_mr > 150]
# VOC2 = VOCb[VOCb.VOC_mr <= 300 ]
# 
# VOCc = data_concat[data_concat.VOC_mr > 250]
# VOC3 = VOCc[VOCc.VOC_mr <= 500 ]
# 
# VOCd = data_concat[data_concat.VOC_mr > 500]
# VOC4 = VOCd[VOCd.VOC_mr <= 550 ]
# 
# VOCe = data_concat[data_concat.VOC_mr > 550]
# VOC5 = VOCe[VOCe.VOC_mr <= 600 ]
# 
# VOCf = data_concat[data_concat.VOC_mr > 600]
# VOC6 = VOCf[VOCf.VOC_mr <= 650 ]
# 
# VOCg = data_concat[data_concat.VOC_mr > 650]
# VOC7 = VOCg[VOCg.VOC_mr <= 700 ]
# 
# VOCh = data_concat[data_concat.VOC_mr > 700]
# VOC8 = VOCh[VOCh.VOC_mr <= 750 ]
# 
# VOCi = data_concat[data_concat.VOC_mr > 750]
# VOC9 = VOCi[VOCi.VOC_mr <= 800 ]


# Linear regression; make a table in an Excel file with all the data in it. 
dummy = []

dummy.append(stats.linregress(VOCsmall.VOC_mr, VOCsmall.MOS1*1000))
dummy.append(stats.linregress(VOCsmall.VOC_mr, VOCsmall.MOS2*1000))
dummy.append(stats.linregress(VOC1.VOC_mr,  VOC1.MOS1*1000))
dummy.append(stats.linregress(VOC1.VOC_mr,  VOC1.MOS2*1000))
# dummy.append(stats.linregress(VOC2.VOC_mr, VOC2.MOS1*1000))
# dummy.append(stats.linregress(VOC2.VOC_mr, VOC2.MOS2*1000))
# dummy.append(stats.linregress(VOC3.VOC_mr, VOC3.MOS1*1000))
# dummy.append(stats.linregress(VOC3.VOC_mr, VOC3.MOS2*1000))
# dummy.append(stats.linregress(VOC4.VOC_mr, VOC4.MOS1*1000))
# dummy.append(stats.linregress(VOC4.VOC_mr, VOC4.MOS2*1000))
# dummy.append(stats.linregress(VOC5.VOC_mr, VOC5.MOS1*1000))
# dummy.append(stats.linregress(VOC5.VOC_mr, VOC5.MOS2*1000))
# dummy.append(stats.linregress(VOC6.VOC_mr, VOC6.MOS1*1000))
# dummy.append(stats.linregress(VOC6.VOC_mr, VOC6.MOS2*1000))
# dummy.append(stats.linregress(VOC7.VOC_mr, VOC7.MOS1*1000))
# dummy.append(stats.linregress(VOC7.VOC_mr, VOC7.MOS2*1000))
# dummy.append(stats.linregress(VOC8.VOC_mr, VOC8.MOS1*1000))
# dummy.append(stats.linregress(VOC8.VOC_mr, VOC8.MOS2*1000))
# dummy.append(stats.linregress(VOC9.VOC_mr, VOC9.MOS1*1000))
# dummy.append(stats.linregress(VOC9.VOC_mr, VOC9.MOS2*1000))

# table = pd.DataFrame(dummy, columns = ('Slope (mV ppb-1)', 'Intercept','R_squared value','p_value','Standard Deviation'))
# table.index = ('[VOC] < 50 MOS1','[VOC] < 50 MOS2', '[VOC1] 50 - 100 MOS1', '[VOC1] 50 - 100 MOS2', '[VOC2] 100 - 150 MOS1', '[VOC2] 100 - 150 MOS2', '[VOC3] 150-200 MOS1','[VOC3] 150-200 MOS2','[VOC4] 200-250 MOS1','[VOC4] 200-250 MOS2','[VOC5] 250-300 MOS1','[VOC5] 250-300 MOS2', '[VOC6] 300-350 MOS1', '[VOC6] 300-350 MOS2', '[VOC7] 350-400 MOS1', '[VOC7] 350-400 MOS2', '[VOC8] 400-450 MOS1','[VOC8] 400-450 MOS2','[VOC9] 450-500 MOS1','[VOC9] 450-500 MOS2')
# 
# table.to_csv('linear_regression.csv')
# print(" Check the Kate file in Google Drive for the new Excel file")

# Create the two subplots, one for each MOS.
gradientsMOS1 = plt.figure("MOS1")
ax1a = gradientsMOS1.add_subplot(1,1,1)

colors = ["red", "blue", "green", "orange", "purple"]

# Making the scatter graphs
ax1a.scatter(VOCsmall.VOC_mr, VOCsmall.MOS1*1000, color="red", linewidth=1)
ax1a.scatter(VOC1.VOC_mr, VOC1.MOS1*1000, color="blue", linewidth=1)
# ax1a.scatter(VOC2.VOC_mr, VOC2.MOS1*1000, color="green", linewidth=1)
# ax1a.scatter(VOC3.VOC_mr, VOC3.MOS1*1000, color="orange", linewidth=1)
# ax1a.scatter(VOC4.VOC_mr, VOC4.MOS1*1000, color="purple", linewidth=1)
# ax1a.scatter(VOC5.VOC_mr, VOC5.MOS1*1000, color="k", linewidth=1)
# ax1a.scatter(VOC6.VOC_mr, VOC6.MOS1*1000, color="red", linewidth=1)
# ax1a.scatter(VOC7.VOC_mr, VOC7.MOS1*1000, color="blue", linewidth=1)
# ax1a.scatter(VOC8.VOC_mr, VOC8.MOS1*1000, color="green", linewidth=1)
# ax1a.scatter(VOC9.VOC_mr, VOC9.MOS1*1000, color="orange", linewidth=1)
ax1a.set_xlabel('[VOC] ppb')
ax1a.set_ylabel('MOS 1 signal (mV)')

gradientsMOS2 = plt.figure("MOS2")
ax2a = gradientsMOS2.add_subplot(1,1,1)
ax2a.scatter(VOCsmall.VOC_mr, VOCsmall.MOS2*1000, color="red", linewidth=1)
ax2a.scatter(VOC1.VOC_mr, VOC1.MOS2*1000, color="blue", linewidth=1)
# ax2a.scatter(VOC2.VOC_mr, VOC2.MOS2*1000, color="green", linewidth=1)
# ax2a.scatter(VOC3.VOC_mr, VOC3.MOS2*1000, color="orange", linewidth=1)
# ax2a.scatter(VOC4.VOC_mr, VOC4.MOS2*1000, color="purple", linewidth=1)
# ax2a.scatter(VOC5.VOC_mr, VOC5.MOS2*1000, color="k", linewidth=1)
# ax2a.scatter(VOC6.VOC_mr, VOC6.MOS2*1000, color="red", linewidth=1)
# ax2a.scatter(VOC7.VOC_mr, VOC7.MOS2*1000, color="blue", linewidth=1)
# ax2a.scatter(VOC8.VOC_mr, VOC8.MOS2*1000, color="green", linewidth=1)
# ax2a.scatter(VOC9.VOC_mr, VOC9.MOS2*1000, color="orange", linewidth=1)
ax2a.set_xlabel('[VOC] ppb')
ax2a.set_ylabel('MOS 2 signal (mV)')


# Linear regression
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(VOCsmall.VOC_mr, VOCsmall.MOS1*1000)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(VOCsmall.VOC_mr, VOCsmall.MOS2*1000)
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(VOC1.VOC_mr,  VOC1.MOS1*1000)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(VOC1.VOC_mr,  VOC1.MOS2*1000)
# slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(VOC2.VOC_mr, VOC2.MOS1*1000)
# slope6, intercept6, R2value6, p_value6, st_err6 = stats.linregress(VOC2.VOC_mr, VOC2.MOS2*1000)
# slope7, intercept7, R2value7, p_value7, st_err7 = stats.linregress(VOC3.VOC_mr, VOC3.MOS1*1000)
# slope8, intercept8, R2value8, p_value8, st_err8 = stats.linregress(VOC3.VOC_mr, VOC3.MOS2*1000)
# slope9, intercept9, R2value9, p_value9, st_err9 = stats.linregress(VOC4.VOC_mr, VOC4.MOS1*1000)
# slope10, intercept10, R2value10, p_value10, st_err10 = stats.linregress(VOC4.VOC_mr, VOC4.MOS2*1000)
# slope11, intercept11, R2value11, p_value11, st_err11 = stats.linregress(VOC5.VOC_mr, VOC5.MOS1*1000)
# slope12, intercept12, R2value12, p_value12, st_err12 = stats.linregress(VOC5.VOC_mr, VOC5.MOS2*1000)
# slope13, intercept13, R2value13, p_value13, st_err13 = stats.linregress(VOC6.VOC_mr, VOC6.MOS1*1000)
# slope14, intercept14, R2value14, p_value14, st_err14 = stats.linregress(VOC6.VOC_mr, VOC6.MOS2*1000)
# slope15, intercept15, R2value15, p_value15, st_err15 = stats.linregress(VOC7.VOC_mr, VOC7.MOS1*1000)
# slope16, intercept16, R2value16, p_value16, st_err16 = stats.linregress(VOC7.VOC_mr, VOC7.MOS2*1000)
# slope17, intercept17, R2value17, p_value17, st_err17 = stats.linregress(VOC8.VOC_mr, VOC8.MOS1*1000)
# slope18, intercept18, R2value18, p_value18, st_err18 = stats.linregress(VOC8.VOC_mr, VOC8.MOS2*1000)
# slope19, intercept19, R2value19, p_value19, st_err19 = stats.linregress(VOC9.VOC_mr, VOC9.MOS1*1000)
# slope20, intercept20, R2value20, p_value20, st_err20 = stats.linregress(VOC9.VOC_mr, VOC9.MOS2*1000)

ax1a.plot([np.min(VOCsmall.VOC_mr), np.max(VOCsmall.VOC_mr)], [(slope1*np.min(VOCsmall.VOC_mr))+intercept1, (slope1*np.max(VOCsmall.VOC_mr))+intercept1])
ax2a.plot([np.min(VOCsmall.VOC_mr), np.max(VOCsmall.VOC_mr)], [(slope2*np.min(VOCsmall.VOC_mr))+intercept2, (slope2*np.max(VOCsmall.VOC_mr))+intercept2])

ax1a.plot([np.min(VOC1.VOC_mr), np.max(VOC1.VOC_mr)], [(slope3*np.min(VOC1.VOC_mr))+intercept3, (slope3*np.max(VOC1.VOC_mr))+intercept3])
ax2a.plot([np.min(VOC1.VOC_mr), np.max(VOC1.VOC_mr)], [(slope4*np.min(VOC1.VOC_mr))+intercept4, (slope4*np.max(VOC1.VOC_mr))+intercept4])

# ax1a.plot([np.min(VOC2.VOC_mr), np.max(VOC2.VOC_mr)], [(slope5*np.min(VOC2.VOC_mr))+intercept5, (slope5*np.max(VOC2.VOC_mr))+intercept5])
# ax2a.plot([np.min(VOC2.VOC_mr), np.max(VOC2.VOC_mr)], [(slope6*np.min(VOC2.VOC_mr))+intercept6, (slope6*np.max(VOC2.VOC_mr))+intercept6])
# 
# ax1a.plot([np.min(VOC3.VOC_mr), np.max(VOC3.VOC_mr)], [(slope7*np.min(VOC3.VOC_mr))+intercept7, (slope7*np.max(VOC3.VOC_mr))+intercept7])
# ax2a.plot([np.min(VOC3.VOC_mr), np.max(VOC3.VOC_mr)], [(slope8*np.min(VOC3.VOC_mr))+intercept8, (slope8*np.max(VOC3.VOC_mr))+intercept8])
# 
# 
# ax1a.plot([np.min(VOC4.VOC_mr), np.max(VOC4.VOC_mr)], [(slope9*np.min(VOC4.VOC_mr))+intercept9, (slope9*np.max(VOC4.VOC_mr))+intercept9])
# ax2a.plot([np.min(VOC4.VOC_mr), np.max(VOC4.VOC_mr)], [(slope10*np.min(VOC4.VOC_mr))+intercept10, (slope10*np.max(VOC4.VOC_mr))+intercept10])
# 
# ax1a.plot([np.min(VOC5.VOC_mr), np.max(VOC5.VOC_mr)], [(slope11*np.min(VOC5.VOC_mr))+intercept11, (slope11*np.max(VOC5.VOC_mr))+intercept11])
# ax2a.plot([np.min(VOC5.VOC_mr), np.max(VOC5.VOC_mr)], [(slope12*np.min(VOC5.VOC_mr))+intercept12, (slope12*np.max(VOC5.VOC_mr))+intercept12])
# 
# ax1a.plot([np.min(VOC6.VOC_mr), np.max(VOC6.VOC_mr)], [(slope13*np.min(VOC6.VOC_mr))+intercept13, (slope13*np.max(VOC6.VOC_mr))+intercept13])
# ax2a.plot([np.min(VOC6.VOC_mr), np.max(VOC6.VOC_mr)], [(slope14*np.min(VOC6.VOC_mr))+intercept14, (slope14*np.max(VOC6.VOC_mr))+intercept14])
# 
# ax1a.plot([np.min(VOC7.VOC_mr), np.max(VOC7.VOC_mr)], [(slope15*np.min(VOC7.VOC_mr))+intercept15, (slope15*np.max(VOC7.VOC_mr))+intercept15])
# ax2a.plot([np.min(VOC7.VOC_mr), np.max(VOC7.VOC_mr)], [(slope16*np.min(VOC7.VOC_mr))+intercept16, (slope16*np.max(VOC7.VOC_mr))+intercept16])
# 
# ax1a.plot([np.min(VOC8.VOC_mr), np.max(VOC8.VOC_mr)], [(slope17*np.min(VOC8.VOC_mr))+intercept17, (slope17*np.max(VOC8.VOC_mr))+intercept17])
# ax2a.plot([np.min(VOC8.VOC_mr), np.max(VOC8.VOC_mr)], [(slope18*np.min(VOC8.VOC_mr))+intercept18, (slope18*np.max(VOC8.VOC_mr))+intercept18])
# 
# ax1a.plot([np.min(VOC9.VOC_mr), np.max(VOC9.VOC_mr)], [(slope19*np.min(VOC9.VOC_mr))+intercept19, (slope19*np.max(VOC9.VOC_mr))+intercept19])
# ax2a.plot([np.min(VOC9.VOC_mr), np.max(VOC9.VOC_mr)], [(slope20*np.min(VOC9.VOC_mr))+intercept20, (slope20*np.max(VOC9.VOC_mr))+intercept20])
print(np.mean(low_VOC.RH1))
'''
plt.show()

