import pandas as pd
import numpy as np
import scipy.optimize as opt
import datetime
from time import strftime
import os
import matplotlib.pyplot as plt


bad_files = []
##################################################### Defining Functions For Use Later #################################################
####### Checks if the files exsist and returns a list of files that do exist

def FileChecker(path,month1, month2, day1,day2,number_of_files):
    filesl=[]
    pfl = []
    month_now = strftime('%m')
    month_now = int(month_now)
    
    month2 = month2+1

    day2 = day2+1
    
    if month1 < 7:
        month1 = 7
    if month2 > 12:
        month2 = 12
    if month2 > month_now:
        month2 = month_now+1
    if day1 < 0:
        day1 = 0
    if day2 > 31:
        day2 = 31
    
    for month in range(month1, month2):
        if month < 10:
            month = '0'+str(month)
        path1 = path + '\\2015'+str(month)+'\\d2015'+str(month)
        for day in range (day1,day2):
            if day < 10:
                day = '0'+str(day)
            path2 = path1 + str(day)
            for filenumber in range(0,number_of_files):
                pfl.append(path2+'_0'+str(filenumber))

        
    filesl = []
    for i in pfl:
        if os.path.exists(i):
            if os.path.getsize(i) < file_size_limit: 
                filesl.append(i)
      

            
    return filesl
    
    
        
#To convert timestamps to a string
def timeconverter(T):
    #	print T
   	return (datetime.datetime.strptime(T,"%y-%m-%d-%H-%M-%S-%f"))


#Splices list at indexes given by 2 lists
def list_multisplicer(l1st,start_inidexes,end_indexes):
    new_lt = []
    for i in range(0,len(start_inidexes)):
        first = start_inidexes[i]
        last = end_indexes[i]
        for pt in range(0,len(l1st)):
            if pt >=first and pt <=last:
                new_lt.append(l1st[pt])
    return new_lt
    
def list_multisplicer_listsout(l1st,start_indexes,end_indexes):
            new_lt = []
            for i in range(0,len(start_indexes)):
                segments = []
                first = start_indexes[i]
                last = end_indexes[i]
                for pt in range(0,len(l1st)):
                    if pt >=first and pt<=last:
                        segments.append(l1st[pt])
                new_lt.append(segments)
                    
            return new_lt
             
                   
#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept

# prints the mfc_setS and mfc_setF values in a nice, easily 
def troubleshooter(x,y):
            differences = []
            
            for i in range(0,len(y)):    
                print 'Cal number = ',i+1
                print 'mfc_setS = ',x[i]
                print 'mfc_setF = ',y[i]
                print 'difference = ',y[i]-x[i]
                print '\n'
                differences.append(y[i]-x[i])
                
            return differences

# Converts a timestamp to a list
def timestamp_convert(timestamp):
    
    if type(timestamp) == pd.tslib.Timestamp:
        timestamp = str(timestamp)
        
        
    elif len(timestamp.split('-')) >= 5:
        c = timestamp.split('-')
        return c
        
    b = timestamp.split('-')
    year = b[0]
    month = b[1]
    c = b[2].split(' ')
    day = c[0]
    d = c[1].split(':')
    hour = d[0]
    minute = d[1]
    e = d[2].split('.')
    second = e[0]
    try:
        millisecond = e[1]
    except IndexError:
        pass
        
    time_list_final = [year,month,day,hour,minute,second]
    try:
        time_list_final.append(millisecond)
    except UnboundLocalError:
        pass
    return time_list_final


############################################################################################################################################################


pid3_correction = 2.59E-05
pid4_correction = 1.36E-5
pid5_correction = 3.03E-5


pd.set_option('precision',9)

cal_stuff = 'Y'
if cal_stuff == 'Y':
    questions = 'Y'
    plots = 'Y'
    cal = 'Y'
else:
    questions = ''
    plots = ''
    cal = ''

data_point_length = 300 # how many data points used for the cals

humid_correct = ''

pid_2_on = ''

pid_3_on = 'Y'

pid_4_on = 'Y'

pid_5_on = 'Y'


Savename = raw_input('What would you like to name the slope file? ')


slopesfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Slope Values files\\'+Savename.title()+'.txt','w')
slopesfile.write('The Time\tSlope 3\tSlope Error 3\tSlope 4\tSlope Error 4\tSlope 5\tSlope Error 5\n')

if humid_correct == 'Y':
    slopescorrectedfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Slope Values files\\'+Savename.title()+' Corrected.txt','w')
    slopescorrectedfile.write('The Time\tSlope 3\tSlope Error 3\tSlope 4\tSlope Error 4\tSlope 5\tSlope Error 5\n')


path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files'

filesl = FileChecker(path,7,9,0,30,15)

date = 907
    
    
  
     
      
for filei in filesl:
    try:
        date = filei[-7:-3]

        xerr = []
        yerr2 = []
        yerr3 = []
        yerr4 = []
        yerr5 = []
        
        npid2 = []
        npid3 = []
        npid4 = []
        npid5 = []
        nISop = []   
            
        dataL = pd.read_csv(filei)
        
        ##   Sorting out the Times   ##
        tIMe = dataL.TheTime
        
        TimeL = dataL.TheTime-dataL.TheTime[0]
        TimeL*=60.*60.*24.
        
        dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
        T1 = pd.datetime(1899,12,30,0)
        T2 = pd.datetime(1970,01,01,0)
        offset=T1-T2
        dataL.TheTime+=offset
        
        #### Relative Humidity ###
        
        if int(date) >= 903:
            RH = dataL.RH
            RH /=4.9
            RH -= 0.16
            RH /= 0.0062
            RH *= 100
            RH /= 103
        
        pid_2_on = ''

        pid_3_on = 'Y'
        
        pid_4_on = 'Y'
        
        pid_5_on = 'Y'
        
                    


        if int(date) < 904:
            pid_5_on = ''
            try:
                pid2d = dataL.pid1.fillna(pd.rolling_mean(dataL.pid1, 7, min_periods=1).shift(-3))
            except AttributeError:
                pid_2_on = ''  
            try:   
                pid3d = dataL.pid2.fillna(pd.rolling_mean(dataL.pid2, 7, min_periods=1).shift(-3))
            except AttributeError:
                pid_3_on = ''  
                
            try:    
                pid4d = dataL.pid3.fillna(pd.rolling_mean(dataL.pid3, 7, min_periods=1).shift(-3))
            except AttributeError:
                pid_4_on = ''    
                    
        if int(date) >= 904:
            pid_2_on = ''
            try:
                pid5d = dataL.pid5.fillna(pd.rolling_mean(dataL.pid5, 7, min_periods=1).shift(-3))
            except AttributeError:
                pid_5_on = ''    

                
            try:   
                pid3d = dataL.pid3.fillna(pd.rolling_mean(dataL.pid3, 7, min_periods=1).shift(-3))
            except AttributeError:
                pid_3_on = ''     
                    
            try:   
                pid4d = dataL.pid4.fillna(pd.rolling_mean(dataL.pid4, 7, min_periods=1).shift(-3))
            except AttributeError:
                pid_4_on = ''    
        
        
        if pid_2_on == 'Y':
            tmp_pid2 = pid2d.notnull()
        
        if pid_3_on == 'Y':
            tmp_pid3 = pid3d.notnull()
        
            
        if pid_4_on == 'Y':
            tmp_pid4 = pid4d.notnull()
        
        if pid_5_on == 'Y':
            tmp_pid5 = pid5d.notnull()
        
        
            
            
            
        tmp_flow = dataL.mfchiR.notnull()
            
        isop_cyl = 13.277	#ppbv
        mfchi_range = 100.	#sccm
        mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
        
        mfclo_range = 20.	#sccm
        mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
        
        dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
        isop_mr = dil_fac*isop_cyl
        
        
    
        dataL['mfchi'] = [(5+((0*i)+1)) for i in range(0,len(dataL))] 
        dataL = dataL.fillna({'mfchi':5})
        
        #############################
        ## Signal vs Isop for calibration experiments
        
        if (cal == 'Y'):
            
            mfc_set = np.zeros((len(dataL.mfclo)),dtype=bool)
            for i in range(1,len(dataL.mfchi)):
                if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i-1],dataL.mfclo[i]!=dataL.mfclo[i-1]))):
                        mfc_set[i] = "True"
                        
            cal_N = np.sum(mfc_set) # number of changes in value for mfclo
                
            cal_pts = [range(0,cal_N)]
            
            
            
            
            
            end_cut_off = 10
            
        
        
            
            mfc_setF = dataL.index[mfc_set]
            
            mfc_setF = mfc_setF[1:]
            mfc_setF -= end_cut_off #taking some data points away from the end to give a bit of a tolerance
            
            
            mfc_setS = [i-data_point_length for i in mfc_setF]    
        
                    
            S = mfc_setS
            F = mfc_setF
        
            cal_cols_new = ['Start Times','End Times','Isop','Isop Stddev']
            cal_cols_c = []
            
            if pid_2_on == 'Y':
                cal_cols_new.append('Pid2 Voltage')
                cal_cols_new.append('Pid2 Stddev')
                if humid_correct == 'Y':
                    cal_cols_c.append('Pid2 Voltage c')
    
                
            if pid_3_on == 'Y':
                cal_cols_new.append('Pid3 Voltage')
                cal_cols_new.append('Pid3 Stddev')
                if humid_correct == 'Y':
                    cal_cols_c.append('Pid3 Voltage c')
    
                        
            if pid_4_on == 'Y':
                cal_cols_new.append('Pid4 Voltage')
                cal_cols_new.append('Pid4 Stddev')
                if humid_correct == 'Y':
                    cal_cols_c.append('Pid4 Voltage c')
            
            if pid_5_on == 'Y':
                cal_cols_new.append('Pid5 Voltage')
                cal_cols_new.append('Pid5 Stddev')
                if humid_correct == 'Y':
                    cal_cols_c.append('Pid5 Voltage c')            
                
    
                        
            cal_df = pd.DataFrame(index=range(0,len(S)), columns=cal_cols_new)
        
            
            if pid_2_on == 'Y':
                pid2_chunks = list_multisplicer_listsout(pid2d,mfc_setS,mfc_setF)
            
                pid2_avgs = [sum(i)/len(i) for i in pid2_chunks]
                pid2_stds = [np.nanstd(i) for i in pid2_chunks]
                
                cal_df['Pid2 Voltage'] = pid2_avgs
                cal_df['Pid2 Stddev'] = pid2_stds
                
            if pid_3_on == 'Y':
                
                pid3_chunks = list_multisplicer_listsout(pid3d,mfc_setS,mfc_setF)
    
                
                pid3_avgs = [sum(i)/len(i) for i in pid3_chunks]
                pid3_stds = [np.nanstd(i) for i in pid3_chunks]
                
                cal_df['Pid3 Voltage'] = pid3_avgs
                cal_df['Pid3 Stddev']= pid3_stds 
                
            if pid_4_on =='Y':
                pid4_chunks = list_multisplicer_listsout(pid4d,mfc_setS,mfc_setF)
                
                pid4_avgs = [sum(i)/len(i) for i in pid4_chunks]
                pid4_stds = [np.nanstd(i) for i in pid4_chunks] 
            
                cal_df['Pid4 Voltage'] = pid4_avgs
                cal_df['Pid4 Stddev'] = pid4_stds
    
                
            if pid_5_on =='Y':
                pid5_chunks = list_multisplicer_listsout(pid5d,mfc_setS,mfc_setF)
                
                pid5_avgs = [sum(i)/len(i) for i in pid5_chunks]
                pid5_stds = [np.nanstd(i) for i in pid5_chunks] 
            
                cal_df['Pid5 Voltage'] = pid5_avgs
                cal_df['Pid5 Stddev'] = pid5_stds
                
                
            isop_chunks = list_multisplicer_listsout(isop_mr,mfc_setS,mfc_setF)
            
            if humid_correct == 'Y':
                RH_chunks = list_multisplicer_listsout(RH,mfc_setS,mfc_setF)
                RH_avgs = [sum(i)/len(i) for i in RH_chunks]
                cal_df['RH'] = RH_avgs
                
            isop_avgs = [sum(i)/len(i) for i in isop_chunks]
            isop_stds = [np.nanstd(i) for i in isop_chunks]
            
            
            
            start_times = [TimeL[i] for i in mfc_setS]
            end_times = [TimeL[i] for i in mfc_setF]
            
        
            
            cal_df['Isop'] = isop_avgs
            cal_df['Isop Stddev'] = isop_stds
            cal_df['Start Times'] = start_times
            cal_df['End Times'] = end_times
        
            
            cal_df = cal_df.dropna()
            cal_df.index = range(0,len(cal_df))
        
        
            ########################## Zero Averaging #########################
            
            
            isop_zero_indexes = []
            for i in range(0,len(cal_df.Isop)):
                if cal_df.Isop[i] < 0.2:
                    isop_zero_indexes.append(i)
        
            
            
            if pid_2_on:
                cal_df['Pid2 Voltage'][isop_zero_indexes] = np.nanmean(cal_df['Pid2 Voltage'][isop_zero_indexes])
        
            if pid_3_on:
                x3 = cal_df['Pid3 Voltage'][isop_zero_indexes]
                cal_df['Pid3 Voltage'][isop_zero_indexes] = sum(x3)/len(x3)
                
            if pid_4_on:
                x4 = cal_df['Pid4 Voltage'][isop_zero_indexes]
                cal_df['Pid4 Voltage'][isop_zero_indexes] = sum(x4)/len(x4)
                
            if pid_5_on:
                x5 = cal_df['Pid5 Voltage'][isop_zero_indexes]
                cal_df['Pid5 Voltage'][isop_zero_indexes] = sum(x5)/len(x5)
                
            
            if pid_2_on:
                cal_df = cal_df.drop_duplicates(subset = 'Pid2 Voltage')
            elif pid_3_on:
                cal_df = cal_df.drop_duplicates(subset = 'Pid3 Voltage')
            elif pid_4_on:
                cal_df = cal_df.drop_duplicates(subset = 'Pid4 Voltage')
            elif pid_5_on:
                cal_df = cal_df.drop_duplicates(subset = 'Pid5 Voltage')
            
            
            cal_df.index = range(0,len(cal_df))
            
            
            ########################## ########################## ########################## 
            
            ########## Tidying up and fitting #########
            
            if humid_correct == 'Y':
                cal_dfc = pd.DataFrame(index=range(0,len(cal_df)), columns=cal_cols_c)
            
            
            isop_fit = [0.,np.max(cal_df.Isop)]    
            
            if pid_2_on:
    
                for i in range(len(cal_df)):
                        yerr2.append(cal_df['Pid2 Stddev'][i]/np.sqrt(len(pid2_chunks[i+1])))
                        
                xdata = cal_df.Isop
                ydata2 = cal_df['Pid2 Voltage'] 
                slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr2)
                pid2_fit = [slope_intercept2[0],(np.max(cal_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
                
                perr2 = np.sqrt(np.diag(pcov2))
                Intercept_error2 = perr2[0]/np.sqrt(cal_N)
                Slope_Error2 = perr2[0]/np.sqrt(cal_N)        
                
                        
            if pid_3_on: 
                
                if humid_correct == 'Y':
                    cal_dfc['Pid3 Voltage c'] = cal_df['Pid3 Voltage']-cal_df['RH']*pid3_correction
                        
                
                for i in range(len(cal_df)):
                    yerr3.append(cal_df['Pid3 Stddev'][i]/np.sqrt(len(pid3_chunks[i+1]))) 
                    
                xdata = cal_df.Isop     
                ydata3 = cal_df['Pid3 Voltage']
                
                if humid_correct == 'Y':
                    ydata3c = cal_dfc['Pid3 Voltage c']
                
                
                slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
                if humid_correct == 'Y':
                    slope_intercept3c,pcov3c = opt.curve_fit(linear_fit, xdata, ydata3c, sigma = yerr3)        
                
                perr3 = np.sqrt(np.diag(pcov3))    
                Intercept_error3 = perr3[0]/np.sqrt(cal_N)
                Slope_Error3 = perr3[0]/np.sqrt(cal_N)  
                
                if humid_correct == 'Y':
                    perr3c = np.sqrt(np.diag(pcov3c))    
                    Intercept_error3c = perr3c[0]/np.sqrt(cal_N)
                    Slope_Error3c = perr3c[0]/np.sqrt(cal_N)      
                
                    
            if pid_4_on: 
                if humid_correct == 'Y':
                    cal_dfc['Pid4 Voltage c'] = cal_df['Pid4 Voltage']-cal_df['RH']*pid4_correction
    
                for i in range(len(cal_df)):
                    yerr4.append(cal_df['Pid4 Stddev'][i]/np.sqrt(len(pid4_chunks[i+1])))
                    
                    
                xdata = cal_df.Isop
                ydata4 = cal_df['Pid4 Voltage']
                if humid_correct == 'Y':
                    ydata4c = cal_dfc['Pid4 Voltage c']
                
                slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
                if humid_correct == 'Y':
                    slope_intercept4c,pcov4c = opt.curve_fit(linear_fit,xdata,ydata4c,sigma = yerr4)
                
                perr4 = np.sqrt(np.diag(pcov4))    
                Intercept_error4 = perr4[0]/np.sqrt(cal_N)
                Slope_Error4 = perr4[0]/np.sqrt(cal_N)
                    
                if humid_correct == 'Y':
                    perr4c = np.sqrt(np.diag(pcov4c))    
                    Intercept_error4c = perr4c[0]/np.sqrt(cal_N)
                    Slope_Error4c = perr4c[0]/np.sqrt(cal_N)
    
            if pid_5_on: 
                if humid_correct == 'Y':
                    cal_dfc['Pid5 Voltage c'] = cal_df['Pid5 Voltage']-cal_df['RH']*pid5_correction
                    
                for i in range(len(cal_df)):
                    yerr5.append(cal_df['Pid5 Stddev'][i]/np.sqrt(len(pid5_chunks[i+1])))
                    
                xdata = cal_df.Isop
                ydata5 = cal_df['Pid5 Voltage']
                if humid_correct == 'Y':
                    ydata5c = cal_dfc['Pid5 Voltage c']
                        
                
                slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr5)
                
                if humid_correct == 'Y':
                    slope_intercept5c,pcov5c = opt.curve_fit(linear_fit, xdata, ydata5c, sigma = yerr5)
                
                perr5 = np.sqrt(np.diag(pcov5))    
                Intercept_error5 = perr5[0]/np.sqrt(cal_N)
                Slope_Error5 = perr5[0]/np.sqrt(cal_N)
                
                if humid_correct == 'Y':
                    perr5c = np.sqrt(np.diag(pcov5c))    
                    Intercept_error5c = perr5c[0]/np.sqrt(cal_N)
                    Slope_Error5c = perr5c[0]/np.sqrt(cal_N)
                
                                                                
            print '\n',filei[-7:],'\n'
            
    
    
            
    
            slopesfile.write(str(tIMe[len(dataL.TheTime)/2])+'\t')
            if pid_3_on == 'Y':
                slopesfile.write(str(slope_intercept3[1]) + '\t' + str(Slope_Error3) + '\t')
            
            if pid_4_on == 'Y':
                slopesfile.write(str(slope_intercept4[1]) + '\t' + str(Slope_Error4) + '\t')
            
            if pid_5_on == 'Y':
                slopesfile.write(str(slope_intercept5[1]) + '\t' + str(Slope_Error3))
            slopesfile.write('\n')
            
            if humid_correct == 'Y':
            
                slopescorrectedfile.write(str(tIMe[len(dataL.TheTime)/2])+'\t')
                slopescorrectedfile.write(str(slope_intercept3c[1]) + '\t' + str(Slope_Error3c) + '\t')
                
        
                slopescorrectedfile.write(str(slope_intercept4c[1]) + '\t' + str(Slope_Error4c) + '\t')
                
        
                slopescorrectedfile.write(str(slope_intercept5c[1]) + '\t' + str(Slope_Error3c) + '\n')
    except:
        bad_files.append(filei)
        
slopesfile.close()
if humid_correct == 'Y':
    slopescorrectedfile.close()
