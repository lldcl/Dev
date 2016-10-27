"""Find the proper data frames from COZI, QCL and DAQ that can be used for comparison"""
import pandas as pd
import operator
import numpy as np
import os
import matplotlib.pyplot as plt
import pylab
import glob
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

# The path to where the raw files are stored
path = 'D:/WACL/data/wacl_data/Raw_data_files/'
# The date of the data been collected
f_date = '201609'
# List all the files in the folder
cal_file_DAQfactory = os.listdir(path + f_date +'/MOS')
cal_file_QCL = os.listdir(path + f_date + '/QCL')
cal_file_COZI = os.listdir(path + f_date + '/COZI')
if 'desktop.ini' in cal_file_DAQfactory:
    cal_file_DAQfactory.remove('desktop.ini')
if 'desktop.ini' in cal_file_COZI:
    cal_file_COZI.remove('desktop.ini')
if 'desktop.ini' in cal_file_QCL:
    cal_file_QCL.remove('desktop.ini')
    cal_file_QCL.remove('txt')

#Define function to find the overlaped time from DAQ, QCL and COZI data
def overlaped(a, b, c):
    Overlaped_data = set(a).intersection(b, c)
    if Overlaped_data:
        return Overlaped_data
    else:
        print("Unable to find overlaped part")
        return bool(Overlaped_data)

for i in cal_file_DAQfactory:
# Pick out characters 18 to 21 to correspond to the filename.
    folder = list(i)[1:5]
    f = '20'+"".join(folder) + '/' +i

#for f in filenames:
    print (f)
#read file into dataframe and call the dataframe data
    data = pd.read_csv(path+f, error_bad_lines=False, warn_bad_lines=False)
	

# convert DAQfactory time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
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
    mean_resampled['MOS1_Av'].to_csv('test.csv',sep='\t', index = False)
    mean_resampled = pd.concat([mean_resampled,Time],axis=1)
# If there are more than one files to be read in together the DAQ function will join them together.
    print ('mean_resampled shape = ',mean_resampled.shape)
    try:
        DAQ = DAQ.append(mean_resampled)
        print (' concatenating')
    except NameError:
        DAQ = mean_resampled.copy(deep=True)
        print (' making DAQ')
		
# Re-make and re-set the index to be the time column for the DAQ dataframe.
T3 = pd.datetime(2015,1,1,0)
dt = pd.Series((DAQ.index - T3),index=DAQ.index,name='dt')
dt = dt.astype(int64)
DAQ = pd.concat([DAQ,dt],axis=1,join_axes=[DAQ.index])
stat = 'Y'

newindex = pd.Series(range(0,DAQ.shape[0]))
DAQ = DAQ.set_index(newindex)
# Returns the initial date and time that the file began
print(DAQ.Time[0])
print(DAQ.Time[len(DAQ.Time)-1])

# This bit of code works out which folder the file is in from the name of the file becasue the data is store in folders named 
# following the format YYYYMM depending on when the file was recorded.
for i in cal_file_QCL:
    folder = list(i)[3:9]
    g = ''.join(folder)+'/QCL/'+i

#for f in filenames:
    print (g)
#read file into dataframe
    QCL = pd.read_csv(path+g)

# convert daqfac time into real time pd.datetime object
    QCL.TheTime = pd.to_datetime(QCL.TheTime,unit='s')

    T1 = pd.datetime(1904,1,1,0)
    T2 = pd.datetime(1970,1,1,0)
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

#Read in the COZI files and add on time index
for i in cal_file_COZI:
# Pick out characters 18 to 21 to correspond to the filename.
    folder = list(i)[13:17]
    f = '20'+"".join(folder)+'/COZI/'+i

#for f in filenames:
    print (f)
#read file into dataframe and call the dataframe data
    data = pd.read_csv(path+f)
	
# convert DAQfactory time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
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
# If there are more than one files to be read in together the COZI function will join them together.
    print ('mean_resampled shape = ',mean_resampled.shape)
    try:
        COZI = COZI.append(mean_resampled)
        print (' concatenating')
    except NameError:
        COZI = mean_resampled.copy(deep=True)
        print (' making COZI')
		
# Re-make and re-set the index to be the time column for the COZI dataframe.
T3 = pd.datetime(2015,1,1,0)
dt = pd.Series((COZI.index - T3),index=COZI.index,name='dt')
dt = dt.astype(int64)
COZI = pd.concat([COZI,dt],axis=1,join_axes=[COZI.index])
stat = 'Y'

newindex = pd.Series(range(0,COZI.shape[0]))
COZI = COZI.set_index(newindex)
# Returns the initial date and time that the file began
print(COZI.Time[0])
print(COZI.Time[len(COZI.Time)-1])
COZI['Time'].to_csv('cozi.csv',sep='\t', index = False)
DAQ['Time'].to_csv('daq.csv',sep='\t', index = False)
QCL['Time'].to_csv('qcl.csv',sep='\t', index = False)
DAQ_time = DAQ.Time
COZI_time = COZI.Time
QCL_time = QCL.Time

result = overlaped(DAQ_time, COZI_time, QCL_time)
print (result)