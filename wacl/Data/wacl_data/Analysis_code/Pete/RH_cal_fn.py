"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
import datetime
import scipy.odr as odr


def RH_cal_fn(path,filename,Time_avg):
	print 'RH cal file = ',filename

	#read file into dataframe
	data = pd.read_csv(path+filename)

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

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH = (((mean_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*10.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

	std_resampled = data.copy(deep=True)
	std_resampled.RH = (((std_resampled.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*std_resampled.Temp*10.)
	std_resampled.TheTime = pd.to_datetime(std_resampled.TheTime,unit='L')
	std_resampled = std_resampled.set_index(std_resampled.TheTime,drop=True)
	std_resampled = std_resampled.resample(Time_avg, how='std',fill_method='pad')

	dRHdt = pd.Series(np.absolute(mean_resampled.RH.diff()),name='dRHdt')
	dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
	nm_pts = 120./float(Time_avg[:-1])
	dRH_ctr=0
	for dp in dRHdt:
		if (dp>0.15):
			dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
		dRH_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dRHdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dRHdt_filt],axis=1,join_axes=[mean_resampled.index])
	std_resampled = pd.concat([std_resampled,dRHdt],axis=1,join_axes=[std_resampled.index])

	#filter out periods when RH changes rapidly (dRHdt<0.2)
	mean_dRHdt_filt = mean_resampled[mean_resampled.dRHdt_filt == 0]
	std_dRHdt_filt = std_resampled[mean_resampled.dRHdt_filt == 0]


	#Returns a Linear Fit
	def linear_fit(params, x):
		return ((params[0]*x)+params[1])    

	linear = odr.Model(linear_fit)

# 	RH_cal_fits = pd.DataFrame(index=['Slope (mV/%)','Slope_err','Intercept (mV)','Intercept_err','RH_min','RH_max','RH_mean','RH_median'],columns=pids)
	filtRH_cal_fits = pd.DataFrame(index=['Slope (mV/%)','Slope_err','Intercept (mV)','Intercept_err','RH_min','RH_max','RH_mean','RH_median'],columns=pids)


	#####Plots############
	colors = ["red", "blue" , "green", "orange", "purple"]
# 	pidfig_resample = plt.figure()
# 	ctr = 1
# 	for p,c in zip(pids,colors):
# 		sfig = 'pax'+str(ctr)
# 		sfig = pidfig_resample.add_subplot(len(pids),1,ctr)
# 		sfig.errorbar(mean_resampled.index,mean_resampled[p]*1e3, yerr = std_resampled[p],color=c)
# 	# 	sfig.plot(mean_resampled.index,mean_resampled[p],color=c)
# 		sfig.set_ylabel(p+' / mV')
# 		sfig.set_xlabel("Time")
# 		sfig.set_ylim([np.min(mean_resampled[p])*1e3,(np.min(mean_resampled[p])*1e3)+0.5])
# 		ax2 = sfig.twinx()
# 		ax2.errorbar(mean_resampled.index,mean_resampled.RH, yerr = std_resampled.RH,color='k')
# 	#	ax2.plot(mean_resampled.index,RH, linewidth=3,color='k')
# 		plt.ylabel("RH / %")
# 		ctr+=1
# 	pidfig_resample.show()
# 
# 	rhcalfig = plt.figure()
# 	ctr = 1
# 	for p,c in zip(pids,colors):
# 		fit_data = odr.RealData(x = mean_resampled.RH,y = mean_resampled[p]*1e3,sx = std_resampled.RH ,sy = std_resampled[p]*1e3)
# 		fit = odr.ODR(fit_data,linear,[5e-5,0.05])
# 		fit_params = fit.run()
# 		RH_cal_fits[p] = [fit_params.beta[0],fit_params.sd_beta[0],fit_params.beta[1],fit_params.sd_beta[1]]
# 
# 		rfig = 'pax'+str(ctr)
# 		rfig = rhcalfig.add_subplot(len(pids),1,ctr)
# 		rfig.plot(mean_resampled.RH,mean_resampled[p]*1e3,'o',color=c)
# 		rfig.plot([np.min(mean_resampled.RH),np.max(mean_resampled.RH)],[(fit_params.beta[0]*np.min(mean_resampled.RH))+fit_params.beta[1],(fit_params.beta[0]*np.max(mean_resampled.RH))+fit_params.beta[1]],color='k')
# 		rfig.set_ylabel(p+' / mV')
# 		rfig.set_xlabel("RH / %")
# 		ctr+=1
# 	rhcalfig.show()

	rhcalfig2 = plt.figure()
	ctr = 1
	import matplotlib.cm as cm
	c=mean_dRHdt_filt.index.dayofyear+(mean_dRHdt_filt.index.hour/24.)+(mean_dRHdt_filt.index.minute/(24.*60.))
	c = (c-np.min(c))/np.max(c-np.min(c))

	#for p,c in zip(pids,colors):
	for p in pids:
		fit_data = odr.RealData(x = mean_dRHdt_filt.RH,y = mean_dRHdt_filt[p]*1e3,sx = std_dRHdt_filt.RH ,sy = std_dRHdt_filt[p]*1e3)
		fit = odr.ODR(fit_data,linear,[5e-5,0.05])
		fit_params = fit.run()
		filtRH_cal_fits[p] = [fit_params.beta[0],fit_params.sd_beta[0],fit_params.beta[1],fit_params.sd_beta[1],np.min(mean_dRHdt_filt.RH),np.max(mean_dRHdt_filt.RH),np.mean(mean_dRHdt_filt.RH),np.median(mean_dRHdt_filt.RH)]

		rfig2 = 'pax'+str(ctr)
		rfig2 = rhcalfig2.add_subplot(len(pids),1,ctr)
	# 	rfig2.plot(mean_dRHdt_filt.RH,mean_dRHdt_filt[p]*1e3,'o',color=c)
		rfig2.scatter(mean_dRHdt_filt.RH,mean_dRHdt_filt[p]*1e3,color=cm.jet(c))
		rfig2.plot([np.min(mean_dRHdt_filt.RH),np.max(mean_dRHdt_filt.RH)],[(fit_params.beta[0]*np.min(mean_dRHdt_filt.RH))+fit_params.beta[1],(fit_params.beta[0]*np.max(mean_dRHdt_filt.RH))+fit_params.beta[1]],color='k')
		rfig2.set_ylabel(p+' / mV')
		rfig2.set_xlabel("RH / %")
		rfig2.set_title(filename)
		ctr+=1
	rhcalfig2.show()

	rh_diffplt = plt.figure()
	rhdax = rh_diffplt.add_subplot(1,1,1)
	rhdax.plot(mean_resampled.index,dRHdt,color='k',linewidth=3)
	rhdax.plot(mean_resampled.index,dRHdt_filt,color='b',linewidth=3)
	rhdax.set_ylabel("dRH/dt")
	rhdax.set_title(filename)
	rh_diffplt.show()

# 	mfc_plt = plt.figure()
# 	mfcax = mfc_plt.add_subplot(1,1,1)
# 	net_flow = ((mean_resampled.mfchiR/5.)*2000.)+((mean_resampled.mfcmidR/5.)*100.)
# 	mfcax.plot(mean_resampled.index,(mean_resampled.mfchiR/5.)*2000.,color='b',linewidth=3)
# 	mfcax.plot(mean_resampled.index,(mean_resampled.mfcmidR/5.)*100.,color='r',linewidth=3)
# 	mfcax.plot(mean_resampled.index,net_flow,color='k',linewidth=3)
# 	mfcax.set_ylabel("net flow / sccm")
# 	mfc_plt.show()

	RH_corr_df = mean_dRHdt_filt.copy(deep=True)

	corr_plt = plt.figure()
	ctr = 1
	for p,c in zip(pids,colors):

		RH_corr_df[p] = mean_dRHdt_filt[p]*1e3-(filtRH_cal_fits[p][0]*mean_dRHdt_filt.RH)


		corrfig2 = corr_plt.add_subplot(len(pids),1,ctr)
		corrfig2.errorbar(RH_corr_df.index,RH_corr_df[p],color=c, yerr = std_dRHdt_filt[p])
		corrfig2.set_ylabel(p+' / mV')
		corrfig2.set_xlabel("Time")
		corrfig2.set_title(filename)
		corrfig2.set_ylim([np.min(RH_corr_df[p]),(np.min(RH_corr_df[p]))+0.5])

		ctr+=1
	corr_plt.show()


	return (filtRH_cal_fits,mean_dRHdt_filt)