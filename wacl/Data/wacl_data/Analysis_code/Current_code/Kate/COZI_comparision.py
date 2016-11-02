"""Analysing DACCIWA MOS files"""

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
cal_file = ['ambientexp2_split_160812_040033','ambientexp2_split_160813_031451','ambientexp2_split_160814_022915','ambientexp2_split_160815_014338']

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
ax1.plot(data_concat.Time, data_concat.RH1_Av, color="blue", label="RH 1 (%)")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green",linewidth = 3, label="Median MOS")
ax1.set_ylabel("Temperature (oC) and RH (%)",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=1)
ax2.legend(loc=2)
Variables.show()


##########################################################################################
# Call the other sensors data file, from the COZI lab.
# The path to the COZI files
path1 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
# The name of the MOS file to be analysed
cal_file1 = ['logging_1min_160811_152954b']

# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file1:
	folder = list(i)[13:17]
	g = '20'+"".join(folder)+'/COZI/'+i

#for f in filenames:
	print g
	#read file into dataframe
	cozi = pd.read_csv(path1+g)

# 	convert daqfac time into real time pd.datetime object
	cozi.TheTime = pd.to_datetime(cozi.TheTime,unit='D')

	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	cozi.TheTime+=offset
# Time average the COZI data every ten seconds
Time_avg = '10S'
 
 # Set the index to be the date and time.
COZI = cozi.copy(deep=True)
COZI.TheTime = pd.to_datetime(COZI.TheTime,unit='L')
COZI = COZI.set_index(COZI.TheTime,drop=True)
COZI = COZI.resample(Time_avg, how='mean',fill_method='pad')
Time = pd.Series(COZI.index,name='Time', index=COZI.index)
COZI = pd.concat([COZI,Time],axis=1)

print( COZI.Time[0])
print(COZI.Time[len(COZI.Time)-1])
# Plot up the variables from the COZI files.

Ozone=['O3_tei_cal_out', 'O3_1', 'O3_3', 'O3_5', 'O3_6', 'O3_7','o3_guest_1']

#plot up the ozone data
ozone = plt.figure("Ozone COZI data")
ax1 = ozone.add_subplot(111)
colors = ["darkblue","royalblue", "skyblue","purple", "blue", "violet", "purple"]
for n,c in zip(Ozone,colors):
	ax1.plot(COZI.Time,COZI[n],color=c,linewidth=3)
	plt.legend(Ozone, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("COZI oxzone (ppb)", size=16)
	plt.xlabel("Time", size=16)	
ozone.show()	

# Plot up the NOX data from the COZI lab. 

NOx = ['NO', 'NO2', 'NO2_caps']

# Plot up the NOx data
Nitrogen = plt.figure("NOx COZI data")
ax1 = Nitrogen.add_subplot(211)

colors = ["lightgreen","green", "darkgreen",]
for p,q in zip(NOx,colors):
	ax1.plot(COZI.Time,COZI[p],color=q,linewidth=3)
	plt.legend(NOx, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("COZI NOx data", size=16)
	plt.xlabel("Time", size=16)	
Nitrogen.show()	

##########################################################################################
# Comparing MOS and COZI ozone and NO2 data - not expecting huge correlations
# Crete a new dataframe called dataframe using the two previous dataframes based on the Time column. Both 
# must have time in the same format under a column called Time.

dataframe = COZI.merge( data_concat , on = "Time" )

# Then chose only the relevant columns for the comparison so not working with tonnes of data.
dataframe = dataframe[["Time","Median_MOS_signal","O3_1",'NO2_caps']]

comparing = plt.figure()
ax1 = comparing.add_subplot(211)
ax3 = ax1.twinx()
ax2 = comparing.add_subplot(212)
ax1.plot(dataframe.Time, dataframe.Median_MOS_signal , color = "black")
ax3.plot( dataframe.Time, dataframe.O3_1 , color = "blue")
ax2.scatter( dataframe.O3_1, dataframe.Median_MOS_signal , color = "blue")
ax1.set_xlabel("Time", size =18)
ax1.set_ylabel("Median MOS signal (V)", size =18)
ax3.set_ylabel("Ozone (ppb)", size=18)
ax2.set_xlabel(" COZI Ozone / ppb", size =18)
ax2.set_ylabel("Median MOS signal (V)", size =18)
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(dataframe.O3_1, dataframe.Median_MOS_signal)
ax2.plot([np.min(dataframe.O3_1), np.max(dataframe.O3_1)], [(slope1*np.min(dataframe.O3_1))+intercept1, (slope1*np.max(dataframe.O3_1))+intercept1])
# Get the linear regression paramenters to have 3 sig figs.
slope1 = ("%.3g" %slope1)
intercept1 = ("%.3g" % (intercept1))
R2value1 = ("%.3g" % (R2value1))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax2.text(5,1.2,'y = ' +str(slope1)+'x +' +str(intercept1)+ '  R2='+str(R2value1), style='italic', fontsize = 18) 
ax1.tick_params(labelsize =18 )
ax2.tick_params(labelsize =18 )
ax3.tick_params(labelsize =18 )

NO2_plot = plt.figure()
ax1 = NO2_plot.add_subplot(211)
ax3 = ax1.twinx()
ax2 = NO2_plot.add_subplot(212)
ax1.plot(dataframe.Time, dataframe.Median_MOS_signal , color = "black")
ax3.plot( dataframe.Time, dataframe.NO2_caps , color = "green")
ax2.scatter( dataframe.NO2_caps, dataframe.Median_MOS_signal , color = "green")
ax1.set_xlabel("Time", size =18)
ax1.set_ylabel("Median MOS signal (V)", size =18)
ax3.set_ylabel("NO2 (ppb)",size=18)
ax2.set_xlabel(" COZI NO2 / ppb", size =18)
ax2.set_ylabel("Median MOS signal (V)", size =18)
ax1.tick_params(labelsize =18 )
ax2.tick_params(labelsize =18 )
ax3.tick_params(labelsize =18 )
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(dataframe.NO2_caps, dataframe.Median_MOS_signal)
ax2.plot([np.min(dataframe.NO2_caps), np.max(dataframe.NO2_caps)], [(slope2*np.min(dataframe.NO2_caps))+intercept2, (slope2*np.max(dataframe.NO2_caps))+intercept2])
# Get the linear regression paramenters to have 3 sig figs.
slope2 = ("%.3g" %slope2)
intercept2 = ("%.3g" % (intercept2))
R2value2 = ("%.3g" % (R2value2))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax2.text(1,1.2,'y = ' +str(slope2)+'x +' +str(intercept2)+ '  R2='+str(R2value2), style='italic', fontsize = 18) 
plt.show()