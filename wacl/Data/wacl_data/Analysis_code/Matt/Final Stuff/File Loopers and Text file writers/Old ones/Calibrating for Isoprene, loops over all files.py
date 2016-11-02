import pandas as pd
import numpy as np
import datetime
from time import strftime
import os
from operator import itemgetter
import scipy.odr as odr


########### ########### Control Panel ########### ###########
print 'Defining functions and variables needed later...\n'
# To control the files that get calibrated
path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files'
month1= 9
month2 = 9
day1 =4
day2 = 30
filenumbers = 20
min_filesize = 750000L
max_filesize = 185032288L


pid_corrections = {3:(1.95036842105e-05),4:(8.74714285714e-06),5:(2.70684210526e-05)}

pd.set_option('precision',8)


data_point_length = 360 # how many data points used for the cals
bad_cal_length = data_point_length



humid_correct = 'Y'

pids_on = np.arange(0,10)



##################################################### Defining Functions For Use Later #################################################
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

    if list1[0] < 0:
        negative_removerS = [i for i in xrange(0,len(list1)) if list1[i]<0]
        negative_removerF = [i for i in xrange(0,len(list2)) if list2[i]<0]

        if negative_removerF < negative_removerS:
            negative_removerF = max(negative_removerS)
            negative_removerS = max(negative_removerS)+1         
        
            A = [0] + list1[negative_removerS:]
            B = list2[negative_removerF:]
        else:
            A = list1[max(negative_removerS)+1:]
            B = list2[max(negative_removerF)+1:]
        
        if len(A)<len(list1):
            A = list(np.zeros(len(list1)-len(A)))+A
        if len(B)<len(list2):
            B = list(np.zeros(len(list2)-len(B)))+B
        return list(A),list(B)
        
        
    else:
        return list(list1),list(list2)

# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))
####### Checks if the files exsist and returns a list of files that do exist
def FileChecker(path,month1, month2, day1,day2,number_of_files,min_file_size_limit,max_file_size_limit):#pop a year in here
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
    for month in xrange(month1, month2):
        if month < 10:
            month = '0'+str(month)
        path1 = path + '\\2015'+str(month)+'\\d2015'+str(month)
        for day in xrange(day1,day2):
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
#For the scipy.odr
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


############################################################################################################################################################
bad_files = []





filesl = FileChecker(path,month1,month2,day1,day2,filenumbers,min_filesize,max_filesize) #Creating a list of all files that are there





print 'Just Checking which files are cal files...\n'
#Finds files that have a changing isoprene concentration and adds them to a list to be read.
#This is to distinguish between isoprene cals and RH cals.
filesln = []   
for filei in filesl:  
    data = pd.read_csv(filei)
    if np.nanstd(data.mfcloR) > 0.6:
        filesln.append(filei)   
#############################        
        
        
        
        
        
to_be_read = [] # indicies of files to be read for filesl

print 'Checking for any cals that are already recorded...\n'
for tkm in  xrange(0,len(filesln)):
    # compares the filename of the files to be read to the filenames that have already been read and stored. If there are any missing, then it puts the index of the file from the list filesl into the to_be_read list.
    try:
        data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Slope and Intercepts.txt', sep = ',')                       
        filename = str(filesln[tkm][-12:])
    
        
        if not filename in set(data.Filename):
            to_be_read.append(tkm)
    except IOError:
        to_be_read = [i for i in xrange(0,len(filesln))]
########################################################    




# If you want to read all filesl in the list, and ignore the to_be_read checker then uncomment the line below   
#to_be_read = [i for i in xrange(0,len(filesl))]  
   
 
  
# Finds which Pids are going to be read, and it makes a list of them.    
pids_on_master = [] # This list is a list of all pids that are going to be read when the program is running


for qwe in to_be_read:  
    dataL = pd.read_csv(filesln[qwe]) 
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
####################################





# This creates a string to be the header of the new dataframe storing all the information on the cals
Pids_string = '' 
for num in pids_on_master:
    Pids_string = Pids_string +'\tPid%s\tPid%s Error'%(num,num)
################################################################




# Stores information about the slope and intercept of each cal
Slope_Intercepts = pd.DataFrame(index = xrange(0,len(to_be_read)),columns = ['Filename']+['Pid%s Slope'%num for num in pids_on_master]+['Pid%s Slope Error'%(num) for num in pids_on_master]+['Pid%s Intercept'%num for num in pids_on_master]+['Pid%s Intercept Error'%(num) for num in pids_on_master])   

# Stores information about the slope and intercept of each cal
Slope_Interceptsc = pd.DataFrame(index = xrange(0,len(to_be_read)),columns = ['Filename']+['Pid%s Slope'%num for num in pids_on_master]+['Pid%s Slope Error'%(num) for num in pids_on_master]+['Pid%s Intercept'%num for num in pids_on_master]+['Pid%s Intercept Error'%(num) for num in pids_on_master])   



# Creates a ditionary of all the cal_dfs        
cal_dfs = {i:() for i in xrange(0,len(to_be_read))}  
# df.append() might work better here (I couldn't make it work though)        
        

# Creates a ditionary of all the corrected cal_dfs        
cal_dfcs = {i:() for i in xrange(0,len(to_be_read))}  
# df.append() might work better here (I couldn't make it work though)            
####################################################  
        
              
                    
                          
                                      
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
#################################################        
        
        
        
        
        
# Beginning of the cal code    

            
n = 0
      
for filei in to_be_read:
    try:
        try:
            date = int(filesln[filei][-7:-3]) # Finding the date of the file
        except ValueError:
            date = int(filesln[filei][-8:-4])
            
        Filename = str(filesln[filei][-12:]) #Finding the filename

        dataL = pd.read_csv(filesln[filei], sep=',')
        
        
        # Finding which pids are in the file
        pids_on_new = []
        for num in pids_on_master:
            try:
                dataL['pid%s'%str(num)]
                pids_on_new.append(num)
            except KeyError:
                pass
                
        pids_on = pids_on_new
        print pids_on
        #############################
        
        
        pid_fits = {i:[] for i in pids_on}
        pidc_fits = {i:[] for i in pids_on}
        pid_names = {i:['Pid %s' % (str(i))] for i in pids_on}
        
        
        
        if np.nanstd(dataL.mfcloR)/len(dataL) < 0.00003:
            proceed = ''
        else:
            proceed = 'Y'
        print 'Loading...\n'    
        if proceed.upper() == 'Y' or proceed.upper() == 'YES':
            dataL.mfcloR = nan_helper(dataL.mfcloR,10,3) # using the nanhelper function defined above to fill in the nan values (10 is the rolling mean length, 3 is the maximum number of nans in the rolling mean)
            ############################################
            
            
            
            ##   Sorting out the Times   ##
            TimeL = dataL.TheTime-dataL.TheTime[0]
            TimeL*=60.*60.*24.
            
            dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
            T1 = pd.datetime(1899,12,30,0)
            T2 = pd.datetime(1970,01,01,0)
            offset=T1-T2
            dataL.TheTime+=offset
            #####################
            

            #### Relative Humidity ###

            dataL.RH = nan_helper(dataL.RH,10,3) # RH correction
            RH = dataL.RH
            RH /=4.96
            RH -= 0.16
            RH /= 0.0062
            
            dataL.Temp *=10
            RH /= (1.0546-(0.00216*dataL.Temp)) # Temperature correction
            #############################################################
                
                
                
            
            ## Adjusting for the isop conc        
            isop_cyl = 13.277	#ppbv
            mfchi_range = 100.	#sccm
            mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
            
            mfclo_range = 20.	#sccm
            mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
            
            dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
            isop_mr = dil_fac*isop_cyl
            ##########################
            
                
            # sets any nan mfchi values to 5, only use if mfchi set is always 5
            dataL['mfchi'] = [(5+((0*i)+1)) for i in xrange(0,len(dataL))] 
            dataL = dataL.fillna({'mfchi':5})
            #################################
            
            
            
            # Storing Dictionaries for the pid data
            pid_data = {num : nan_helper(dataL['pid%s'%(str(num))],10,3) for num in pids_on} # uses nan helper here
            pid_data_corrected = {num : pid_data[num]-(RH*pid_corrections[num]) for num in pids_on} # performs a point by point RH correction
            ##################################################################################################################################    
        
            
            
            
            
            ## Finding where the isoprene concentration changes
            mfc_set = np.zeros((len(dataL.mfclo)),dtype=bool)
            for i in xrange(1,len(dataL.mfchi)):
                if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i-1],dataL.mfclo[i]!=dataL.mfclo[i-1]))):
                        mfc_set[i] = "True"
            ###############################
            
            
            
                        
            # Defining useful variables for later                                    
            cal_N = np.sum(mfc_set) # number of changes in value for mfclo 
                
            cal_pts = [xrange(0,cal_N)] # index for cal_df
            ###########################
            
        
        
        
            #Setting indexes to take the cal data from
            mfc_setF = list(dataL.index[mfc_set]) # The of each cal point
                
            mfc_setS = [i-data_point_length for i in mfc_setF]    
        
            if mfc_setS[0] < 0:         
                S = negative_remover(mfc_setS,mfc_setF)[0]
                F = negative_remover(mfc_setS,mfc_setF)[1]          
            else:
                S = list(mfc_setS)
                F = list(mfc_setF) 
            ######################
        
        
        
        
        
            # Creating dataframes to store the ammended setter indexes
            SF_indexes = pd.DataFrame(index = ['S','F'], columns = ['RH']+['Pid%s'%num for num in pids_on])
            SF_indexes_corrected = pd.DataFrame(index = ['S','F'], columns = ['RH']+['Pid%s'%num for num in pids_on])
            ##########################################################################################################
            
            
            
            
            # Ammending the Setter indexes to find the flatest part of the signal to take the cal data from                        
            for num in pids_on:
                SF = cal_point_ammender(pid_data[num],bad_cal_length,S,F)
                SF_indexes['Pid%s'%num]['S'] = SF[0]
                SF_indexes['Pid%s'%num]['F'] = SF[1]
                
                SFc = cal_point_ammender(pid_data_corrected[num],bad_cal_length,S,F)
                SF_indexes_corrected['Pid%s'%num]['S'] = SFc[0]
                SF_indexes_corrected['Pid%s'%num]['F'] = SFc[1]
            ###################################################
            
            
            
            
            
            # Creating DataFrames to store the rolling average information.
            Rolling_Averages = pd.DataFrame(index = pids_on+['RH'], columns = ['Rolling Average'])
            
            Corrected_Rolling_Averages = pd.DataFrame(index = pids_on+['RH'], columns = ['Rolling Average'])
            ################################################################################################
            
            
            
            # Creating DataFrames to store the spliced data.
            Spliced_Data = pd.DataFrame(index = pids_on, columns = ['Pids','Pids listsout','Pid_Avgs','RH','RH listout','Isop listout','Times'])
    
            Corrected_Spliced_Data = pd.DataFrame(index = pids_on, columns = ['Pids','Pids listsout','Pid_Avgs','RH','RH listout','Isop listout','Times'])
            ##############################################################################################################################################
            
            
            
            
            #Filling the roling averages and spliced data dataframes        
            Rolling_Averages['Rolling Average']['RH'] = pd.rolling_mean(RH,200,20)
            Corrected_Rolling_Averages['Rolling Average']['RH'] = Rolling_Averages['Rolling Average']['RH']
            
            for num in pids_on:
                
                    Rolling_Averages['Rolling Average'][num] = pd.rolling_mean(pid_data[num],200,20)
                    Corrected_Rolling_Averages['Rolling Average'][num] = pd.rolling_mean(pid_data_corrected[num],200,20)               
                
                    Spliced_Data['Times'][num] = list_multisplicer(dataL.TheTime,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                    Corrected_Spliced_Data['Times'][num] = list_multisplicer(dataL.TheTime,SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
                    
                    Spliced_Data['RH'][num] = list_multisplicer(RH,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                    Spliced_Data['RH listout'][num] = list_multisplicer_listsout(RH,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])                    
                    Corrected_Spliced_Data['RH'][num] = list_multisplicer(RH,SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
                    Corrected_Spliced_Data['RH listout'][num] = list_multisplicer_listsout(RH,SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
                    
                    Spliced_Data['Isop listout'][num] = list_multisplicer_listsout(isop_mr,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                    Corrected_Spliced_Data['Isop listout'][num] = list_multisplicer_listsout(isop_mr,SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
                    
                    Spliced_Data['Pids'][num] = list_multisplicer(pid_data[num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                    Spliced_Data['Pids listsout'][num] = list_multisplicer_listsout(pid_data[num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])                   
                    Corrected_Spliced_Data['Pids'][num] = list_multisplicer(pid_data[num],SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
                    Corrected_Spliced_Data['Pids listsout'][num] = list_multisplicer_listsout(pid_data[num],SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
                
                    Spliced_Data['Pid_Avgs'][num] = list_multisplicer(Rolling_Averages['Rolling Average'][num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
                    Corrected_Spliced_Data['Pid_Avgs'][num] = list_multisplicer(Rolling_Averages['Rolling Average'][num],SF_indexes_corrected['Pid%s'%num]['S'],SF_indexes_corrected['Pid%s'%num]['F'])
            ###########################################################################################################################################################################################
            
            
            
            
            # Calculating means and errors to fill cal_df with
            
            
            #Calculating the mean of the data in the chunks for the cal points
            Voltages = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in Spliced_Data['Pids listsout'][num]] for num in pids_on})
            Voltages_corrected = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in Corrected_Spliced_Data['Pids listsout'][num]] for num in pids_on})
            
            # Calculating the standard errors for the cal points
            Errors = pd.DataFrame({'Pid%s Stderr'%(num) : [np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['Pids listsout'][num]] for num in pids_on})
            Errors_corrected = pd.DataFrame({'Pid%s Stderr'%(num) : [np.nanstd(i)/np.sqrt(data_point_length) for i in Corrected_Spliced_Data['Pids listsout'][num]] for num in pids_on})
            
            #Finding time at Start and end of cal points
            Start_Times = pd.DataFrame({'Start Time': [dataL.TheTime[i] for i in S]})
            End_Times = pd.DataFrame({'End Time': [dataL.TheTime[i] for i in F]})
            
            #Finding the mean of the isoprene in the chunks and the standard error (like Voltages adn Errors)
            Isoprene_error = pd.DataFrame({'Isop Error': [np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['Isop listout'][num]]})
            Isoprene = pd.DataFrame({'Isop': [np.nanmean(i) for i in Spliced_Data['Isop listout'][num]]})
        
            #Average  RH for the chunks
            cal_RH = pd.DataFrame({'RH':[np.nanmean(i) for i in Spliced_Data['RH listout'][num]]})
            Error_RH = pd.DataFrame({'RH Stderr':[np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['RH listout'][num]]})   
            #########################################################################################################################
            
            
            
            
            # Merges above dataframes into one (for corrected and uncorrected data)
            cal_df = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Error_RH,Voltages, Errors], axis=1, join='inner')
            cal_dfc = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Error_RH,Voltages_corrected, Errors_corrected], axis=1, join='inner')
            ##############################################################################################################################################
            
            
            
            
            
            
            
            
            # Averaging the Zero isoprene values in cal_df
            
            
            #finds the index of the data frame when Isoprene = 0
            isop_zero_indexes = [i for i in xrange(0,len(cal_df.Isop)) if np.around(cal_df.Isop[i],1) == 0.0]            
            
            # Sets the pid voltages when the isoprene = zero, to the average of the pid voltages when the isoprene = 0, for each pid.
            cal_df.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]] = [np.mean(cal_df.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]])[i] for i in xrange(0,len(pids_on))]
            cal_dfc.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]] = [np.mean(cal_dfc.loc[isop_zero_indexes,['Pid%s Voltage'%(num) for num in pids_on]])[i] for i in xrange(0,len(pids_on))]
            
            #Drops the duplicates that arise when setting the pid voltages when isoprene = 0, in cal_df/cal_dfc, to the average of the pid voltages when isoprene = 0
            cal_df = cal_df.drop_duplicates(subset = ['Pid%s Voltage'%num for num in pids_on])
            cal_dfc = cal_dfc.drop_duplicates(subset = ['Pid%s Voltage'%num for num in pids_on])
            
            #resets the indexes so the code works
            cal_df.index = xrange(0,len(cal_df))
            cal_dfc.index = xrange(0,len(cal_dfc))       
            ######################################
            
            
            
            isop_fit = [0.,np.max(cal_df.Isop)]  # This list contains the x-coords to plot the line of best fit with  
            
            xdata = cal_df.Isop
            
        
        
        
            # Stores the slope values and intecept values and errors
            Values = pd.DataFrame(index = pids_on, columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])
            Corrected_Values = pd.DataFrame(index = pids_on, columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])
            #####################################################################################################################
        
        
        
        
        
        
        
        
            # Finding the slope and intercept and errors for the cals.
        
            for num in pids_on:
                
                if humid_correct == 'Y':
                    
                        ydatac = cal_dfc.loc[:,'Pid%s Voltage'%str(num)] # corrected y data
                        
                        initial_estimatesc = np.polyfit(cal_df['Isop'],ydatac,1) # an initial estimate for the parameters (the slope and intercept)

                        #Fitting a line of best fit
                        datac = odr.RealData(x = cal_dfc['Isop'],y =cal_dfc['Pid%s Voltage'%(str(num))],sx = cal_dfc['Isop Error']*np.sqrt(data_point_length),sy = cal_dfc['Pid%s Stderr'%str(num)]*np.sqrt(data_point_length))
                        fitc = odr.ODR(datac,linear,initial_estimatesc)
                        paramsc = fitc.run()
                        
                        
                        # Using the slope and intercept to find the min and max y-coords
                        pidc_fits[num] = (paramsc.beta[1],(np.max(cal_dfc.Isop)*paramsc.beta[0])+paramsc.beta[1])
                        
                        # Popping the ouputs into a dataframe
                        Corrected_Values['Slope'][num] = paramsc.beta[0]
                        Corrected_Values['Intercept'][num] = paramsc.beta[1]
                        Corrected_Values['Slope Error'][num] = paramsc.sd_beta[0]
                        Corrected_Values['Intercept Error'][num] = paramsc.sd_beta[1]
                        
                        #Saving the slope and intercept values with erors in a big data frame with everything in.
                        Slope_Intercepts.loc[n,'Filename'] = Filename
                        Slope_Intercepts.loc[n,'Pid%s Intercept'%num] = Corrected_Values.loc[num,'Intercepts']
                        Slope_Intercepts.loc[n,'Pid%s Intercept Error'%num] = Corrected_Values.loc[num,'Intercept Errors']
                        Slope_Intercepts.loc[n,'Pid%s Slope'%num] = Corrected_Values.loc[num,'Slopes']
                        Slope_Intercepts.loc[n,'Pid%s Slope Error'%num] = Corrected_Values.loc[num,'Slope Errors']
                        
                
                        
                #Same as the corrected bit above        
                ydata = cal_df.loc[:,'Pid%s Voltage'%str(num)]
                
                initial_estimates = np.polyfit(cal_df['Isop'],ydata,1)
                
                data = odr.RealData(x = cal_df['Isop'],y =cal_df['Pid%s Voltage'%(str(num))],sx = cal_df['Isop Error']*np.sqrt(data_point_length),sy = cal_df['Pid%s Stderr'%str(num)]*np.sqrt(data_point_length))
                fit = odr.ODR(data,linear,initial_estimates)
                params = fit.run()
        
                pid_fits[num] = (params.beta[1],(np.max(cal_df.Isop)*params.beta[0])+params.beta[1])
        
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
                
                
                #Storing all the corrected dataframe information into a dictionary
                cal_dfcs[n] = cal_dfc
            #########################
            
                
                    
                            
            # Showing the progress of the code    
            n = n+1
            if n == len(to_be_read):
                print '\n\nAll Done! :D'
            print '%s down, %s to go'%(n,str(len(to_be_read)-n)), '( ',np.around(float(n*100)/len(to_be_read),1),'% )'   
        
        else:
            bad_files.append(Filename)#If there are any files that don't appear to be cal files this logs them
            
            
            
    except 'bob': #If there is an error pop it here and it will stop the code crashing, however it won't record that cal data though.
            print '\n\n--------------------\n\n'
            print filesln[filei], 'This isn\'t working'
            print '\n\n--------------------\n\n'

if len(bad_files)>0:
    print 'Here are the files that don\'t look like cals:\n', bad_files # Prints the name of any files that don't appear to be cal files         
#########################################################################


# Saving the Data



# Seeing whether there is already a file with some of this information stored in it.
try:
    
    data_already_in_cal_points = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Cal Data.txt', sep=',')
    there_is_already_data_in_the_file = 'Y'
        
except IOError:
    there_is_already_data_in_the_file = 'N'    
    
    
    

try:
    
    data_already_there_slopes = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Slope and Intercepts.txt', sep = ',')    
    there_are_already_slopes_in_the_file = 'Y'
    
except IOError:
    there_are_already_slopes_in_the_file = 'N'
############################################# 
    
    
    
# Checking whether we have just performed some cals and if we have then this makes a big dataframe of all the cal data and then adds it to the cal data we already have if we have any    
if there_are_new_values_to_be_added == 'Y':   
    New_Values = pd.concat([cal_dfs[n] for n in xrange(0,len(to_be_read))], axis=0)
    
    if there_is_already_data_in_the_file == 'Y':

        Final_Values = data_already_in_cal_points.append(New_Values)

        Final_Values.to_csv(path_or_buf='C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Cal Data.txt', sep=',')
    
    else:
        New_Values.to_csv(path_or_buf='C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Cal Data.txt', sep=',')
    
    
    
    
    
    
    if there_are_already_slopes_in_the_file == 'Y':
        
        Final_Slopes = data_already_there_slopes.append(Slope_Intercepts)
        
        Final_Slopes.to_csv(path_or_buf = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Slope and Intercepts.txt', sep = ',')
    
    else:
        Slope_Intercepts.to_csv(path_or_buf = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Slope and Intercepts.txt', sep = ',')
################################################################################################################################################

    
    


# saving the Corrected Data (comments as above)




try:
    
    data_already_in_cal_points = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Cal Data Corrected.txt', sep=',')
    there_is_already_data_in_the_file = 'Y'
        
except IOError:
    there_is_already_data_in_the_file = 'N'    
    
    
    

try:
    
    data_already_there_slopes = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Corrected Slope and Intercepts.txt', sep = ',')    
    there_are_already_slopes_in_the_file = 'Y'
    
except IOError:
    there_are_already_slopes_in_the_file = 'N'
    
    
    
    
if there_are_new_values_to_be_added == 'Y':   
    New_Values = pd.concat([cal_dfcs[n] for n in xrange(0,len(to_be_read))], axis=0)
    
    if there_is_already_data_in_the_file == 'Y':

        Final_Values = data_already_in_cal_points.append(New_Values)



            
            
        Final_Values.to_csv(path_or_buf='C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Cal Data Corrected.txt', sep=',')
    else:
        New_Values.to_csv(path_or_buf='C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Cal Data Corrected.txt', sep=',')
    
    
    
    
    
    
    if there_are_already_slopes_in_the_file == 'Y':
        
        Final_Slopes = data_already_there_slopes.append(Slope_Interceptsc)
        
        Final_Slopes.to_csv(path_or_buf = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Corrected Slope and Intercepts.txt', sep = ',')
    else:
        Slope_Interceptsc.to_csv(path_or_buf = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\Isop Corrected Slope and Intercepts.txt', sep = ',')
