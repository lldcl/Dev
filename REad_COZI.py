"""Similar to REad_DAQfactory"""
import pandas as pd
import operator
import numpy as np
import os
import matplotlib.pyplot as plt
import pylab
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

# The path to where the raw files are stored
path = '..\Data\\'
# The date of the data been collected
f_date = '\\201608'
# List all the files in the folder
cal_file = os.listdir(path + f_date + '\DAQfactory_split_files\\')
# The name of the COZI file to be analysed
#cal_file = ['ambientexp2_split_160801_041004', ]

# This bit of code works out which folder the file is in from the name of the file becasue the data is store in folders named 
# following the format YYYYMM depending on when the file was recorded.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
    folder = list(i)[18:22]
    f = '20'+"".join(folder)+'\DAQfactory_split_files\\'+i

#for f in filenames:
    print (f)
#read file into dataframe and call the dataframe data
    data = pd.read_csv(path + f)
	

# 	convert DAQfactory time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
# DAQfactory is the programme we are using to record the data into CSV files.
    data.TheTime = pd.to_datetime(data.TheTime,unit='D')

    T1 = pd.datetime(1899,12,30,0)
    T2 = pd.datetime(1970,1,1,0)
    offset=T1-T2
    data.TheTime+=offset
# Ten second averaging of the raw data
    Time_avg = '10S'
# Make a new copy of the data called mean_resampled 
    mean_resampled = data.copy(deep=True)
    mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
# Set the index to be the time column, when you do this it drops the index, even though it is set to False.
    mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
    mean_resampled = mean_resampled.resample(Time_avg, how = 'mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
    Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
    mean_resampled['MOS1_Av'].to_csv('test.csv',sep='\t', index = False)
    mean_resampled = pd.concat([mean_resampled,Time],axis=1)
# If there are more than one files to be read in together the data_concat function will join them together.
    print ('mean_resampled shape = ',mean_resampled.shape)
    try:
        data_concat = data_concat.append(mean_resampled)
        print (' concatenating')
    except NameError:
        data_concat = mean_resampled.copy(deep=True)
        print (' making data_concat')
		
# Re-make and re-set the index to be the time column for the data_concat dataframe.
T3 = pd.datetime(2015,1,1,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype(int64)
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
    temp = matrix(data_concat[n][1:]) - matrix(data_concat[n][0:-1])
    temp = pd.DataFrame(temp)
    temp = pd.DataFrame.transpose(temp)
    ax1.plot(data_concat.Time[1:],temp,color=c,linewidth=3)
    #ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    pylab.ylim([-0.09,0.09])
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("MOS (V, differentiated)", size=20)
   # plt.ylabel("MOS (V)", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
plt.show()