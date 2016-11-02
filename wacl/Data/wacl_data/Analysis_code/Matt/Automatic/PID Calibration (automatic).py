import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
import time
import os


#creating a list for the values for data

il2 = []
il3 = []
sl2 = []
sl3 = []
r2 = []
r3 = []

bss = '\ko'

questions = ''
cal = 'Y'
plots = ''


pd.set_option('precision',7)

#############################
## Data read

if questions == 'Y':
    #####Asking if the user would like to load from the memory stick
    pogk = 2
    while pogk == 2:
        memorystickq = raw_input('Are you loading from a your memory stick? ')
        if memorystickq == 'y' or memorystickq == 'yes' or memorystickq == 'YES' or memorystickq == 'Yes' or memorystickq == 'Y':
            print '\n\n(Okie doke, loading from E:\Bursary thing\PID Data\Organised and or Edited)'+bss[0]
            path = "E:\Bursary thing\PID Data\Organised and or Edited"+bss[0]
            pogk = 1
        elif memorystickq == 'no' or memorystickq == 'n' or memorystickq == 'No' or memorystickq =='NO' or memorystickq == 'N':
            print '\n\n(Okie doke, loading from C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited then)'
            path = 'C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited'+bss[0]
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
            filenameb = str((time.strftime('%m-%d')))+'\d' + str((time.strftime('%Y%m%d'))) + '_0'
            pogk = 0
        elif dateq == 'n' or dateq == 'no' or dateq == 'No' or dateq == 'NO' or dateq == 'N':
            date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
            filenameb =  date[0:2] + '-' + date[2:4] + '\d20' + str((time.strftime('%y'))) + date + '_0'
            pogk = 0
            print filenameb
        else:
            print 'Please enter y or n...'
else:
    print 'please enter the filename into the code'
    filenameb = ''
    path = ''



p = []
filesl=[]
pfl = []

print 'IF THIS DOES\'NT WORK CHECK THE PATH'
path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Organised_Data_Files'


bss = '\ko'
d = int(str((time.strftime('%d'))))
m = int(str((time.strftime('%m'))))


for i in range (8,d+1):
    if i<10:
        filenamea = bss[0]+'07-0'+str(i)
    else:
        filenamea = bss[0]+'07-'+str(i)
        
    for pt in range(0,25):
        if i<10:
            filenameb = '\d2015070'+str(i)+'_0'+str(pt)
        else:
            filenameb = '\d201507'+str(i)+'_0'+str(pt)
        
        pfl.append(path+filenamea + filenameb)
     



for i in range (0,len(pfl)):   
    p.append(os.path.exists(pfl[i]))

 
for i in range(0,len(pfl)):
    if p[i] == True:
        filesl.append(pfl[i])


for i in range(0,len(filesl)):
    filenamei = filesl[i]
    data1 = pd.read_csv(filenamei)
    
    try:
        data1 = pd.read_csv(path+filenamei)
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
            cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid2_V','pid2_stddev','pid3_V','pid3_stddev']
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
        
    
        #############################
        ## Plots
        if (cal == 'Y'):
    
               	##### PID 2
               	slope2,intercept2,r_value2,p_value2,std_err2=stats.linregress(cal_df.Isop,cal_df.pid2_V)
           	isop_fit = [0.,np.max(cal_df.Isop)]
           	pid2_fit = [intercept2,(np.max(cal_df.Isop)*slope2)+intercept2]
           	
           	global il2
           	global sl2
           	global r2
           	
           	il2.append(intercept2)
           	sl2.append(slope2)           	
           	r2.append(r_value2)
           	           	           	           	
           	##### PID 3
           	slope3,intercept3,r_value3,p_value3,std_err3=stats.linregress(cal_df.Isop,cal_df.pid3_V)
           	isop_fit = [0.,np.max(cal_df.Isop)]
           	pid3_fit = [intercept3,(np.max(cal_df.Isop)*slope3)+intercept3]
           	
           	il3.append(intercept3)
           	sl3.append(slope3)
           	r3.append(r_value3)
	
        if plots == 'Y':
        
                ##### PID 2
                pid2_avg = pd.rolling_mean(data1.pid1,100)
               	fig1 =plt.figure()
               	ax1 = fig1.add_subplot(111)
           	pid2 = ax1.plot(Time[tmp_pid2],data1.pid1[tmp_pid2], linewidth=3,color='r')
           	pid2_10s = ax1.plot(Time[tmp_pid2],pid2_avg[tmp_pid2], linewidth=3,color='b')
           	plt.ylabel("PID2 / V")
           	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
           	isop = ax2.plot(Time[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')
            
           	
                ax2.plot([Time[data1.index[mfc_setS]],Time[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
          	ax2.plot([Time[data1.index[mfc_setF]],Time[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')
            
           	ax2.yaxis.tick_right()
           	ax2.yaxis.set_label_position("right")
           	plt.ylabel("Isop / ppb")
           	plt.xlabel('Time / s', fontsize = 20)
           	
           	fig3 = plt.figure()
                plt.plot(cal_df.Isop,cal_df.pid2_V,"o")
           	plt.plot(isop_fit,pid2_fit)
           	plt.ylabel('Pid2 / V', fontsize = 20)
           	plt.xlabel('[Isop] / ppb', fontsize = 20)
           	
           	
           	
           	##### PID 3
           	pid3_avg = pd.rolling_mean(data1.pid2,100)
               	fig1 = plt.figure()
               	ax1 = fig1.add_subplot(111)
           	pid3 = ax1.plot(Time[tmp_pid3],data1.pid2[tmp_pid3], linewidth=3,color='r')
           	pid3_10s = ax1.plot(Time[tmp_pid3],pid3_avg[tmp_pid3], linewidth=3,color='b')
           	plt.ylabel("PID3 / V")
           	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
           	isop = ax2.plot(Time[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')
            
           	
                ax2.plot([Time[data1.index[mfc_setS]],Time[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
          	ax2.plot([Time[data1.index[mfc_setF]],Time[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')
            
           	ax2.yaxis.tick_right()
           	ax2.yaxis.set_label_position("right")
           	plt.ylabel("Isop / ppb")
           	plt.xlabel('Time / s', fontsize = 20)
           	
           	fig3 = plt.figure()
                plt.plot(cal_df.Isop,cal_df.pid3_V,"o")
           	plt.plot(isop_fit,pid3_fit)
           	plt.ylabel('Pid3 / V', fontsize = 20)
           	plt.xlabel('[Isop] / ppb', fontsize = 20)

    
                plt.show()

	
    except IOError:
        pass
        
    datad = {'Intercepts': [il2,il3], 'Slopes':[sl2,sl3], 'R_Values':[r2,r3]}
    frame_cals = pd.DataFrame(datad, index = ['Pid_2', 'Pid_3'])
