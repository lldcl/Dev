import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
import time
import os

'''This Code is giving an IOError need to fix'''

#creating a list for the values for data

il2 = []
il3 = []
sl2 = []
sl3 = []
r2 = []
r3 = []

p = []
filesl=[]
files2 = []
pfl = []

bss = '\ko'

questions = ''
cal = 'Y'
plots = ''


pd.set_option('precision',7)





print 'IF THIS DOES\'NT WORK CHECK THE PATH'
path = 'E:\Bursary thing\PID Data\Organised and or Edited'


filesl=[]
pfl = []
day = time.strftime('%d')
day = int(day)


bss = '\ko'
for i in range (8,day+1):
    if i<10:
        path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Organised_Data_Files'+bss[0]+'07-0'+str(i)
    else:
        path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Organised_Data_Files'+bss[0]+'07-'+str(i)
        
    for pt in range(1,35):
        if i<10:
            filename = '\d2015070'+str(i)+'_0'+str(pt)
        else:
            filename = '\d201507'+str(i)+'_0'+str(pt)
        
        pfl.append(path+filename)
     


p = []
for i in range (0,len(pfl)):   
    p.append(os.path.exists(pfl[i]))

n=0    
for i in range(0,len(pfl)):
    if p[i] == True:
        filesl.append(pfl[i])
        
        

fig1 = plt.figure()        
ax1 = fig1.add_subplot(111)


for i in range(0,len(filesl)):
    filenamei = filesl[i]


    data1 = pd.read_csv(filenamei, engine = 'c')
    

    
    try:
        
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
        
        if cal == 'Y':
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
           	
           	print intercept2
           	
           	il2.append(intercept2)
           	print 'peter'
           	sl2.append(slope2)           	
           	r2.append(r_value2)
           	           	           	           	
           	##### PID 3
           	slope3,intercept3,r_value3,p_value3,std_err3=stats.linregress(cal_df.Isop,cal_df.pid3_V)
           	isop_fit = [0.,np.max(cal_df.Isop)]
           	pid3_fit = [intercept3,(np.max(cal_df.Isop)*slope3)+intercept3]
           	
           	il3.append(intercept3)
           	sl3.append(slope3)
           	r3.append(r_value3)
	


	
    except IOError:
        files2.append(filenamei)
    except AttributeError:
        pass
        
    datad = {'Intercepts': [il2,il3], 'Slopes':[sl2,sl3], 'R_Values':[r2,r3]}
    frame_cals = pd.DataFrame(datad, index = ['Pid_2', 'Pid_3'])
