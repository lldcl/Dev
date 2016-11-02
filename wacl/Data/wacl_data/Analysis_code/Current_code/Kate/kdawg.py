"""Analysing ambiet air files. Lots of regression plots"""

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
cal_file =['ambientexp2_split_160810_025056','ambientexp2_split_160810_072949','ambientexp2_split_160810_120843','ambientexp2_split_160810_164735','ambientexp2_split_160810_212627','ambientexp2_split_160811_020521','ambientexp2_split_160812_083920','ambientexp2_split_160812_131813','ambientexp2_split_160812_175706','ambientexp2_split_160812_223559','ambientexp2_split_160813_031451','ambientexp2_split_160813_075344','ambientexp2_split_160813_123237','ambientexp2_split_160813_171130','ambientexp2_split_160813_215023','ambientexp2_split_160814_022915','ambientexp2_split_160814_070808','ambientexp2_split_160814_114701','ambientexp2_split_160814_162553','ambientexp2_split_160814_210446','ambientexp2_split_160815_014338','ambientexp2_split_160815_062231','ambientexp2_split_160815_110123','ambientexp2_split_160815_154018','ambientexp2_split_160815_201911','ambientexp2_split_160816_005804','ambientexp2_split_160816_053657','ambientexp2_split_160816_101551','ambientexp2_split_160816_145444','ambientexp2_split_160816_193338','ambientexp2_split_160817_001231','ambientexp2_split_160818_040552','ambientexp2_split_160818_084443','ambientexp2_split_160818_132339','ambientexp2_split_160818_180233','ambientexp2_split_160818_224127','ambientexp2_split_160819_032021','ambientexp2_split_160819_083604']
#cal_file =['ambientexp2_split_160808_090051','ambientexp2_split_160808_133947','ambientexp2_split_160808_181841','ambientexp2_split_160808_225736','ambientexp2_split_160809_033630','ambientexp2_split_160809_081524','ambientexp2_split_160809_125417','ambientexp2_split_160809_173311','ambientexp2_split_160809_221204','ambientexp2_split_160811_020521']
#cal_file = ['ambientexp2_split_160818_040552','ambientexp2_split_160818_084443','ambientexp2_split_160818_132339','ambientexp2_split_160818_180233','ambientexp2_split_160818_224127','ambientexp2_split_160819_032021','ambientexp2_split_160819_083604']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	folder = list(i)[18:22]
	f = '20'+"".join(folder)+'/DAQfactory_split_files/'+i

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
# If there are more than files the data_concat function will join tem together.
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

# Returns the initial date and time that the file began
print(data_concat.Time[0])
print(data_concat.Time[len(data_concat.Time)-1])

# Median MOS signal
#data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']].median(axis=1)
# Without the broken MOS 4 and 6
data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
data_concat['Mean_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].mean(axis=1)
##########################################################################################
#Other electrochemical sensprs in line with the MOS

import matplotlib.cm as cm
c = data_concat.Time
c = (c-np.min(c))/np.max(c-np.min(c))

numbers = range(1,10) 
ctr=1
variables = ['O3_OP1_Av', 'CO_OP1_Av', 'NO_OP1_Av','NO2_OP1_Av','RH1_Av','RH2_Av','Temp1_Av','Temp2_Av','Voltage_Av']
colours = ['blue','orange','green','purple','navy','navy','red','red','black']
units=['ppb','ppb','ppb','ppb','(%)','(%)','oC','oC','V']
for i,p,q,x in zip(variables,colours,units,numbers):
	figure_i = plt.figure()
	ax1 = figure_i.add_subplot(211)
	ax3 = ax1.twinx()
	ax2 = figure_i.add_subplot(212)
	ax1.plot(data_concat.Time, data_concat[i], label=i, color= p)
	ax3.plot(data_concat.Time, data_concat.Median_MOS_signal, color= 'black')
	ax1.set_xlabel("Time", size=18)
	ax1.set_ylabel(i+" ("+q+")", size=18)
	ax3.set_ylabel("Median MOS (V)", size =18)
	ax2.scatter(data_concat[i], data_concat.Median_MOS_signal, color=cm.jet(c))
	ax2.set_xlabel(i,size=18)
	ax2.set_ylabel("Median MOS (V)",size=18)
	slopex, interceptx, R2valuex, p_valuex, st_errx = stats.linregress(data_concat[i], data_concat.Median_MOS_signal) 
	ax2.plot([np.min(data_concat[i]), np.max(data_concat[i])], [(np.min(data_concat[i])*slopex+interceptx), (np.max(data_concat[i])*slopex+interceptx)])
	slopex = ("%.3g" %slopex)
	interceptx = ("%.3g" %interceptx)
	anchored_text = AnchoredText(i+"y= "+slopex+ "x + " +interceptx , loc=2)
	ax2.add_artist(anchored_text)
	ax2.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
	ctr+=1
	ax1.tick_params(labelsize=18)
	ax2.tick_params(labelsize=18)
	ax3.tick_params(labelsize=18)
	figure_i.show()
	
# Using the mean of the MOS sensor instead of the median. The median is more accurate.
# for i,p,q in zip(variables,colours,units):
# 	figure_i = plt.figure()
# 	ax1 = figure_i.add_subplot(211)
# 	ax3 = ax1.twinx()
# 	ax2 = figure_i.add_subplot(212)
# 	ax1.plot(data_concat.Time, data_concat[i], label=i, color= p)
# 	ax3.plot(data_concat.Time, data_concat.Mean_MOS_signal, color= 'black')
# 	ax1.set_xlabel("Time")
# 	ax1.set_ylabel(i+" ("+q+")")
# 	ax3.set_ylabel("Mean MOS (V)")
# 	ax2.scatter(data_concat[i], data_concat.Mean_MOS_signal, color=cm.jet(c))
# 	ax2.set_xlabel(i)
# 	ax2.set_ylabel("Mean MOS (V)")
# 	
# 	figure_i.show()
