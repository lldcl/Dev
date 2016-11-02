import pandas as pd
import numpy as np
from scipy import stats
from matplotlib.offsetbox import AnchoredText


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160324_01']


for i in cal_file:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

	#dT = seconds since file start
	dT = data.TheTime-data.TheTime[0]
	dT*=60.*60.*24.

	#convert daqfac time into real time pd.datetime object
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
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
#'timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])

data_concat['Temperature'] = (data_concat.Temp*100)

'''How to make a CSV file in python. First a new dataframe must be made, and in this case it is called marvdata. Then you must specify which dataframe you want the data from 
here it is (data_concat), followed by the index you want for the new dataframe (here I want the index to be the same as it was for the previous daaframe, which was th time 
and date) and finally the columns you want to copy into the new dataframe( this was RH1 and Temp here). The copy = True part tells you that a copy of the data will be made
and any subsequent changes to the reference data will NOT be changed in the copy, unless the code is run again.
'''
marvdata = pd.DataFrame(data_concat,data_concat.index,columns=['RH1','Temp'],copy=True)

'''This section tells the code to transform the new dataframe into a CSV file (which will open as an Excel file by default). The action command is the to_csv bit and the 
pink bit in the brackets is the new filename. This file can then be found in the same folder as the code. It can be moved afterwards if this is not good.'''
marvdata.to_csv('d20160324_01.csv')





