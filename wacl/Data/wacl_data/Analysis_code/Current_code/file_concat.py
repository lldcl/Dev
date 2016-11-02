"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis


path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201510/'

filenames = ['d20151021_01','d20151021_02','d20151021_03','d20151021_04','d20151021_05']
#'d20151019_04','d20151020_01','d20151020_02','d20151020_03','d20151020_04','d20151021_01']
#['d20151013_01','d20151013_02','d20151013_03','d20151013_04','d20151014_02','d20151014_03','d20151014_04','d20151015_01b','d20151015_02','d20151015_03','d20151016_02']
RH_file =['N','N','N','N','N']
#['Y','Y','Y','Y','N','N','N','N','N','N','N']


for f,RHf in zip(filenames,RH_file):
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

	#find all pids in file
	sub = 'pid'
	pids = [s for s in data.columns if sub in s]

	if (RHf == 'Y'):
		isop_cyl = 0.00
	else:
		isop_cyl = 1100.	#13.277	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)

	Time_avg = '30S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH = (((mean_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*10.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

concat_filename = str(path+'30sconcat_1021.csv')
data_concat.to_csv(path_or_buf=concat_filename)

################################################
#plot up the pid voltages
pidfig = plt.figure()
ax1 = pidfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(data_concat.index,data_concat[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")
plt.show()

#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(3,1,1)
rhax.plot(data_concat.index,data_concat.RH,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(3,1,2)
isopax.plot(data_concat.index,data_concat.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("Isop / ppbv")

varfig.show()

