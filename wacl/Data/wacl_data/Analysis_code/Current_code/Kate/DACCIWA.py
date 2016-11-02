"""Analysing DACCIWA MOS files"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/DACCIWA/'
#cal_file = ['a20160713_03']
cal_file = ['a20160713_01','a20160713_02','a20160713_03']

for i in cal_file:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i

#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f,header=0)

# 	convert daqfac time into real time pd.datetime object
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')

	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	Time_avg = '10S'
 
	mean_resampled = data.copy(deep=True)
	mean_resampled.RH = data.ard26
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)	
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
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)


name = {'Time':'Time','ard0':'MS1_num','ard1':'MOSar1','ard2':'MS1std','ard3':'MS2_num','ard4':'MOSar2','ard5':'MS2std','ard6':'MS3_num','ard7':'MOSar3','ard8':'MS3std','ard9':'MS4_num','ard10':'MOSar4','ard11':'MS4std','ard12':'MS5_num','ard13':'MOSar5','ard14':'MS5std','ard15':'MS6_num','ard16':'MOSar6','ard17':'MS6std','ard18':'MS7_num','ard19':'MOSar7','ard20':'MS7std','ard21':'MS8_num','ard22':'MOSar8','ard23':'MS8std','ard24':'Temp','ard25':'Temp_std','ard26':'RH','ard27':'RH_std','dt':'dt'}
namesnew = [ name[a] for a in data_concat.columns]
#print namesnew
data_concat.columns = namesnew

print(data_concat.Time[0])

sub = 'MOS'
MOS = [s for s in data_concat.columns if sub in s]
# plot up the MOS voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("MOS (V)", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
MOSfig.show()

# Median MOS signal
data_concat['Median_MOS_signal'] = data_concat[['MOSar1','MOSar2','MOSar3','MOSar4','MOSar5','MOSar6','MOSar7','MOSar8']].median(axis=1)
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green", linewidth=5, label="MOS")
ax2.plot(data_concat.Time, data_concat.Temp, color="red", label="Temp (oC)")
median.show()


Variables = plt.figure("Temp and humidity")
ax1 = Variables.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Temp, color="red", label="Temp")
ax2.plot(data_concat.Time, data_concat.RH, color="blue", label="RH (%)")
ax1.set_ylabel("Temp (oC)")
ax2.set_ylabel("RH (%)")
Variables.show()

# Call the other sensors data file.
path1 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/DACCIWA/'

cal_file1 = 'other_sensors_20160713_01.csv'

wb = path1+cal_file1

other = pd.read_csv(wb)
# 	convert daqfac time into real time pd.datetime object
other.Time = pd.to_datetime(other.Time,unit='D')

T1 = pd.datetime(2016,07,11, 0)
# T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(2016,07,18,0)
offset=T1-T2
other.Time+=offset

Time_avg = '10S'
 
mean = other.copy(deep=True)
mean.TheTime = pd.to_datetime(mean.Time,unit='L')
mean = mean.set_index(mean.Time,drop=True)
mean = mean.resample(Time_avg, how='mean',fill_method='pad')
Time = pd.Series(mean.index,name='Time', index=mean.index)
mean = pd.concat([mean,Time],axis=1)

other = plt.figure("From other sensors")
ax1 = other.add_subplot(111)
ax1.plot(mean.Time, mean.NO, color="lightgreen")
ax1.plot(mean.Time, mean.Nox, color="green")
ax1.plot(mean.Time, mean.o3_2b, color="blue")
ax1.plot(mean.Time, mean.carbon_monox, color="navy")
ax1.plot(mean.Time, mean.so2, color="purple")
ax1.plot(mean.Time, mean.ch4_dry, color="black")	
ax1.set_xlabel("Time")
print(mean.Time[0])
other.show()
	
fig = plt.figure("Other variables data")
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax3 = ax1.twinx()

ax1.plot(mean.Time, mean.o3_2b, color="blue",label="Ozone")
ax1.plot(mean.Time, mean.carbon_monox, color="orange", linewidth=4, label="CO")
ax1.plot(mean.Time, mean.so2, color="purple", label="SO2")
ax1.plot(mean.Time, mean.ch4_dry, color="black", label="Methane")
ax1.set_ylabel("CO, SO2, ozone and methane")
ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
ax3.plot(data_concat.Time, data_concat.Median_MOS_signal, color="red", linewidth=5, label="MOS")
ax3.set_ylabel("Median MOS signal (V)")
plt.legend()#bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
ax2.plot(mean.Time, mean.NO, color="lightgreen", linewidth=3,label="NO")
ax2.plot(mean.Time, mean.Nox, color="green", linewidth=3, label="NOx")
ax2.legend()
ax2.set_ylabel("NO and NOx")
plt.legend()#bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
# leg = plt.gca().get_legend()
# ltext  = leg.get_texts()  # all the text.Text instance in the legend
# plt.setp(ltext, fontsize='small')    # the legend text fontsize
# Plot the MOS data on the same time axis.
fig.show()


