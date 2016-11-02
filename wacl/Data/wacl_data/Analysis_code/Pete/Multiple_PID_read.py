import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats
from scipy.fftpack import fft
from matplotlib.widgets import SpanSelector


def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]
#############################
## Data read

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'
filename1 = '201509/d20150923_014'
cal = 'N'
cor_baseline = 'N'
stat_check = 'Y'
plots = 'N'
perform_fft = 'Y'

data1 = pd.read_csv(path+filename1)
Time = data1.TheTime-data1.TheTime[0]
Time*=60.*60.*24.

data1.TheTime = pd.to_datetime(data1.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1.TheTime+=offset

pid1_interp = np.array(data1.pid4)
nans, x=nan_helper(pid1_interp)
pid1_interp[nans]=np.interp(x(nans),x(~nans),pid1_interp[~nans])

#f_pid2 = np.isfinite(data1.pid2)
pid2_interp = np.array(data1.pid5)
nans, x=nan_helper(pid2_interp)
pid2_interp[nans]=np.interp(x(nans),x(~nans),pid2_interp[~nans])


#############################
### calculate stats on selections of data
### returns mean and std dev of data selections and data selections after linear trend removed

if (stat_check == 'Y'):
	st_pts = list(range(100000,300000))

	statfig = plt.figure()
	ax1 = statfig.add_subplot(111)
	ax1.plot(data1.index,pid1_interp,color='b')
	ax1.plot(data1.index,pid2_interp,color='r')
	ax1.plot([st_pts[0],st_pts[0]],[0.052,0.056],color='K') 
	ax1.plot([st_pts[len(st_pts)-1],st_pts[len(st_pts)-1]],[0.052,0.056],color='K')
	plt.ylim(0.052,0.056)
	plt.ylabel("PID / V")
#	ax2 = statfig.add_subplot(111, sharex=ax1, frameon=False)
#	ax2.plot(data1.index,data1.mfcloR,color='g')
#	ax2.yaxis.tick_right()

	print  'Number of points	= ',len(st_pts)
	print  'Mean PID1			= ',np.mean(data1.pid4[st_pts])
	print  'Standard dev PID1	= ',np.std(data1.pid4[st_pts])
	
	print  'Mean PID 2			= ',np.mean(data1.pid5[st_pts])
	print  'Standard dev PID 2	= ',np.std(data1.pid5[st_pts])

	plt.show()

	baseT_df = pd.DataFrame(data1.pid5[st_pts])
	baseT_df.set_index(data1.TheTime[st_pts],inplace=True)
	stddevs = []
	means = []
	srate = [100,200,500,1000,2000,5000,10000,20000,30000]
	for t in srate:
		avems = str(t)+'L'
		tmp = baseT_df.resample(avems,how='mean')
		stddevs.append(np.std(tmp.pid5))
		means.append(np.mean(tmp.pid5))
	
	plt.figure()
	plt.plot(np.array(srate)/1000.,3.*np.array(stddevs)/0.00025,color='b')
	plt.xlabel('Averaging time / s')
	plt.ylabel('3 sigma LOD / ppbv')
	plt.show()



#############################
### calculate fft of PID signals (currently assume a fixed 0.1 s time resolution of the data, despite slight fluctuations in this and missing data - need to improve this)

if (perform_fft == 'Y'):

	print 'PID #2'
	print 'mean 	= ',np.mean(pid1_interp[st_pts])
	print 'median	= ',np.median(pid1_interp[st_pts])
	print 'stddev	= ',np.std(pid1_interp[st_pts])

	fft1= np.fft.rfft(pid2_interp[st_pts])
	freq_fft1 = np.fft.rfftfreq(len(pid2_interp[st_pts]),d=0.1)
	plt.figure()
	plt.plot(freq_fft1,np.abs(fft1),color='r')
	plt.yscale('log')
	plt.xscale('log')
	plt.ylabel('fft', fontsize = 20)
	plt.xlabel('Hz', fontsize = 20)
	plt.title('PID #2 fft')

	# #start of fft filter from http://exnumerus.blogspot.co.uk/2011/12/how-to-remove-noise-from-signal-using.html
	f_signal = 0.016
	def filter_rule(x,freq):
		band = 0.005
		if abs(freq)>f_signal+band or abs(freq)<f_signal-band:
			return 0
		else:
			return x

	F_filtered = np.array([filter_rule(x,freq) for x,freq in zip(fft1,freq_fft1)])
 
	# reconstruct the filtered signal
	s_filtered = np.fft.irfft(F_filtered)

	x=np.array(data1.TheTime[st_pts])
	#x=x[1:]

	plt.figure()
	plt.plot(data1.TheTime[st_pts],pid1_interp[st_pts],color='b')
	plt.plot(x,s_filtered+np.mean(pid1_interp[st_pts]),color='r')

	print 'PID #3'
	print 'mean 	= ',np.mean(pid2_interp[st_pts])
	print 'median	= ',np.median(pid2_interp[st_pts])
	print 'stddev	= ',np.std(pid2_interp[st_pts])

	fft2= np.fft.rfft(pid2_interp[st_pts])
	freq_fft2 = np.fft.rfftfreq(len(pid2_interp[st_pts]),d=0.1)

	# slope,intercept,r_value,p_value,std_err=stats.linregress(np.log10(freq_fft2[1:200]),np.log10(np.abs(fft2[1:200])))
	# fft2_fit = (slope*np.log10(freq_fft2[1:200]))+intercept

	plt.figure()
	plt.plot(freq_fft2,np.abs(fft2),color='b')
	#plt.plot(freq_fft2[1:200],np.power(10,fft2_fit),color='k')
	plt.yscale('log')
	plt.xscale('log')
	plt.ylabel('fft', fontsize = 20)
	plt.xlabel('Hz', fontsize = 20)
	plt.title('PID #3 fft')


#############################
## Plots
if (plots == 'Y'):
	f_pid1 = np.isfinite(data1.pid4)
	f_pid2 = np.isfinite(data1.pid5)
	f_pid3 = np.isfinite(data1.pid3)
	
	
	pid1_avg = pd.rolling_mean(data1.pid4[f_pid1],100)
	pid2_avg = pd.rolling_mean(data1.pid5[f_pid2],100)
	pid3_avg = pd.rolling_mean(data1.pid3[f_pid3],100)
	

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	pid1 = ax1.plot(data1.TheTime[f_pid1],data1.pid4[f_pid1], linewidth=3,color='r',label='PID#2 10Hz')
	pid1_10s = ax1.plot(data1.TheTime[f_pid1],pid1_avg[f_pid1], linewidth=3,color='k',label='PID#2 10s av')
	pid2 = ax1.plot(data1.TheTime[f_pid2],data1.pid5[f_pid2], linewidth=3,color='b',label='PID#3 10Hz')
	pid2_10s = ax1.plot(data1.TheTime[f_pid2],pid2_avg[f_pid2], linewidth=3,color='k',label='PID#3 10s av')
	pid3 = ax1.plot(data1.TheTime[f_pid3],data1.pid3[f_pid3], linewidth=3,color='g',label='PID#4 10Hz')
	pid3_10s = ax1.plot(data1.TheTime[f_pid3],pid3_avg[f_pid3], linewidth=3,color='k',label='PID#4 10s av')
	handles, labels = ax1.get_legend_handles_labels()
	plt.legend(handles, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0.)
	plt.ylabel("PID / V")
	plt.xlabel('Time / s', fontsize = 20)
	
	
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
	Temp = ax2.plot(data1.TheTime,data1.Temp*100., linewidth=3,color='g')
	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	plt.ylabel("Temp / oC")
	ax2.set_ylim(0.,35.)
	
#	plt.show()
	
# 	fig2 = plt.figure()
# 	plt.hist(pid1_interp,bins=200,range=[np.median(pid1_interp)-0.0005,np.median(pid1_interp)+0.0005])
# 	#range=[pid1_interp.mean()-(0.15*pid1_interp.std()),pid1_interp.mean()+(0.005*pid1_interp.std())])
# 	plt.xlabel("PID / V")
# 	plt.ylabel("Count")
# 	plt.title('PID #2')
# 	plt.xlim(np.median(pid1_interp)-0.0005,np.median(pid1_interp)+0.0005)
# 
# 	fig3 = plt.figure()
# 	plt.hist(pid2_interp,bins=200,range=[np.median(pid2_interp)-0.0005,np.median(pid2_interp)+0.0005])
# 	plt.xlabel("PID / V")
# 	plt.ylabel("Count")
# 	plt.title('PID #3')
# 	plt.xlim(np.median(pid2_interp)-0.0005,np.median(pid2_interp)+0.0005)
# 
# 	bxplt_data = [pid1_interp,pid2_interp]
# 	fig4 = plt.figure()
# 	plt.boxplot(bxplt_data)
# #	plt.yscale('log')
# 	plt.ylabel("PID / V")
# 	plt.xticks([1,2],['PID #2','PID #3'])
# 
# 	fig5 = plt.figure()
# 	plt.boxplot(bxplt_data,0,'')
# 	plt.ylabel("PID / V")

	isop_cyl = 13.277	#ppbv
	mfchi_range = 100.	#sccm
	mfchi_sccm = data1.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data1.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
	isop_mr = dil_fac*isop_cyl
	fig6 = plt.figure()
	ax1 = fig6.add_subplot(111)
	pid6 = ax1.plot(data1.TheTime,isop_mr, linewidth=3,color='g')
	plt.ylabel("Isop / ppbv")
	plt.xlabel('Time / s', fontsize = 20)

    
	plt.show()

