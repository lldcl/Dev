"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis


path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201512/'

filenames = ['d20151203_06']
# 'd20151123_02','d20151123_03','d20151123_04','d20151123_05','d20151123_06','d20151124_01','d20151124_02','d20151124_04','d20151124_05','d20151124_07','d20151125_01','d20151125_02','d20151125_03','d20151125_04']
#'d20151124_01','d20151124_02','d20151124_04','d20151124_05']
#['d20151123_02','d20151123_03','d20151123_04','d20151123_05','d20151123_06']

for f in filenames:
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

# 	if (RHf == 'Y'):
# 		isop_cyl = 0.00
# 	else:
	isop_cyl = 685.4822	#ppbv
	mfchi_range =2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100.	#sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	dRHdt = pd.Series(np.absolute(mean_resampled.RH1.diff()),name='dRHdt')
	dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
	nm_pts = 60./float(Time_avg[:-1])
	dRH_ctr=0
	for dp in dRHdt:
		if (dp>0.2):
			dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
		dRH_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dRHdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dRHdt_filt],axis=1,join_axes=[mean_resampled.index])

	#filter out periods when RH changes rapidly (dRHdt<0.2)
	mean_resampled = mean_resampled[mean_resampled.dRHdt_filt == 0]

	disopdt = pd.Series(np.absolute(mean_resampled.isop_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>0.1):
			disopdt_filt[disop_ctr:int(disop_ctr+nm_pts)] = 1
		disop_ctr+=1

	mean_resampled = pd.concat([mean_resampled,disopdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,disopdt_filt],axis=1,join_axes=[mean_resampled.index])

	#filter out periods when RH changes rapidly (dRHdt<0.2)
	mean_resampled = mean_resampled[mean_resampled.disopdt_filt == 0]


	
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

# data_concat.dropna()

var = ['RH1','VS','Temp','isop_mr','MOS1','MOS2']+pids

data_concat.index=range(0,len(data_concat.index))
# train_data = pd.concat([data_concat[0:700],data_concat[1600:8500],data_concat[14500:16050],data_concat[16552:18000]])
train_data = pd.concat([data_concat[0:700],data_concat[1000:1350]])
train_data = train_data[var]
train_data.index=range(0,len(train_data.index))
train_data.replace([np.inf, -np.inf], np.nan).dropna(how="all")

test_data = data_concat[701:999]
test_data = test_data[var]
test_data.index=range(0,len(test_data.index))
test_data.dropna()

train_filename = str(path+'/10strain_1203_06.csv')
train_data.to_csv(path_or_buf=train_filename)

test_filename = str(path+'/10stest_1203_06.csv')
test_data.to_csv(path_or_buf=test_filename)

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

Trpidfig = plt.figure()
ax1 = Trpidfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(train_data.index,train_data[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")

Tpidfig = plt.figure()
ax1 = Tpidfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(test_data.index,test_data[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")


#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(4,1,1)
rhax.plot(data_concat.index,data_concat.RH1,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(4,1,2)
isopax.plot(data_concat.index,data_concat.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("Isop / ppbv")

Tax = varfig.add_subplot(4,1,3)
Tax.plot(data_concat.index,data_concat.Temp*100.,color='r',linewidth=3)
Tax.set_ylabel("Temp / oC")

Vax = varfig.add_subplot(4,1,4)
Vax.plot(data_concat.index,data_concat.VS,color='k',linewidth=3)
Vax.set_ylabel("VS / V")

mosfig = plt.figure()
mosax = mosfig.add_subplot(1,1,1)
mosax.plot(data_concat.index,data_concat.MOS1,color='b')
mosax.plot(data_concat.index,data_concat.MOS2,color='r')
mosax.set_ylabel("MOS (V)")


plt.show()
# varfig.show()

