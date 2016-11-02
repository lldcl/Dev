"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
import datetime
import scipy.odr as odr

#Returns a Linear Fit
def linear_fit(params, x):
    return ((params[0]*x)+params[1])    

linear = odr.Model(linear_fit)

###################################

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'

filename = '201511/d20151103_04'

print filename
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

#data=data[100000:600000]

isop_cyl = 723.	#13.277	#ppbv
mfchi_range = 2000.	#sccm
mfchi_sccm = data.mfchiR*(mfchi_range/5.)
mfclo_range = 20.	#sccm
mfclo_sccm = data.mfcloR*(mfclo_range/5.)
dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')

data = pd.concat([data,isop_mr],axis=1)#,join_axes=[mean_resampled.index])

#find all pids in file
sub = 'pid'
pids = [s for s in data.columns if sub in s]
exp_rh_slopes = pd.Series([0.086987,0.038339,0.064982],index= pids)

Time_avg = '30S'

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
mean_resampled = pd.concat([mean_resampled,dRHdt],axis=1,join_axes=[mean_resampled.index])
std_resampled = pd.concat([std_resampled,dRHdt],axis=1,join_axes=[std_resampled.index])

for p in pids:
   name = str('Corr_'+p)
   tmp_ar = (mean_resampled[p]*1e3)-(exp_rh_slopes[p]*mean_resampled.RH)
   tmp_sr = pd.Series(tmp_ar,index=mean_resampled.index,name=name)
   mean_resampled = pd.concat([mean_resampled,tmp_sr],axis=1,join_axes=[mean_resampled.index])

#filter out periods when RH changes rapidly (dRHdt<0.2)
mean_dRHdt_filt = mean_resampled[mean_resampled.dRHdt < 0.15]
std_dRHdt_filt = std_resampled[std_resampled.dRHdt < 0.15]

#create dataframe to store isop cal results
isop_cal_fits = pd.DataFrame(index=['Slope (mV/ppbv)','Slope_err','Intercept (mV)','Intercept_err'],columns=pids)
filtisop_cal_fits = pd.DataFrame(index=['Slope (mV/ppbv)','Slope_err','Intercept (mV)','Intercept_err'],columns=pids)


#####Plots############
colors = ["red", "blue" , "green", "orange", "purple"]
pidfig_resample = plt.figure()
ctr = 1
for p,c in zip(pids,colors):
	sfig = 'pax'+str(ctr)
	sfig = pidfig_resample.add_subplot(len(pids),1,ctr)
	sfig.errorbar(mean_resampled.index,mean_resampled[p]*1e3, yerr = std_resampled[p],color=c)
	sfig.set_ylabel(p+' / mV')
	sfig.set_xlabel("Time")
	sfig.set_ylim([np.min(mean_resampled[p])*1e3,(np.min(mean_resampled[p])*1e3)+1.5])
	ctr+=1
pidfig_resample.show()


#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(3,1,1)
rhax.plot(mean_resampled.index,mean_resampled.RH,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(3,1,2)
isopax.plot(mean_resampled.index,mean_resampled.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("Isop / ppbv")

rhdax = varfig.add_subplot(3,1,3)
rhdax.plot(mean_resampled.index,mean_resampled.dRHdt,color='k',linewidth=3)
rhdax.set_ylabel("dRH/dt")

varfig.show()


corr_plt = plt.figure()
ctr = 1
for p,c in zip(pids,colors):

# 	RH_corr_df[p] = mean_dRHdt_filt[p]*1e3-(exp_rh_slopes[p]*mean_dRHdt_filt.RH)
    name = str('Corr_'+p)
    corrfig2 = corr_plt.add_subplot(len(pids),1,ctr)
    corrfig2.errorbar(mean_resampled.index,mean_resampled[name],color=c, yerr = std_resampled[p])
    corrfig2.set_ylabel('Corr_'+p+' / mV')
    corrfig2.set_xlabel("Time")
# 	corrfig2.set_ylim([np.min(RH_corr_df[p]),(np.min(RH_corr_df[p]))+1.5])

    ctr+=1
corr_plt.show()


isopcalfig2 = plt.figure()
ctr = 1
for p,c in zip(pids,colors):
	name= str('Corr_'+p)
	fit_data = odr.RealData(x = mean_resampled.isop_mr,y = mean_resampled[name],sx = std_resampled.RH ,sy = std_resampled[p]*1e3)
	fit = odr.ODR(fit_data,linear,[5e-5,0.05])
	fit_params = fit.run()
	isop_cal_fits[p] = [fit_params.beta[0],fit_params.sd_beta[0],fit_params.beta[1],fit_params.sd_beta[1]]

	ifig2 = 'pax'+str(ctr)
	ifig2 = isopcalfig2.add_subplot(len(pids),1,ctr)
	ifig2.plot(mean_resampled.isop_mr,mean_resampled[name],'o',color=c)
	ifig2.plot([np.min(mean_resampled.isop_mr),np.max(mean_resampled.isop_mr)],[(fit_params.beta[0]*np.min(mean_resampled.isop_mr))+fit_params.beta[1],(fit_params.beta[0]*np.max(mean_resampled.isop_mr))+fit_params.beta[1]],color='k')
	ifig2.set_ylabel(name+' / mV')
	ifig2.set_xlabel("Isop / ppbv")
	ctr+=1
isopcalfig2.show()


isopcalfig3 = plt.figure()
ctr = 1
for p,c in zip(pids,colors):
	name= str('Corr_'+p)
	fit_data = odr.RealData(x = mean_dRHdt_filt.isop_mr,y = mean_dRHdt_filt[name],sx = std_dRHdt_filt.RH ,sy = std_dRHdt_filt[p]*1e3)
	fit = odr.ODR(fit_data,linear,[5e-5,0.05])
	fit_params = fit.run()
	filtisop_cal_fits[p] = [fit_params.beta[0],fit_params.sd_beta[0],fit_params.beta[1],fit_params.sd_beta[1]]

	ifig3 = 'pax'+str(ctr)
	ifig3 = isopcalfig3.add_subplot(len(pids),1,ctr)
	ifig3.plot(mean_dRHdt_filt.isop_mr,mean_dRHdt_filt[name],'o',color=c)
	ifig3.plot([np.min(mean_dRHdt_filt.isop_mr),np.max(mean_dRHdt_filt.isop_mr)],[(fit_params.beta[0]*np.min(mean_dRHdt_filt.isop_mr))+fit_params.beta[1],(fit_params.beta[0]*np.max(mean_dRHdt_filt.isop_mr))+fit_params.beta[1]],color='k')
	ifig3.set_ylabel(name+'filt / mV')
	ifig3.set_xlabel("Isop / ppbv")
	ctr+=1
isopcalfig3.show()

pid_isop_df = mean_dRHdt_filt.copy(deep=True)
pid_isop_std_df = std_dRHdt_filt.copy(deep=True)

corrisop_plt = plt.figure()
ctr=1

isop_cal_slopes = pd.Series([0.172570,0.038339,0.245062], index = pids)
isop_cal_intercepts = pd.Series([52.089377,52.753197,52.893292], index = pids)
isop_cal_fits.pid5[0] = 0.038339
for p,c in zip(pids,colors):
	name= str('Corr_'+p)
	pid_isop_df[name] = ((pid_isop_df[name])-filtisop_cal_fits[p][2])/filtisop_cal_fits[p][0]
	pid_isop_std_df[name] = ((pid_isop_std_df[p]*1e3)-filtisop_cal_fits[p][2])/filtisop_cal_fits[p][0]
#	pid_isop_df[name] = ((pid_isop_df[name])-isop_cal_intercepts[p])/isop_cal_slopes[p]
#	pid_isop_std_df[name] = ((pid_isop_std_df[p]*1e3)-isop_cal_intercepts[p])/isop_cal_slopes[p]
	corrfig3 = corrisop_plt.add_subplot(len(pids),1,ctr)
	corrfig3.errorbar(pid_isop_df.index,pid_isop_df[name],color=c, yerr = pid_isop_std_df[p])
	corrfig3.plot(pid_isop_df.index,pid_isop_df.isop_mr,'--',color='g',linewidth=3)
	corrfig3.set_ylabel('Corr_'+p+' / ppb')
	corrfig3.set_xlabel("Time")
	ctr+=1
corrisop_plt.show()



