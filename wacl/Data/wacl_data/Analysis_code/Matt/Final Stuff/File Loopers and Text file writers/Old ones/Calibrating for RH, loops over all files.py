import pandas as pd
from time import strftime
import numpy as np
from operator import itemgetter
import scipy.odr as odr
import os


########### ########### Control Panel ########### ###########

path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals'
month1= 9
month2 = 9
day1 =0
day2 = 30
filenumbers = 20
min_filesize = 0
max_filesize = 19756704L


Questions = 'Y'



timing = 70 #If the code isn't picking out all the plateaus then adjust this.



data_point_length = 2000 # If you want to cal with more data for each point adjust this. (If the code gives a ValueError becuase min() arg is an empty sequence lower this)
bad_cal_length = 500

pids_on = np.arange(0,1000) # selecting which pids to use, at the moment all of them are selected

##########################################################################################################



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
def FileChecker(path,month1, month2, day1,day2,number_of_files,min_file_size_limit,max_file_size_limit):
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
            if os.path.getsize(i) < max_file_size_limit and os.path.getsize(i) > min_file_size_limit: 
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

def linear_fit_new(params, x):
    return ((params[0]*x)+params[1])    
linear = odr.Model(linear_fit_new)                  
                                    
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

filesl = FileChecker(path,month1,month2,day1,day2,filenumbers,min_filesize,max_filesize)

date = 911

try:
    data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH cals.txt',sep ='\t')

except ValueError:
    RHcalfile.write('Filename\tIsop\tIsop Error\tPid3 Slope Value\tPid3 Slope Error\tPid4 Slope Value\tPid4 Slope Error\tPid5 Slope Value\tPid5 Slope Error\n')
    RHcalpointfile.write('Filename\tIsop\tIsop Error\tRH\tRH Error\tPid3 Voltage\tPid3 Voltage Error\tPid4 Voltage\tPid4 Voltage Error\tPid5 Voltage\tPid5 Voltage Error\n')

already_read_checker = [] # to be read

print 'Checking for any cals that are already recorded...\n'
for tkm in  xrange(0,len(filesl)):
    
    try:
        data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH Cal Data Points.txt', sep = '\t')                       
        filename = str(filesl[tkm][-12:])
    
        
        if not filename in set(data.Filename):
            already_read_checker.append(tkm)
    except ValueError:
        already_read_checker = [i for i in xrange(0,len(filesl))]
    

        
if already_read_checker == []:
    print 'Sorry no more cals to add in that range of files, you could try expanding the range of files I check.' 
else:
    x = len(already_read_checker)
    if x > 1:
        print 'Okie Doke adding %s extra data points then' % str(x)
    if x == 1:
        print 'Okie Doke adding 1 extra data point then'
  
   
   
   
   
   
   
   
   
   
   
   
# Beginning of the cal code  
n = 0
for qwe in already_read_checker:
                    
    dataL = pd.read_csv(filesl[qwe])                       

    
    filenumber = filesl[qwe][-12:]
  
    if np.nanstd(dataL.mfcloR)/len(dataL) > 0.00003:
        proceed = ''
    else:
        proceed = 'Y'
        
    if proceed.upper() == 'Y' or proceed.upper() == 'YES':
        
        dataL.mfcloR = nan_helper(dataL.mfcloR,10,3)
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
            
        Isop = np.nanmean(isop_mr)
        Isop_Error = np.nanstd(isop_mr)/np.sqrt(len(dataL)) 
        
        
        
        pids_on_new = []
        for num in pids_on:
            try:
                dataL['pid%s'%str(num)]
                pids_on_new.append(num)
            except KeyError:
                pass
                
        pids_on = pids_on_new
        pid_data = {num : nan_helper(dataL['pid%s'%(str(num))],10,3) for num in pids_on} # uses nan helper here
    
                        
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
        dataL.RH = nan_helper(dataL.RH,10,3) # RH correction
        RH = dataL.RH
        RH /=4.96
        RH -= 0.16
        RH /= 0.0062
        
        RH /= (1.0546-(0.00216*dataL.Temp)) # Temperature correction
        ############## ############## ############## ############## 
        
        
        
        
        
        ############## ############## Trying to find where the RH changes Drastically (for new cal Points) ############## ############## 
        
        RH_set = []
        
    
        sensitivty_mean = np.nanmean([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)])
        sesnitivty_std = np.nanstd([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)])
        
        for i in xrange(0,len(RH)-timing,timing):
            if abs(RH[i]-RH[i+timing]) >= sensitivty_mean+sesnitivty_std:
                RH_set.append(i)
    
                
        
        Setters = []
        for i in xrange(0,len(RH_set)-1):
            if abs(RH_set[i]-RH_set[i+1]) > 200:
                Setters.append(i)
        
        RH_setF = [RH_set[i] for i in Setters]
        
        RH_setS = [i-data_point_length for i in RH_setF]
        
        if RH_setS[0]<0:
            SF = negative_remover(RH_setS,RH_setF)
            S = SF[0]
            F = SF[1]   
        else:
            S = RH_setS
            F = RH_setF
            
            
        
        
        
        
        RH_stds = [np.nanstd(RH[S[i]:F[i]]) for i in xrange(0,len(S))]
        
        SF = cal_point_ammender(RH,bad_cal_length,S,F)
        S = SF[0]
        F = SF[1] 
        
                
        diff = [F[i]-S[i] for i in xrange(len(F))]   
        
        ############## ############## ############## ############## ############## ############## ############## ############## 
        #Calculating the mean of the data in the chunks for the cal points
        Voltages = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in list_multisplicer_listsout(pid_data[num],S,F)] for num in pids_on})
        
        # Calculating the standard errors for the cal points
        Errors = pd.DataFrame({'Pid%s Stderr'%num : [np.nanstd(i)/np.sqrt(data_point_length) for i in list_multisplicer_listsout(pid_data[num],S,F)] for num in pids_on})
        
        #Finding time at Start and end of cal points
        Start_Times = pd.DataFrame({'Start Time': [TimeL[i] for i in S]})
        End_Times = pd.DataFrame({'End Time': [TimeL[i] for i in F]})
        
        #Finding the mean of the isoprene in the chunks and the standard error (like Voltages adn Errors)
        Isoprene_error = pd.DataFrame({'Isop Error': [np.nanstd(i)/np.sqrt(data_point_length) for i in list_multisplicer_listsout(isop_mr,S,F)]})
        Isoprene = pd.DataFrame({'Isop': [np.nanmean(i) for i in list_multisplicer_listsout(isop_mr,S,F)]})
    
        #Average  RH for the chunks
        cal_RH = pd.DataFrame({'RH':[np.nanmean(i) for i in list_multisplicer_listsout(RH,S,F)]})
        Error_RH = pd.DataFrame({'RH Stderr':[np.nanstd(i)/np.sqrt(data_point_length) for i in list_multisplicer_listsout(RH,S,F)]})   
        #merges above dataframes into one (for corrected and uncorrected data)
        cal_df = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Error_RH,Voltages, Errors], axis=1, join='inner')
    
        ############## ############## Deciding the columns in cal_df and chunking the data ############## ############## 
            
        RH_fit = [0.,np.max(cal_df.RH)]
        
        
        
    
        
        xdata = [i for i in cal_df.RH]
        xerr = [cal_df['RH Stderr'][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
        
        
        Values = pd.DataFrame(index = pids_on, columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])
        
        
        
        
        Rolling_Averages = pd.DataFrame(index = pids_on+['RH'], columns = ['Rolling Average'])
        Spliced_Data = pd.DataFrame(index = pids_on+['non pid specific'], columns = ['Pids','Pid_Avgs','RH','Times'])
    
        Spliced_Data['Times']['non pid specific'] = list_multisplicer(dataL.TheTime,S,F)
        Spliced_Data['RH']['non pid specific'] = list_multisplicer(RH,S,F)
        
        Rolling_Averages['Rolling Average']['RH'] = pd.rolling_mean(RH,200,20)
        
        
        
        pid_fits = {num:[] for num in pids_on}
        
        for num in pids_on:
                
                yerr = [cal_df['Pid%s Stderr'%str(num)][i]/np.sqrt(diff[i]) for i in xrange(0,len(cal_df))]
                
                ydata = [i for i in cal_df['Pid%s Voltage'%str(num)]] 
                
                datac = odr.RealData(x = cal_df['RH'],y =cal_df['Pid%s Voltage'%(str(num))],sx = cal_df['RH Stderr']*np.sqrt(data_point_length),sy = cal_df['Pid%s Stderr'%str(num)]*np.sqrt(data_point_length))
                fit = odr.ODR(datac,linear,[5e-5,0.05])
                params = fit.run()
                
                    
                pid_fits[num] = [params.beta[1],(np.max(cal_df.RH)*params.beta[0])+params.beta[1]]    
    
        
    
                
                Rolling_Averages['Rolling Average'][num] = pd.rolling_mean(pid_data[num],200,20)
            
                Spliced_Data['Pids'][num] = list_multisplicer(pid_data[num],S,F)
            
                Spliced_Data['Pid_Avgs'][num] = list_multisplicer(Rolling_Averages['Rolling Average'][num],S,F)
                
                Values['Intercepts'][num] = "%.2g" % params.beta[1]
                Values['Slopes'][num]= "%.3g" % params.beta[0]
                Values['Slope Errors'][num] = "%.1g" % params.sd_beta[0]
                Values['Intercept Errors'][num] = "%.1g" % params.sd_beta[1]
    
    
    
    for row in xrange(0,len(cal_df)):
        Pid_voltage_string = ''       
        for num in pids_on:
            Pid_voltage_string = Pid_voltage_string +'\t'+ str(cal_df.loc[row,'Pid%s Voltage'%str(num)])+'\t'+str(cal_df.loc[row,'Pid%s Stderr'%str(num)])
        
        
        RHcalpointfile.write(filesl[qwe][-12:]+'\t'+str(cal_df.loc[row,'Isop'])+'\t'+str(cal_df.loc[row,'Isop Error'])+'\t'+str(cal_df.loc[row,'RH'])+'\t'+str(cal_df.loc[row,'RH Stderr'])+Pid_voltage_string+'\n')
    
    
    slopes_string = '' 
    for num in pids_on:
        slopes_string = slopes_string + '\t' + str(Values['Slopes'][num]) + '\t' + str(Values['Slope Errors'][num])
      
          
    RHcalfile.write(filesl[qwe][-12:]+'\t'+str(Isop)+'\t'+str(np.nanmean(cal_df.loc[:,'Isop Error']))+'\t'+slopes_string +'\n')
    
    
    print 'Isop = ', Isop
    n = n+1
    print '%s down, %s to go'%(n,str(len(already_read_checker)-n)), '( ',np.around(float(n*100)/len(already_read_checker),1),'% )\n\n'
RHcalfile.close()
RHcalpointfile.close()