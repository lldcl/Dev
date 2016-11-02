import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
import time

backslashstring = '\ko'
pd.set_option('precision',8)

#############################
## User Interface

#####Asking if the user would like to load from the memory stick
pogk = 2
while pogk == 2:
    memorystickq = raw_input('Are you loading from a your memory stick? ')
    memorystickq = memorystickq.lower()
    if memorystickq == 'y' or memorystickq == 'yes':
        print '\n\n(Okie doke, loading from E:\Bursary thing\PID Data\Organised and or Edited)'+backslashstring[0]
        path = "E:\Bursary thing\PID Data\Organised and or Edited"+backslashstring[0]
        pogk = 1
    elif memorystickq == 'no' or memorystickq == 'n':
        print '\n\n(Okie doke, loading from C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited then)'
        path = 'C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited'+backslashstring[0]
        pogk = 1
    elif memorystickq == 'somewhere else' or memorystickq == 'elsewhere':
        path = raw_input('please enter where you would like to load from: ')
    else:
        print 'Please enter y or n...'


#####Asking if the user would like to load from today's data
while pogk == 1:
    dateq = raw_input('\nDo you want to load from today\'s data? ').lower()
    if dateq == 'y' or dateq == 'yes':
        print """\n(Okie doke, loading today's data)"""
        filename1 = str((time.strftime('%m-%d')))+'\d20' + str((time.strftime('%y%m%d'))) + '_0'+ raw_input('Which file would you like to load? ')
        pogk = 2
    elif dateq == 'n' or dateq == 'no':
        date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
        filename1 =  date[0:2] + '-' + date[2:4] + '\d20' + str((time.strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
        pogk = 0
        print filename1
    else:
        print 'Please enter y or n...'
        
        
        
########################################
######Data Read  
 
 
cal = 'Y' # To ask it to run the cal program
plots = 'Y' # To ask it to plot the graphs
print "\nThis is the file reference", path + filename1
data1 = pd.read_csv(path+filename1)
Time = data1.TheTime-data1.TheTime[0]
Time*=60.*60.*24.

data1.TheTime = pd.to_datetime(data1.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1.TheTime+=offset

tmp_pid2 = data1.pid1.notnull()
tmp_pid3 = data1.pid2.notnull()
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
    cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid2_V','pid3_V','pid2_stddev','pid3_stddev']
  
    
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
        tp_pid2 = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
        tp_pid3 = data1.pid2[mfc_setS[pt]:mfc_setF[pt]]
        cal_df.Isop[pt] = tp_Isop.mean()
        cal_df.Isop_stddev[pt] = tp_Isop.std()
        cal_df.pid2_V[pt] = tp_pid2.mean()
        cal_df.pid2_stddev[pt] = tp_pid2.std()
        cal_df.pid3_V[pt] = tp_pid3.mean()
        cal_df.pid3_stddev[pt] = tp_pid3.std()
        cal_df.StartT[pt] = Time[mfc_setS[pt]]
        cal_df.EndT[pt] = Time[mfc_setF[pt]]
        
        
        
        
        
###############################
########## Pid 2 plot
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
		
		slope2,intercept2,r_value2,p_value2,std_err2=stats.linregress(cal_df.Isop,cal_df.pid2_V)
		isop_fit = [0.,np.max(cal_df.Isop)]
		pid2_fit = [intercept2,(np.max(cal_df.Isop)*slope2)+intercept2]
		fig3 = plt.figure()
		plt.plot(cal_df.Isop,cal_df.pid2_V,"o")
		plt.plot(isop_fit,pid2_fit)
		plt.ylabel('Pid2 / V', fontsize = 20)
		plt.xlabel('[Isop] / ppb', fontsize = 20)
#		plt.ylim(0,1e-4)

###########################
######## Pid 3 plot

if (plots == 'Y'):

	pid_avg = pd.rolling_mean(data1.pid1,300)

	fig1 = plt.figure()
	
	ax1 = fig1.add_subplot(111)
	
	pid = ax1.plot(Time[tmp_pid3],data1.pid1[tmp_pid3], linewidth=3,color='r')
	pid_10s = ax1.plot(Time[tmp_pid3],pid_avg[tmp_pid3], linewidth=3,color='b')
	
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
		
		slope3,intercept3,r_value3,p_value3,std_err3=stats.linregress(cal_df.Isop,cal_df.pid3_V)
		isop_fit = [0.,np.max(cal_df.Isop)]
		pid3_fit = [intercept3,(np.max(cal_df.Isop)*slope3)+intercept3]
		fig3 = plt.figure()
		plt.plot(cal_df.Isop,cal_df.pid3_V,"o")
		plt.plot(isop_fit,pid3_fit)
		plt.ylabel('Pid / V', fontsize = 20)
		plt.xlabel('[Isop] / ppb', fontsize = 20)
		
	plt.show()

###############################################
#### Stat Testing ####


####    Standard Deviation

start_time = 1
end_time = 3000

start_timea = 1
end_timea = 3000

pid2 = data1.pid1[start_time:end_time]
pid3 = data1.pid2[start_timea:end_timea]


###############################################
############# Histogram


###########################################
########### Checking for good R Values and printing data
	
print '\n(graphs will appear in a new windows)\n'
if r_value2 < 0.83 and r_value3 <0.83:
    
    x = str( 'Both Pids give bad R values' )
    print x.upper(), '\n\n'
    
    data = {'Intercepts':[intercept2, intercept3], 'Slopes':[slope2,slope3], 'R Values':[r_value2,r_value3]}
    frame = pd.DataFrame(data,index=['PID2','PID3'])
    print frame
    
elif r_value2 < 0.83:
    x = str( 'Pid 2 gives a bad R value' )
    print x.upper(), '\n\n'
    
    data = {'Intercepts':[intercept2, intercept3], 'Slopes':[slope2,slope3], 'R Values':[r_value2,r_value3]}
    frame = pd.DataFrame(data,index=['PID2','PID3'])
    print frame
    
elif r_value3 < 0.83:
    x = str( 'Pid 3 gives a bad R value' )
    print x.upper(), '\n\n'
    
    data = {'Intercepts':[intercept2, intercept3], 'Slopes':[slope2,slope3], 'R Values':[r_value2,r_value3]}
    frame = pd.DataFrame(data,index=['PID2','PID3'])
    print frame

else:
    
    data = {'Intercepts':[intercept2, intercept3], 'Slopes':[slope2,slope3], 'R Values':[r_value2,r_value3]}
    frame = pd.DataFrame(data,index=['PID2','PID3'])
    print frame





