import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats
from scipy.fftpack import fft
from matplotlib.widgets import SpanSelector

import numpy as np

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
filename1 = '201509/d20150902_05'
cal = 'N'
cor_baseline = 'N'
plots = 'Y'

data1 = pd.read_csv(path+filename1)
Time = data1.TheTime-data1.TheTime[0]
Time*=60.*60.*24.

data1.TheTime = pd.to_datetime(data1.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1.TheTime+=offset

RH = ((data1.RH/4.9)-0.16)/0.0062

#############################
## Plots
if (plots == 'Y'):
	f_pid1 = np.isfinite(data1.pid1)
	f_pid2 = np.isfinite(data1.pid2)
	f_pid3 = np.isfinite(data1.pid3)
	
	
	pid1_avg = pd.rolling_mean(data1.pid1[f_pid1],100)
	pid2_avg = pd.rolling_mean(data1.pid2[f_pid2],100)
	pid3_avg = pd.rolling_mean(data1.pid3[f_pid3],100)
	
	M2_RH = 1.0e-5
	C2_RH = 0.054
	RH_cor_pid2 = pid2_avg-(M2_RH*RH[f_pid2])

	M3_RH = 1.0e-5
	C3_RH = 0.053
	RH_cor_pid3 = pid3_avg-(M3_RH*RH[f_pid3])


	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
# 	pid1 = ax1.plot(data1.TheTime[f_pid1],data1.pid1[f_pid1], linewidth=3,color='r',label='PID#2 10Hz')
# 	pid1_10s = ax1.plot(data1.TheTime[f_pid1],pid1_avg, linewidth=3,color='k',label='PID#2 10s av')
	pid2 = ax1.plot(data1.TheTime[f_pid2],data1.pid2[f_pid2], linewidth=3,color='b',label='PID#3 10Hz')
	pid2_10s = ax1.plot(data1.TheTime[f_pid2],pid2_avg, linewidth=3,color='k',label='PID#3 10s av')
	pid3 = ax1.plot(data1.TheTime[f_pid3],data1.pid3[f_pid3], linewidth=3,color='g',label='PID#4 10Hz')
	pid3_10s = ax1.plot(data1.TheTime[f_pid3],pid3_avg, linewidth=3,color='k',label='PID#4 10s av')
	handles, labels = ax1.get_legend_handles_labels()
	plt.legend(handles, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0.)
	plt.ylabel("PID / V")
	plt.xlabel('Time / s', fontsize = 20)

	

	isop_cyl = 13.277	#ppbv
	mfchi_range = 100.	#sccm
	mfchi_sccm = data1.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data1.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
	isop_mr = dil_fac*isop_cyl
	fig2 = plt.figure()
	ax1 = fig2.add_subplot(111)
	pid2 = ax1.plot(data1.TheTime,isop_mr, linewidth=3,color='g')
	plt.ylabel("Isop / ppbv")
	plt.xlabel('Time / s', fontsize = 20)
	ax2 = fig2.add_subplot(111, sharex=ax1, frameon=False)
	Temp = ax2.plot(data1.TheTime,RH, linewidth=3,color='b')
	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	plt.ylabel("RH / %")

	fig3 = plt.figure()
	ax1 = fig3.add_subplot(111)
	pid2 = ax1.plot(data1.TheTime[f_pid2],pid2_avg, linewidth=3,color='b',label='PID#3 10Hz')
	pid2_RH = ax1.plot(data1.TheTime[f_pid2],RH_cor_pid2, linewidth=3,color='k',label='PID#3 RH cor')
	handles, labels = ax1.get_legend_handles_labels()
	plt.legend(handles, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0.)
	plt.ylabel("PID / V")
	plt.xlabel('Time / s', fontsize = 20)

	fig4 = plt.figure()
	ax1 = fig4.add_subplot(111)
	pid3 = ax1.plot(data1.TheTime[f_pid3],pid3_avg, linewidth=3,color='g',label='PID#4 10Hz')
	pid3_RH = ax1.plot(data1.TheTime[f_pid3],RH_cor_pid3, linewidth=3,color='k',label='PID#4 RH cor')
	handles, labels = ax1.get_legend_handles_labels()
	plt.legend(handles, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0.)
	plt.ylabel("PID / V")
	plt.xlabel('Time / s', fontsize = 20)

    
	plt.show()

