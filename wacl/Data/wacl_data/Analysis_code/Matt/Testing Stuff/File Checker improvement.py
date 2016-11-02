import pandas as pd
import numpy as np
import scipy.optimize as opt
import datetime
from time import strftime
import os

########### ########### Control Panel ########### ###########
print 'Defining functions and variables needed later...\n'
# To control the files that get calibrated
path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files'
month1= 9
month2 = 9
day1 =7
day2 = 7
filenumbers = 20
min_filesize = 750000L
max_filesize = 185032288L


pid_corrections = {3:(1.8664285714285712e-05),4:(9.2661904761904766e-06),5:(2.6714285714285718e-05)}

pd.set_option('precision',8)


data_point_length = 360 # how many data points used for the cals
bad_cal_length = data_point_length



humid_correct = 'Y'


pids_on = [3,4,5]



questions = 'Y'


##################################################### Defining Functions For Use Later #################################################
### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation

def cal_point_ammender(data_set,bad_cal_length,S,F):
    
    shifter = len(dataL)/(20*len(S)*11) # shifts cal chunk by a quarter of the length of the cal point either side of the original chunk (from the end indexes back by the the how many data points are being used) (20 is the number of iterations of the chunk getting moved then the standard deviation being found)
    
    Snew = np.zeros(len(S)) # creating a new list for new start indices
    Fnew = np.zeros(len(F)) # creating a new list for new end indices 
     
    for i in xrange(0,len(S)): # loops over all cal points

        orig_std = np.nanstd(data_set[S[i]:F[i]]) # finds the original standard deviation (of chunk in question)
        
        if orig_std > 0.7: # if the original standard deviation is too high set the data point length to the bad cal length (shorter distance between S and F but currently set to be the same)
            S[i] = F[i] - bad_cal_length

        # left_shift_stds compiles a dictionary of the standard deviations of the chunk shifted left (by the length of the shifter, 20 times)
        left_shift_stds = {k:[np.nanstd(data_set[S[i]-(k*shifter):F[i]-(k*shifter)])] for k in xrange(0,20)} # 20 is the number of iterations (how many times the code shifts the chunk and takes the standard deviation)
        nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])] #If there are any nans in the dictionary then this finds their indexes and then the for loop below removes them.
        for t in nanL:
            del(left_shift_stds[t])
            
        minPairL = min(left_shift_stds.iteritems(), key=itemgetter(1)) # finding minimum standard deviation and the index



        right_shift_stds = {k:[np.nanstd(data_set[S[i]+(k*shifter):F[i]+(k*shifter)])] for k in xrange(0,20)}
        nanR = [q for q in right_shift_stds if np.isnan(right_shift_stds[q])]
        for t in nanR:
            del(right_shift_stds[t])
            
        minPairR = min(right_shift_stds.iteritems(), key=itemgetter(1))
        
                            
        if minPairL[1][0] < minPairR[1][0]:
            
            Snew[i] = S[i] - minPairL[0]*shifter
            Fnew[i] = F[i] - minPairL[0]*shifter
            
        elif minPairL[1][0] > minPairR[1][0]:
            Snew[i] = S[i] + minPairR[0]*shifter
            Fnew[i] = F[i] + minPairR[0]*shifter
        else:
            
            Snew[i] = S[i]
            Fnew[i] = F[i]
    Snew = list(Snew)
    Fnew = list(Fnew)   
            
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

# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))
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
    if day1 <= 0:
        day1 = 1
    if day2 > 31:
        day2 = 31
    for month in np.arange(month1, month2):
        if month < 10:
            month = '0'+str(month)
        path1 = path + '\\2015'+str(month)+'\\d2015'+str(month)
        for day in range (day1,day2):
            if day < 10:
                day = '0'+str(day)
            path2 = path1 + str(day)

            for filenumber in np.arange(1,number_of_files):
                pfl.append(path2+'_0'+str(filenumber))

    filesl = []
    for i in pfl:
        if os.path.exists(i):
            if os.path.getsize(i) < max_file_size_limit and os.path.getsize(i) > min_file_size_limit: 
                filesl.append(i)
      

            
    return filesl
    
    
        
#To convert timestamps to a string
def timeconverter(T):
    #	print T
   	return (datetime.datetime.strptime(T,"%y-%m-%d-%H-%M-%S-%f"))


#Splices list at indexes given by 2 lists
def list_multisplicer(l1st,start_inidexes,end_indexes):
    new_lt = []
    for i in np.arange(0,len(start_inidexes)):
        first = start_inidexes[i]
        last = end_indexes[i]
        for pt in np.arange(0,len(l1st)):
            if pt >=first and pt <=last:
                new_lt.append(l1st[pt])
    return new_lt
    
def list_multisplicer_listsout(l1st,start_indexes,end_indexes):
            new_lt = []
            for i in np.arange(0,len(start_indexes)):
                segments = []
                first = start_indexes[i]
                last = end_indexes[i]
                for pt in np.arange(0,len(l1st)):
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
            
            for i in np.arange(0,len(y)):    
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


#pid3_correction = 2.59E-05
#pid4_correction = 1.36E-5
#pid5_correction = 3.03E-5
print 'Opening files...\n'

calfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Cal Data.txt','a')
calfilec = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Cal Data Corrected.txt','a')
slopesfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Slopes.txt','a')
if humid_correct == 'Y':
    slopescorrectedfile = open('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Slopes Corrected.txt','a')


try:
    pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Cal Data.txt',sep='\t')
except:
    slope_string = ''
    if 3 in pids_on:
        slope_string = slope_string + '\tSlope 3\tSlope Error 3'
    if 4 in pids_on:
        slope_string = slope_string + '\tSlope 4\tSlope Error 4'
    if 5 in pids_on:
        slope_string = slope_string + '\tSlope 5\tSlope Error 5'
        
        
    Pid_String = ''
    if 3 in pids_on:
        Pid_String = Pid_String + '\tPid 3\tPid Error 3'
    if 4 in pids_on:
        Pid_String = Pid_String + '\tPid 4\tPid Error 4'
    if 5 in pids_on:
        Pid_String = Pid_String + '\tPid 5\tPid Error 5'
    
    
    
    calfile.write('Filename\tThe Time\tRH\tIsop%s\n'%(Pid_String))
    
    
    calfilec.write('Filename\tThe Time\tRH\tIsop%s\n'%(Pid_String))
    
    
    slopesfile.write('The Time'+'\t'+'RH'+slope_string+'\n')
    
    if humid_correct == 'Y':
        
        slopescorrectedfile.write('The Time'+'\t'+'RH'+slope_string+'\n')


filesl = FileChecker(path,month1,month2,day1,day2,filenumbers,min_filesize,max_filesize)


print 'Just Checking which files are cal files...\n'
filesln = []   
for filei in filesl:  
    data = pd.read_csv(filei)
    if np.nanstd(data.mfcloR) > 0.6:
        filesln.append(filei)   
        
        
        
        


     
          
               
                    
                              
    
already_read_checker = []

print 'Checking for any cals that are already recorded...\n'
for tkm in  xrange(0,len(filesln)):
    
    try:
        data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Cal Data.txt', sep = '\t')                       
        filename = str(filesln[tkm][-12:])
    
        
        if not filename in set(data.Filename):
            already_read_checker.append(tkm)
    except ValueError:
        already_read_checker = [i for i in xrange(0,len(filesln))]
        
        
if len(already_read_checker) == 0:
    print 'There are no files to be read in the specified range'
else:
    x = len(already_read_checker)
    if x > 1:
        print 'Okie Doke adding %s extra cals then' % str(x)
    if x == 1:
        print 'Okie Doke adding 1 extra cal then'
    print 'Running Calibrations and writing text files...\n'      
        
n = 0
      
for filei in already_read_checker:
    try:
        try:
            date = int(filesln[filei][-7:-3])
        except ValueError:
            date = int(filesln[filei][-8:-4])
            
        filename = str(filesln[filei][-12:])
        dataL = pd.read_csv(filei,sep='\t')
        for num in pids_on:
            try:
                dataL['pid%s'%str(num)]
            except KeyError:
                pids_on.remove(num)
        
        pid_names = {i:['Pid %s' % (str(i))] for i in pids_on}
        
        pid_fits = {num:[] for num in pids_on}
        pidc_fits = {num:[] for num in pids_on}
        
        
        
        if np.nanstd(dataL.mfcloR) < 0.5:
            proceed = raw_input('Sorry this doesn\'t look like a cal file, the isop level doesn\'t really change much\n\nWould you like to proceed? ')
        else:
            proceed = 'Y'
            
        if proceed.upper() == 'Y' or proceed.upper() == 'YES':
            dataL.mfcloR = nan_helper(dataL.mfcloR,10,3) # using the nanhelper function defined above to fill in the nan values (10 is the rolling mean length, 3 is the maximum number of nans in the rolling mean)
            print 'Analysing and Adjusting...'
            print '\tAdjusting the Times...'
            
            ##   Sorting out the Times   ##
            TimeL = dataL.TheTime-dataL.TheTime[0]
            TimeL*=60.*60.*24.
            
            dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
            T1 = pd.datetime(1899,12,30,0)
            T2 = pd.datetime(1970,01,01,0)
            offset=T1-T2
            dataL.TheTime+=offset
            
            #### Relative Humidity ###
            print '\tAdjusting the RH...'
            if int(date) >= 903:
                dataL.RH = nan_helper(dataL.RH,10,3) # RH correction
                RH = dataL.RH
                RH /=4.96
                RH -= 0.16
                RH /= 0.0062
                
                RH /= (1.0546-(0.00216*dataL.Temp)) # Temperature correction
        
            else:
                humid_correct = ''
                
            
            print '\tAdjusting the isop...'
            ## Adjusting for the isop conc        
            isop_cyl = 13.277	#ppbv
            mfchi_range = 100.	#sccm
            mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
            
            mfclo_range = 20.	#sccm
            mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
            
            dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
            isop_mr = dil_fac*isop_cyl
        
            
                
            # sets any nan mfchi values to 5, only use if mfchi set is always 5
            print 'Filling in missing mfchi values...'
            dataL['mfchi'] = [(5+((0*i)+1)) for i in xrange(0,len(dataL))] 
            dataL = dataL.fillna({'mfchi':5})
            
            
            pid_data = {num : nan_helper(dataL['pid%s'%(str(num))],10,3) for num in pids_on} # uses nan helper here
            pid_data_corrected = {num : pid_data[num]-(RH*pid_corrections[num]) for num in pids_on} # performs a point by point RH correction
                
        
            
            #############################
            ## Signal vs Isop for calibration experiments
            print 'Setting Cal Points...'   
            
                
            mfc_set = np.zeros((len(dataL.mfclo)),dtype=bool)
            for i in xrange(1,len(dataL.mfchi)):
                if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i-1],dataL.mfclo[i]!=dataL.mfclo[i-1]))):
                        mfc_set[i] = "True"
                        
            cal_N = np.sum(mfc_set) # number of changes in value for mfclo
                
            cal_pts = [xrange(0,cal_N)]
        
            
        
            mfc_setF = dataL.index[mfc_set]
                
            mfc_setS = [i-data_point_length for i in mfc_setF]    
        
            if mfc_setS[0] < 0:         
                S = negative_remover(mfc_setS,mfc_setF)[0]
                F = negative_remover(mfc_setS,mfc_setF)[1]          
            else:
                S = list(mfc_setS)
                F = list(mfc_setF) 
            
            if F[0] < 500:
                del(F[0])
                del(S[0])
            
        
            SF_indexes = {num:cal_point_ammender(pid_data[num],bad_cal_length,S,F) for num in pids_on} # This is what calls the ammender to minimise standard deviation of the cal points (for uncorrected)
            SF_indexes_corrected = {num:cal_point_ammender(pid_data_corrected[num],bad_cal_length,S,F) for num in pids_on} # This is finding the best indecies for the corrected data usin cal point ammender
                        
        
        
            
            #Calculating the mean of the data in the chunks for the cal points
            Voltages = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in list_multisplicer_listsout(pid_data[num],SF_indexes[num][0],SF_indexes[num][1])] for num in pids_on})
            
            # Calculating the standard errors for the cal points
            Errors = pd.DataFrame({'Pid%s Stderr'%num : [np.nanstd(i)/np.sqrt(data_point_length) for i in list_multisplicer_listsout(pid_data[num],SF_indexes[num][0],SF_indexes[num][1])] for num in pids_on})
            
            #Finding time at Start and end of cal points
            Start_Times = pd.DataFrame({'Start Time': [TimeL[i] for i in S]})
            End_Times = pd.DataFrame({'End Time': [TimeL[i] for i in F]})
            
            #Finding the mean of the isoprene in the chunks and the standard error (like Voltages adn Errors)
            Isoprene_error = pd.DataFrame({'Isop Error': [np.nanstd(i)/np.sqrt(data_point_length) for i in list_multisplicer_listsout(isop_mr,S,F)]})
            Isoprene = pd.DataFrame({'Isop': [np.nanmean(i) for i in list_multisplicer_listsout(isop_mr,S,F)]})
        
            #Average  RH for the chunks
            cal_RH = pd.DataFrame({'RH':[np.nanmean(i) for i in list_multisplicer_listsout(RH,S,F)]})
            
            # Same as Voltages and Errors above but corrected for RH
            Voltages_corrected = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in list_multisplicer_listsout(pid_data_corrected[num],SF_indexes_corrected[num][0],SF_indexes_corrected[num][1])] for num in pids_on})
            Errors_corrected = pd.DataFrame({'Pid%s Stderr'%num : [np.nanstd(i)/np.sqrt(data_point_length) for i in list_multisplicer_listsout(pid_data_corrected[num],SF_indexes_corrected[num][0],SF_indexes_corrected[num][1])] for num in pids_on})
            
            #merges above dataframes into one (for corrected and uncorrected data)
            cal_df = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Voltages, Errors], axis=1, join='inner')
            cal_dfc = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Voltages_corrected, Errors_corrected], axis=1, join='inner')
            ########################## Zero Averaging #########################
            
            #finds the index of the data frame when Isoprene = 0
            isop_zero_indexes = [i for i in xrange(0,len(cal_df.Isop)) if cal_df.Isop[i] < 0.2] #use np.around here
        
            #Sets the pid voltages when the isoprene is zero to the average of the pid voltages when the isoprene when the isoprene is zero, for each pid.
            cal_df.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]] = [np.mean(cal_df.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]])[i] for i in xrange(0,len(pids_on))]
            cal_dfc.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]] = [np.mean(cal_dfc.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]])[i] for i in xrange(0,len(pids_on))]
        
            
            #Drops the duplicates that arise when setting the pid voltages when isoprene = 0, in cal_df/cal_dfc, to the average of the pid voltages when isoprene = 0
            cal_df = cal_df.drop_duplicates(subset = ['Pid%s Voltage'%num for num in pids_on])
            cal_dfc = cal_dfc.drop_duplicates(subset = ['Pid%s Voltage'%num for num in pids_on])
            
            #resets the indexes so the code works
            cal_df.index = xrange(0,len(cal_df))
            cal_dfc.index = xrange(0,len(cal_dfc))       
            
            
            isop_fit = [0.,np.max(cal_df.Isop)]    
            
            xdata = cal_df.Isop
            
            
            # Stores the slope values and intecept values and errors
            Values = {'Slope':{num:[] for num in pids_on},'Intercept':{num:[] for num in pids_on},'Slope Error':{num:[] for num in pids_on},'Intercept Error':{num:[] for num in pids_on}} #update to be a dict_comphrension
            Corrected_Values = {'Slope':{num:[] for num in pids_on},'Intercept':{num:[] for num in pids_on},'Slope Error':{num:[] for num in pids_on},'Intercept Error':{num:[] for num in pids_on} }
        
        
            for num in pids_on:
                
                if humid_correct == 'Y':
                    
                        ydatac = cal_dfc.loc[:,'Pid%s Voltage'%str(num)]
                        # Finds the fit     
                        slope_interceptc,pcovc = opt.curve_fit(linear_fit, xdata, ydatac, sigma = cal_dfc['Pid%s Stderr' %(num)])
            
                        pidc_fits[num] = (slope_interceptc[0],(np.max(cal_df.Isop)*slope_interceptc[1])+slope_interceptc[0])
                        #Finds errors from the pcov output (above)
                        perrc = np.sqrt(np.diag(pcovc))    
                        Intercept_errorc = perrc[0]/np.sqrt(cal_N)
                        Slope_Errorc = perrc[1]/np.sqrt(cal_N)
        
                        Corrected_Values['Slope'][num] = slope_interceptc[1]
                        Corrected_Values['Intercept'][num] = slope_interceptc[0]
                        Corrected_Values['Slope Error'][num] = Slope_Errorc
                        Corrected_Values['Intercept Error'][num] = Intercept_errorc
                                            
            
                ydata = cal_df.loc[:,'Pid%s Voltage'%str(num)]  
                slope_intercept,pcov = opt.curve_fit(linear_fit, xdata, ydata, sigma = cal_df['Pid%s Stderr' %(num)])
                pid_fits[num] = (slope_intercept[0],(np.max(cal_df.Isop)*slope_intercept[1])+slope_intercept[0])
                
                perr = np.sqrt(np.diag(pcov))    
                Intercept_error = perr[0]/np.sqrt(cal_N)
                Slope_Error = perr[1]/np.sqrt(cal_N)
                
                Values['Slope'][num] = slope_intercept[1]
                Values['Intercept'][num] = slope_intercept[0]
                Values['Slope Error'][num] = Slope_Error
                Values['Intercept Error'][num] = Intercept_error
                
            RH_mean = str(np.nanmean(RH))   
                
            for pkl in xrange(0,len(cal_df)):
                Isop_string = ''
                Isop_stringc = ''
                if 3 in pids_on:
                    Isop_string = Isop_string +'\t'+ str(cal_df.loc[pkl,'Pid3 Voltage'])+'\t'+str(cal_df.loc[pkl,'Pid3 Stddev']/np.sqrt(data_point_length))
                if 4 in pids_on:
                    Isop_string = Isop_string +'\t'+ str(cal_df.loc[pkl,'Pid4 Voltage'])+'\t'+str(cal_df.loc[pkl,'Pid4 Stddev']/np.sqrt(data_point_length))
                    
                if 5 in pids_on:
                    Isop_string = Isop_string+'\t'+str(cal_df.loc[pkl,'Pid5 Voltage'])+'\t'+str(cal_df.loc[pkl,'Pid5 Stddev']/np.sqrt(data_point_length))
                else:
                    Isop_string = Isop_string+'\t\t'
                calfile.write(filename+'\t'+str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+'\t'+str(cal_df.loc[pkl,'Isop'])+Isop_string+'\n')
            
                
                if humid_correct == 'Y':     
                    if 3 in pids_on:
                        Isop_stringc = Isop_stringc +'\t'+ str(cal_dfc.loc[pkl,'Pid3 Voltage'])+'\t'+str(cal_dfc.loc[pkl,'Pid3 Stddev']/np.sqrt(data_point_length))
                    if 4 in pids_on:
                        Isop_stringc = Isop_stringc +'\t'+ str(cal_dfc.loc[pkl,'Pid4 Voltage'])+'\t'+str(cal_dfc.loc[pkl,'Pid4 Stddev']/np.sqrt(data_point_length))
                        
                    if 5 in pids_on:
                        Isop_stringc = Isop_stringc+'\t'+str(cal_dfc.loc[pkl,'Pid5 Voltage'])+'\t'+str(cal_dfc.loc[pkl,'Pid5 Stddev']/np.sqrt(data_point_length))    
                    else:
                        Isop_stringc = Isop_stringc+'\t\t'       
                    calfilec.write(filename+'\t'+str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+'\t'+str(cal_df.loc[pkl,'Isop'])+Isop_stringc+'\n')
        
        
             
        
        
        
        slope_values_string = ''
        
        for num in pids_on: 
            slope_values_string = slope_values_string + '\t' + str(Values['Slope'][3]) + '\t' + str(Values['Slope_Error'][3])

            
        slopesfile.write(str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+slope_values_string+'\n')   
        
        if humid_correct == 'Y':
        
            slope_values_stringc = ''
            for num in pids_on: 
                slope_values_stringc = slope_values_stringc + '\t' + str(Corrected_Values['Slope'][3]) + '\t' + str(Corrected_Values['Slope_Error'][3])
            
            slopescorrectedfile.write(str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+slope_values_stringc+'\n')
          
        n = n+1
        if n == len(already_read_checker)/2:
            print 'Halfway There!\n'
        elif n == len(already_read_checker):
            print '\n\nAll Done! :D'
        print '%s down, %s to go'%(n,str(len(already_read_checker)-n)), '( ',np.around(float(n*100)/len(already_read_checker),1),'% )'   
         
    except 'bob':
        print '\n\n--------------------\n\n'
        print filesln[filei], 'This isn\'t working'
        print '\n\n--------------------\n\n'
        
#(IndexError,ValueError,TypeError)   
calfilec.close()        
calfile.close()
slopesfile.close()
if humid_correct == 'Y':
    slopescorrectedfile.close()
