import pandas as pd
import matplotlib.pyplot as plt
from time import strftime
import numpy as np
import scipy.optimize as opt
#import matplotlib.patches as mpatches

pid_3_on = 'Y'
pid_4_on = 'Y'
pid_5_on = 'Y'
Questions = 'Y'

############## ############## ##############  Defining Useful Functions ############## ############## ############## 

# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))

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
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Zero Isoprene\\'    
        filenameL = 'd2015test.txt'
        print '\nReading Data...'
        dataL = pd.read_csv(pathL+filenameL)
        date = 1
        
    elif date == 'bi' or date == 'bg' or date == 'big':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Zero Isoprene\\'    
        filenameL = 'd20150904_0big(post 0903).txt'
        print '\nReading Data...'
        dataL = pd.read_csv(pathL+filenameL)
        date = 904
        
    elif date == '12':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 1.5\\'
        filenamel = 'd20150914_02'
        dataL = pd.read_csv(pathL+filenamel)
        dataL = dataL.drop(['mfcloR','mfchiR','mfclo'],1)
        date = 914
        
        
    elif date == 'both':
        pid_5_on = ''
        pid_2_on = ''
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Zero Isoprene\\'
        filenameL1 = 'd2015test.txt'
        filenameL2 = 'd20150904_0big(post 0903).txt'
        print '\nReading Data...'
        dataL1 = pd.read_csv(pathL+filenameL1)
        dataL2 = pd.read_csv(pathL+filenameL2)
        print '\nMerging DataFrames...'
        dataL1.columns = ['TheTime','pid2','pid3','pid4','mfcloR','mfchiR','mfclo','Temp','RH']
        dataL1 = dataL1.drop(['pid2','Temp','mfcloR','mfchiR','mfclo'],1)
        dataL2 = dataL2.drop(['pid5','Temp','mfcloR','mfchiR','mfclo'],1)
        dataL2.index = range(len(dataL1),len(dataL1)+len(dataL2))
        dataL = pd.concat([dataL1,dataL2])
        date = 905
    
    elif date == '4':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 0.5\\'
        filenamel = 'd20150911_02'
        dataL = pd.read_csv(pathL+filenamel)
        dataL = dataL.drop(['mfcloR','mfchiR','mfclo'],1)
        date = 911
    
    elif date == '20':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 2.5\\'
        filenamel = 'd20150915_02'
        dataL = pd.read_csv(pathL+filenamel)
        dataL = dataL.drop(['mfcloR','mfchiR','mfclo'],1)
        date = 915   
    else:
        try:
            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
            filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)
            dataL = dataL.drop(['mfcloR','mfchiR','mfclo'],1)
            
        except IOError:
            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)

    
    
  
print '\nCorrecting different Pid Labels and interpolating nans...'

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



print '\nFormatting data...'
            
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
print '\nSelecting cal points...'

S = range(0,len(dataL),500)
F = [i+250 for i in S[:-1]]+[len(dataL)-10]

############## ############## ############## ############## ############## ############## ############## ############## 

############## ############## Deciding the columns in cal_df and chunking the data ############## ############## 
print '\nSplicing Data...'
RH_chunks = list_multisplicer_listsout(RH,S,F)


cal_cols = ['Start Times','End Times','RH','RH Stddev','Cal Length']
          
            
############## ############## Finding averages and stds of the chunks ############## ##############              
cal_df = pd.DataFrame(index=range(0,len(S)), columns=cal_cols)
       
diff = [F[i]-S[i] for i in range(len(F))]
        
RH_chunks = list_multisplicer_listsout(RH,S,F)


cal_cols = ['Start Times','End Times','RH','RH Stddev']

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
print '\nCalculating Averages of new points...'
cal_df = pd.DataFrame(index=range(0,len(S)), columns=cal_cols)


RH_avgs = [np.nanmean(i) for i in RH_chunks]
RH_stds = [np.nanstd(i) for i in RH_chunks]

if pid_3_on == 'Y':
    pid3_avgs = [np.nanmean(i) for i in pid3_chunks]
    pid3_stds = [np.nanstd(i) for i in pid3_chunks]

if pid_4_on == 'Y':
    pid4_avgs = [np.nanmean(i) for i in pid4_chunks]
    pid4_stds = [np.nanstd(i) for i in pid4_chunks]

if pid_5_on == 'Y':
    pid5_avgs = [np.nanmean(i) for i in pid5_chunks]
    pid5_stds = [np.nanstd(i) for i in pid5_chunks]

starts = [dataL.TheTime[i] for i in S]
ends = [dataL.TheTime[i] for i in F]


cal_df['Cal Length'] = diff

cal_df['RH'] = RH_avgs
cal_df['RH Stddev'] = RH_stds

if pid_3_on == 'Y':
    cal_df['Pid3 Voltage'] = pid3_avgs
    cal_df['Pid3 Stddev'] = pid3_stds
    
if pid_4_on == 'Y':
    cal_df['Pid4 Voltage'] = pid4_avgs
    cal_df['Pid4 Stddev'] = pid4_stds

if pid_5_on == 'Y':
    cal_df['Pid5 Voltage'] = pid5_avgs
    cal_df['Pid5 Stddev'] = pid5_stds

cal_df['Start Times'] = starts
cal_df['End Times'] = ends
    
    
s = np.nanstd(cal_df['RH Stddev'])
m = np.nanmean(cal_df['RH Stddev'])



######################### ######################### #########################
RH_fit = [0.,np.max(cal_df.RH)]

tolerance = 0.05

dodgy_cal_indexes = [i for i in range(0,len(cal_df)) if cal_df['RH Stddev'][i] > m+tolerance*s]

for i in range(0,len(F)):
    if i in dodgy_cal_indexes:
        F[i] = 0
        S[i] = 0
F.sort()
S.sort()

for i in range(0,len(cal_df['RH Stddev'])):
    if cal_df['RH Stddev'][i] > m+tolerance*s:
        cal_df['RH Stddev'][i] = np.nan
cal_df.dropna()
cal_df.index = range(0,len(cal_df))

dodgy_cal_indexes = [i for i in range(0,len(cal_df)) if cal_df['Pid3 Stddev'][i] > m+tolerance*s]

for i in range(0,len(F)):
    if i in dodgy_cal_indexes:
        F[i] = 0
        S[i] = 0
F.sort()
S.sort()


for i in range(0,len(cal_df['Pid3 Stddev'])):
    if cal_df['Pid3 Stddev'][i] > m+tolerance*s:
        cal_df['Pid3 Stddev'][i] = np.nan
cal_df.dropna()
cal_df.index = range(0,len(cal_df))

val_ind = []
intercepts =[]
intercept_errors =[]
slopes = []    
slope_errors = []



xdata = [i for i in cal_df.RH]
xerr = [cal_df['RH Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]

print '\nPlotting Dem Graphs...\n\n\n'

fig_cal = plt.figure()

if pid_5_on == 'Y':
    
        yerr5 = [cal_df['Pid5 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata5 = [i for i in cal_df['Pid5 Voltage']] 
        slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr5)
        pid5_fit = [slope_intercept5[0],(np.max(cal_df.RH)*slope_intercept5[1])+slope_intercept5[0]]
        
        axc1 = fig_cal.add_subplot(311)
        plt.title('Pid 5, y = '+"%.2g" %slope_intercept5[1]+'x + '+"%.2g" % slope_intercept5[0])
        pid5_cal_points = axc1.errorbar(cal_df.RH,cal_df['Pid5 Voltage'], xerr = xerr, yerr = yerr5, fmt='x')
        pid5cal_fit = axc1.plot(RH_fit,pid5_fit)
        
        perr5 = np.sqrt(np.diag(pcov5))
        Intercept_error5 = perr5[0]/np.sqrt(len(S))
        Slope_Error5 = perr5[0]/np.sqrt(len(S))  
        val_ind.append('Pid 5')
        
        pid5_rolling_avg = pd.rolling_mean(pid5d,200)
        
        pid5_spliced = list_multisplicer(pid5d,S,F)
    
        pid5_avg_spliced = list_multisplicer(pid5_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept5[0])
        slopes.append("%.3g" % slope_intercept5[1])
        slope_errors.append("%.1g" % Slope_Error5)
        intercept_errors.append("%.1g" % Intercept_error5)
        
    
 
if pid_3_on == 'Y':
        
        yerr3 = [cal_df['Pid3 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata3 = [i for i in cal_df['Pid3 Voltage']] 
        slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
        pid3_fit = [slope_intercept3[0],(np.max(cal_df.RH)*slope_intercept3[1])+slope_intercept3[0]]
        
        axc2 = fig_cal.add_subplot(312)
        plt.title('Pid 3, y = '+"%.2g" % slope_intercept3[1]+'x + '+ "%.2g" %slope_intercept3[0])
        pid3_cal_points = axc2.errorbar(cal_df.RH,cal_df['Pid3 Voltage'], xerr = xerr, yerr = yerr3, fmt='x')
        pid3_cal_fit = axc2.plot(RH_fit,pid3_fit)
        
        perr3 = np.sqrt(np.diag(pcov3))
        Intercept_error3 = perr3[0]/np.sqrt(len(S))
        Slope_Error3 = perr3[0]/np.sqrt(len(S))
        val_ind.append('Pid 3')
        
        pid3_rolling_avg = pd.rolling_mean(pid3d,200)
    
        pid3_spliced = list_multisplicer(pid3d,S,F)
    
        pid3_avg_spliced = list_multisplicer(pid3_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept3[0])
        slopes.append("%.3g" % slope_intercept3[1])
        slope_errors.append("%.1g" % Slope_Error3)
        intercept_errors.append("%.1g" % Intercept_error3)


if pid_4_on == 'Y': 
    
        yerr4 = [cal_df['Pid4 Stddev'][i]/np.sqrt(diff[i]) for i in range(0,len(cal_df))]
        
        ydata4 = [i for i in cal_df['Pid4 Voltage']] 
        slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
        pid4_fit = [slope_intercept4[0],(np.max(cal_df.RH)*slope_intercept4[1])+slope_intercept4[0]]
        
        axc3 = fig_cal.add_subplot(313)
        plt.title('Pid 4, y = '+"%.2g" %slope_intercept4[1]+'x + '+"%.2g" %slope_intercept4[0])
        pid4_cal_points = axc3.errorbar(cal_df.RH,cal_df['Pid4 Voltage'], xerr = xerr, yerr = yerr4, fmt='x')
        pid4_cal_fit = axc3.plot(RH_fit,pid4_fit)
        
        perr4 = np.sqrt(np.diag(pcov4))
        Intercept_error4 = perr4[0]/np.sqrt(len(S))
        Slope_Error4 = perr4[0]/np.sqrt(len(S))
        val_ind.append('Pid 4')
    
        pid4_rolling_avg = pd.rolling_mean(pid4d,200)
    
        pid4_spliced = list_multisplicer(pid4d,S,F) 
    
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



############## Splicing Lists for Plotting ############## 

times = list_multisplicer(dataL.TheTime,S,F)

RH_spliced = list_multisplicer(RH,S,F)



############## ############## Plotting ############## ############## 

figRH = plt.figure()


ax1RH= figRH.add_subplot(221)
plt.title('Spliced Graphs')

ax1RH.plot(times,RH_spliced,color='b',linewidth = 2)
ax1RH.plot(dataL.TheTime,pd.rolling_mean(RH,100,30),color='g',linewidth = 1)



ax2RH = figRH.add_subplot(223)




ax3RH = figRH.add_subplot(222)
plt.title('Raw Data')
ax3RH.plot(dataL.TheTime,RH,color = 'b')



ax4RH = figRH.add_subplot(224)


if pid_3_on == 'Y':
    ax2RH.plot(times,pid3_spliced,color='b')
    ax2RH.plot(times,pid3_avg_spliced,linewidth = 1,color='b')
    ax2RH.plot(dataL.TheTime,pid3_rolling_avg,color='r')
    
    
if pid_4_on == 'Y':
    ax2RH.plot(times,pid4_spliced,color='m')
    ax2RH.plot(times,pid4_avg_spliced,linewidth = 1,color='m')
    ax2RH.plot(dataL.TheTime,pid4_rolling_avg,color='g')

if pid_5_on == 'Y':
    ax2RH.plot(times,pid5_spliced,color='k')
    ax2RH.plot(times,pid5_avg_spliced,linewidth = 1,color='k')
    ax2RH.plot(dataL.TheTime,pid5_rolling_avg,color='y')

plt.show()

print 'Number of Cal Points = ',len(cal_df)