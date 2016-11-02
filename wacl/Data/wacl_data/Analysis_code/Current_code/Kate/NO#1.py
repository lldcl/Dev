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
cal_file = ['d20160317_01']

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

	#filter out periods when isop changes rapidly (disopdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	dNOdt = pd.Series(np.absolute(mean_resampled.NO.diff()),name='dNOdt')
	dNOdt_filt = pd.Series(0, index=dNOdt.index,name='dNOdt_filt')
	dNO_ctr=0
	for dp in dNOdt:
		if (dp>1.):
			dNOdt_filt[dNO_ctr:int(dNO_ctr+nm_pts)] = 1
		dNO_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dNOdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dNOdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.dNOdt_filt == 0]

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
rawfig = plt.figure("Raw MOS vs [NO]")

axa = rawfig.add_subplot(2,1,1)
axb = rawfig.add_subplot(2,1,2)

import matplotlib.cm as cm
c=data_concat.index.dayofyear+(data_concat.index.hour/24.)+(data_concat.index.minute/(24.*60.))
c = (c-np.min(c))/np.max(c-np.min(c))

axa.scatter(data_concat.NO, data_concat.MOS1,color=cm.jet(c),marker='o')
axb.scatter(data_concat.NO, data_concat.MOS2,color=cm.jet(c),marker='o')

axa.set_ylabel("MOS1 (V)")
axb.set_ylabel("MOS2 (V)")
axa.set_xlabel("NO (ppb)")
axb.set_xlabel("NO (ppb)")

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
cor2.plot(data_concat.dt, data_concat.NO, color='silver')

cor5.plot(data_concat.dt,data_concat.MOS2,color='teal',marker='o')
cor7.plot(data_concat.dt, data_concat.NO, color='silver')


cor9ax.plot(data_concat.dt, data_concat.RH1, color='royalblue', linewidth =3)
cor11ax.plot(data_concat.dt, data_concat.Temp*100, color='firebrick', linewidth = 3)
cor11ax.plot(data_concat.dt, data_concat.Temp2*100, color='k', linewidth = 3)
cor13ax.plot(data_concat.dt, data_concat.VS, color = 'darkviolet', linewidth = 3)

cor11ax.set_ylabel("Temperature")
cor1ax.set_ylabel("MOS1 (V)")
cor5.set_ylabel("MOS2 (V)")
cor9ax.set_ylabel("RH")
cor7.set_ylabel("Total NO /ppb")
cor13ax.set_ylabel(" Supply voltage (V)")

### Need to plot up the VOC sensitivity polts, with linear regression.
# Finding the NO sensitivity
# Bin the data into bins of 1ppb NO, get an average for this data and then plot this.
# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 1 ppb of VOC sections, and take an average of the data.
bin1 = stats.binned_statistic(data_concat.NO, MOS1_cor, statistic='mean', bins=100, range=(0,100))
bin2 = stats.binned_statistic(data_concat.NO, MOS2_cor, statistic='mean', bins=100, range=(0,100))
bin3 = stats.binned_statistic(data_concat.NO, data_concat.NO, statistic='mean', bins=100, range=(0,100))
bin4 = stats.binned_statistic(data_concat.NO, MOS1_cor, statistic=stddev, bins=100, range=(0,100))
bin5 = stats.binned_statistic(data_concat.NO, MOS2_cor, statistic=stddev, bins=100, range=(0,100))
bin6 = stats.binned_statistic(data_concat.NO, data_concat.NO, statistic=stddev, bins=100, range=(0,100))
# Turn into pandas to get rid of NaNs.
MOS1_cor = pd.Series(bin1[0])
MOS2_cor = pd.Series(bin2[0])
NO = pd.Series(bin3[0])
st1 = pd.Series(bin4[0])
st2 = pd.Series(bin5[0])
stIs = pd.Series(bin6[0])
# get rid of NaNs for both the data and the standard deviation.
MOS1_cor = MOS1_cor.dropna()
MOS2_cor = MOS2_cor.dropna()
NO = NO.dropna()
st1 = st1.dropna()
st2 = st2.dropna()
stIs = stIs.dropna()

NOPLOT = plt.figure("NO sensitivity with the general background removed")
ax1 = NOPLOT.add_subplot(2,1,1)
ax2 = NOPLOT.add_subplot(2,1,2)

ax1.scatter(NO, MOS1_cor, color="g")
ax1.errorbar(NO, MOS1_cor, xerr=stIs, yerr=st1, lw=1, fmt='o', color="g")
ax2.scatter(NO, MOS2_cor, color="b")
ax2.errorbar(NO, MOS2_cor, xerr=stIs, yerr=st2, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_ylabel("MOS2 signal / v")
ax1.set_xlabel("NO / ppb")
ax2.set_xlabel("NO / ppb")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(NO, MOS1_cor)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(NO, MOS2_cor)
ax1.plot([np.min(NO), np.max(NO)], [(slope3*np.min(NO))+intercept3, (slope3*np.max(NO))+intercept3])
ax2.plot([np.min(NO), np.max(NO)], [(slope4*np.min(NO))+intercept4, (slope4*np.max(NO))+intercept4])
print ("Gradient of NO vs MOS1", slope3)
print ("Intercept of NO vsMOS1", intercept3)
print ("R2 of NO vs MOS1", R2value3)
print ("Gradient of NO vs MOS2", slope4)
print ("Intercept of NO vs MOS2", intercept4)
print ("R2 of NO vs MOS2", R2value4)
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
ax1.text((np.min(NO))*1.0001, np.max(MOS1_cor)*0.999 ,'y = ' +str(slope3)+'x +' +str(intercept3), style='italic', fontsize = 15) 
ax1.text((np.min(NO))*1.0001, np.max(MOS1_cor)*0.975, '$R^2 value$ = '+str(R23), style = 'italic', fontsize=15)
ax2.text((np.min(NO))*1.0001, np.max(MOS2_cor)*0.999 ,'y = ' +str(slope4)+'x +' +str(intercept4), style='italic', fontsize = 15) 
ax2.text((np.min(NO))*1.0001, np.max(MOS2_cor)*0.975, '$R^2 value$ = '+str(R24), style = 'italic', fontsize=15)

"""
	
rangefig = plt.figure("Section 1")
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
stdeNO = [np.std(df_xrange1.NO), np.std(df_xrange2.NO),np.std(df_xrange3.NO),np.std(df_xrange4.NO),np.std(df_xrange5.NO)]

conc = [np.mean(df_xrange1.NO), np.mean(df_xrange2.NO),np.mean(df_xrange3.NO), np.mean(df_xrange4.NO),np.mean(df_xrange5.NO)]


# Plotting an NO cal.
cal = plt.figure()
ax1 = cal.add_subplot(2,1,1)
ax2 = cal.add_subplot(2,1,2)
ax1.scatter(conc, cal_pointsMOS1, color = "forestgreen")
ax1.errorbar(conc, cal_pointsMOS1, xerr=stdeNO, yerr=stdeMOS1, lw=1, fmt='o', color="g")
ax1.set_xlabel("NO (ppm)")
ax1.set_ylabel("Average MOS1 for selected regions (V)")
ax2.scatter(conc, cal_pointsMOS2, color = "indigo")
ax2.set_ylabel("Average MOS2 for selected regions (V)")
ax2.errorbar(conc, cal_pointsMOS2, xerr=stdeNO, yerr=stdeMOS2, lw=1, fmt='o', color="m")
ax2.set_xlabel("NO (ppm)")
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
ax1.text((np.min(conc))*1.0000001, 1.84 ,'y = ' +str(slope1)+'x +' +str(intercept1), style='italic', fontsize = 15) 
ax1.text((np.min(conc))*1.0000001, 1.82, '$R^2 value$ = '+str(R21), style = 'italic', fontsize=15)
ax2.text((np.min(conc))*1.0000001, 1.75 ,'y = ' +str(slope2)+'x +' +str(intercept2), style='italic', fontsize = 15) 
ax2.text((np.min(conc))*1.0000001, 1.73, '$R^2 value$ = '+str(R22), style = 'italic', fontsize=15)
	

plt.show()"""
plt.show()

