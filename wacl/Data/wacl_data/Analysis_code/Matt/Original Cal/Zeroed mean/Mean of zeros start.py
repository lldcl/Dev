import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import time

# Where the mfclo = 0 replace the pid values with mean pid values
path = 'C:\Users\Matt\Bursary thing\PID Data\RAW'
filename1 ='\d20150713_07'



plots='Y'
cal = 'Y'
avg_0 = 'Y'

data1 = pd.read_csv(path+filename1)


if avg_0 == 'Y':
    
    pid2 = data1.pid1
    pid3 = data1.pid2
    lo = data1.mfclo
    
    
    pid2_zeros = []
    pid3_zeros = []
    
    
    for i in range (0,len(lo)):        
        if lo[i] == 0:
            pid2_zeros.append(pid2[i])
            pid3_zeros.append(pid3[i])
    
    mean_pid2 = np.nanmean(pid2_zeros)
    mean_pid3 = np.nanmean(pid2_zeros)
    
    
    
    for n,i in enumerate(lo):
            if i==0:
                pid2[n]=mean_pid2
                pid3[n]=mean_pid3



tmp_pid2 = data1.pid1.notnull() #finding the numbers and filtering out null values
tmp_pid3 = data1.pid2.notnull()
tmp_flow = data1.mfchiR.notnull()


isop_cyl = 13.277	#ppbv
mfchi_range = 100.	#sccm
mfchi_sccm = data1.mfchiR*(mfchi_range/5.)  #Don't really understand why this is happening yet

mfclo_range = 20.	#sccmmfclo_sccm = data1.mfcloR*(mfclo_range/5.)
mfclo_sccm = data1.mfcloR*(mfclo_range/5.)

dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = dil_fac*isop_cyl

if (cal == 'Y'):
        
        mfc_set = np.zeros((len(data1.mfclo)),dtype=bool)
        for i in range(1,len(data1.mfchi)):
            if (np.logical_and(np.logical_and(np.isfinite(data1.mfchi[i]),np.isfinite(data1.mfclo[i])),np.logical_or(data1.mfchi[i]!=data1.mfchi[i-1],data1.mfclo[i]!=data1.mfclo[i-1]))):
                    mfc_set[i] = 'True' # finding the places the mflo (isopropylene concentration) changes value
        cal_N = np.sum(mfc_set) #amount of True values in mfc_set
        
        cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid2_V','pid3_V','pid2_stddev','pid3_stddev'] #columns for the data frame
        
        
        cal_pts = [range(0,cal_N)] #index for the data frame
        
        delay = 300   #Delay at start of cal step
        cal_df = pd.DataFrame(index=cal_pts, columns=cal_cols) #creating the data frame for the cal data
        
        mfc_setS = data1.index[mfc_set]
        mfc_setS+=delay #placing the blue line where the mfclo value changes and adding the delay onto that
        
        mfc_setF = data1.index[mfc_set]
        mfc_setF = np.append(mfc_setF,len(data1.TheTime))
        mfc_setF = np.delete(mfc_setF,0)
        mfc_setF-=11      #Delay at end of cal step
        


for pt in range(0,cal_N):
    #check that the flows are the same at the start and end of the range over which you are averaging
        if (np.logical_and(data1.mfclo[mfc_setS[pt]]==data1.mfclo[mfc_setF[pt]],data1.mfchi[mfc_setS[pt]]==data1.mfchi[mfc_setF[pt]])): #if it is true that the green and blue line = each other
            
            tp_Isop = isop_mr[mfc_setS[pt]:mfc_setF[pt]] 
            
            tp_pid2 = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
            tp_pid3 = data1.pid2[mfc_setS[pt]:mfc_setF[pt]]
            
            cal_df.Isop[pt] = tp_Isop.mean()
            cal_df.Isop_stddev[pt] = tp_Isop.std()
            
            cal_df.pid2_V[pt] = tp_pid2.mean()
            cal_df.pid2_stddev[pt] = tp_pid2.std()
            
            cal_df.pid3_V[pt] = tp_pid3.mean()
            cal_df.pid3_stddev[pt] = tp_pid3.std()
            
            cal_df.StartT[pt] = data1.TheTime[mfc_setS[pt]]
            cal_df.EndT[pt] = data1.TheTime[mfc_setF[pt]]

##### PID 2
slope2,intercept2,r_value2,p_value2,std_err2=stats.linregress(cal_df.Isop,cal_df.pid2_V)
isop_fit = [0.,np.max(cal_df.Isop)]
pid2_fit = [intercept2,(np.max(cal_df.Isop)*slope2)+intercept2]
	
##### PID 3
slope3,intercept3,r_value3,p_value3,std_err3=stats.linregress(cal_df.Isop,cal_df.pid3_V)
isop_fit = [0.,np.max(cal_df.Isop)]
pid3_fit = [intercept3,(np.max(cal_df.Isop)*slope3)+intercept3]
	
	


if plots == 'Y':
    
        
                ##### PID 2
                pid2_avg = pd.rolling_mean(data1.pid1,300) #taking a mean of the data every 10 seconds
                
               	fig1 =plt.figure()
               	ax1 = fig1.add_subplot(111)
               	
           	pid2 = ax1.plot(data1.TheTime[tmp_pid2],data1.pid1[tmp_pid2], linewidth=3,color='r') #plotting the pid2 data against the time
           	pid2_10s = ax1.plot(data1.TheTime[tmp_pid2],pid2_avg[tmp_pid2], linewidth=3,color='b') #plotting the pid3 data against the time
           	
           	plt.ylabel("PID2 / V")
           	
           	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
           	
           	isop = ax2.plot(data1.TheTime[tmp_flow],isop_mr[tmp_flow], linewidth=1,color='g') #plotting the mfclo readings
           	
                ax2.plot([data1.TheTime[data1.index[mfc_setS]],data1.TheTime[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-') #plotting blue line
          	ax2.plot([data1.TheTime[data1.index[mfc_setF]],data1.TheTime[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-') #plotting green line
            
           	ax2.yaxis.tick_right()
           	ax2.yaxis.set_label_position("right")
           	
           	plt.ylabel("Isop / ppb")
           	plt.xlabel('Time / s', fontsize = 20)
           	
           	fig2 = plt.figure()
                
                plt.plot(cal_df.Isop,cal_df.pid2_V,"o")                
           	plt.plot(isop_fit,pid2_fit)
           	plt.ylabel('Pid2 / V', fontsize = 20)
           	plt.xlabel('[Isop] / ppb', fontsize = 20)
           	
           	
           	
           	##### PID 3
           	pid3_avg = pd.rolling_mean(data1.pid2,300)
               	fig1a = plt.figure()
               	ax1 = fig1.add_subplot(111)
           	pid3 = ax1.plot(data1.TheTime[tmp_pid3],data1.pid2[tmp_pid3], linewidth=3,color='r')
           	pid3_10s = ax1.plot(data1.TheTime[tmp_pid3],pid3_avg[tmp_pid3], linewidth=3,color='b')
           	plt.ylabel("PID3 / V")
           	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
           	isop = ax2.plot(data1.TheTime[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')
            
           	
                ax2.plot([data1.TheTime[data1.index[mfc_setS]],data1.TheTime[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
          	ax2.plot([data1.TheTime[data1.index[mfc_setF]],data1.TheTime[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')
            
           	ax2.yaxis.tick_right()
           	ax2.yaxis.set_label_position("right")
           	plt.ylabel("Isop / ppb")
           	plt.xlabel('Time / s', fontsize = 20)
           	
           	fig2a = plt.figure()
                plt.plot(cal_df.Isop,cal_df.pid3_V,"o")
           	plt.plot(isop_fit,pid3_fit)
           	plt.ylabel('Pid3 / V', fontsize = 20)
           	plt.xlabel('[Isop] / ppb', fontsize = 20)
                print '\n(graphs will appear in a new windows)\n'
                
plt.show()


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