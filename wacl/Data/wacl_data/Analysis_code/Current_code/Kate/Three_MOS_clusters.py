"""Analysing files containing data from three clusters of 8 MOS sensors."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

# The path to the raw files
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
# The name of the MOS file to be analysed
#cal_file =['d160905_060841','d160905_091251',
cal_file=['d160913_092635','d160914_085814']
#cal_file=['d160908_090258','d160909_134057']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	folder = list(i)[1:5]
	f = '20'+"".join(folder)+"/"+i

#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)
	

# 	convert daqfac time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')

	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset
# Ten second averaging of the raw data
	Time_avg = '10S'
# Make a new copy of the data called mean_resampled 
	mean_resampled = data.copy(deep=True)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
#Set the index to be the time column, when you do this it drops the index, even though it is set to False.
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)
	
	#filter out periods when isop changes rapidly (disopdt<0.1) and for 60 seconds afterwards
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
	
# If there are more than files the data_concat function will join them together.
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'
		
# Re-make and re-set the index to be the time column for the data_concat dataframe.
T3 = pd.datetime(2015,01,01,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('int')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)

diff = plt.figure("Differential")
ax1 = diff.add_subplot(111)
ax1.plot(data_concat.Time, data_concat.dVOCdt, color="red")
diff.show()
# Returns the initial date and time that the file began
print(data_concat.Time[0])
print(data_concat.Time[len(data_concat.Time)-1])

# Finding the median MOS signal
data_concat['Median_MOS1'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
data_concat['Median_MOS2'] = data_concat[['MOS1b_Av','MOS2b_Av','MOS3b_Av','MOS5b_Av','MOS7b_Av','MOS8b_Av']].median(axis=1)
data_concat['Median_MOS3'] = data_concat[['MOS1c_Av','MOS2c_Av','MOS3c_Av','MOS5c_Av','MOS7c_Av','MOS8c_Av']].median(axis=1)
##########################################################################################

median = ['Median_MOS1', 'Median_MOS2','Median_MOS3']
numbers = [1,2,3,4]
color = ["blue","green","purple","orange"]
median_plot = plt.figure()

for i,n,p in zip(median,numbers, color):
	ax1 = median_plot.add_subplot(111)
	ax2 = ax1.twinx()
	ax1.plot( data_concat.Time, data_concat[i], color=p, label=i)
	ax1.set_xlabel("Time")
	ax1.set_ylabel("MOS median (V)",size=18)
	ax2.plot(data_concat.Time, data_concat.VOC, color="k")
	ax2.set_ylabel("VOC conc (ppm)",size=18)
	ax1.legend()
	ax1.tick_params(labelsize=20)
plt.show()	

# Plot up the VOC conc vs the MOS median for each cluster, with linear regression.
plot = plt.figure("Median calibration")
for i,x,q in zip(median,numbers, color):
	figure_i = plt.figure()
	ax1 = figure_i.add_subplot(111)
	ax1.scatter(data_concat.VOC, data_concat[i], color= q)
	slope, intercept, R2value, p_value, st_err = stats.linregress(data_concat.VOC, data_concat[i]) 
	ax1.plot([np.min(data_concat.VOC), np.max(data_concat.VOC)], [(np.min(data_concat.VOC)*slope+intercept), (np.max(data_concat.VOC)*slope+intercept)])
	slope = ("%.3g" %slope)
	intercept = ("%.3g" %intercept)
	R2v = ("%.3g" %R2value)
	anchored_text = AnchoredText(i+"y= "+slope+ "x + " +intercept + "  R2 value = "+R2v, loc=2)
	ax1.add_artist(anchored_text)	
	
		
# Determining the standard deviation between the different MOS clusters
# Make a new column which averages the three medians.

data_concat["Average_MOS"] = data_concat[['Median_MOS1','Median_MOS2','Median_MOS3']].mean(axis=1)
data_concat["Stddev_MOS"] = data_concat[['Median_MOS1','Median_MOS2','Median_MOS3']].std(axis=1)
data_concat["pos"] = data_concat.Average_MOS + data_concat.Stddev_MOS
data_concat["neg"] = data_concat.Average_MOS - data_concat.Stddev_MOS
deviation = plt.figure()
ax1 = deviation.add_subplot(111)
ax1.plot(data_concat.Time, data_concat.Average_MOS, color="k")
ax1.errorbar(data_concat.Time, data_concat.Average_MOS, yerr= data_concat.Stddev_MOS, color="silver")
###########################################
data_concat["VOCppb"] = data_concat.VOC*1000
plot = plt.figure("Median calibration with binning")
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
for k,x,q in zip(median,numbers, color):
# Bin the data into 1 ppb of VOC sections, and take an average of the data.
	bin_ka = stats.binned_statistic(data_concat.VOCppb, data_concat[k], statistic='mean', bins=120, range=(0,120))
	bin2 = stats.binned_statistic(data_concat.VOCppb, data_concat.VOC, statistic='mean', bins=120, range=(0,120))
	bin_kb = stats.binned_statistic(data_concat.VOCppb, data_concat[k], statistic=stddev, bins=120, range=(0,120))
	bin3 = stats.binned_statistic(data_concat.VOCppb, data_concat.VOC, statistic=stddev, bins=120, range=(0,120))
	bin_stddev = stats.binned_statistic(data_concat.VOCppb, data_concat[k], statistic=stddev, bins=120, range=(0,120))
	bin3 = stats.binned_statistic(data_concat.VOCppb, data_concat.VOC, statistic=stddev, bins=120, range=(0,120))
	
	# Turn into pandas series and get rid of NaNs.
	bin_ka = pd.Series(bin_ka[0])
	VOC = pd.Series(bin2[0])
	st1 = pd.Series(bin_kb[0])
	stIs = pd.Series(bin3[0])
	bin_k = bin_ka.dropna()
	VOC = VOC.dropna()
	st1 = st1.dropna()
	stIs = stIs.dropna()
	
	figure_k = plt.figure()
	ax1 = figure_k.add_subplot(111)
	ax1.scatter(VOC, bin_k, color= q)
	ax1.errorbar(VOC, bin_k, xerr=stIs, yerr=st1, lw=1, fmt='o', color=q)
	slopek, interceptk, R2valuek, p_valuek, st_errk = stats.linregress(VOC, bin_k) 
	ax1.plot([np.min(VOC), np.max(VOC)], [(np.min(VOC)*slopek+interceptk), (np.max(VOC)*slopek+interceptk)])
	slopek = ("%.3g" %slopek)
	interceptk = ("%.3g" %interceptk)
	R2vk = ("%.3g" %R2valuek)
	anchored_text = AnchoredText(k+" y= "+slopek+ "x + " +interceptk + "  R2 value = "+R2vk, loc=2)
	ax1.add_artist(anchored_text)	
	ax1.set_xlabel(" VOC concentration (ppb)",size=18)
	ax1.set_ylabel(" Median MOS (V)",size=18)
	ax1.tick_params(labelsize=20)
	


# get rid of NaNs for both the data and the standard deviation.
"""
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

import matplotlib.cm as cm
c = data_concat.Time
c = (c-np.min(c))/np.max(c-np.min(c))

numbers = range(1,12) 
ctr=1
variables = ['O3_ave1', 'O3_ave2','CO_ave1','CO_ave2','NO_ave1','NO_ave2','NO2_ave1','NO2_ave2','HIH1_Av','LM65T1_Av','SV_Av']
colours = ['blue','orange','green','purple','navy','lightblue','red','darkgreen','black', 'silver','violet']
units=['ppb','ppb','ppb','ppb','ppb','ppb','ppb','(%)','oC','V']
for i,p,q,x in zip(variables,colours,units,numbers):
	figure_i = plt.figure()
	ax1 = figure_i.add_subplot(211)
	ax3 = ax1.twinx()
	ax2 = figure_i.add_subplot(212)
	ax1.plot(data_concat.Time, data_concat[i], label=i, color= p)
	ax3.plot(data_concat.Time, data_concat.Average_MOS, color= 'black')
	ax1.set_xlabel("Time")
	ax1.set_ylabel(i+" ("+q+")")
	ax3.set_ylabel("Median MOS (V)")
	ax2.scatter(data_concat[i], data_concat.Average_MOS, color=cm.jet(c))
	ax2.set_xlabel(i)
	ax2.set_ylabel("Median MOS (V)")
	slopex, interceptx, R2valuex, p_valuex, st_errx = stats.linregress(data_concat[i], data_concat.Average_MOS) 
	ax2.plot([np.min(data_concat[i]), np.max(data_concat[i])], [(np.min(data_concat[i])*slopex+interceptx), (np.max(data_concat[i])*slopex+interceptx)])
	slopex = ("%.3g" %slopex)
	interceptx = ("%.3g" %interceptx)
	anchored_text = AnchoredText(i+"y= "+slopex+ "x + " +interceptx , loc=2)
	ax2.add_artist(anchored_text)
	ax2.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
	ctr+=1
	figure_i.show()"""

plt.show()
