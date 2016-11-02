import os
from time import strftime
import pandas as pd
import numpy as np
import scipy.optimize as opt
from operator import itemgetter

pid_3_on = 'Y'
pid_4_on = 'Y'
pid_5_on = 'Y'

timing = 75 #If the code isn't picking out all the plateaus then adjust this.

shifter = 75 #You can change this if the code cals at dodgy points

no_of_data_points = 2000 # If you want to cal with more data for each point adjust this. (If the code gives a ValueError becuase min() arg is an empty sequence lower this)
bad_cal_length = no_of_data_points

RHcalpointfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH Cal Data Points.txt','a')
RHcalfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH cals.txt','a')





### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation
def cal_point_ammender(data_set,bad_cal_length,S,F):
    shifter = (len(dataL)*1)/(20*(len(S)+2)*5)
    
    Snew = np.zeros(len(S))
    Fnew = np.zeros(len(F))    
    for i in xrange(0,len(S)):

        orig_std = np.nanstd(data_set[S[i]:F[i]])
        
        if orig_std > 0.7:
            S[i] = F[i] - bad_cal_length

        
        left_shift_stds = {k:[np.nanstd(data_set[S[i]-(k*shifter):F[i]-(k*shifter)])] for k in xrange(0,20)}
        nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
        for t in nanL:
            del(left_shift_stds[t])
            
        minPairL = min(left_shift_stds.iteritems(), key=itemgetter(1))


        
        if minPairL[1][0] < orig_std:
            
            Snew[i] = S[i] - minPairL[0]*shifter
            Fnew[i] = F[i] - minPairL[0]*shifter

        else:
            
            Snew[i] = S[i]
            Fnew[i] = F[i]
               
    if Snew[0] < 0:
        SF = negative_remover(Snew,Fnew)
        Snew = SF[0]
        Fnew = SF[1]
        
    return Snew,Fnew      
        
        
####### Checks if the files exsist and returns a list of files that do exist
def FileChecker(path,month1, month2, day1,day2,number_of_files,file_size_limit):
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
    
    for month in xrange(month1, month2):
        if month < 10:
            month = '0'+str(month)
        path1 = path+'\\d2015'+str(month)
        for day in xrange (day1,day2):
            if day < 10:
                day = '0'+str(day)
            path2 = path1 + str(day)
            for filenumber in xrange(0,number_of_files):
                pfl.append(path2+'_0'+str(filenumber))

        
    filesl = []
    for i in pfl:
        if os.path.exists(i):
            if os.path.getsize(i) < file_size_limit: 
                filesl.append(i)
      

            
    return filesl
    
    




############## ############## ##############  Defining Useful Functions ############## ############## ############## 
   
###### Removes the negative values if they appear at the begining of the selection indexes (mfc_setS and mfc_setF)
def negative_remover(list1,list2):
    negative_removerF = []
    negative_removerS = []

    
    if list1[0] < 0:
        for i in xrange(0,len(list1)):
            if list2[i]<0:
                negative_removerF.append(i)
            if list1[i] < 0:
                negative_removerS.append(i)

        if negative_removerF < negative_removerS:
            negative_removerF = max(negative_removerS)
            negative_removerS = max(negative_removerS)+1         
        
            A = [0] + list1[negative_removerS:]
            B = list2[negative_removerF:]
        else:
            A = list1[max(negative_removerS)+1:]
            B = list2[max(negative_removerF)+1:]
        return A,B        


# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))

#Removes Duplicates
def remove_duplicates(l):
    return list(set(l))

#Splices list at indexes given by 2 lists
def list_multisplicer(l1st,start_inidexes,end_indexes):
    new_lt = []
    for i in xrange(0,len(start_inidexes)):
        first = start_inidexes[i]
        last = end_indexes[i]
        for pt in xrange(0,len(l1st)):
            if pt >=first and pt <=last:
                new_lt.append(l1st[pt])
    return new_lt
    
def list_multisplicer_listsout(l1st,start_indexes,end_indexes):
            new_lt = []
            for i in xrange(0,len(start_indexes)):
                segments = []
                first = start_indexes[i]
                last = end_indexes[i]
                for pt in xrange(0,len(l1st)):
                    if pt >=first and pt<=last:
                        segments.append(l1st[pt])
                new_lt.append(segments)
                    
            return new_lt


#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept
                
                                    
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
    
    
    
############## ############## ############## ############## ############## ############## ############## ############## 
#FileChecker(path,month1, month2, day1,day2,number_of_files,file_size_limit)
filesl = FileChecker('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals',9,10,0,30,10,25386763L)

date = 911
try:
    data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH cals.txt',sep ='\t')

except ValueError:
    RHcalfile.write('Filename\tIsop\tIsop Error\tPid3 Slope Value\tPid3 Slope Error\tPid4 Slope Value\tPid4 Slope Error\tPid5 Slope Value\tPid5 Slope Error\n')
    RHcalpointfile.write('Filename\tIsop\tIsop Error\tRH\tRH Error\tPid3 Voltage\tPid3 Voltage Error\tPid4 Voltage\tPid4 Voltage Error\tPid5 Voltage\tPid5 Voltage Error\n')

already_read_checker = []
print '\nChecking for any cals that are already recorded...\n'
for tkm in  xrange(0,len(filesl)):

    filenumber = filesl[tkm][-12:]
    
    try:
        data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH cals.txt', sep = '\t')                       
        filename = str(filesl[tkm][-12:])
    
        
        if not filename in set(data.Filename):
            already_read_checker.append(tkm)
    except:
        already_read_checker = [i for i in xrange(0,len(filesl))] 

        
if already_read_checker == []:
    print 'Sorry no more cals to add in that range of files, you could try expanding the range of files I check.' 
else:
    x = len(already_read_checker)
    if x > 1:
        print 'Okie Doke adding %s extra data points then' % str(x)
    if x == 1:
        print 'Okie Doke adding 1 extra data point then'
        
n = 0
for qwe in already_read_checker:
                    
    dataL = pd.read_csv(filesl[qwe])                       

    
    filenumber = filesl[qwe][-12:]
############## ##############  Data Read ############## ##############     

    isop_cyl = 13.277	#ppbv
    mfchi_range = 100.	#sccm
    mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
    
    mfclo_range = 20.	#sccm
    mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
    
    dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
    isop_mr = dil_fac*isop_cyl
    
    Isop = isop_mr
    mfcloR_error = (np.nanstd(dataL.mfcloR)/np.sqrt(len(dataL)))
    mfchiR_error = (np.nanstd(dataL.mfchiR)/np.sqrt(len(dataL)))
    Isop_Error = (np.sqrt(mfchi_range/5.*(mfcloR_error**2))+(np.sqrt(mfclo_range*(mfcloR_error**2))+np.sqrt(mfchi_range/5.*(mfcloR_error**2))))
    Isop = np.nanmean(Isop)
    if int(date) < 904:
        pid_5_on = ''
        try:
            pid2d = nan_helper(dataL.pid1,10,3)
        except AttributeError:
            pid_2_on = ''  
        try:   
            pid3d = nan_helper(dataL.pid2,10,3)
        except AttributeError:
            pid_3_on = ''  
        try:    
            pid4d = nan_helper(dataL.pid2,10,3)    
        except AttributeError:
            pid_4_on = ''    
        
    if int(date) >= 904:
        pid_2_on = ''
        try:
            pid5d = nan_helper(dataL.pid5,10,3)    
        except AttributeError:
            pid_5_on = ''     
        try:   
            pid3d = nan_helper(dataL.pid3,10,3)         
        except AttributeError:
            pid_3_on = ''           
        try:   
            pid4d = nan_helper(dataL.pid4,10,3) 
        except AttributeError:
                    pid_4_on = '' 
                    
    ############## ############## ############## ############## ############## 
    
    
    
                
    ############## Formatting the Time ############## ##############   
    TimeL = dataL.TheTime-dataL.TheTime[0]
    TimeL*=60.*60.*24.
    
    dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
    T1 = pd.datetime(1899,12,30,0)
    T2 = pd.datetime(1970,01,01,0)
    offset=T1-T2
    dataL.TheTime+=offset
    ############## ############## ############## ############## 
    
    
    
    
    
    ############## Converting RH Voltage to RH % ############## 
    dataL.RH = nan_helper(dataL.RH,10,3)
    RH = dataL.RH
    RH /=4.96
    RH -= 0.16
    RH /= 0.0062
    RH /= (1.0546-(0.00216*dataL.Temp))
    ############## ############## ############## ############## 
    
    
    
    
    
    ############## ############## Trying to find where the RH changes Drastically (for new cal Points) ############## ############## 
    
    RH_set = []
    
    sensitivty_mean = np.nanmean([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)])
    sesnitivty_std = np.nanstd([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)])
    
    for i in xrange(0,len(RH)-timing):
        if abs(RH[i]-RH[i+timing]) > sensitivty_mean+(0.35*sesnitivty_std):
            RH_set.append(i)
    
    Setters = []
    for i in xrange(0,len(RH_set)-1):
        if abs(RH_set[i]-RH_set[i+1]) > no_of_data_points/2:
            Setters.append(i)
    
    RH_setF = [RH_set[i] for i in Setters]
    
    RH_setS = [i-no_of_data_points for i in RH_setF]
    
    if RH_setS[0]<0:
        SF = negative_remover(RH_setS,RH_setF)
        S = SF[0]
        F = SF[1]   
    else:
        S = RH_setS
        F = RH_setF
        
        
    
    
    
    
    RH_stds = [np.nanstd(RH[S[i]:F[i]]) for i in xrange(0,len(S))]
    SF = cal_point_ammender(RH,bad_cal_length,S,F)
    
    for i in xrange(0,len(S)):
    

            orig_std = np.nanstd(RH[S[i]:F[i]])
            
            if np.nanstd(RH[S[i]:F[i]]) > 0.7:
                S[i] = F[i] - bad_cal_length
    
            
            left_shift_stds = {}
            for k in xrange(1,20):
                x_shiftL = k*shifter
                left_shift_stds[k] = np.nanstd(RH[S[i]-x_shiftL:F[i]-x_shiftL])
            dogel = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
            for t in dogel:
                del(left_shift_stds[t])
                
            minPairL = min(left_shift_stds.iteritems(), key=itemgetter(1))
    
    
            right_shift_stds = {}
            for k in xrange(1,20):
                x_shiftR = k*shifter
                right_shift_stds[k] = np.nanstd(RH[S[i]+x_shiftR:F[i]+x_shiftR])
                
            dogeR = [q for q in right_shift_stds if np.isnan(right_shift_stds[q])]
            for t in dogeR:
                del(right_shift_stds[t])
                
            minPairR = min(right_shift_stds.iteritems(), key=itemgetter(1))
    
            
            
            if minPairL[1] < orig_std and minPairL[1] < minPairR[1]:
                S[i] = S[i]-minPairL[0]*shifter
                F[i] = F[i]-minPairL[0]*shifter
            elif minPairR[1] < orig_std and minPairR[1] < minPairL[1]:
                S[i] = S[i]+minPairR[0]*shifter
                F[i] = F[i]+minPairR[0]*shifter        
    
    
            
    if S[0] < 1:       
        SF = negative_remover(S,F)
        S = SF[0]
        F = SF[1]   
        
            
    diff = [F[i]-S[i] for i in xrange(len(F))]   
    
    ############## ############## ############## ############## ############## ############## ############## ############## 
    
    ############## ############## Deciding the columns in cal_df and chunking the data ############## ############## 
    RH_chunks = list_multisplicer_listsout(RH,S,F)
    
    
    cal_cols = ['Start Times','End Times','RH','RH Stddev','Cal Length']
    
    
    if pid_5_on == 'Y':
        
                pid5_chunks = list_multisplicer_listsout(pid5d,S,F)
                
                cal_cols.append('Pid5 Voltage')
                cal_cols.append('Pid5 Stddev')
                
    if pid_3_on == 'Y':
            
            pid3_chunks = list_multisplicer_listsout(pid3d, S, F)
        
            cal_cols.append('Pid3 Voltage')
            cal_cols.append('Pid3 Stddev')
    
    if pid_4_on == 'Y':
            
            pid4_chunks = list_multisplicer_listsout(pid4d, S, F)
            
            cal_cols.append('Pid4 Voltage')
            cal_cols.append('Pid4 Stddev')
            
    ############## ############## ############## ############## ############## ############## ##############              
                
                
                
                
    ############## ############## Finding averages and stds of the chunks ############## ##############              
    cal_df = pd.DataFrame(index=xrange(0,len(S)), columns=cal_cols)
    
    for i in xrange(0,len(cal_df)):
        cal_df.RH[i] = np.nanmean(RH_chunks[i])
        cal_df['RH Stddev'][i] =np.nanstd(RH_chunks[i])
            
        if pid_3_on == 'Y':
            cal_df['Pid3 Voltage'][i] = np.nanmean(pid3_chunks[i])
            cal_df['Pid3 Stddev'][i] = np.nanstd(pid3_chunks[i])
            
        if pid_4_on == 'Y':
            cal_df['Pid4 Voltage'][i] = np.nanmean(pid4_chunks[i])
            cal_df['Pid4 Stddev'][i] = np.nanstd(pid4_chunks[i])
            
        if pid_5_on == 'Y':
            cal_df['Pid5 Voltage'][i] = np.nanmean(pid5_chunks[i])
            cal_df['Pid5 Stddev'][i] = np.nanstd(pid5_chunks[i])
        cal_df['Cal Length'][i] = diff[i]
        cal_df['Start Times'][i] = dataL.TheTime[S[i]]
        cal_df['End Times'][i] = dataL.TheTime[F[i]]
        
        RH = str(cal_df['RH'][i])
        RH_error = str(cal_df['RH Stddev'][i]/np.sqrt(cal_df['Cal Length'][i]))
        Pid3_v = str(cal_df['Pid3 Voltage'][i])
        Pid3_err = str(cal_df['Pid3 Stddev'][i]/np.sqrt(cal_df['Cal Length'][i]))
        Pid4_v = str(cal_df['Pid4 Voltage'][i])
        Pid4_err = str(cal_df['Pid4 Stddev'][i]/np.sqrt(cal_df['Cal Length'][i]))        
        Pid5_v = str(cal_df['Pid5 Voltage'][i])
        Pid5_err = str(cal_df['Pid5 Stddev'][i]/np.sqrt(cal_df['Cal Length'][i]))     
        
            
        RHcalpointfile.write(str(filenumber)+'\t'+str(Isop)+'\t'+RH+'\t'+RH_error+'\t'+Pid3_v+'\t'+Pid3_err+'\t'+Pid4_v+'\t'+Pid4_err+'\t'+Pid5_v+'\t'+Pid5_err+'\n')
    
    ############## ############## ############## ############## ############## ############## ############## 

    
    
    
    xdata = [i for i in cal_df.RH]
    xerr = [cal_df['RH Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
    
    Values = pd.DataFrame(index = [3,4,5], columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])
    
    
    
    if pid_3_on == 'Y':
            
            yerr3 = [cal_df['Pid3 Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
            
            ydata3 = [i for i in cal_df['Pid3 Voltage']] 
            slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
            pid3_fit = [slope_intercept3[0],(np.max(cal_df.RH)*slope_intercept3[1])+slope_intercept3[0]]
            
                    
            perr3 = np.sqrt(np.diag(pcov3))
            Intercept_error3 = perr3[0]/np.sqrt(len(S))
            Slope_Error3 = perr3[1]/np.sqrt(len(S))
    
            
            pid3_rolling_avg = pd.rolling_mean(pid3d,200)
        
            pid3_spliced = list_multisplicer(pid3d,S,F)
        
            pid3_avg_spliced = list_multisplicer(pid3_rolling_avg,S,F)
            
            Values['Intercepts'][3] = "%.2g" % slope_intercept3[0]
            Values['Slopes'][3]= "%.3g" % slope_intercept3[1]
            Values['Slope Errors'][3] = "%.1g" % Slope_Error3
            Values['Intercept Errors'][3] = "%.1g" % Intercept_error3
    
    
    if pid_4_on == 'Y': 
        
            yerr4 = [cal_df['Pid4 Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
            
            ydata4 = [i for i in cal_df['Pid4 Voltage']] 
            slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
            pid4_fit = [slope_intercept4[0],(np.max(cal_df.RH)*slope_intercept4[1])+slope_intercept4[0]]
            
    
            
            perr4 = np.sqrt(np.diag(pcov4))
            Intercept_error4 = perr4[0]/np.sqrt(len(S))
            Slope_Error4 = perr4[1]/np.sqrt(len(S))
        
            pid4_rolling_avg = pd.rolling_mean(pid4d,200)
        
            pid4_spliced = list_multisplicer(pid4d,S,F) 
        
            pid4_avg_spliced = list_multisplicer(pid4_rolling_avg,S,F)  
            
            Values['Intercepts'][4] = "%.2g" % slope_intercept4[0]
            Values['Slopes'][4]= "%.3g" % slope_intercept4[1]
            Values['Slope Errors'][4] = "%.1g" % Slope_Error4
            Values['Intercept Errors'][4] = "%.1g" % Intercept_error4
    
    if pid_5_on == 'Y':
        
            yerr5 = [cal_df['Pid5 Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
            
            ydata5 = [i for i in cal_df['Pid5 Voltage']] 
            slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr5)
            pid5_fit = [slope_intercept5[0],(np.max(cal_df.RH)*slope_intercept5[1])+slope_intercept5[0]]
            
    
            
            perr5 = np.sqrt(np.diag(pcov5))
            Intercept_error5 = perr5[0]/np.sqrt(len(S))
            Slope_Error5 = perr5[1]/np.sqrt(len(S))  
            
            pid5_rolling_avg = pd.rolling_mean(pid5d,200)
            
            pid5_spliced = list_multisplicer(pid5d,S,F)
        
            pid5_avg_spliced = list_multisplicer(pid5_rolling_avg,S,F)
            
            Values['Intercepts'][5] = "%.2g" % slope_intercept5[0]
            Values['Slopes'][5]= "%.3g" % slope_intercept5[1]
            Values['Slope Errors'][5] = "%.1g" % Slope_Error5
            Values['Intercept Errors'][5] = "%.1g" % Intercept_error5
    
    
    print 'Isop = ', Isop
    

    
    RHcalfile.write('\n'+str(filenumber)+'\t'+str(Isop)+'\t'+str(Isop_Error)+'\t'+str(Values['Slopes'][3])+'\t'+str(Values['Slope Errors'][3])+'\t'+str(Values['Slopes'][4])+'\t'+str(Values['Slope Errors'][4])+'\t'+str(Values['Slopes'][5])+'\t'+str(Values['Slope Errors'][5])+'\n')
    n = n+1
    print '%s down, %s to go'%(n,str(len(already_read_checker)-n)), '( ',np.around(float(n*100)/len(already_read_checker),1),'% )\n\n'
RHcalfile.close()
RHcalpointfile.close()