import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time as time
import os as os
import scipy.optimize as opt

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

xerr = []
yerr3 = []
yerr2 = []

npid2 = []
npid3 = []
nISop = []

bss = '\ko'

questions = ''
cal = 'Y'
plots = ''
avg_0 = 'Y'

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
        
        try:
                zero_time = 100 # how long the zero at the end will be
        
        
                mfc_setF = data1.index[mfc_set]
                mfc_setF = np.append(mfc_setF,(mfc_setF[len(mfc_setF)-1]+zero_time))
                mfc_setF = np.delete(mfc_setF,0)
                mfc_setF-=11      #Delay at end of cal step
                    
                
                
                
                
                for pt in range(0,cal_N):
                #check that the flows are the same at the start and end of the range over which you are averaging
                    if (np.logical_and(data1.mfclo[mfc_setS[pt]]==data1.mfclo[mfc_setF[pt]],data1.mfchi[mfc_setS[pt]]==data1.mfchi[mfc_setF[pt]])):
                        
                            tp_Isop = isop_mr[mfc_setS[pt]:mfc_setF[pt]] # Takes slices of the data everytime the value of mfclo changes
                            tp_pid2 = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
                            tp_pid3 = data1.pid2[mfc_setS[pt]:mfc_setF[pt]]
                            tp_lo = data1.mfclo[mfc_setS[pt]:mfc_setF[pt]]
        
                            
                            
                            cal_df.Isop[pt] = tp_Isop.mean()
                            cal_df.Isop_stddev[pt] = tp_Isop.std()
                                
                            
                            cal_df.pid2_V[pt] = tp_pid2.mean()
                            cal_df.pid2_stddev[pt] = tp_pid2.std()
                    
                            
                            cal_df.pid3_V[pt] = tp_pid3.mean()
                            cal_df.pid3_stddev[pt] = tp_pid3.std()
                            
                            
                            cal_df.StartT[pt] = Time[mfc_setS[pt]]
                            cal_df.EndT[pt] = Time[mfc_setF[pt]]
                            
                            
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
                                mean_pid3 = np.nanmean(pid3_zeros)
                            
                                if (np.any(tp_lo)== 0):
                                    cal_df.pid2_V[pt] = mean_pid2
                                    cal_df.pid3_V[pt] = mean_pid3
        
        except (KeyError,IndexError):
                    print '\n\nCheck the length of zero_time at the end it may be too long\n\n'  
                                    
        cal_df = cal_df.drop_duplicates(subset = 'pid2_V')        
        cal_df = cal_df.dropna()                    
        cal_df.index = np.arange(len(cal_df))
    
        for i in range(len(cal_df)):
            xerr.append(cal_df.Isop_stddev[i]/np.sqrt(889))
                
        for i in range(len(cal_df)):
            yerr2.append(cal_df.pid2_stddev[i]/np.sqrt(889))
    
        for i in range(len(cal_df)):
            yerr3.append(cal_df.pid3_stddev[i]/np.sqrt(889))
                
            if (cal == 'Y'):
        
                cal_df.Isop = cal_df.Isop.astype(float) 
                cal_df.pid2_V = cal_df.pid2_V.astype(float)                
                cal_df.pid3_V = cal_df.pid3_V.astype(float)
                        
                ############# Fitting the data
                #######
                
                
                def linear_fit(slope, intercept, x):
                    return (slope*x)+intercept
        
                
                ydata2 = cal_df.pid2_V        
                ydata3 = cal_df.pid3_V
                
                xdata = cal_df.Isop
        
                        
                isop_fit = [0.,np.max(cal_df.Isop)]
                                    
                        ##### PID 2
               	slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr2)
               	pid2_fit = [slope_intercept2[0],(np.max(cal_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
               	
               	##### PID 3
               	slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
               	pid3_fit = [slope_intercept3[0],(np.max(cal_df.Isop)*slope_intercept3[1])+slope_intercept3[0]]
               	
    
      
           	'''il3.append(intercept3)
           	sl3.append(slope3)'''

	


	
    except IOError:
        files2.append(filenamei)
    except AttributeError:
        pass
        
    datad = {'Intercepts': [il2,il3], 'Slopes':[sl2,sl3], 'R_Values':[r2,r3]}
    frame_cals = pd.DataFrame(datad, index = ['Pid_2', 'Pid_3'])
