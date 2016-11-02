"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis


path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201603/'

filenames = ['d20160324_01']		
for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

	#dT = seconds since file start
	dT = data.TheTime-data.TheTime[0]
	dT*=60.*60.*24.
	T_int = data.TheTime
	T_int.name='T_int'
	data = pd.concat([data,T_int],axis=1)


	#convert daqfac time into real time pd.datetime object
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	isop_cyl = 40000	#ppbv
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
	nm_pts = 240./float(Time_avg[:-1])
# 	dRH_ctr=0
# 	for dp in dRHdt:
# 		if (dp>0.2):
# 			dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
# 		dRH_ctr+=1
# 
# 	mean_resampled = pd.concat([mean_resampled,dRHdt],axis=1,join_axes=[mean_resampled.index])
# 	mean_resampled = pd.concat([mean_resampled,dRHdt_filt],axis=1,join_axes=[mean_resampled.index])
# 
# 	#filter out periods when RH changes rapidly (dRHdt<0.2)
# 	mean_resampled = mean_resampled[mean_resampled.dRHdt_filt == 0]

	disopdt = pd.Series(np.absolute(mean_resampled.isop_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>1.):
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

data_concat.dropna()

var = ['RH1','VS','Temp','isop_mr','MOS1','MOS2','T_int']

data_concat = data_concat[var]
data_concat.index=range(0,len(data_concat.index))

train_data = pd.concat([data_concat[0:799],data_concat[1200:]],axis=0)
train_data.index=range(0,len(train_data.index))

test_data = data_concat[800:1200]
test_data.index=range(0,len(test_data.index))

train_filename = str(path+'/30strain_100216_1.csv')
train_data.to_csv(path_or_buf=train_filename)

test_filename = str(path+'/30stest_100216_1.csv')
test_data.to_csv(path_or_buf=test_filename)

################################################
#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(5,1,1)
rhax.plot(data_concat.index,data_concat.RH1,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(5,1,2)
isopax.plot(data_concat.index,data_concat.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("VOC / ppbv")

Tax = varfig.add_subplot(5,1,3)
Tax.plot(data_concat.index,data_concat.Temp*100.,color='r',linewidth=3)
Tax.set_ylabel("Temp / oC")

Vax = varfig.add_subplot(5,1,4)
Vax.plot(data_concat.index,data_concat.VS,color='k',linewidth=3)
Vax.set_ylabel("VS / V")

MOSax = varfig.add_subplot(5,1,5)
MOSax.plot(data_concat.index,data_concat.MOS1,color='b',linewidth=3)
MOSax.plot(data_concat.index,data_concat.MOS2,color='r',linewidth=3)
MOSax.set_ylabel("MOS / V")

plt.show()

#plot up other variables
trainfig = plt.figure()

rhax = trainfig.add_subplot(5,1,1)
rhax.plot(train_data.index,train_data.RH1,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = trainfig.add_subplot(5,1,2)
isopax.plot(train_data.index,train_data.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("VOC / ppbv")

Tax = trainfig.add_subplot(5,1,3)
Tax.plot(train_data.index,train_data.Temp*100.,color='r',linewidth=3)
Tax.set_ylabel("Temp / oC")

Vax = trainfig.add_subplot(5,1,4)
Vax.plot(train_data.index,train_data.VS,color='k',linewidth=3)
Vax.set_ylabel("VS / V")

MOSax = trainfig.add_subplot(5,1,5)
MOSax.plot(train_data.index,train_data.MOS1,color='b',linewidth=3)
MOSax.plot(train_data.index,train_data.MOS2,color='r',linewidth=3)
MOSax.set_ylabel("MOS / V")

plt.show()

#plot up other variables
testfig = plt.figure()

rhax = testfig.add_subplot(5,1,1)
rhax.plot(test_data.index,test_data.RH1,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = testfig.add_subplot(5,1,2)
isopax.plot(test_data.index,test_data.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("VOC / ppbv")

Tax = testfig.add_subplot(5,1,3)
Tax.plot(test_data.index,test_data.Temp*100.,color='r',linewidth=3)
Tax.set_ylabel("Temp / oC")

Vax = testfig.add_subplot(5,1,4)
Vax.plot(test_data.index,test_data.VS,color='k',linewidth=3)
Vax.set_ylabel("VS / V")

MOSax = testfig.add_subplot(5,1,5)
MOSax.plot(test_data.index,test_data.MOS1,color='b',linewidth=3)
MOSax.plot(test_data.index,test_data.MOS2,color='r',linewidth=3)
MOSax.set_ylabel("MOS / V")

plt.show()

