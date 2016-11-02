import pandas as pd
from time import strftime
import numpy as np
from operator import itemgetter
import scipy.odr as odr
import os


########### ########### Control Panel ########### ###########

#path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals'
path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data/201509/Humidity Cals'
month1= 9
month2 = 9
day1 = 0
day2 = 30
filenumbers = 20
min_filesize = 0
max_filesize = 19756704L



timing = 70 #If the code isn't picking out all the plateaus then adjust this.



data_point_length = 1000 # If you want to cal with more data for each point adjust this. (If the code gives a ValueError becuase min() arg is an empty sequence lower this)
bad_cal_length = 1000



##########################################################################################################




### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation
def cal_point_ammender(data_set,bad_cal_length,S,F):
    shifter = (len(dataL)*1)/(20*(len(S)+2)*4)

    
    
    Snew = list(np.zeros(len(S)))
    Fnew = list(np.zeros(len(F)))    
    for i in xrange(0,len(S)):

        orig_std = np.nanstd(data_set[S[i]:F[i]])
        
        if orig_std > 0.7:
            S[i] = F[i] - bad_cal_length

        
        left_shift_stds = {k:[np.nanstd(data_set[S[i]-(k*shifter):F[i]-(k*shifter)])] for k in xrange(0,20) if S[i] - (k*shifter) > 0}
        nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
        for t in nanL:
            del(left_shift_stds[t])
        

        
        
        try:    
            minPairL = min(left_shift_stds.iteritems(), key=itemgetter(1))
      
        except ValueError:
            minPairL = (0,[orig_std])

        
        if minPairL[1][0] < orig_std:
            
            Snew[i] = S[i] - minPairL[0]*shifter
            Fnew[i] = F[i] - minPairL[0]*shifter

        else:
            
            Snew[i] = S[i]
            Fnew[i] = F[i]

    zeros = [i for i in xrange(0,len(Snew)) if Snew[i] == 0. and Fnew[i] == 0.]
    
    if zeros != []:
        for i in zeros:
            del Snew[i]
            del Fnew[i]        
            
                          
    if Snew[0] < 0:
        SF = negative_remover(Snew,Fnew)
        Snew = SF[0]
        Fnew = SF[1]
     

    
    return Snew,Fnew      
        
        
            
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
#Not currenty used
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
    
# For ODR function (error in x and y)
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
        path1 = path+'/d2015'+str(month)
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
############## ############## ############## ############## ############## ############## ############## ############## 
#FileChecker(path,month1, month2, day1,day2,number_of_files,file_size_limit)

filesl = FileChecker(path,month1,month2,day1,day2,filenumbers,min_filesize,max_filesize)




to_be_read = [] # indicies of files to be read for filesl

print 'Checking for any cals that are already recorded...\n'
for tkm in  xrange(0,len(filesl)):
    # compares the filename of the files to be read to the filenames that have already been read and stored. If there are any missing, then it puts the index of the file from the list filesl into the to_be_read list.
    try:
#        data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Slope Intercepts.txt', sep = ',')                       
        data = pd.read_csv('/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Slope Intercepts.txt', sep = ',')                       
        filename = str(filesl[tkm][-12:])
    
        
        if not filename in set(data.Filename):
            to_be_read.append(tkm)
    except IOError:
        to_be_read = [i for i in xrange(0,len(filesl))]
    



# Prints out info on what's beig read       
if len(to_be_read) == 0:
    there_are_new_values_to_be_added = 'N'
    print 'Sorry no more cals to add in that range of files, you could try expanding the range of files I check.' 
else:
    there_are_new_values_to_be_added = 'Y'
    x = len(to_be_read)
    if x > 1:
        print 'Okie Doke adding %s extra cals then' % str(x)
    if x == 1:
        print 'Okie Doke adding 1 extra cal then'
  
   
# If you want to read all filesl in the list, and ignore the to_be_read checker then uncomment the line below   
#to_be_read = [i for i in xrange(0,len(filesl))]  
   
 
  
# Finds which Pids are going to be read, and it makes a list of them.    
pids_on_master = []


for qwe in to_be_read:  
    dataL = pd.read_csv(filesl[qwe]) 
    pids_on_tester = np.arange(0,1000)
    pids_on_new = []
    for num in pids_on_tester:
        try:
            dataL['pid%s'%str(num)]
            pids_on_new.append(num)
        except KeyError:
            pass

    for i in pids_on_new:
        if not i in pids_on_master:
            pids_on_master.append(i)

# This creates a string to be the header of the new dataframe storing all the information on the cals
Pids_string = '' 
for num in pids_on_master:
    Pids_string = Pids_string +'\tPid%s\tPid%s Error'%(num,num)


# Stores information about the slope and intercept of each cal
Slope_Intercepts = pd.DataFrame(index = xrange(0,len(to_be_read)),columns = ['Filename']+['Pid%s Slope'%num for num in pids_on_master]+['Pid%s Slope Error'%(num) for num in pids_on_master]+['Pid%s Intercept'%num for num in pids_on_master]+['Pid%s Intercept Error'%(num) for num in pids_on_master])   

  
    
      
# Creates a ditionary of all the cal_dfs        
cal_dfs = {i:() for i in xrange(0,len(to_be_read))}  
# df.append() might work better here (I couldn't make it work though) 
   
       
# Beginning of the cal code  
n = 0
for qwe in to_be_read:
    
    dataL = pd.read_csv(filesl[qwe])                       

    
    Filename = filesl[qwe][-12:]
  
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
        for num in pids_on_master:
            try:
                dataL['pid%s'%str(num)]
                pids_on_new.append(num)
            except KeyError:
                pass
                
        pids_on = pids_on_new
        print pids_on
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
        
        dataL.Temp *=10
        RH /= (1.0546-(0.00216*dataL.Temp)) # Temperature correction
        ############## ############## ############## ############## 
        
        
        
        
        
        ############## ############## Trying to find where the RH changes Drastically (for new cal Points) ############## ############## 
        
        RH_set = []
        
        timing = 150 
    
        sensitivty_mean = np.nanmean([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)]) # the mean of the rolling mean
        sesnitivty_std = np.nanstd([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)]) # the standard of the rolling standard
    
        
        #finds where the drastic changes are in the RH data        
        for i in xrange(0,len(RH)-timing,timing):
            if abs(RH[i]-RH[i+timing]) >= sensitivty_mean+sesnitivty_std:
                RH_set.append(i)
    
                
        
        Setters = []
        for i in xrange(0,len(RH_set)):
            if abs(RH_set[i-1]-RH_set[i]) > 300:
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
        
        
        # Ammends the bad cal points for all pids
        SF_indexes = pd.DataFrame(index = ['S','F'], columns = ['RH']+['Pid%s'%num for num in pids_on])
        

        
        for num in pids_on:
            SF = cal_point_ammender(pid_data[num],bad_cal_length,S,F)
            SF_indexes['Pid%s'%num]['S'] = SF[0]
            SF_indexes['Pid%s'%num]['F'] = SF[1]
            
            
                
        diff = data_point_length   
        
        
        #Rolling Averages of the pids and RH
        Rolling_Averages = pd.DataFrame(index = pids_on+['RH'], columns = ['Rolling Average'])
        #Chunked up data for the pids and RH, for plotting
        Spliced_Data = pd.DataFrame(index = pids_on, columns = ['Pids','Pids listsout','Pid_Avgs','RH','RH listout','Isop listout','Times'])
    
    
        
        
        #filling the roling averages and spliced data dataframes
        
    
        
        Rolling_Averages['Rolling Average']['RH'] = pd.rolling_mean(RH,200,20)
        
        for num in pids_on:
                Rolling_Averages['Rolling Average'][num] = pd.rolling_mean(pid_data[num],200,20)
                
            
                Spliced_Data['Times'][num] = list_multisplicer(dataL.TheTime,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                
                Spliced_Data['RH'][num] = list_multisplicer(RH,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                Spliced_Data['RH listout'][num] = list_multisplicer_listsout(RH,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                
                Spliced_Data['Isop listout'][num] = list_multisplicer_listsout(isop_mr,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                
                Spliced_Data['Pids'][num] = list_multisplicer(pid_data[num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                Spliced_Data['Pids listsout'][num] = list_multisplicer_listsout(pid_data[num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
            
                Spliced_Data['Pid_Avgs'][num] = list_multisplicer(Rolling_Averages['Rolling Average'][num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
        
        
        
        ############## ############## ############## ############## ############## ############## ############## ############## 
        #Calculating the mean of the data in the chunks for the cal points
        Voltages = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in Spliced_Data['Pids listsout'][num]] for num in pids_on})
        
        # Calculating the standard errors for the cal points
        Errors = pd.DataFrame({'Pid%s Stderr'%(num) : [np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['Pids listsout'][num]] for num in pids_on})
        
        #Finding time at Start and end of cal points
        Start_Times = pd.DataFrame({'Start Time': [dataL.TheTime[i] for i in S]})
        End_Times = pd.DataFrame({'End Time': [dataL.TheTime[i] for i in F]})
        
        #Finding the mean of the isoprene in the chunks and the standard error (like Voltages adn Errors)
        Isoprene_error = pd.DataFrame({'Isop Error': [np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['Isop listout'][num]]})
        Isoprene = pd.DataFrame({'Isop': [np.nanmean(i) for i in Spliced_Data['Isop listout'][num]]})
    
        #Average  RH for the chunks
        cal_RH = pd.DataFrame({'RH':[np.nanmean(i) for i in Spliced_Data['RH listout'][num]]})
        Error_RH = pd.DataFrame({'RH Stderr':[np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['RH listout'][num]]})   
        #merges above dataframes into one (for corrected and uncorrected data)
        cal_df = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Error_RH,Voltages, Errors], axis=1, join='inner')
    
        ############## ############## Deciding the columns in cal_df and chunking the data ############## ############## 
            
        RH_fit = [0.,np.max(cal_df.RH)]
    
        
    
        xerr = [cal_df['RH Stderr'][i] for i in xrange(0,len(cal_df))]
        
        #Values of Slopes, Intercepts and errors
        Values = pd.DataFrame(index = pids_on, columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])
        
        
        
    
        
        
        
        pid_fits = {num:[] for num in pids_on}
        
        
        xdata = [i for i in cal_df['RH']]
        
        for num in pids_on:
                
                yerr = [cal_df['Pid%s Stderr'%str(num)][i] for i in xrange(0,len(cal_df))]
                
                ydata = [i for i in cal_df['Pid%s Voltage'%num]] 
                
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
                
                Slope_Intercepts.loc[n,'Filename'] = Filename
                Slope_Intercepts.loc[n,'Pid%s Intercept'%num] = Values.loc[num,'Intercepts']
                Slope_Intercepts.loc[n,'Pid%s Intercept Error'%num] = Values.loc[num,'Intercept Errors']
                Slope_Intercepts.loc[n,'Pid%s Slope'%num] = Values.loc[num,'Slopes']
                Slope_Intercepts.loc[n,'Pid%s Slope Error'%num] = Values.loc[num,'Slope Errors']                
        
        #Storing all the dataframe information into a dictionary
        cal_dfs[n] = cal_df
        


    print 'Isop = ', Isop
    n = n+1
    print '%s down, %s to go'%(n,str(len(to_be_read)-n)), '( ',np.around(float(n*100)/len(to_be_read),1),'% )\n\n'







# Saving the Data


try:
#    data_already_in_cal_points = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Cal Points.txt', sep=',')    
    data_already_in_cal_points = pd.read_csv('/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Cal Points.txt', sep=',')
    there_is_already_data_in_the_file = 'Y'
        
except IOError:
    there_is_already_data_in_the_file = 'N'    
    
    
    

try:
#    data_already_there_slopes = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Slope Intercepts.txt', sep = ',')        
    data_already_there_slopes = pd.read_csv('/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Slope Intercepts.txt', sep = ',')    
    there_is_already_slopes_in_the_file = 'Y'
    
except IOError:
    there_is_already_slopes_in_the_file = 'N'
    
    
    
    
    
if there_are_new_values_to_be_added == 'Y':   
    New_Values = pd.concat([cal_dfs[n] for n in xrange(0,len(to_be_read))], axis=0)
    
    if there_is_already_data_in_the_file == 'Y':

        Final_Values = data_already_in_cal_points.append(New_Values)



            
#        Final_Values.to_csv(path_or_buf='C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Cal Points.txt', sep=',')            
        Final_Values.to_csv(path_or_buf='/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Cal Points.txt', sep=',')
    else:
#        New_Values.to_csv(path_or_buf='C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Cal Points.txt', sep=',')
        New_Values.to_csv(path_or_buf='/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Cal Points.txt', sep=',')
    
    
    
    
    
    
    if there_is_already_slopes_in_the_file == 'Y':
        
        Final_Slopes = data_already_there_slopes.append(Slope_Intercepts)
        
#        Final_Slopes.to_csv(path_or_buf = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Slope Intercepts.txt', sep = ',')
        Final_Slopes.to_csv(path_or_buf = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Slope Intercepts.txt', sep = ',')
    else:
#        Slope_Intercepts.to_csv(path_or_buf = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\RH Slope Intercepts.txt', sep = ',')
        Slope_Intercepts.to_csv(path_or_buf = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis//RH Slope Intercepts.txt', sep = ',')
          




