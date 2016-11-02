# Reading the QCL files from Jim. These record methane, methanol and ethane.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText
import csv

# Call the other sensors data file, from the GC lab.
# The path to the QCL file
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
# The name of the MOS file to be analysed
cal_file = ['QCL20161006.csv','QCL20161008.csv','QCL20161009.csv','QCL20161010.csv','QCL20161011.csv',]


# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
	folder = list(i)[3:9]
	g = ''.join(folder)+'/QCL/'+i

#for f in filenames:
	print g
	#read file into dataframe
	QCL = pd.read_csv(path+g)

# 	convert daqfac time into real time pd.datetime object
	QCL.TheTime = pd.to_datetime(QCL.TheTime,unit='s')

	T1 = pd.datetime(1904,01,01,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	QCL.TheTime+=offset

# Set the index to be the date and time.
QCL = QCL.copy(deep=True)
QCL.TheTime = pd.to_datetime(QCL.TheTime,unit='L')
QCL = QCL.set_index(QCL.TheTime,drop=True)
Time = pd.Series(QCL.index,name='Time', index=QCL.index)
QCL = pd.concat([QCL,Time],axis=1)

print( QCL.Time[0])
print(QCL.Time[len(QCL.Time)-1])
#######################################################################
# The path to where the raw files are stored
path1 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

# The name of the MOS file to be analysed
cal_file1 = ['d161006_114307','d161007_084204','d161007_163350','d161008_211106','d161010_014753','d161010_083516','d161011_084534',]
#cal_file1 = ['d160913_092635','d160928_103119','d160928_161841','d160929_074207','d160929_093719','d160929_143317','d160930_140157','d161003_084630','d161003_180949']
# This bit of code works out which folder the file is in from the name of the file becasue the data is store in folders named 
# following the format YYYYMM depending on when the file was recorded.
for i in cal_file1:
# Pick out characters 18 to 21 to correspond to the filename.
	folder = list(i)[1:5]
	f = '20'+"".join(folder)+'/'+i

	print f
#read file into dataframe and call the dataframe data
	data = pd.read_csv(path1+f)
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
data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']].median(axis=1)
#data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
# Plot the median MOS signal with temperature, over time.
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green", linewidth=5, label="MOS")
ax2.plot(data_concat.Time, data_concat.HIH1_Av, color="pink", label="Temp 2 (oC)")
ax1.set_ylabel("Median MOS signal (V)")
ax1.set_xlabel("Time")
ax2.set_ylabel("Temperature")
median.show()

# Plot up temperature and humidity which are recorded in the same air flow as the MOS.
Variables = plt.figure("Temp and humidity")
ax1 = Variables.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.HIH1_Av, color="red", label="Temp 1 (oC)")
ax1.plot(data_concat.Time, data_concat.LM65T1_Av, color="blue", label="RH 1 (%)")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green",linewidth = 3, label="Median MOS")
ax1.set_ylabel("Temperature (oC) and RH (%)",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=1)
ax2.legend(loc=2)
Variables.show()

#######################################################################
# Merge these two dataframes so they can be plotted together.s

Merged = QCL.merge(data_concat, on = "Time" )

# Then chose only the relevant columns for the comparison so not working with tonnes of data.
Merged = Merged[["Time","Median_MOS_signal",'C2H6','CH4','CH3OH','CH4_A']]
low_methane = Merged[Merged.CH4 > 1500]
comparing = plt.figure()
ax1 = comparing.add_subplot(111)
ax3 = ax1.twinx()
ax1.plot(Merged.Time, Merged.Median_MOS_signal , color = "black")
ax3.plot( Merged.Time, Merged.C2H6 , color = "blue", label="Ethane")
ax3.plot( low_methane.Time, low_methane.CH4 , color = "orange", label="Methane")
ax3.plot( Merged.Time, Merged.CH3OH , color = "green", label="Methanol")
ax1.set_xlabel("Time", size =18)
ax1.set_ylabel("Median MOS signal (V)", size =18)
ax3.set_ylabel("VOCs", size=18)
ax1.tick_params(labelsize = 18 )
ax3.tick_params(labelsize = 18 )
ax3.legend()

Merged["Total_VOC"] = Merged[['C2H6','CH4','CH3OH']].sum(axis=1)
del_lows = Merged[Merged.Total_VOC > 1500]

total = plt.figure("Total VOC against Median MOS")
ax1 = total.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(Merged.Time, Merged.Median_MOS_signal,color="green")
ax2.plot(del_lows.Time, del_lows.Total_VOC, color="purple")
ax1.set_ylabel("Median MOS (V)")
ax2.set_ylabel(" Total QCL VOC")
ax1.set_xlabel("Time")
plt.show()


