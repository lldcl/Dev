import pandas as pd
import matplotlib.pyplot as plt

# Data file from sensors - DAQfactory txt file
path2 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/'

cal_file = ['mos_data_081616_02.txt','mos_data_081616_03.txt']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	f = "".join(path2)+i
#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(f)
	

# 	convert daqfac time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')

	T1 = pd.datetime(1970,01,01,2,20,0)
	T2 = pd.datetime(1970,01,01,0,0,15)
	offset=T1-T2
	data.TheTime+=offset
# Ten second averaging of the raw data
# 	Time_avg = '0S'
# Make a new copy of the data called mean_resampled 
	mean_resampled = data.copy(deep=True)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
#Set the index to be the time column, when you do this it drops the index, even though it is set to False.
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
# 	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
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

print data_concat.TheTime[0]
#read file into dataframe

# Turn the time into a number:
new_time = pd.to_datetime(data_concat.Time)

#plot up the MOS voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Sensor_ave,color="green",linewidth=3)
ax1.set_ylabel("MOS voltage (V)")
ax1.set_xlabel("Time")


"""
# plot an overall chart
compare = plt.figure("MOS vs MS data")
ax1 = compare.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data.Sensor_ave, color="green", linewidth =3)
ax2.plot(mydf.Date_and_time, mydf.TIC, color="navy", linewidth = 3)
ax2.plot(mydf3.Date_and_time, mydf3.TIC, color = "royalblue")
ax2.plot(mydf4.Date_and_time, mydf4.TIC, color = "cornflowerblue")
ax2.plot(mydf5.Date_and_time, mydf5.TIC, color = "skyblue")
ax2.plot(mydf6.Date_and_time, mydf6.TIC, color = "teal")
ax2.plot(mydf6.Date_and_time, mydf6.TIC, color = "blue")
ax1.set_xlabel("Time", size=18)
ax1.set_ylabel("MOS voltage (V)", size=18)
ax2.set_ylabel("TIC MS intensity", size=18)
plt.title( filename2, size = 20)
# """
# compare.show()
plt.show()
