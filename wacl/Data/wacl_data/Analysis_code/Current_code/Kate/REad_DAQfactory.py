"""Analysing the MOS files collected by running ambient air over the sensors. MOS refers to the metal oxide sensors, which 
are more sensitive towards VOCs but there are a few other sensors in the same air flow too. These include a Temp probe, an 
RH probe and electrochemical sensors monitoring CO, NO, NO2 and ozone becasue we are worried these might interfere with 
the MOS signal"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

# The path to where the raw files are stored
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# The name of the MOS file to be analysed
cal_file = ['ambientexp2_split_160811_020521']

# This bit of code works out which folder the file is in from the name of the file becasue the data is store in folders named 
# following the format YYYYMM depending on when the file was recorded.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	folder = list(i)[18:22]
	f = '20'+"".join(folder)+'/DAQfactory_split_files/'+i

#for f in filenames:
	print f
#read file into dataframe and call the dataframe data
	data = pd.read_csv(path+f)
	

# 	convert DAQfactory time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
# DAQfactory is the programme we are using to record the data into CSV files.
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
# Set the index to be the time column, when you do this it drops the index, even though it is set to False.
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)	
# If there are more than one files to be read in together the data_concat function will join them together.
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

# Find all the columns in the file that have these titles, as these are the MOS columns.
sub = 'MOS'
MOS=['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']
# Plot up the MOS voltages
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
#data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']].median(axis=1)
# Without the broken MOS 4 and 6
data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
# Plot the median MOS signal with temperature, over time.
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green", linewidth=5, label="MOS")
ax2.plot(data_concat.Time, data_concat.Temp2_Av, color="pink", label="Temp 2 (oC)")
ax1.set_ylabel("Median MOS signal (V)")
ax1.set_xlabel("Time")
ax2.set_ylabel("Temperature")
median.show()

# Plot up temperature and humidity which are recorded in the same air flow as the MOS.
Variables = plt.figure("Temp and humidity")
ax1 = Variables.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Temp1_Av, color="red", label="Temp 1 (oC)")
ax1.plot(data_concat.Time, data_concat.Temp2_Av, color="pink", label="Temp 2 (oC)")
#ax1.plot(data_concat.Time, data_concat.Temp3_Av, color="purple", label="Temp 3 (oC)")
ax1.plot(data_concat.Time, data_concat.RH1_Av, color="blue", label="RH 1 (%)")
#ax2.plot(data_concat.Time, data_concat.RH2_Av, color="navy", label="RH 2 (%)")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green",linewidth = 3, label="Median MOS")
ax1.set_ylabel("Temperature (oC) and RH (%)",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=1)
ax2.legend(loc=2)
Variables.show()

# Correlation plot
correlation = plt.figure("Temp and humidity correlated")
ax1a = correlation.add_subplot(111)
#ax2 = ax1a.twinx()
ax1a.scatter(data_concat.Temp1_Av, data_concat.Median_MOS_signal, color="red", label="Temp 1 (oC)")
#ax1a.scatter(data_concat.RH1_Av, data_concat.Median_MOS_signal , color="blue", label="RH 1 (%)")
ax1a.set_ylabel("Median MOS (V)",size=16)
ax1a.set_xlabel(" Temperature (oC) and RH (%)",size=16)
ax1a.legend(loc=1)
#ax2.legend(loc=2)
correlation.show()


##########################################################################################
#Other electrochemical sensprs in line with the MOS

Variables1 = plt.figure("CO, ozone and NOx")

# Find all the columns in the file that have these titles, as these are the MOS columns.
CO=['CO_OP1_Av','CO_OP2_Av']
# Plot up the CO data
ax1 = Variables1.add_subplot(311)
colors = ["black","firebrick"]
for u,v in zip(CO,colors):
    ax1.plot(data_concat.Time,data_concat[u],color=v,linewidth=3)
    plt.legend(CO, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("Carbon monoxide", size=20)
    plt.xlabel("Time", size=20)	

ozo=['O3_OP1_Av','O3_OP2_Av']
# Plot up the ozone data
ax2 = Variables1.add_subplot(312)
colors = ["blue","darkblue"]
for w,x in zip(ozo,colors):
    ax2.plot(data_concat.Time,data_concat[w],color=x,linewidth=3)
    plt.legend(ozo, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("Ozone", size=20)
    plt.xlabel("Time", size=20)	

NOx=['NO2_OP1_Av','NO2_OP2_Av', 'NO_OP1_Av','NO_OP2_Av']
# Plot up the NOx data
ax3 = Variables1.add_subplot(313)
colors = ["green","darkgreen"]
for y,z in zip(NOx,colors):
    ax3.plot(data_concat.Time,data_concat[y],color=z,linewidth=3, label=[y])
    plt.legend(NOx, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("NOx", size=20)
    plt.xlabel("Time", size=20)	
Variables1.show()


# MOS versus in-line electrochemical ozone and NO data 
MOSozone = plt.figure("MOS and in-line ozone and NO sensor")
ax1 = MOSozone.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.O3_OP1_Av, color="blue", label="Ozone (ppb)")
ax1.plot(data_concat.Time, data_concat.NO2_OP1_Av, color="green", label="NO2 (ppb)")
ax1.plot(data_concat.Time, data_concat.CO_OP1_Av, color="orange", label="CO")
ax1.plot(data_concat.Time, data_concat.NO_OP1_Av, color="purple", label="NO (ppb)")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="black",linewidth = 3, label="Median MOS")
ax1.set_ylabel("Ozone and NO2",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=2)
ax2.legend(loc=1)
MOSozone.show()

# The MOS sensors are (supposedly) more sensitive towards VOCs and CO is the closest to this class of compound out of 
# the electrochemical sensors so this is plotted up separately. 
MOSCO = plt.figure("MOS and in-line CO sensor")
ax1 = MOSCO.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot(data_concat.Time, data_concat.CO_OP1_Av, color="orange", label="CO")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="black",linewidth = 3, label="Median MOS")
ax1.set_ylabel("CO",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=2)
ax2.legend(loc=1)
MOSCO.show()

# A plot to see if there is a strong correlation between the two. 
COdep = plt.figure("MOS and CO linked?")
ax1 = COdep.add_subplot(111)
ax1.scatter(data_concat.CO_OP1_Av, data_concat.Median_MOS_signal,  color="silver", label="CO")
ax1.set_xlabel("CO",size=16)
ax1.set_ylabel(" Median MOS (V)",size=16)
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(data_concat.CO_OP1_Av, data_concat.Median_MOS_signal)
ax1.plot([np.min(data_concat.CO_OP1_Av), np.max(data_concat.CO_OP1_Av)], [(slope1*np.min(data_concat.CO_OP1_Av))+intercept1, (slope1*np.max(data_concat.CO_OP1_Av))+intercept1])
# Get the linear regression paramenters to have 3 sig figs.
slope1 = ("%.3g" %slope1)
intercept1 = ("%.3g" % (intercept1))
R2value1 = ("%.3g" % (R2value1))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(1,2,'y = ' +str(slope1)+'x +' +str(intercept1)+ 'R2='+str(R2value1), style='italic', fontsize = 15) 
COdep.show()
