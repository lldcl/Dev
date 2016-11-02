import pandas as pd
import matplotlib.pyplot as plt
from time import strftime
import numpy as np
import scipy.optimize as opt
from operator import itemgetter
#import matplotlib.patches as mpatches

pid_3_on = 'Y'
pid_4_on = 'Y'
pid_5_on = 'Y'
Questions = 'Y'



timing = 75 #If the code isn't picking out all the plateaus then adjust this.

shifter = 50 #You can change this if the code cals at dodgy points

no_of_data_points = 2000 # If you want to cal with more data for each point adjust this. (If the code gives a ValueError becuase min() arg is an empty sequence lower this)
length_of_bad_cals = 1000



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


# Adds extra Cal points to bits that have a flat bit longer than the specified amount
def cal_adder(number_of_additions,S,F,tolerance_length,cal_length,cal_spacing):
    long_ones = [i for i in xrange(0,len(S)) if S[i] - S[i-1] > tolerance_length]
    
    for pt in xrange(0,(number_of_additions-1)):
        F = F + [F[i] for i in long_ones]
        S = S + [S[i] for i in long_ones]
        
    F.sort()
    S.sort()
    
    S_indexes = [i for i in xrange(0,len(S)) if S[i] == S[i-(number_of_additions-1)]]
    F_indexes = [i for i in xrange(0,len(F)) if F[i] == F[i-(number_of_additions-1)]]
    
    for i in F_indexes:
        for pt in xrange(0,number_of_additions):
            if pt >= 1:
                F[i-pt] = F[i-pt] - (pt*(cal_spacing))
    
    for i in S_indexes:
        for pt in xrange(0,number_of_additions):
            if pt >= 1:
                S[i-pt] = S[i-pt] - (pt*(cal_spacing))
    
        
    return S,F

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


                        
    
    
############## ##############  Data Read ############## ##############     
if Questions == 'Y':
    date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
    if date == 'test':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Isoprene = 0.0\\'    
        filenameL = 'd2015test.txt'
        print '\nReading Data...'
        dataL = pd.read_csv(pathL+filenameL)
        
        date = 1
        
    elif date == 'bi' or date == 'bg' or date == 'big':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 0.0\\'    
        filenameL = 'd20150904_0big(post 0903).txt'
        print '\nReading Data...'
        dataL = pd.read_csv(pathL+filenameL)
        
        date = 904
 #d20150915_05       
    elif date == '12':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 1.5\\'
        filenamel = 'big'
        dataL = pd.read_csv(pathL+filenamel)
        
        date = 911
        

    
    elif date == '20':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 2.5\\'
        filenamel = 'big'
        dataL = pd.read_csv(pathL+filenamel)
        
        date = 911        
    elif date == '8':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 2.0\\'
        filenamel = 'big'
        dataL = pd.read_csv(pathL+filenamel)
        
        date = 911     
               
    elif date == 'both':
        pid_5_on = ''
        pid_2_on = ''
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Isoprene = 0.0\\'
        filenameL1 = 'd2015test.txt'
        filenameL2 = 'd20150904_0big(post 0903).txt'
        print '\nReading Data...'
        dataL1 = pd.read_csv(pathL+filenameL1)
        dataL2 = pd.read_csv(pathL+filenameL2)
        print '\nMerging DataFrames...'
        dataL1.columns = ['TheTime','pid2','pid3','pid4','mfcloR','mfchiR','mfclo','Temp','RH']
        dataL1 = dataL1.drop(['pid2'],1)

        dataL2.index = xrange(len(dataL1),len(dataL1)+len(dataL2))
        dataL = pd.concat([dataL1,dataL2])
        date = 905
    
    elif date == '4':
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 0.5\\'
        filenamel = 'big'
        dataL = pd.read_csv(pathL+filenamel)
        
        date = 911

    else:
        try:
            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
            filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)

            
        except IOError:
            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)
            
        except IOError:
            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\\2015'+date[0:2]
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)

  
print '\nCorrecting different Pid Labels and interpolating nans...'

isop_cyl = 13.277	#ppbv
mfchi_range = 100.	#sccm
mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)

mfclo_range = 20.	#sccm
mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)

dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = dil_fac*isop_cyl

Isop = np.nanmean(isop_mr)

for i in xrange(0,len(isop_mr)):
    if isop_mr[i] > Isop + 0.25 or isop_mr[i] < Isop - 0.25:
        cal_cut_off = i + 50
    if isop_mr[i+1] < Isop + 0.25 and isop_mr[i+1] > Isop - 0.25:
        break
try:
    if cal_cut_off > len(dataL)/2: 
        dataL = dataL[:cal_cut_off]
        dataL.index = xrange(0,len(dataL))  
    if cal_cut_off < len(dataL)/2:      
        dataL = dataL[cal_cut_off:]
        dataL.index = xrange(0,len(dataL)) 
except NameError:
    pass
    
Isop = np.nanmean(isop_mr)/2
Isop_Error = np.nanstd(isop_mr)/np.sqrt(len(dataL)) 

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
    
    
print '\nAmmending bad cal points...' 




RH_stds = [np.nanstd(RH[S[i]:F[i]]) for i in xrange(0,len(S))]

for i in xrange(0,len(S)):
    

            orig_std = np.nanstd(RH[S[i]:F[i]])
            
            if orig_std > 0.7:
                S[i] = F[i] - length_of_bad_cals
    
            
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
print '\nSplicing Data...'
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
    
    cal_df['Start Times'][i] = dataL.TheTime[S[i]]
    cal_df['End Times'][i] = dataL.TheTime[F[i]]
############## ############## ############## ############## ############## ############## ############## 

RH_fit = [0.,np.max(cal_df.RH)]






val_ind = []
intercepts =[]
intercept_errors =[]
slopes = []    
slope_errors = []



xdata = [i for i in cal_df.RH]
xerr = [cal_df['RH Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]

print '\nPlotting Dem Graphs...\n\n\n'

fig_cal = plt.figure()
  
 
if pid_3_on == 'Y':
        
        yerr3 = [cal_df['Pid3 Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
        
        ydata3 = [i for i in cal_df['Pid3 Voltage']] 
        slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
        pid3_fit = [slope_intercept3[0],(np.max(cal_df.RH)*slope_intercept3[1])+slope_intercept3[0]]
        
        axc2 = fig_cal.add_subplot(312)
        plt.title('Pid 3, y = '+"%.2g" % slope_intercept3[1]+'x + '+ "%.2g" %slope_intercept3[0])
        pid3_cal_points = axc2.errorbar(cal_df.RH,cal_df['Pid3 Voltage'], xerr = xerr, yerr = yerr3, fmt='x')
        pid3_cal_fit = axc2.plot(RH_fit,pid3_fit)
        
        perr3 = np.sqrt(np.diag(pcov3))
        Intercept_error3 = perr3[0]/np.sqrt(len(S))
        Slope_Error3 = perr3[1]/np.sqrt(len(S))
        val_ind.append('Pid 3')
        
        pid3_rolling_avg = pd.rolling_mean(pid3d,200)
    
        pid3_spliced = list_multisplicer(pid3d,S,F)
    
        pid3_avg_spliced = list_multisplicer(pid3_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept3[0])
        slopes.append("%.3g" % slope_intercept3[1])
        slope_errors.append("%.1g" % Slope_Error3)
        intercept_errors.append("%.1g" % Intercept_error3)


if pid_4_on == 'Y': 
    
        yerr4 = [cal_df['Pid4 Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
        
        ydata4 = [i for i in cal_df['Pid4 Voltage']] 
        slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
        pid4_fit = [slope_intercept4[0],(np.max(cal_df.RH)*slope_intercept4[1])+slope_intercept4[0]]
        
        axc3 = fig_cal.add_subplot(313)
        plt.title('Pid 4, y = '+"%.2g" %slope_intercept4[1]+'x + '+"%.2g" %slope_intercept4[0])
        pid4_cal_points = axc3.errorbar(cal_df.RH,cal_df['Pid4 Voltage'], xerr = xerr, yerr = yerr4, fmt='x')
        pid4_cal_fit = axc3.plot(RH_fit,pid4_fit)
        
        perr4 = np.sqrt(np.diag(pcov4))
        Intercept_error4 = perr4[0]/np.sqrt(len(S))
        Slope_Error4 = perr4[1]/np.sqrt(len(S))
        val_ind.append('Pid 4')
    
        pid4_rolling_avg = pd.rolling_mean(pid4d,200)
    
        pid4_spliced = list_multisplicer(pid4d,S,F) 
    
        pid4_avg_spliced = list_multisplicer(pid4_rolling_avg,S,F)  
        
        intercepts.append("%.2g" % slope_intercept4[0])
        slopes.append("%.3g" % slope_intercept4[1])
        slope_errors.append("%.1g" % Slope_Error4)
        intercept_errors.append("%.1g" % Intercept_error4)

if pid_5_on == 'Y':
    
        yerr5 = [cal_df['Pid5 Stddev'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
        
        ydata5 = [i for i in cal_df['Pid5 Voltage']] 
        slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr5)
        pid5_fit = [slope_intercept5[0],(np.max(cal_df.RH)*slope_intercept5[1])+slope_intercept5[0]]
        
        axc1 = fig_cal.add_subplot(311)
        plt.title('Pid 5, y = '+"%.2g" %slope_intercept5[1]+'x + '+"%.2g" % slope_intercept5[0])
        pid5_cal_points = axc1.errorbar(cal_df.RH,cal_df['Pid5 Voltage'], xerr = xerr, yerr = yerr5, fmt='x')
        pid5cal_fit = axc1.plot(RH_fit,pid5_fit)
        
        perr5 = np.sqrt(np.diag(pcov5))
        Intercept_error5 = perr5[0]/np.sqrt(len(S))
        Slope_Error5 = perr5[1]/np.sqrt(len(S))  
        val_ind.append('Pid 5')
        
        pid5_rolling_avg = pd.rolling_mean(pid5d,200)
        
        pid5_spliced = list_multisplicer(pid5d,S,F)
    
        pid5_avg_spliced = list_multisplicer(pid5_rolling_avg,S,F)
        
        intercepts.append("%.2g" % slope_intercept5[0])
        slopes.append("%.3g" % slope_intercept5[1])
        slope_errors.append("%.1g" % Slope_Error5)
        intercept_errors.append("%.1g" % Intercept_error5)
                

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
    ax2RH.plot(times,pid3_avg_spliced,linewidth = 1,color='r')
    ax2RH.plot(dataL.TheTime,pid3_rolling_avg,color='b')
    
    
if pid_4_on == 'Y':
    ax2RH.plot(times,pid4_spliced,color='m')
    ax2RH.plot(times,pid4_avg_spliced,linewidth = 1,color='g')
    ax2RH.plot(dataL.TheTime,pid4_rolling_avg,color='m')

if pid_5_on == 'Y':
    ax2RH.plot(times,pid5_spliced,color='k')
    ax2RH.plot(times,pid5_avg_spliced,linewidth = 1,color='y')
    ax2RH.plot(dataL.TheTime,pid5_rolling_avg,color='k')

plt.show()

print 'Number of Cal Points = ',len(cal_df)