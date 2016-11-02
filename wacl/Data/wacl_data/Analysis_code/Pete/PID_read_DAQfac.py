import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats

#############################
## Data read

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_data_files/'
filename1 = '201507/d20150715_010'
cal = 'N'
cor_baseline = 'N'
stat_check = 'N'
plots = 'Y'

if (stat_check == 'Y'):
   st_pts = [2000]
   end_pts = [52000]

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
## Find zero isoprene periods and remove linear trend from entire data series

if (cor_baseline == 'Y'):

   zero = (np.logical_and(np.logical_and(np.isfinite(data1.mfchi),np.isfinite(data1.mfclo)),data1.mfclo==0))
      
   
   
   

#############################
## Signal vs Isop for calibration experiments

if (cal == 'Y'):
   mfc_set = np.zeros((len(data1.mfclo)),dtype=bool)
   for i in range(1,len(data1.mfchi)):
      if (np.logical_and(np.logical_and(np.isfinite(data1.mfchi[i]),np.isfinite(data1.mfclo[i])),np.logical_or(data1.mfchi[i]!=data1.mfchi[i-1],data1.mfclo[i]!=data1.mfclo[i-1]))):
         mfc_set[i] = "True"
   cal_N = np.sum(mfc_set)
   cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid_V','pid_stddev','pid_supV','pid_supV_stddev']
   cal_pts = [range(0,cal_N)] 
   delay = 100.
   cal_df = pd.DataFrame(index=cal_pts, columns=cal_cols)

   mfc_setS = data1.index[mfc_set]
   mfc_setS+=delay

   mfc_setF = data1.index[mfc_set]
   mfc_setF = np.append(mfc_setF,len(data1.TheTime))
   mfc_setF = np.delete(mfc_setF,0)
   mfc_setF-=11
   
   for pt in range(0,cal_N):
      if (np.logical_and(data1.mfclo[mfc_setS[pt]]==data1.mfclo[mfc_setF[pt]],data1.mfchi[mfc_setS[pt]]==data1.mfchi[mfc_setF[pt]])):
         if (data1.mfclo[mfc_setS[pt]]==0):
            tp_pidZ = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
            tp_TZ = Time[mfc_setS[pt]:mfc_setF[pt]]
            if (pt==0):
               signal_baseline = tp_pidZ.mean()
               time_baseline = tp_TZ.mean()
            else:
               signal_baseline = np.append(signal_baseline,tp_pidZ.mean())
               time_baseline = np.append(time_baseline,tp_TZ.mean())
         tp_Isop = isop_mr[mfc_setS[pt]:mfc_setF[pt]]
         tp_pid = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
      cal_df.Isop[pt] = tp_Isop.mean()
      cal_df.Isop_stddev = tp_Isop.std()
      cal_df.pid_V[pt] = tp_pid.mean()
      cal_df.pid_stddev = tp_pid.std()		
      
   if (cor_baseline == 'Y'):
      cal_zero = np.empty(len(cal_df.pid_V))
      cal_zero[:] = np.nan
      print cal_zero
      for z in range(len(cal_df.Isop)):
         if (cal_df.Isop[z] < 0.03):
            cal_zero[z] = cal_df.pid_V[z]
      for zc in range(len(cal_df.Isop)):
         if (cal_df.Isop[zc] > 0.03):
            cal_df.pid_V[zc] = cal_df.pid_V[zc]-np.mean([cal_zero[zc-1],cal_zero[zc+1]])

### cal code for files pre 18/06/15
#	flow_changeT = Time[np.logical_or(data1.mfclo.notnull(),data1.mfchi.notnull())]
#	cal_N = 1len(flow_changeT)	#19
#    cal_df.StartT = [50,500,950,1200,1600,1800,2100,2500,2850,3000,3200,3375,3650,4000,4150,4350,4560,4675,4900]  #manual points for d20150611_02
#    cal_df.EndT = [450,900,1150,1550,1750,2025,2300,2800,2975,3040,3350,3550,3900,4100,4300,4480,4640,4810,5400]
# 
#    for pt in range(0,cal_N):
#       tp_Isop = isop_mr.loc[(Time > cal_df.StartT[pt]) & (Time < cal_df.EndT[pt])]
#       tp_pid = data1.pid1.loc[(Time > cal_df.StartT[pt]) & (Time < cal_df.EndT[pt])]
# 		if (pt==0):
# 			tp_Isop = isop_mr.loc[(Time < flow_changeT.iloc[pt])]
# 			tp_pid = data1.pid1.loc[(Time < flow_changeT.iloc[pt])]
# 		else:
# 			tp_Isop = isop_mr.loc[(Time > flow_changeT.iloc[pt-1]+delay) & (Time < flow_changeT.iloc[pt])]
# 			tp_pid = data1.pid1.loc[(Time > flow_changeT.iloc[pt-1]+delay) & (Time < flow_changeT.iloc[pt])]
#       cal_df.Isop[pt] = tp_Isop.mean()
#       cal_df.Isop_stddev = tp_Isop.std()
#       cal_df.pid_V[pt] = tp_pid.mean()
#       cal_df.pid_stddev = tp_pid.std()

#############################
### calculate stats on selections of data
### returns mean and std dev of data selections and data selections after linear trend removed

if (stat_check == 'Y'):
   stat_pts = len(st_pts)
   stat_cols = ['StartT','EndT','pid_V','pid_stddev','dtpid_V','dtpid_stddev']
   stat_lines = [range(0,stat_pts)]
   stat_df = pd.DataFrame(index=stat_lines, columns=stat_cols)
   for pt in range(0,stat_pts):
      tp_pid1 = data1.pid1.loc[(Time > st_pts[pt]) & (Time < end_pts[pt])]
      tp_pid = tp_pid1[np.isfinite(tp_pid1)]
      tp_T   = Time.loc[(Time > st_pts[pt]) & (Time < end_pts[pt])]
      tp_T = tp_T[np.isfinite(tp_pid1)]
      
      dt_tp_pid = signal.detrend(tp_pid)+tp_pid.mean()
      
      plt.plot(tp_T,tp_pid)
      plt.plot(tp_T,dt_tp_pid,color='r')      
      plt.show()

      stat_df.StartT[pt] = st_pts[pt]
      stat_df.EndT[pt] = end_pts[pt]
      stat_df.pid_V[pt] = tp_pid.mean()
      stat_df.pid_stddev[pt] = tp_pid.std()
      stat_df.dtpid_V[pt] = dt_tp_pid.mean()
      stat_df.dtpid_stddev[pt] = dt_tp_pid.std()

#       test_fft=np.fft.fft(tp_pid)
#       freq_fft = np.fft.fftfreq(tp_T.shape[-1])
#       plt.plot(freq_fft, test_fft.real, freq_fft, test_fft.imag)
#       plt.show()

#############################
## Plots
if (plots == 'Y'):

	pid_avg = pd.rolling_mean(data1.pid1,300)

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	pid = ax1.plot(Time[tmp_pid],data1.pid1[tmp_pid], linewidth=3,color='r')
#	pid_10s = ax1.plot(Time[tmp_pid],pid_avg[tmp_pid], linewidth=3,color='b')
# 	if (cal == 'Y'):
# 	   pid_base = ax1.plot(time_baseline,signal_baseline, "o")

	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
	isop = ax2.plot(Time[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')

	# if (cal == 'Y'):
	# 	for pt in range(0,cal_N):
	# 		ax2.plot([flow_changeT.iloc[pt],flow_changeT.iloc[pt]],[0.,500.],color='b',linestyle = '-')
	# 		if (pt<cal_N-1):
	# 			ax2.plot([flow_changeT.iloc[pt]+delay,flow_changeT.iloc[pt]+delay],[0.,500.],color='b',linestyle = '--')
	# 

# 	if (cal == 'Y'):
# 		ax2.plot([Time[data1.index[mfc_setS]],Time[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
# 		ax2.plot([Time[data1.index[mfc_setF]],Time[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')

	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)

	fig2 = plt.figure()
	# plt.plot(data1.TheTime,data1.mfcloR,color='r',linewidth=3)
	# plt.plot(data1.TheTime,data1.mfchiR,color='b',linewidth=3)
	plt.plot(Time,mfclo_sccm,color='r',linewidth=3)
	plt.plot(Time,mfchi_sccm,color='b',linewidth=3)
	plt.ylabel('Flow / sccm', fontsize = 20)
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

	fig4 = plt.figure()
	plt.plot(Time,data1.mfclo)
	plt.plot(Time,data1.mfchi)
	plt.ylabel('MFC set / V', fontsize = 20)
	plt.xlabel('Time / s', fontsize = 20)

	fig5 = plt.figure()
	ax1 = fig5.add_subplot(111)
	pid_supV = ax1.plot(Time[tmp_flow],data1.pidv[tmp_flow], linewidth=3,color='b')
	plt.ylabel("PID supply / V")
	#ax2 = fig5.add_subplot(111, sharex=ax1, frameon=False)
	#pid = ax2.plot(Time[tmp_pid],data1.pid1[tmp_pid], linewidth=3,color='r')
	#ax2.yaxis.tick_right()
	#ax2.yaxis.set_label_position("right")
	#plt.ylabel("PID signal / V")
	plt.xlabel('Time / s', fontsize = 20)


	fig6 = plt.figure()
	plt.plot(data1.pidv,data1.pid1,"o")
	plt.ylabel('Pid / V', fontsize = 20)
	plt.xlabel('PID supply / V', fontsize = 20)


# 	fig7 = plt.figure()
# 	plt.plot(Time[zero],data1.pid1[zero])


	plt.show()
