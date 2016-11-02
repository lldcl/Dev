"""Carbon monoxide MOS data file reader/plotter to look at individual files run with the dilute VOC mix.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160322_04']
filename = ['d20160309_01']

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
	
		#filter out periods when [CO] changes rapidly (dCOdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	dCOdt = pd.Series(np.absolute(mean_resampled.CO.diff()),name='dCOdt')
	dCOdt_filt = pd.Series(0, index=dCOdt.index,name='dCOdt_filt')
	dCO_ctr=0
	for dp in dCOdt:
		if (dp>0.01):
			dCOdt_filt[dCO_ctr:int(dCO_ctr+nm_pts)] = 1
		dCO_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dCOdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dCOdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.dCOdt_filt == 0]
	
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

"""COraw = plt.figure()
ax1 = COraw.add_subplot(2,1,1)
ax5 = ax1.twinx()
ax2 = COraw.add_subplot(2,1,2)
ax6 = ax2.twinx()

ax1.plot(data_concat.index, data_concat.MOS1, color = "teal")
ax1.set_ylabel("MOS1 (V)")
ax2.plot(data_concat.index, data_concat.MOS2, color = "darkorchid")
ax2.set_ylabel("MOS2 (V)")
ax5.plot(data_concat.index, data_concat.CO, color = "silver")
ax6.plot(data_concat.index, data_concat.CO, color = "silver")
ax5.set_ylabel("CO (ppm)")
ax6.set_ylabel("CO (ppm)")

if (stat == 'Y'):
	#select points on graph
	print "Click at either end of range"
	x = ginput(10) 

	#slice df and calculate stats on selected range. The second co-ordinate = 0 because I dont need the y-coordinates
	#from the x table that I've created. Go to terminal and write x then return to see what I mean.
	xmin1 = int(x[0][0])
	xmax1 = int(x[1][0])
	xmin2 = int(x[2][0])
	xmax2 = int(x[3][0])
	xmin3 = int(x[4][0])
	xmax3 = int(x[5][0])
	xmin4 = int(x[6][0])
	xmax4 = int(x[7][0])
	xmin5 = int(x[8][0])
	xmax5 = int(x[9][0])
	print "The selected x (index) range is"
	print xmin1,xmax1
	print xmin2,xmax2
	print xmin3,xmax3
	df_xrange1 = data_concat.iloc[xmin1:xmax1]
	df_xrange2 = data_concat.iloc[xmin2:xmax2]
	df_xrange3 = data_concat.iloc[xmin3:xmax3]
	df_xrange4 = data_concat.iloc[xmin4:xmax4]
	df_xrange5 = data_concat.iloc[xmin5:xmax5]
	
	plt.close()"""
	
"""COselect = plt.figure("Plot the selected regions")
	ax1 = COselect.add_subplot(1,1,1)
	ax2 = COselect.add_subplot(2,1,2)
	ax1.plot(data_concat.index,data_concat.MOS1,color="forestgreen",linewidth=3)
	ax1.plot([xmin1,xmin1],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax1.plot([xmax1,xmax1],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax1.plot([xmin2,xmin2],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax1.plot([xmax2,xmax2],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax1.plot([xmin3,xmin3],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax1.plot([xmax3,xmax3],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
	ax1.set_ylabel("MOS1 / V")
	ax1.set_xlabel("Index")
	ax2.plot(data_concat.index,data_concat.MOS2,color="indigo",linewidth=3)
 	ax2.plot([xmin1,xmin1],[np.min(np.min(data_concat.MOS2))*0.98,np.max(np.max(data_concat.MOS2))*1.02],color='k',linewidth=3)
  	ax2.plot([xmax1,xmax1],[np.min(np.min(data_concat.MOS2))*0.98,np.max(np.max(data_concat.MOS2))*1.02],color='k',linewidth=3)
  	ax2.plot([xmin2,xmin2],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax2.plot([xmax2,xmax2],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax2.plot([xmin3,xmin3],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax2.plot([xmax3,xmax3],[np.min(np.min(data_concat.MOS1))*0.98,np.max(np.max(data_concat.MOS1))*1.02],color='k',linewidth=3)
 	ax2.set_ylabel("MOS2 / V")
 	ax2.set_xlabel("Index")"""
	
"""rangefig = plt.figure("Section 1")
ax1 = rangefig.add_subplot(2,1,1)
ax2 = rangefig.add_subplot(2,1,2)
ax1.plot(df_xrange1.dt,df_xrange1.MOS1 ,color="forestgreen")
ax1.set_ylabel("MOS1  (V)")
ax1.set_xlabel("Time")
print 'MOS1 section 1 mean =',np.mean(df_xrange1.MOS1)
print 'MOS1 section 1 stddev =',np.std(df_xrange1.MOS1)
ax2.plot(df_xrange1.dt,df_xrange1.MOS2 ,color="indigo")
ax2.set_ylabel("MOS2  (V)")
ax2.set_xlabel("Time")
print 'MOS2 section 1 mean =',np.mean(df_xrange1.MOS2)
print 'MOS2 section 1 stddev =',np.std(df_xrange1.MOS2)

range2fig = plt.figure("Section 2")
ax1 = range2fig.add_subplot(2,1,1)
ax2 = range2fig.add_subplot(2,1,2)
ax1.plot(df_xrange2.dt,df_xrange2.MOS1 ,color="forestgreen")
ax1.set_ylabel("MOS1  (V)")
ax1.set_xlabel("Time")
print 'MOS1 section 2 mean =',np.mean(df_xrange2.MOS1)
print 'MOS1 section 2 stddev =',np.std(df_xrange2.MOS1)
ax2.plot(df_xrange2.dt,df_xrange2.MOS2 ,color="indigo")
ax2.set_ylabel("MOS2  (V)")
ax2.set_xlabel("Time")
print 'MOS2 section 2 mean =',np.mean(df_xrange2.MOS2)
print 'MOS2 section 2 stddev =',np.std(df_xrange2.MOS2)

cal_pointsMOS1 = [np.mean(df_xrange1.MOS1), np.mean(df_xrange2.MOS1),np.mean(df_xrange3.MOS1),np.mean(df_xrange4.MOS1),np.mean(df_xrange5.MOS1)]
cal_pointsMOS2 = [np.mean(df_xrange1.MOS2), np.mean(df_xrange2.MOS2),np.mean(df_xrange3.MOS2),np.mean(df_xrange4.MOS2),np.mean(df_xrange5.MOS2)]
stdeMOS1 = [np.std(df_xrange1.MOS1), np.std(df_xrange2.MOS1),np.std(df_xrange3.MOS1),np.std(df_xrange4.MOS1),np.std(df_xrange5.MOS1)]
stdeMOS2 = [np.std(df_xrange1.MOS2), np.std(df_xrange2.MOS2),np.std(df_xrange3.MOS2),np.std(df_xrange4.MOS2),np.std(df_xrange5.MOS2)]
stdeCO = [np.std(df_xrange1.CO), np.std(df_xrange2.CO),np.std(df_xrange3.CO),np.std(df_xrange4.CO),np.std(df_xrange5.CO)]

conc = [np.mean(df_xrange1.CO), np.mean(df_xrange2.CO),np.mean(df_xrange3.CO), np.mean(df_xrange4.CO),np.mean(df_xrange5.CO)]


# Plotting an CO cal.
cal = plt.figure()
ax1 = cal.add_subplot(2,1,1)
ax2 = cal.add_subplot(2,1,2)
ax1.scatter(conc, cal_pointsMOS1, color = "forestgreen")
ax1.errorbar(conc, cal_pointsMOS1, xerr=stdeCO, yerr=stdeMOS1, lw=1, fmt='o', color="g")
ax1.set_xlabel("CO (ppm)")
ax1.set_ylabel("Average MOS1 for selected regions (V)")
ax2.scatter(conc, cal_pointsMOS2, color = "indigo")
ax2.set_ylabel("Average MOS2 for selected regions (V)")
ax2.errorbar(conc, cal_pointsMOS2, xerr=stdeCO, yerr=stdeMOS2, lw=1, fmt='o', color="m")
ax2.set_xlabel("CO (ppm)")
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(conc, cal_pointsMOS1)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(conc, cal_pointsMOS2)
ax1.plot([np.min(conc), np.max(conc)], [(slope1*np.min(conc))+intercept1, (slope1*np.max(conc))+intercept1])
ax2.plot([np.min(conc), np.max(conc)], [(slope2*np.min(conc))+intercept2, (slope2*np.max(conc))+intercept2])
slope1 = ("%.3g" %slope1)
intercept1 = ("%.3g" % (intercept1))
R21 = ("%.3g" % (R2value1))
slope2 = ("%.3g" %slope2)
intercept2 = ("%.3g" % (intercept2))
R22 = ("%.3g" % (R2value2))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(0.1, 1.9 ,'y = ' +str(slope1)+'x +' +str(intercept1), style='italic', fontsize = 15) 
ax1.text(0.1, 1.88, '$R^2 value$ = '+str(R21), style = 'italic', fontsize=15)
ax2.text(0.1, 1.75 ,'y = ' +str(slope2)+'x +' +str(intercept2), style='italic', fontsize = 15) 
ax2.text(0.1, 1.73, '$R^2 value$ = '+str(R22), style = 'italic', fontsize=15)"""

# Plot the differential of the [SO2]
diff_fig = plt.figure()
ax1 = diff_fig.add_subplot(211)
ax2 = diff_fig.add_subplot(212)
ax1.plot(mean_resampled.index, mean_resampled.CO.diff())
ax2.plot(mean_resampled.index, mean_resampled.dCOdt_filt)

# The median MOS signal
data_concat['Median_MOS_signal'] = data_concat[['MOSar1','MOSar2','MOSar3','MOSar4','MOSar5','MOSar6','MOSar7','MOSar8']].median(axis=1)
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.index, data_concat.Median_MOS_signal, color="green")
#Plot the CO conc from the CO box.
ax2.plot(data_concat.index, data_concat.CO, color = "blue")
ax1.set_xlabel("Index",size =18)
ax2.set_ylabel("CO conc (ppb)", size=18)
ax1.set_ylabel('Median MOS signal (V)',size=18)
plt.title(cal_file, size=20)

CO_cal = plt.figure()
ax1 = CO_cal.add_subplot(111)
ax1.scatter(data_concat.CO, data_concat.Median_MOS_signal, color = "black")
ax1.set_xlabel("CO concentration (ppb)", size=18)
ax1.set_ylabel("Median MOS signal (V)", size=18)
slope, intercept, R2value, p_value, st_err = stats.linregress(data_concat.CO, data_concat.Median_MOS_signal)
ax1.plot([np.min(data_concat.CO), np.max(data_concat.CO)], [(np.min(data_concat.CO)*slope+intercept), (np.max(data_concat.CO)*slope+intercept)])
slope = ("%.3g" %slope)
intercept = ("%.3g" %intercept)
anchored_text1 = AnchoredText("MOS y= "+slope+ "x + " +intercept , prop=dict(size=15),loc=2)
ax1.add_artist(anchored_text1)
plt.title("CO calibration", size=20)

	
plt.show()