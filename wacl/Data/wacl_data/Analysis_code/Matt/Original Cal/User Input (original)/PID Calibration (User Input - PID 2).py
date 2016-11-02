import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
import time

backslashstring = '\ko'

#############################
## Data read

#####Asking if the user would like to load from the memory stick
pogk = 2
while pogk == 2:
    memorystickq = raw_input('Are you loading from a your memory stick? ')
    if memorystickq == 'y' or memorystickq == 'yes' or memorystickq == 'YES' or memorystickq == 'Yes' or memorystickq == 'Y':
        print '\n\n(Okie doke, loading from E:\Bursary thing\PID Data\Organised and or Edited)'+backslashstring[0]
        path = "E:\Bursary thing\PID Data\Organised and or Edited"+backslashstring[0]
        pogk = 1
    elif memorystickq == 'no' or memorystickq == 'n' or memorystickq == 'No' or memorystickq =='NO' or memorystickq == 'N':
        print '\n\n(Okie doke, loading from C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited then)'
        path = 'C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited'+backslashstring[0]
        pogk = 1
    elif memorystickq == 'somewhere else' or memorystickq == 'elsewhere':
        path = raw_input('please enter where you would like to load from: ')
    else:
        print 'Please enter y or n...'


#####Asking if the user would like to load from today's data
while pogk == 1:
    dateq = raw_input('\nDo you want to load from today\'s data? ')
    if dateq == 'y' or dateq == 'yes' or dateq == 'YES' or dateq == 'Yes' or dateq == 'Y':
        print """\n(Okie doke, loading today's data)"""
        filename1 = str((time.strftime('%m-%d')))+'\d20' + str((time.strftime('%y%m%d'))) + '_0'+ raw_input('Which file would you like to load? ')
        pogk = 2
    elif dateq == 'n' or dateq == 'no' or dateq == 'No' or dateq == 'NO' or dateq == 'N':
        date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
        filename1 =  date[0:2] + '-' + date[2:4] + '\d20' + str((time.strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
        pogk = 0
        print filename1
    else:
        print 'Please enter y or n...'
 
 
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

tmp_pid2 = data1.pid2.notnull()
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
    cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid2_V','pid2_stddev']
    cal_pts = [range(0,cal_N)] 
    delay = 300   #Delay at start of cal step
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
        tp_pid2 = data1.pid2[mfc_setS[pt]:mfc_setF[pt]]
        cal_df.Isop[pt] = tp_Isop.mean()
        cal_df.Isop_stddev[pt] = tp_Isop.std()
        cal_df.pid2_V[pt] = tp_pid2.mean()
        cal_df.pid2_stddev[pt] = tp_pid2.std()
        cal_df.StartT[pt] = Time[mfc_setS[pt]]
        cal_df.EndT[pt] = Time[mfc_setF[pt]]
      

#############################
## Plots
if (plots == 'Y'):

	pid2_avg = pd.rolling_mean(data1.pid2,300)

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	pid2 = ax1.plot(Time[tmp_pid2],data1.pid2[tmp_pid2], linewidth=3,color='r')
	pid2_10s = ax1.plot(Time[tmp_pid2],pid2_avg[tmp_pid2], linewidth=3,color='b')
	plt.ylabel("PID2 / V")
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
		
		slope,intercept,r_value,p_value,std_err=stats.linregress(cal_df.Isop,cal_df.pid2_V)
		isop_fit = [0.,np.max(cal_df.Isop)]
		pid2_fit = [intercept,(np.max(cal_df.Isop)*slope)+intercept]
		fig3 = plt.figure()
		plt.plot(cal_df.Isop,cal_df.pid2_V,"o")
		plt.plot(isop_fit,pid2_fit)
		plt.ylabel('Pid2 / V', fontsize = 20)
		plt.xlabel('[Isop] / ppb', fontsize = 20)
#		plt.ylim(0,1e-4)

	plt.show()
	
print '\n(graphs will appear in a new window)\n'
if r_value < 0.9:
    print path + filename1, ' gives a bad R value (',r_value,') '
    print '\n---------------------------------------------------\n'	
    print 'intercept = ', intercept
    print 'slope = ', slope
    print 'R value =', r_value
else:
    print '\n---------------------------------------------------\n'	
    print 'intercept = ', intercept
    print 'slope = ', slope
    print 'R value =', r_value

start_time = 1
end_time = 3000

start_timea = 1
end_timea = 3000

pid1 = data1.pid1[start_time:end_time]
pid2 = data1.pid2[start_timea:end_timea]



print 'pid1 std = ', np.std(pid1)
print 'pid2 std = ', np.std(pid2)
   
'''if (stat_check == 'Y'):
   st_pts = [2000]
   end_pts = [52000]
    
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
      stat_df.dtpid_stddev[pt] = dt_tp_pid.std()'''