"""VOC MOS data file reader to find the median signal of all 8 MOS in Teflon block.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160503_01']

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

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	#filter out periods when [VOC] changes rapidly (disopdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	dVOCdt = pd.Series(np.absolute(mean_resampled.VOC.diff()),name='dVOCdt')
	dVOCdt_filt = pd.Series(0, index=dVOCdt.index,name='dVOCdt_filt')
	dVOC_ctr=0
	for dp in dVOCdt:
		if (dp>0.01):
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
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('int')
#'timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)


# Find all the columns with MOS in the title for use in loops.
sub = 'MOSar'
MOSar = [s for s in data_concat.columns if sub in s]

#plot up the MOS voltages
# Give it something to count through at the same time as the MOS, so it changes color.
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
#Use a counter to count through numbers in integers, beginning at one.
ctr=1
MOSloop = plt.figure("Raw MOS signal")
for n,c in zip(MOSar,colors):
	ax = 'MOSraw'+str(ctr)
	ax = MOSloop.add_subplot(9,1,ctr)
	ax.scatter(data_concat.index, data_concat[n],color=c,linewidth=3)
	ax.set_xlim([data_concat.index[0], data_concat.index[len(data_concat.index)-1]])
	ax.set_ylabel(n)
	ax.set_xlabel("Index")
	ctr+=1
MOSloop.show()

# Add a new column to the dataset, which finds the median of all the MOS signals.
data_concat['Median_MOS_signal'] = data_concat[['MOSar1','MOSar2', 'MOSar3','MOSar4', 'MOSar5', 'MOSar6', 'MOSar7', 'MOSar8']].median(axis=1)
data_concat['Q1'] = np.percentile(data_concat[['MOSar1','MOSar2', 'MOSar3','MOSar4', 'MOSar5', 'MOSar6', 'MOSar7', 'MOSar8']],25,axis=1)
data_concat['Q3'] = np.percentile(data_concat[['MOSar1','MOSar2', 'MOSar3','MOSar4', 'MOSar5', 'MOSar6', 'MOSar7', 'MOSar8']],75,axis=1)

#Plot up the median signal
plot_median = plt.figure("Median of the MOS signal")
ax1 = plot_median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.index, data_concat.Median_MOS_signal, linewidth=3, color = 'darkgreen')
ax1.plot(data_concat.index, data_concat.Q1, linewidth=2, color = 'greenyellow')
ax1.plot(data_concat.index, data_concat.Q3, linewidth=2, color = 'greenyellow')
#the [VOC] are given in ppm as this is what the COSI lab MFC uses. Multiply the conc by 1000 to get ppb.
ax2.plot(data_concat.index, data_concat.VOC*1000, color='k')
plt.title(cal_file, size=20)
ax1.set_ylabel("Median MOS (V)", size =18)
ax1.set_xlabel("Time since file began (s)", size =18)
ax2.set_ylabel("VOC conc. (ppb)",size=18)
plot_median.show()

# Median signal versus [VOC]
VOC = data_concat.VOC*1000
cal = plt.figure()
ax1 = cal.add_subplot(111)
ax1.scatter(VOC, data_concat.Median_MOS_signal)
ax1.set_xlabel("VOC concentration (ppb)", size=18)
ax1.set_ylabel("Median MOS signal (V)", size =18)
slope, intercept, r_value, p_value, std_err = stats.linregress(VOC, data_concat.Median_MOS_signal)
ax1.plot([np.min(VOC), np.max(VOC)], [(slope*np.min(VOC))+intercept, (slope*np.max(VOC))+intercept])
slope = ("%.3g" %slope)
intercept = ("%.3g" %intercept)
anchored_text = AnchoredText("y= "+slope+ "x + " +intercept , loc=2)
ax1.add_artist(anchored_text)
plt.title(cal_file, size=20)
cal.show()














