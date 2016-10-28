import os
import pandas as pd
import operator
import numpy as np
import matplotlib.pyplot as plt
import pylab
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

# The path to where the raw files are stored
path = "..\Data\wacl_data\Raw_data_files\\"
f_date = '\\201610'
# The name of the MOS file to be analysed
#cal_file = ['d160902_101257']
cal_file = os.listdir(path + f_date +'\MOS')
if 'desktop.ini' in cal_file:
    cal_file.remove('desktop.ini')

# This bit of code works out which folder the file is in from the name of the file becasue the data is store in folders named 
# following the format YYYYMM depending on when the file was recorded.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
    folder = list(i)[1:5]
    f = '20'+"".join(folder)+'\\'+i

#for f in filenames:
    print (f)
#read file into dataframe and call the dataframe data
    data = pd.read_csv(path+f, error_bad_lines=False, warn_bad_lines=False)
    #data = pd.read_csv(path+f)
	

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
    mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
    Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
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
header = ['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av', 'MOS6_Av','MOS7_Av','MOS8_Av', 'HIH1_Av', 'LM65T1_Av','SV_Av']
#data_concat.to_csv('test.csv', index = False, columns = header)
data_concat.to_csv('test.csv', columns = header)

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)
# Returns the initial date and time that the file began
print(data_concat.Time[0])
print(data_concat.Time[len(data_concat.Time)-1])
#for v, h, n in zip(data_concat['SV_Av'], data_concat['HIH1_Av'], range(1,len(data_concat['SV_Av']))):
#    print( v * (0.0062 * h + 0.16))
#temp.to_csv('v_out.csv')
