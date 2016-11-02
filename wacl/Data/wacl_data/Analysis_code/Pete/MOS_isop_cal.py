"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201512/'


################### function to calculate bg
def baseline_cor(filenames):

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
	# dt = pd.Series((data_concat.index - data_concat.index[0]),index=data_concat.index,name='dt')
	dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
	dt = dt.astype('timedelta64[s]')
	data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])

	mosdf = pd.concat([data_concat.dt,data_concat.MOS1,data_concat.MOS2,data_concat.RH2],axis=1)
	mosdf = mosdf.dropna()
	x_var = ['RH2','dt']
	x_train = mosdf[x_var]
	y_train = mosdf.MOS1

	linear_MOS1 = linear_model.LinearRegression()
	linear_MOS1.fit(x_train, y_train)
	linear_MOS1.score(x_train, y_train)
# 	print 'MOS1'
# 	print('Coefficient: \n', linear_MOS1.coef_)
# 	print('Intercept: \n', linear_MOS1.intercept_)
# 	MOS1_pred = linear_MOS1.predict(x_train)

	y_train = mosdf.MOS2
	linear_MOS2 = linear_model.LinearRegression()
	linear_MOS2.fit(x_train, y_train)
	linear_MOS2.score(x_train, y_train)
# 	print 'MOS2'
# 	print('Coefficient: \n', linear_MOS2.coef_)
# 	print('Intercept: \n', linear_MOS2.intercept_)
# 	MOS2_pred = linear_MOS2.predict(x_train)


# Plots
# 	mosfig = plt.figure()
# 	mos1ax = mosfig.add_subplot(2,1,1)
# 	mos1ax.plot(mosdf.dt,mosdf.MOS1,color='b',marker='o')
# 	mos1ax.plot(mosdf.dt,MOS1_pred)
# 	mos1ax.set_ylabel("MOS1 (V)")
# 
# 	mos1ax = mosfig.add_subplot(2,1,2)
# 	mos1ax.plot(mosdf.dt,mosdf.MOS2,color='r',marker='o')
# 	mos1ax.plot(mosdf.dt,MOS2_pred)
# 	mos1ax.set_ylabel("MOS2 (V)")
# 	plt.show()
	
	return(linear_MOS1.coef_,linear_MOS2.coef_,linear_MOS1.intercept_,linear_MOS2.intercept_)

#################################

baseline_file = ['d20151208_04']
a1,a2,b1,b2 = baseline_cor(baseline_file)

cal_file = ['d20151208_03']

for f in cal_file:
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

	#filter out periods when isop changes rapidly (disopdt<0.1) and for 300 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	disopdt = pd.Series(np.absolute(mean_resampled.isop_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>0.1):
			disopdt_filt[disop_ctr:int(disop_ctr+nm_pts)] = 1
		disop_ctr+=1

	mean_resampled = pd.concat([mean_resampled,disopdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,disopdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.disopdt_filt == 0]

# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

T3 = pd.datetime(2015,01,01,0)
# dt = pd.Series((data_concat.index - data_concat.index[0]),index=data_concat.index,name='dt')
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])

MOS1_cor = data_concat.MOS1-((a1[0]*data_concat.RH2)+(a1[1]*data_concat.dt)+b1)
MOS2_cor = data_concat.MOS2-((a2[0]*data_concat.RH2)+(a2[1]*data_concat.dt)+b2)

cor1fig = plt.figure()
cor1ax = cor1fig.add_subplot(2,1,1)
cor1ax.plot(data_concat.dt,data_concat.MOS1,color='b',marker='o')
cor1ax.set_ylabel("MOS1 (V)")
cor1ax = cor1fig.add_subplot(2,1,2)
cor1ax.plot(data_concat.dt,MOS1_cor,color='k',marker='o')
cor1ax.set_ylabel("MOS1 (V)")

cor2fig = plt.figure()
cor2ax = cor2fig.add_subplot(2,1,1)
cor2ax.plot(data_concat.dt,data_concat.MOS2,color='r',marker='o')
cor2ax.set_ylabel("MOS2 (V)")
cor2ax = cor2fig.add_subplot(2,1,2)
cor2ax.plot(data_concat.dt,MOS2_cor,color='k',marker='o')
cor2ax.set_ylabel("MOS2 (V)")


plt.show()

