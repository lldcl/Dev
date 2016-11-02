import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats

#############################
## Data read

x = raw_input('Are you loading from a your memory stick? ')
if x == 'y':
    print 'Okie doke, loading from J:\Bursary thing\PID Data'
    path = 'J:\Bursary thing\PID Data'
elif x == 'yes':
    print 'Okie doke, loading from I:\Bursary thing\PID Data'
    path = 'J:\Bursary thing\PID Data'
elif x == 'Yes':
    print 'Okie doke, loading from I:\Bursary thing\PID Data'
    path = 'J:\Bursary thing\PID Data'
elif x == 'YES':
    print 'Okie doke, loading from I:\Bursary thing\PID Data'
    path = 'I:\Bursary thing\PID Data'
else:
    print 'Okie doke, loading from C:\Users\Matt\Python stuff and data\Calibration Graphs then'
    path = 'C:\Users\Matt\Python stuff and data\Calibration Graphs'


filename1 = '\d2015' + raw_input('Which file do you want to load? ')
cal = 'Y'
plots = 'Y'
print "\nThis is the file reference", path + filename1
data1 = pd.read_csv(path+filename1)
Time = data1.TheTime-data1.TheTime[0]
Time*=60.*60.*24.

data1.TheTime = pd.to_datetime(data1.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1.TheTime+=offset

tmp_pid = data1.pid1.notnull()
tmp_flow = data1.mfchiR.notnull()

isop_cyl = 13.277	#ppbv
mfchi_range = 100.	#sccm
mfchi_sccm = data1.mfchiR*(mfchi_range/5.)

mfclo_range = 20.	#sccm
mfclo_sccm = data1.mfcloR*(mfclo_range/5.)

dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = dil_fac*isop_cyl

#############################
## Signal vs Isop for calibration experiments

if (cal == 'Y'):
   mfc_set = np.zeros((len(data1.mfclo)),dtype=bool)
   for i in range(1,len(data1.mfchi)):
      if (np.logical_and(np.logical_and(np.isfinite(data1.mfchi[i]),np.isfinite(data1.mfclo[i])),np.logical_or(data1.mfchi[i]!=data1.mfchi[i-1],data1.mfclo[i]!=data1.mfclo[i-1]))):
         mfc_set[i] = "True"
   cal_N = np.sum(mfc_set)
   cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid_V','pid_stddev']
   cal_pts = [range(0,cal_N)] 
   delay = 200      #Delay at start of cal step
   cal_df = pd.DataFrame(index=cal_pts, columns=cal_cols)

   mfc_setS = data1.index[mfc_set]
   mfc_setS+=delay

   mfc_setF = data1.index[mfc_set]
   mfc_setF = np.append(mfc_setF,len(data1.TheTime))
   mfc_setF = np.delete(mfc_setF,0)
   mfc_setF-=11      #Delay at end of cal step
   
   for pt in range(0,cal_N):
   #check that the flows are the same at the start and end of the range over which you are averaging
      if (np.logical_and(data1.mfclo[mfc_setS[pt]]==data1.mfclo[mfc_setF[pt]],data1.mfchi[mfc_setS[pt]]==data1.mfchi[mfc_setF[pt]])):
         tp_Isop = isop_mr[mfc_setS[pt]:mfc_setF[pt]]
         tp_pid = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
         cal_df.Isop[pt] = tp_Isop.mean()
         cal_df.Isop_stddev[pt] = tp_Isop.std()
         cal_df.pid_V[pt] = tp_pid.mean()
         cal_df.pid_stddev[pt] = tp_pid.std()
         cal_df.StartT[pt] = Time[mfc_setS[pt]]
         cal_df.EndT[pt] = Time[mfc_setF[pt]]
      

#############################
## Plots
if (plots == 'Y'):

	pid_avg = pd.rolling_mean(data1.pid1,300)

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	pid = ax1.plot(Time[tmp_pid],data1.pid1[tmp_pid], linewidth=3,color='r')
	pid_10s = ax1.plot(Time[tmp_pid],pid_avg[tmp_pid], linewidth=3,color='b')
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
	isop = ax2.plot(Time[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')

	if (cal == 'Y'):
		ax2.plot([Time[data1.index[mfc_setS]],Time[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
		ax2.plot([Time[data1.index[mfc_setF]],Time[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')

	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)

	if (cal == 'Y'):
		
		slope,intercept,r_value,p_value,std_err=stats.linregress(cal_df.Isop,cal_df.pid_V)
		isop_fit = [0.,np.max(cal_df.Isop)]
		pid_fit = [intercept,(np.max(cal_df.Isop)*slope)+intercept]
		fig3 = plt.figure()
		plt.plot(cal_df.Isop,cal_df.pid_V,"o")
		plt.plot(isop_fit,pid_fit)
		plt.ylabel('Pid / V', fontsize = 20)
		plt.xlabel('[Isop] / ppb', fontsize = 20)
#		plt.ylim(0,1e-4)

	plt.show()
	
print '\n(graphs will appear in a new window)\n'
print 'intercept = ', intercept
print 'slope = ', slope
print 'R value =', r_value