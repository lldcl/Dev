import pandas as pd
import matplotlib.pyplot as plt
from time import strftime
import numpy as np
import scipy.optimize as opt

pid_2_on = ''
pid_3_on = 'Y'
pid_4_on = 'Y'
pid_5_on = 'Y'
Questions = 'Y'

############## ############## ##############  Defining Useful Functions ############## ############## ############## 

#Removes Duplicates
def remove_duplicates(l):
    return list(set(l))

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

    
        
                
    
    
############## ##############  Data Read ############## ##############     

if Questions == 'Y':
    date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
    if date == 'test':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\'    
        filenameL = 'd2015test.txt'
        dataL = pd.read_csv(pathL+filenameL)
        date = 1
    elif date == 'big pid5 too' or date == 'post 0903' or date == 'big':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\'    
        filenameL = 'd20150904_0big(post 0903).txt'
        dataL = pd.read_csv(pathL+filenameL)
        date = 904
    else:
        try:
            pathL = 'C:\Users\95ellism\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
            filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
            dataL = pd.read_csv(pathL+filenameL)
            
        except IOError:
            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
            dataL = pd.read_csv(pathL+filenameL)

    
    
  
if int(date) < 904:
        pid_5_on = ''
if int(date)>=904:
    pid_2_on = '' 
       
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

RH = dataL.RH
RH /=4.9
RH -= 0.16
RH /= 0.0062
RH *= 100
RH /= 103

############## ############## ############## ############## 




############## ############## Trying to find where the RH changes Drastically (for new cal Points) ############## ############## 

no_of_data_points = 300
shift_left = 600

mfc_set = []
for i in range(0,len(RH)-100):
    if abs(RH[i]-RH[i+100]) > 1.2:
        mfc_set.append(i)

Setters = []
for i in range(0,len(mfc_set)-1):
    if abs(mfc_set[i]-mfc_set[i+1]) > 50:
        Setters.append(i)

mfc_setF = [mfc_set[i] for i in Setters]

F = [i-shift_left for i in mfc_setF]
S = [i-no_of_data_points for i in F]

negative_remover = []
if S[0] < 0:
    for i in range(0,len(S)):
        if S[i]<0:
            negative_remover.append(i)
            
    first_pos_index = max(negative_remover)
    S = S[first_pos_index+1:]
    F = F[first_pos_index+1:]     




diff = [F[i]-S[i] for i in range(len(F))]

############## ############## ############## ############## ############## ############## ############## ############## 



############## Scaling Isop to look a bit better ############## 


Isop = dataL.mfcloR
Isop *= 0.7

############## ############## ############## ############## 

RH_chunks = list_multisplicer_listsout(RH,S,F)




cal_cols = ['Start Times','End Times','RH','RH Stddev']

if int(date) < 904:
    if pid_2_on == 'Y':
    
            pid2_chunks = list_multisplicer_listsout(dataL.pid1,S,F)
            
            cal_cols.append('Pid2 Voltage')
            cal_cols.append('Pid2 Stddev')
else:
    if pid_5_on == 'Y':
    
            pid5_chunks = list_multisplicer_listsout(dataL.pid5,S,F)
            
            cal_cols.append('Pid5 Voltage')
            cal_cols.append('Pid5 Stddev')
        
        
if int(date) < 904:        
    if pid_3_on == 'Y':
        
        
        pid3_chunks = list_multisplicer_listsout(dataL.pid2, S, F)
    
        cal_cols.append('Pid3 Voltage')
        cal_cols.append('Pid3 Stddev')

else:
     if pid_3_on == 'Y':
        
        
        pid3_chunks = list_multisplicer_listsout(dataL.pid3, S, F)
    
        cal_cols.append('Pid3 Voltage')
        cal_cols.append('Pid3 Stddev')       
    
    
if int(date) >= 904:    
    if pid_4_on == 'Y':
        
        pid4_chunks = list_multisplicer_listsout(dataL.pid4, S, F)
        
        cal_cols.append('Pid4 Voltage')
        cal_cols.append('Pid4 Stddev')
        
else:
    if pid_4_on == 'Y':
        
        pid4_chunks = list_multisplicer_listsout(dataL.pid3, S, F)
        
        cal_cols.append('Pid4 Voltage')
        cal_cols.append('Pid4 Stddev')
            
cal_df = pd.DataFrame(index=range(0,len(S)), columns=cal_cols)

for i in range(0,len(cal_df)):
    cal_df.RH[i] = np.nanmean(RH_chunks[i])
    cal_df['RH Stddev'][i] =np.nanstd(RH_chunks[i])
    if pid_2_on == 'Y':
        cal_df['Pid2 Voltage'][i] = np.nanmean(pid2_chunks[i])
        cal_df['Pid2 Stddev'][i] = np.nanstd(pid2_chunks[i])
        
    if pid_3_on == 'Y':
        cal_df['Pid3 Voltage'][i] = np.nanmean(pid3_chunks[i])
        cal_df['Pid3 Stddev'][i] = np.nanstd(pid3_chunks[i])
        
    if pid_4_on == 'Y':
        cal_df['Pid4 Voltage'][i] = np.nanmean(pid4_chunks[i])
        cal_df['Pid4 Stddev'][i] = np.nanstd(pid4_chunks[i])
        
    if pid_5_on == 'Y':
        cal_df['Pid5 Voltage'][i] = np.nanmean(pid5_chunks[i])
        cal_df['Pid5 Stddev'][i] = np.nanstd(pid5_chunks[i])
    
    cal_df['Start Times'][i] = dataL.TheTime[S[i]]
    cal_df['End Times'][i] = dataL.TheTime[F[i]]


RH_fit = [0.,np.max(cal_df.RH)]






val_ind = []
intercepts =[]
intercept_errors =[]
slopes = []    
slope_errors = []





RH_ints = [int(i) for i in cal_df.RH]

indexes1 = []
uniqs = []
for i in range(0,len(RH_ints)):
    if not RH_ints[i] in uniqs:
        uniqs.append(RH_ints[i])    
        indexes1.append(i)
indexes2 = []
for i in range(0,len(cal_df['RH Stddev'])):
    if cal_df['RH Stddev'][i] < 1:
        indexes2.append(i)

    
indexes = list(set(indexes1)&set(indexes2))           
cal_df.RH = cal_df.RH[indexes]
cal_df = cal_df.dropna()

cal_df.index = range(0,len(cal_df))






xdata = [i for i in cal_df.RH]
xerr = [cal_df['RH Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]



fig_cal = plt.figure()
if int(date) >= 904:
    if pid_2_on == 'Y':
        yerr2 = [cal_df['Pid2 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata2 = [i for i in cal_df['Pid2 Voltage']] 
        slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr2)
        pid2_fit = [slope_intercept2[0],(np.max(cal_df.RH)*slope_intercept2[1])+slope_intercept2[0]]
        
        axc1 = fig_cal.add_subplot(311)
        plt.title('Pid 2')
        pid2_cal_points = axc1.errorbar(cal_df.RH,cal_df['Pid2 Voltage'], xerr = xerr, yerr = yerr2, fmt='x')
        pid2cal_fit = axc1.plot(RH_fit,pid2_fit)
        
        perr2 = np.sqrt(np.diag(pcov2))
        Intercept_error2 = perr2[0]/np.sqrt(len(S))
        Slope_Error2 = perr2[0]/np.sqrt(len(S))  
        val_ind.append('Pid 2')

        pid2_rolling_avg = pd.rolling_mean(dataL.pid1,200)
        
        pid2_spliced = list_multisplicer(dataL.pid1,S,F)
    
        pid2_avg_spliced = list_multisplicer(pid2_rolling_avg,S,F)

            
        intercepts.append("%.2g" % slope_intercept2[0])
        slopes.append("%.3g" % slope_intercept2[1])
        slope_errors.append("%.1g" % Slope_Error2)
        intercept_errors.append("%.1g" % Intercept_error2)
    if pid_5_on == 'Y':
        yerr5 = [cal_df['Pid5 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata5 = [i for i in cal_df['Pid5 Voltage']] 
        slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr5)
        pid5_fit = [slope_intercept5[0],(np.max(cal_df.RH)*slope_intercept5[1])+slope_intercept5[0]]
        
        axc1 = fig_cal.add_subplot(311)
        plt.title('Pid 5')
        pid5_cal_points = axc1.errorbar(cal_df.RH,cal_df['Pid5 Voltage'], xerr = xerr, yerr = yerr5, fmt='x')
        pid5cal_fit = axc1.plot(RH_fit,pid5_fit)
        
        perr5 = np.sqrt(np.diag(pcov5))
        Intercept_error5 = perr5[0]/np.sqrt(len(S))
        Slope_Error5 = perr5[0]/np.sqrt(len(S))  
        val_ind.append('Pid 5')
        
        pid5_rolling_avg = pd.rolling_mean(dataL.pid5,200)
        
        pid5_spliced = list_multisplicer(dataL.pid5,S,F)
    
        pid5_avg_spliced = list_multisplicer(pid5_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept5[0])
        slopes.append("%.3g" % slope_intercept5[1])
        slope_errors.append("%.1g" % Slope_Error5)
        intercept_errors.append("%.1g" % Intercept_error5)
        
    
if int(date) >= 904:    
    if pid_3_on == 'Y':
        
        yerr3 = [cal_df['Pid3 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata3 = [i for i in cal_df['Pid3 Voltage']] 
        slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
        pid3_fit = [slope_intercept3[0],(np.max(cal_df.RH)*slope_intercept3[1])+slope_intercept3[0]]
        
        axc2 = fig_cal.add_subplot(312)
        plt.title('Pid 3')
        pid3_cal_points = axc2.errorbar(cal_df.RH,cal_df['Pid3 Voltage'], xerr = xerr, yerr = yerr3, fmt='x')
        pid3_cal_fit = axc2.plot(RH_fit,pid3_fit)
        
        perr3 = np.sqrt(np.diag(pcov3))
        Intercept_error3 = perr3[0]/np.sqrt(len(S))
        Slope_Error3 = perr3[0]/np.sqrt(len(S))
        val_ind.append('Pid 3')
        
        pid3_rolling_avg = pd.rolling_mean(dataL.pid3,200)
    
        pid3_spliced = list_multisplicer(dataL.pid3,S,F)
    
        pid3_avg_spliced = list_multisplicer(pid3_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept3[0])
        slopes.append("%.3g" % slope_intercept3[1])
        slope_errors.append("%.1g" % Slope_Error3)
        intercept_errors.append("%.1g" % Intercept_error3)

else:
    
    if pid_3_on == 'Y':
        
        yerr3 = [cal_df['Pid3 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata3 = [i for i in cal_df['Pid3 Voltage']] 
        slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
        pid3_fit = [slope_intercept3[0],(np.max(cal_df.RH)*slope_intercept3[1])+slope_intercept3[0]]
        
        axc2 = fig_cal.add_subplot(312)
        plt.title('Pid 3')
        pid3_cal_points = axc2.errorbar(cal_df.RH,cal_df['Pid3 Voltage'], xerr = xerr, yerr = yerr3, fmt='x')
        pid3_cal_fit = axc2.plot(RH_fit,pid3_fit)
        
        perr3 = np.sqrt(np.diag(pcov3))
        Intercept_error3 = perr3[0]/np.sqrt(len(S))
        Slope_Error3 = perr3[0]/np.sqrt(len(S))
        val_ind.append('Pid 3')
        
        pid3_rolling_avg = pd.rolling_mean(dataL.pid2,200)
    
        pid3_spliced = list_multisplicer(dataL.pid2,S,F)
    
        pid3_avg_spliced = list_multisplicer(pid3_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept3[0])
        slopes.append("%.3g" % slope_intercept3[1])
        slope_errors.append("%.1g" % Slope_Error3)
        intercept_errors.append("%.1g" % Intercept_error3)


if int(date) >= 904:
    if pid_4_on == 'Y':    
        
        yerr4 = [cal_df['Pid4 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata4 = [i for i in cal_df['Pid4 Voltage']] 
        slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
        pid4_fit = [slope_intercept4[0],(np.max(cal_df.RH)*slope_intercept4[1])+slope_intercept4[0]]
        
        axc3 = fig_cal.add_subplot(313)
        plt.title('Pid 4')
        pid4_cal_points = axc3.errorbar(cal_df.RH,cal_df['Pid4 Voltage'], xerr = xerr, yerr = yerr4, fmt='x')
        pid4_cal_fit = axc3.plot(RH_fit,pid4_fit)
        
        perr4 = np.sqrt(np.diag(pcov4))
        Intercept_error4 = perr4[0]/np.sqrt(len(S))
        Slope_Error4 = perr4[0]/np.sqrt(len(S))
        val_ind.append('Pid 4')
    
        pid4_rolling_avg = pd.rolling_mean(dataL.pid4,200)
    
        pid4_spliced = list_multisplicer(dataL.pid4,S,F) 
    
        pid4_avg_spliced = list_multisplicer(pid4_rolling_avg,S,F)  
        
        intercepts.append("%.2g" % slope_intercept4[0])
        slopes.append("%.3g" % slope_intercept4[1])
        slope_errors.append("%.1g" % Slope_Error4)
        intercept_errors.append("%.1g" % Intercept_error4)


else:    
    if pid_4_on == 'Y':    
        
        yerr4 = [cal_df['Pid4 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata4 = [i for i in cal_df['Pid4 Voltage']] 
        slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
        pid4_fit = [slope_intercept4[0],(np.max(cal_df.RH)*slope_intercept4[1])+slope_intercept4[0]]
        
        axc3 = fig_cal.add_subplot(313)
        plt.title('Pid 4')
        pid4_cal_points = axc3.errorbar(cal_df.RH,cal_df['Pid4 Voltage'], xerr = xerr, yerr = yerr4, fmt='x')
        pid4_cal_fit = axc3.plot(RH_fit,pid4_fit)
        
        perr4 = np.sqrt(np.diag(pcov4))
        Intercept_error4 = perr4[0]/np.sqrt(len(S))
        Slope_Error4 = perr4[0]/np.sqrt(len(S))
        val_ind.append('Pid 4')
    
        pid4_rolling_avg = pd.rolling_mean(dataL.pid3,200)
    
        pid4_spliced = list_multisplicer(dataL.pid3,S,F) 
    
        pid4_avg_spliced = list_multisplicer(pid4_rolling_avg,S,F)  
        
        intercepts.append("%.2g" % slope_intercept4[0])
        slopes.append("%.3g" % slope_intercept4[1])
        slope_errors.append("%.1g" % Slope_Error4)
        intercept_errors.append("%.1g" % Intercept_error4)


Values = pd.DataFrame(index = val_ind, columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])

Values['Intercepts'] = [i for i in intercepts]
Values['Slopes'] = [i for i in slopes]
Values['Slope Errors'] = [i for i in slope_errors]
Values['Intercept Errors'] = [i for i in intercept_errors]


print Values


############## Calculating a rolling mean for pids ############## 


############## ############## ############## ############## 




############## Splicing Lists for Plotting ############## 

times = list_multisplicer(dataL.TheTime,S,F)

RH_spliced = list_multisplicer(RH,S,F)


############## ############## ############## ############## 





############## ############## Plotting ############## ############## 

figRH = plt.figure()


ax1RH= figRH.add_subplot(221)
plt.title('Spliced Graphs')

ax1RH.plot(times,RH_spliced,color='b')
ax1RH.plot(dataL.TheTime,pd.rolling_mean(RH,100),color='g')



ax2RH = figRH.add_subplot(223)




ax3RH = figRH.add_subplot(222)
plt.title('Raw Data')
ax3RH.plot(dataL.TheTime,RH,color = 'b')



ax4RH = figRH.add_subplot(224)








if pid_2_on == 'Y':
    ax2RH.plot(times,pid2_spliced,color='k')
    ax2RH.plot(times,pid2_avg_spliced,linewidth = 3,color='k')
    ax4RH.plot(dataL.TheTime,pid2_rolling_avg,color='k')
    
    
    
if pid_3_on == 'Y':
    ax2RH.plot(times,pid3_spliced,color='b')
    ax2RH.plot(times,pid3_avg_spliced,linewidth = 3,color='b')
    ax4RH.plot(dataL.TheTime,pid3_rolling_avg,color='b')
    
    
    
if pid_4_on == 'Y':
    ax2RH.plot(times,pid4_spliced,color='m')
    ax2RH.plot(times,pid4_avg_spliced,linewidth = 3,color='m')
    ax4RH.plot(dataL.TheTime,pid4_rolling_avg,color='m')

if pid_5_on == 'Y':
    ax2RH.plot(times,pid5_spliced,color='m')
    ax2RH.plot(times,pid5_avg_spliced,linewidth = 3,color='m')
    ax4RH.plot(dataL.TheTime,pid5_rolling_avg,color='m')

plt.show()