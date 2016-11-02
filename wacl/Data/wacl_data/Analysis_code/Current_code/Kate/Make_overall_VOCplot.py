"""Universal MOS data file reader/plotter to look at individual files
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'


#################################
# File with the isoprene in to plot the isoprene sensitivity.
#cal_file = ['d20151210_07','d20151211_01','d20151211_02','d20151214_01','d20151215_01','d20151215_02','d20151216_01','d20151217_01','d20151218_02','d20151218_03']
cal_file = ['d20160201_02','d20160202_03','d20160203_01']

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
# Set the paprameters for the lab. There are three different Mass Flow controllers and these control the concentrations of VOC.
	Total_VOC = 40000.	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100.	#sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
# Apply the dilution factor to calculate the [VOC]
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
	VOC_mr = pd.Series(dil_fac*Total_VOC,name='VOC_mr')
	data = pd.concat([data,VOC_mr],axis=1)
# Average the data every 10 seconds.
	Time_avg = '10S'
# Copy a set of the data (so files aren't changed) to set a new index and sort the time out.
	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

#filter out periods when [VOC] changes rapidly (dVOCdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	dVOCdt = pd.Series(np.absolute(mean_resampled.VOC_mr.diff()),name='dVOCdt')
	dVOCdt_filt = pd.Series(0, index=dVOCdt.index,name='dVOCdt_filt')
	dVOC_ctr=0
	for dp in dVOCdt:
		if (dp>1.):
			dVOCdt_filt[dVOC_ctr:int(dVOC_ctr+nm_pts)] = 1
		dVOC_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dVOCdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dVOCdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.dVOCdt_filt == 0]

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

# Plot the raw MOS data against [VOC] conc. For these files, there are only two working MOS sensors.
rawfig = plt.figure("Raw MOS vs [VOC]")

axa = rawfig.add_subplot(2,1,1)
axb = rawfig.add_subplot(2,1,2)

axa.scatter(data_concat.VOC_mr,data_concat.MOS1,color='b',marker='o')
axb.scatter(data_concat.VOC_mr, data_concat.MOS2,color='g',marker='o')

axa.set_ylabel("MOS1 (V)")
axb.set_ylabel("MOS2 (V)")
axa.set_xlabel("VOC (ppb)")
axb.set_xlabel("VOC (ppb)")

# Plot both the MOS data over time.
cor2fig = plt.figure("MOS over time")
cor5ax = cor2fig.add_subplot(2,1,1)
cor7ax = cor2fig.add_subplot(2,1,2)
cor6 = cor5ax.twinx()
cor8 = cor7ax.twinx()

cor5ax.plot(data_concat.dt, data_concat.MOS1,color='r',marker='o')
cor6.plot(data_concat.dt, data_concat.VOC_mr, color='k')
cor7ax.plot(data_concat.dt,data_concat.MOS2,color='k',marker='o')
cor8.plot(data_concat.dt, data_concat.VOC_mr, color='k')

cor5ax.set_ylabel("MOS1 (V)")
cor6.set_ylabel("Total VOC /ppb")
cor8.set_ylabel("Total VOC / ppb")
cor7ax.set_ylabel("MOS1(V)")

# Combine the results of the two sensors - take an average of the two readings at set timepoints.
# Then calculate the standarddeviation between the two.
data_concat['Average_MOS'] = data_concat[['MOS1','MOS2']].mean(axis=1)
data_concat['Stddev'] = data_concat[['MOS1','MOS2']].std(axis=1)
average = plt.figure()
ax1 = average.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.dt, data_concat.Average_MOS)
ax2.plot(data_concat.dt, data_concat.VOC_mr, color="k")
average.show()

####################################
# Not using the averaged MOS
# Filter the data into two different dataframes, depending on the concentration of VOC. All datapoints with [VOC] less than 100 ppb
#go into data_lowVOC, and all others go into data_highVOC.
data_lowVOC = data_concat[data_concat.VOC_mr < 101]
data_highVOC = data_concat[data_concat.VOC_mr > 99]
# Plot the [VOC] vs the MOS signal, with the standard deviation between the sensors as errorbars.
VOCPLOT = plt.figure("VOC sensitivity")
ax1 = VOCPLOT.add_subplot(1,1,1)
ax1.scatter(data_lowVOC.VOC_mr, data_lowVOC.Average_MOS, color="g")
ax1.errorbar(data_lowVOC.VOC_mr, data_lowVOC.Average_MOS, yerr=data_lowVOC.Stddev, lw=1, fmt='o', color="g")
ax1.set_ylabel("MOS average / V")
ax1.set_xlabel("VOC / ppb")
slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(data_lowVOC.VOC_mr, data_lowVOC.Average_MOS)
ax1.plot([np.min(data_lowVOC.VOC_mr), np.max(data_lowVOC.VOC_mr)], [(slope5*np.min(data_lowVOC.VOC_mr))+intercept5, (slope5*np.max(data_lowVOC.VOC_mr))+intercept5])
print ("Intercept of VOC vsMOS1", intercept5)
print ("R2 of VOC vs MOS1", R2value5)

ax1.scatter(data_highVOC.VOC_mr, data_highVOC.Average_MOS, color="b")
ax1.errorbar(data_highVOC.VOC_mr, data_highVOC.Average_MOS, yerr=data_highVOC.Stddev, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS average / V")
ax1.set_xlabel("VOC / ppb")
slope6, intercept6, R2value6, p_value6, st_err6 = stats.linregress(data_highVOC.VOC_mr, data_highVOC.Average_MOS)
ax1.plot([np.min(data_highVOC.VOC_mr), np.max(data_highVOC.VOC_mr)], [(slope6*np.min(data_highVOC.VOC_mr))+intercept6, (slope6*np.max(data_highVOC.VOC_mr))+intercept6])
print ("Intercept of VOC vsMOS1", intercept6)
print ("R2 of VOC vs MOS1", R2value6)

### Need to plot up the VOC sensitivity polts, with linear regression.
# Finding the VOC sensitivity
# Bin the data into bins of 1ppb [VOC], get an average for this data and then plot this.
# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 1 ppb of VOC sections, and take an average of the data.
bin1 = stats.binned_statistic(data_lowVOC.VOC_mr, data_lowVOC.MOS1, statistic='mean', bins=500, range=(0,500))
bin2 = stats.binned_statistic(data_lowVOC.VOC_mr, data_lowVOC.MOS2, statistic='mean', bins=500, range=(0,500))
bin3 = stats.binned_statistic(data_lowVOC.VOC_mr, data_lowVOC.VOC_mr, statistic='mean', bins=500, range=(0,500))
bin4 = stats.binned_statistic(data_lowVOC.VOC_mr, data_lowVOC.MOS1, statistic=stddev, bins=500, range=(0,500))
bin5 = stats.binned_statistic(data_lowVOC.VOC_mr, data_lowVOC.MOS2, statistic=stddev, bins=500, range=(0,500))
bin6 = stats.binned_statistic(data_lowVOC.VOC_mr, data_lowVOC.VOC_mr, statistic=stddev, bins=500, range=(0,500))
# Turn into pandas to get rid of NaNs.
MOS1_low = pd.Series(bin1[0])
MOS2_low = pd.Series(bin2[0])
VOC_low = pd.Series(bin3[0])
st1_low = pd.Series(bin4[0])
st2_low = pd.Series(bin5[0])
stIs_low = pd.Series(bin6[0])
# get rid of NaNs for both the data and the standard deviation.
MOS1_low = MOS1_low.dropna()
MOS2_low = MOS2_low.dropna()
VOC_low = VOC_low.dropna()
st1_low = st1_low.dropna()
st2_low = st2_low.dropna()
stIs_low = stIs_low.dropna()


# Now apply the binning to the data greater than 100 ppm. 
# Bin the data into 1 ppb of VOC sections, and take an average of the data.
bin7 = stats.binned_statistic(data_highVOC.VOC_mr, data_highVOC.MOS1, statistic='mean', bins=500, range=(0,500))
bin8 = stats.binned_statistic(data_highVOC.VOC_mr, data_highVOC.MOS2, statistic='mean', bins=500, range=(0,500))
bin9 = stats.binned_statistic(data_highVOC.VOC_mr, data_highVOC.VOC_mr, statistic='mean', bins=500, range=(0,500))
bin10 = stats.binned_statistic(data_highVOC.VOC_mr, data_highVOC.MOS1, statistic=stddev, bins=500, range=(0,500))
bin11 = stats.binned_statistic(data_highVOC.VOC_mr, data_highVOC.MOS2, statistic=stddev, bins=500, range=(0,500))
bin12 = stats.binned_statistic(data_highVOC.VOC_mr, data_highVOC.VOC_mr, statistic=stddev, bins=500, range=(0,500))
# Turn into pandas to get rid of NaNs.
MOS1_high = pd.Series(bin7[0])
MOS2_high = pd.Series(bin8[0])
VOC_high = pd.Series(bin9[0])
st3_high = pd.Series(bin10[0])
st4_high = pd.Series(bin11[0])
stI_high = pd.Series(bin12[0])
# get rid of NaNs for both the data and the standard deviation.
MOS1_high = MOS1_high.dropna()
MOS2_high = MOS2_high.dropna()
VOC_high = VOC_high.dropna()
st3_high = st3_high.dropna()
st4_high = st4_high.dropna()
stI_high = stI_high.dropna()

# Plot the low [VOC] and the high [VOC] regions on the same graph, but as separate datasets. Give them both errorbars too.
Overall = plt.figure(" Overall [VOC] sensitivity for MOS1")
ax1 = Overall.add_subplot(111)
# Plot the data
ax1.scatter(VOC_low, MOS1_low, color="green")
ax1.scatter(VOC_high, MOS1_high, color="blue")
# Plot the errorbars
ax1.errorbar(VOC_low, MOS1_low, xerr = stIs_low, yerr = st1_low, fmt='o')
ax1.errorbar(VOC_high, MOS1_high,xerr = stI_high, yerr=st3_high, fmt='o')
# Linear regression for both datasets - plotting the line of best fit too.
slope8, intercept8, R2value8, p_value8, st_err8 = stats.linregress(VOC_low, MOS1_low)
ax1.plot([np.min(VOC_low), np.max(VOC_low)], [(slope8*np.min(VOC_low))+intercept8, (slope8*np.max(VOC_low))+intercept8])
slope9, intercept9, R2value9, p_value9, st_err9 = stats.linregress(VOC_high, MOS1_high)
ax1.plot([np.min(VOC_high), np.max(VOC_high)], [(slope9*np.min(VOC_high))+intercept9, (slope9*np.max(VOC_high))+intercept9])

# Get the linear regression paramenters to have 3 sig figs.
slope8 = ("%.3g" %slope8)
intercept8 = ("%.3g" % (intercept8))
R28 = ("%.3g" % (R2value8))
slope9 = ("%.3g" %slope9)
intercept9 = ("%.3g" % (intercept9))
R29 = ("%.3g" % (R2value9))

# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(300, 2.0, 'VOC low y = ' +str(slope8)+'x +' +str(intercept8), fontsize = 20) 
ax1.text(300, 1.75, '$R^2 value$ = '+str(R28), style = 'italic', fontsize=20)
ax1.text(300, 1.5,'VOC high y = ' +str(slope9)+'x +' +str(intercept9), fontsize = 20) 
ax1.text(300, 1.25, '$R^2 value$ = '+str(R29), style = 'italic', fontsize=20)
ax1.tick_params(labelsize=22)
# Give the plot a title and axis labels
# plt.title("MOS1 VOC calibration")
ax1.set_ylabel("MOS1 signal (V)", size=18)
ax1.set_xlabel("VOC conc (ppb)", size=18)

# Repeat for MOS2
Overall2 = plt.figure(" Overall [VOC] sensitivity for MOS2")
ax2 = Overall2.add_subplot(111)
ax2.scatter(VOC_low, MOS2_low, color="purple")
ax2.scatter(VOC_high, MOS2_high, color="orange")
ax2.errorbar(VOC_low, MOS2_low, xerr = stIs_low, yerr = st2_low, fmt='o')
ax2.errorbar(VOC_high, MOS2_high, xerr = stI_high, yerr=st4_high, fmt='o')
ax2.tick_params(labelsize=18)
# Linear regression for both datasets - plotting the line of best fit too.
slope10, intercept10, R2value10, p_value10, st_err10 = stats.linregress(VOC_low, MOS2_low)
ax2.plot([np.min(VOC_low), np.max(VOC_low)], [(slope10*np.min(VOC_low))+intercept10, (slope10*np.max(VOC_low))+intercept10])
slope11, intercept11, R2value11, p_value11, st_err11 = stats.linregress(VOC_high, MOS2_high)
ax2.plot([np.min(VOC_high), np.max(VOC_high)], [(slope11*np.min(VOC_high))+intercept11, (slope11*np.max(VOC_high))+intercept11])

# Get the linear regression paramenters to have 3 sig figs.
slope10 = ("%.3g" %slope10)
intercept10 = ("%.3g" % (intercept10))
R210 = ("%.3g" % (R2value10))
slope11 = ("%.3g" %slope11)
intercept11 = ("%.3g" % (intercept11))
R211 = ("%.3g" % (R2value11))

# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax2.text(300, 2.0, 'VOC low y = ' +str(slope10)+'x +' +str(intercept10), style='italic', fontsize = 15) 
ax2.text(300, 1.75, '$R^2 value$ = '+str(R210), style = 'italic', fontsize=15)
ax2.text(300, 1.5,'VOC high y = ' +str(slope11)+'x +' +str(intercept11), style='italic', fontsize = 15) 
ax2.text(300, 1.25, '$R^2 value$ = '+str(R211), style = 'italic', fontsize=15)
plt.title("MOS2 VOC calibration")
ax2.set_ylabel("MOS2 signal (V)", size=18)
ax2.set_xlabel("VOC conc (ppb)", size=18)




plt.show()


