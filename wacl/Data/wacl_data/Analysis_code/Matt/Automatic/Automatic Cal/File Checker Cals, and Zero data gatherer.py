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
day1 =0
day2 = 30
filenumbers = 20
min_filesize = 750000L
max_filesize = 185032288L



# Control The length of the cal points, these numbers probably don't need changing

data_point_length = 375 # how many data points used for the cals
bad_cal_length = 375
shift_scale = 3.5 # A higher number here decreases the amount of movement in the cals (if it were 1 it would allow the cal point to move the length of a cal, if it were 2 it would allow the cal point to move half the length of 


humid_correct = 'Y'

cal_stuff = 'Y'
arduino = ''


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



pid_2_on = ''

pid_3_on = 'Y'

pid_4_on = 'Y'

pid_5_on = 'Y'


pd.set_option('precision',9)
##################################################### Defining Functions For Use Later #################################################
### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation
### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation
class functions(object):
    from operator import itemgetter
    left_shift_stds = {}
    right_shift_stds = {}
    nanL = []
    nanR = []
    
    def cal_point_ammender(self,data_set,bad_cal_length,shifter,S,F):
        S = list(S)
        F = list(F)
        for i in xrange(0,len(S)):
            orig_std = np.nanstd(data_set[S[i]:F[i]])
            
            if orig_std > 0.7:
                S[i] = F[i] - bad_cal_length
    
            
            left_shift_stds = {}
            for k in xrange(1,20):
                x_shiftL = k*shifter
                left_shift_stds[k] = np.nanstd(data_set[S[i]-x_shiftL:F[i]-x_shiftL])
            nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
            for t in nanL:
                del(left_shift_stds[t])
                
            minPairL = min(left_shift_stds.iteritems(), key=self.itemgetter(1))
    
    
            right_shift_stds = {}
            for k in xrange(1,20):
                x_shiftR = k*shifter
                right_shift_stds[k] = np.nanstd(data_set[S[i]+x_shiftR:F[i]+x_shiftR])
                
            nanR = [q for q in right_shift_stds if np.isnan(right_shift_stds[q])]
            for t in nanR:
                del(right_shift_stds[t])
                
            minPairR = min(right_shift_stds.iteritems(), key=self.itemgetter(1))
    
            
            
            if minPairL[1] < orig_std and minPairL[1] < minPairR[1]:
                S[i] = S[i]-minPairL[0]*shifter
                F[i] = F[i]-minPairL[0]*shifter
            elif minPairR[1] < orig_std and minPairR[1] < minPairL[1]:
                S[i] = S[i]+minPairR[0]*shifter
                F[i] = F[i]+minPairR[0]*shifter  

        if S[0] < 0:
            SF = negative_remover(S,F)
            S = SF[0]
            F = SF[1]
            
        return S,F  
        
func = functions() 
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
    if pid_3_on == 'Y':
        slope_string = slope_string + '\tSlope 3\tSlope Error 3'
    if pid_4_on == 'Y':
        slope_string = slope_string + '\tSlope 4\tSlope Error 4'
    if pid_5_on == 'Y':
        slope_string = slope_string + '\tSlope 5\tSlope Error 5'
        
        
    Pid_String = ''
    if pid_3_on == 'Y':
        Pid_String = Pid_String + '\tPid 3\tPid Error 3'
    if pid_4_on == 'Y':
        Pid_String = Pid_String + '\tPid 4\tPid Error 4'
    if pid_5_on == 'Y':
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
        
        pid_2_on = ''

        pid_3_on = 'Y'
        
        pid_4_on = 'Y'
        
        pid_5_on = 'Y'    
            
        dataL = pd.read_csv(filesln[filei])
        xerr = []
        yerr = {1:[],2:[],3:[],4:[],5:[]}

        dataL.mfcloR = nan_helper(dataL.mfcloR,10,3)
        x = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\fit file.txt', sep = '\t')
        names = [i for i in x['Unnamed: 0']]
        x.index = names
        x = x.drop('Unnamed: 0',1)

        pid3_correction = [((x['Slope']['Pid3']*i)+x['Intercept']['Pid3']) for i in dataL.mfcloR]
        pid3_correctm = pid3_correctm = np.nanmean(pid3_correction)
        
        pid4_correction = [((x['Slope']['Pid4']*i)+x['Intercept']['Pid4']) for i in dataL.mfcloR]
        pid4_correctm = pid4_correctm = np.nanmean(pid4_correction)
        
        pid5_correction = [((x['Slope']['Pid5']*i)+x['Intercept']['Pid5']) for i in dataL.mfcloR]
        pid5_correctm = pid5_correctm = np.nanmean(pid5_correction)

        ##   Sorting out the Times   ##
        TimeL = dataL.TheTime-dataL.TheTime[0]
        TimeL*=60.*60.*24.
        
        dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
        T1 = pd.datetime(1899,12,30,0)
        T2 = pd.datetime(1970,01,01,0)
        offset=T1-T2
        dataL.TheTime+=offset
        print '\tLoading...'
        #### Relative Humidity ###

        if int(date) >= 822:
            dataL.RH = nan_helper(dataL.RH,10,3)
            RH = dataL.RH
            RH /=4.96
            RH -= 0.16
            RH /= 0.0062

            RH /= (1.0546-(0.00216*dataL.Temp))

        else:
            humid_correct = ''
            
        
        ## Adjusting for the isop conc        
        isop_cyl = 13.277	#ppbv
        mfchi_range = 100.	#sccm
        mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
        
        mfclo_range = 20.	#sccm
        mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
        
        dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
        isop_mr = dil_fac*isop_cyl
        
        dataL['mfchi'] = [(5+((0*i)+1)) for i in xrange(0,len(dataL))] 
        dataL = dataL.fillna({'mfchi':5})
        

        if int(date) < 904:
            pid_5_on = ''
            try:
                pid2d = nan_helper(dataL.pid1,10,3)
                pid2d.name = 'pid2'
                pid2dc = ''
            except AttributeError:
                pid_2_on = ''  
            
            try:   
                pid3d = nan_helper(dataL.pid2,10,3)
                pid3d.name = 'pid3'
                if humid_correct == 'Y':
                    pid3dc = pid3d - RH*pid4_correction
                else:
                    pid3dc = ''
                    
            except AttributeError:
                pid_3_on = ''  
                
            try:    
                pid4d = nan_helper(dataL.pid3,10,3)
                pid4d.name = 'pid4'
                if humid_correct == 'Y':
                    pid4dc = pid4d - RH*pid4_correction
                else:
                    pid4dc = ''
                    
            except AttributeError:
                pid_4_on = ''    
                    
        if int(date) >= 904:
            pid_2_on = ''
            try:
                pid5d = nan_helper(dataL.pid5,10,3)
        
                if humid_correct == 'Y':
                    pid5dc = pid5d - RH*pid5_correction
                else:
                    pid5dc = ''
                    
            except AttributeError:
                pid_5_on = ''    
                
            try:   
                pid3d = nan_helper(dataL.pid3,10,3)
                
                if humid_correct == 'Y':
                    pid3dc = pid3d - RH*pid3_correction
                else:
                    pid3dc = ''            
            except AttributeError:
                pid_3_on = ''     
                    
            try:   
                pid4d = nan_helper(dataL.pid4,10,3)
        
                if humid_correct == 'Y':
                    pid4dc = pid4d - RH*pid4_correction
                else:
                    pid4dc = ''            
            except AttributeError:
                        pid_4_on = '' 
        
                
        
        
        
        
        
        #############################
        ## Signal vs Isop for calibration experiments

    
        
        mfc_set = np.zeros((len(dataL.mfclo)),dtype=bool)
        for i in xrange(1,len(dataL.mfchi)):
            if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i-1],dataL.mfclo[i]!=dataL.mfclo[i-1]))):
                    mfc_set[i] = "True"
                    
        cal_N = np.sum(mfc_set) # number of changes in value for mfclo
            
        cal_pts = [xrange(0,cal_N)]
        
    
        end_cut_off = 60
        
    
        mfc_setF = dataL.index[mfc_set]
        
        mfc_setF -= end_cut_off #taking some data points away from the end to give a bit of a tolerance
        
        mfc_setS = [i-data_point_length for i in mfc_setF]    
    
        if mfc_setS[0] < 0:         
            S = negative_remover(mfc_setS,mfc_setF)[0]
            F = negative_remover(mfc_setS,mfc_setF)[1]          
        else:
            S = mfc_setS
            F = mfc_setF 
            
        shifter = int(len(dataL)/(len(S)*20*shift_scale))
        
        SF3 = func.cal_point_ammender(pid3d,bad_cal_length,shifter,S,F)
        S3 = SF3[0]
        F3 = SF3[1]     

        SF4 = func.cal_point_ammender(pid4d,bad_cal_length,shifter,S,F)
        S4 = SF4[0]
        F4 = SF4[1] 
           
        if pid_5_on == 'Y':
            SF5 = func.cal_point_ammender(pid5d,bad_cal_length,shifter,S,F)
            S5 = SF5[0]
            F5 = SF5[1]                
    
        if humid_correct == 'Y':
            SF3c = func.cal_point_ammender(pid3dc,bad_cal_length,shifter,S,F)
            S3c = SF3c[0]
            F3c = SF3c[1]
        
            SF4c = func.cal_point_ammender(pid4dc,bad_cal_length,shifter,S,F)
            S4c = SF4c[0]
            F4c = SF4c[1]    
            if pid_5_on == 'Y':
                SF5c = func.cal_point_ammender(pid5dc,bad_cal_length,shifter,S,F)
                S5c = SF5c[0]
                F5c = SF5c[1]   
        
        
        troubleshoot = ''
        if troubleshoot == 'Y':
            for x in xrange(0,len(S)):
                print S[x], F[x]
                print F[x]-S[x]
                print '\n------\n'
    
                

        cal_cols_new = ['Start Times','End Times','Isop','Isop Stddev']
        cal_cols_c = []
        
        if pid_2_on == 'Y':
            cal_cols_new.append('Pid2 Voltage')
            cal_cols_new.append('Pid2 Stddev')
    
            
        if pid_3_on == 'Y':
            cal_cols_new.append('Pid3 Voltage')
            cal_cols_new.append('Pid3 Stddev')
            if humid_correct == 'Y':
                cal_cols_c.append('Pid3 Voltage')
                cal_cols_c.append('Pid3 Stddev')
        
                    
        if pid_4_on == 'Y':
            cal_cols_new.append('Pid4 Voltage')
            cal_cols_new.append('Pid4 Stddev')
            if humid_correct == 'Y':
                cal_cols_c.append('Pid4 Voltage')
                cal_cols_c.append('Pid4 Stddev')
        
        if pid_5_on == 'Y':
            cal_cols_new.append('Pid5 Voltage')
            cal_cols_new.append('Pid5 Stddev')
            if humid_correct == 'Y':
                cal_cols_c.append('Pid5 Voltage')
                cal_cols_c.append('Pid5 Stddev')
    
        cal_df = pd.DataFrame(index=xrange(0,len(S)), columns=cal_cols_new)
    
        if humid_correct == 'Y':
            cal_dfc = pd.DataFrame(index=xrange(0,len(cal_df)), columns=cal_cols_c)
        
    
                
        if pid_3_on == 'Y':
            if humid_correct == 'Y':      
                pid3_chunksc = list_multisplicer_listsout(pid3dc,S3c,F3c)
                
                pid3_avgsc = [np.nanmean(i) for i in pid3_chunksc]
                pid3_stdsc = [np.nanstd(i) for i in pid3_chunksc]
                
    
            
            pid3_chunks = list_multisplicer_listsout(pid3d,S3,F3)
            
            pid3_avgs = [np.nanmean(i) for i in pid3_chunks]
            pid3_stds = [np.nanstd(i) for i in pid3_chunks]
            
    
            
        if pid_4_on =='Y':
            if humid_correct == 'Y':  
                pid4_chunksc = list_multisplicer_listsout(pid4dc,S4c,F4c)
                
                pid4_avgsc = [np.nanmean(i) for i in pid4_chunksc]
                pid4_stdsc = [np.nanstd(i) for i in pid4_chunksc] 
                
    
            
            pid4_chunks = list_multisplicer_listsout(pid4d,S4,F4)
            
            pid4_avgs = [np.nanmean(i) for i in pid4_chunks]
            pid4_stds = [np.nanstd(i) for i in pid4_chunks] 
        
    
            
        if pid_5_on =='Y':
            if humid_correct == 'Y':
                pid5_chunksc = list_multisplicer_listsout(pid5dc,S5c,F5c)
                
                pid5_avgsc = [np.nanmean(i) for i in pid5_chunksc]
                pid5_stdsc = [np.nanstd(i) for i in pid5_chunksc] 
    
            
            pid5_chunks = list_multisplicer_listsout(pid5d,S5,F5)
            
            pid5_avgs = [np.nanmean(i) for i in pid5_chunks]
            pid5_stds = [np.nanstd(i) for i in pid5_chunks] 
        
        if pid_3_on == 'Y':
            if humid_correct == 'Y':
                cal_dfc.loc[:,'Pid3 Voltage'] = pid3_avgsc
                cal_dfc.loc[:,'Pid3 Stddev']= pid3_stdsc 
                
            cal_df.loc[:,'Pid3 Voltage'] = pid3_avgs
            cal_df.loc[:,'Pid3 Stddev']= pid3_stds    
            
            
        if pid_4_on == 'Y':  
            if humid_correct == 'Y':  
                cal_dfc.loc[:,'Pid4 Voltage'] = pid4_avgsc
                cal_dfc.loc[:,'Pid4 Stddev']= pid4_stdsc 
                
            cal_df.loc[:,'Pid4 Voltage'] = pid4_avgs
            cal_df.loc[:,'Pid4 Stddev']= pid4_stds  
            
            
        if pid_5_on == 'Y':    
            if humid_correct == 'Y':
                cal_dfc.loc[:,'Pid5 Voltage'] = pid5_avgsc
                cal_dfc.loc[:,'Pid5 Stddev']= pid5_stdsc 
                
            cal_df.loc[:,'Pid5 Voltage'] = pid5_avgs
            cal_df.loc[:,'Pid5 Stddev']= pid5_stds 
        
    
        isop_chunks = list_multisplicer_listsout(isop_mr,S,F)
        
        isop_avgs = [np.nanmean(i) for i in isop_chunks]
        isop_stds = [np.nanstd(i) for i in isop_chunks]
        
        
        start_times = [TimeL[i] for i in S]
        end_times = [TimeL[i] for i in F]
        
        if humid_correct == 'Y':
            RH_chunks = list_multisplicer_listsout(RH,S,F)
            RH_avgs = [np.nanmean(i) for i in RH_chunks]
            cal_df.loc[:,'RH'] = RH_avgs
    
        cal_df.loc[:,'Isop'] = isop_avgs
        cal_df.loc[:,'Isop Stddev'] = isop_stds
        cal_df.loc[:,'Start Times'] = start_times
        cal_df.loc[:,'End Times'] = end_times
        
        cal_df_orig = cal_df # Saving an unaltered cal_df
    
        
        cal_df = cal_df.dropna()
        cal_df.index = xrange(0,len(cal_df))
    
        RH_mean = str(np.nanmean(RH))
        
        ########################## Writing the cal data into a text file #########################
        
        for pkl in xrange(0,len(cal_df)):
            Isop_string = ''
            Isop_stringc = ''
            if pid_3_on == 'Y':
                Isop_string = Isop_string +'\t'+ str(cal_df.loc[pkl,'Pid3 Voltage'])+'\t'+str(cal_df.loc[pkl,'Pid3 Stddev']/np.sqrt(data_point_length))
            if pid_4_on == 'Y':
                Isop_string = Isop_string +'\t'+ str(cal_df.loc[pkl,'Pid4 Voltage'])+'\t'+str(cal_df.loc[pkl,'Pid4 Stddev']/np.sqrt(data_point_length))
                
            if pid_5_on == 'Y':
                Isop_string = Isop_string+'\t'+str(cal_df.loc[pkl,'Pid5 Voltage'])+'\t'+str(cal_df.loc[pkl,'Pid5 Stddev']/np.sqrt(data_point_length))
            else:
                Isop_string = Isop_string+'\t\t'
            calfile.write(filename+'\t'+str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+'\t'+str(cal_df.loc[pkl,'Isop'])+Isop_string+'\n')
           
            
            if humid_correct == 'Y':     
                if pid_3_on == 'Y':
                    Isop_stringc = Isop_stringc +'\t'+ str(cal_dfc.loc[pkl,'Pid3 Voltage'])+'\t'+str(cal_dfc.loc[pkl,'Pid3 Stddev']/np.sqrt(data_point_length))
                if pid_4_on == 'Y':
                    Isop_stringc = Isop_stringc +'\t'+ str(cal_dfc.loc[pkl,'Pid4 Voltage'])+'\t'+str(cal_dfc.loc[pkl,'Pid4 Stddev']/np.sqrt(data_point_length))
                    
                if pid_5_on == 'Y':
                    Isop_stringc = Isop_stringc+'\t'+str(cal_dfc.loc[pkl,'Pid5 Voltage'])+'\t'+str(cal_dfc.loc[pkl,'Pid5 Stddev']/np.sqrt(data_point_length))    
                else:
                    Isop_stringc = Isop_stringc+'\t\t'       
                calfilec.write(filename+'\t'+str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+'\t'+str(cal_df.loc[pkl,'Isop'])+Isop_stringc+'\n')
            
        ########################## Zero Averaging #########################

                
        isop_zero_indexes = []        
        
        
        for i in xrange(0,len(cal_df.Isop)):
            if cal_df.Isop[i] < 0.2:
                isop_zero_indexes.append(i)
                
        
        if pid_3_on:
            cal_df.loc[isop_zero_indexes,'Pid3 Voltage'] = np.nanmean(cal_df['Pid3 Voltage'][isop_zero_indexes])
            if humid_correct == 'Y':
                cal_dfc.loc[isop_zero_indexes,'Pid3 Voltage'] = np.nanmean(cal_dfc['Pid3 Voltage'][isop_zero_indexes])            
                
        if pid_4_on:
            cal_df.loc[isop_zero_indexes,'Pid4 Voltage'] = np.nanmean(cal_df['Pid4 Voltage'][isop_zero_indexes])
            
            if humid_correct == 'Y':
                cal_dfc.loc[isop_zero_indexes,'Pid4 Voltage'] = np.nanmean(cal_dfc['Pid4 Voltage'][isop_zero_indexes])
    
        if pid_5_on:
            cal_df.loc[isop_zero_indexes,'Pid5 Voltage'] = np.nanmean(cal_df['Pid5 Voltage'][isop_zero_indexes])
            if humid_correct == 'Y':
                cal_dfc.loc[isop_zero_indexes,'Pid5 Voltage'] = np.nanmean(cal_dfc['Pid5 Voltage'][isop_zero_indexes])
        
        
    
    
        ########################## ########################## ########################## 
        print '\t...\n\n'
        ########## Tidying up and fitting #########
        
        if pid_3_on:
            cal_df = cal_df.drop_duplicates(subset = 'Pid3 Voltage')
            if humid_correct == 'Y':
                cal_dfc = cal_dfc.drop_duplicates(subset = 'Pid3 Voltage')
        elif pid_4_on:
            cal_df = cal_df.drop_duplicates(subset = 'Pid4 Voltage')
            if humid_correct == 'Y':
                cal_dfc = cal_dfc.drop_duplicates(subset = 'Pid4 Voltage')
        elif pid_5_on:
            cal_df = cal_df.drop_duplicates(subset = 'Pid5 Voltage')
            if humid_correct == 'Y':
                cal_dfc = cal_dfc.drop_duplicates(subset = 'Pid5 Voltage')
    
    
        cal_df.index = xrange(0,len(cal_df))
        if humid_correct == 'Y':
            cal_dfc.index = xrange(0,len(cal_dfc))
        
    
 
                
        
        isop_fit = [0.,np.max(cal_df.Isop)]    
        
        xdata = cal_df.Isop
        
    
        Values = {'Slope':{3:[],4:[],5:[]},'Intercept':{3:[],4:[],5:[]},'Slope Error':{3:[],4:[],5:[]},'Intercept Error':{3:[],4:[],5:[]}}
        Corrected_Values = {'Slope':{3:[],4:[],5:[]},'Intercept':{3:[],4:[],5:[]},'Slope Error':{3:[],4:[],5:[]},'Intercept Error':{3:[],4:[],5:[]}}
                        
        if pid_3_on:        
            
            for i in xrange(len(cal_df)):
                yerr[3].append(cal_df['Pid3 Stddev'][i]/np.sqrt(len(pid3_chunks[i]))) 
                
                
            if humid_correct == 'Y':
                
                        ydata3c = cal_dfc['Pid3 Voltage']    
                        slope_intercept3c,pcov3c = opt.curve_fit(linear_fit, xdata, ydata3c, sigma = yerr[3])
                        perr3c = np.sqrt(np.diag(pcov3c))    
                        Intercept_error3c = perr3c[0]/np.sqrt(cal_N)
                        Slope_Error3c = perr3c[1]/np.sqrt(cal_N)
                            
    
    
            ydata3 = cal_df['Pid3 Voltage']
            slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr[3])
    
            perr3 = np.sqrt(np.diag(pcov3))    
            Intercept_error3 = perr3[0]/np.sqrt(cal_N)
            Slope_Error3 = perr3[1]/np.sqrt(cal_N)        
                
                            
        if pid_4_on: 
                
                                    
                for i in xrange(len(cal_df)):
                    yerr[4].append(cal_df['Pid4 Stddev'][i]/np.sqrt(len(pid4_chunks[i])))
                
                if humid_correct == 'Y':
        
                            ydata4c = cal_dfc['Pid4 Voltage']    
                            slope_intercept4c,pcov4c = opt.curve_fit(linear_fit, xdata, ydata4c, sigma = yerr[4])
                            perr4c = np.sqrt(np.diag(pcov4c))    
                            Intercept_error4c = perr4c[0]/np.sqrt(cal_N)
                            Slope_Error4c = perr4c[1]/np.sqrt(cal_N)
        
                                        
        
                ydata4 = cal_df['Pid4 Voltage']
                slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr[4])
                
                perr4 = np.sqrt(np.diag(pcov4))    
                Intercept_error4 = perr4[0]/np.sqrt(cal_N)
                Slope_Error4 = perr4[1]/np.sqrt(cal_N)
                
                
        if pid_5_on: 
            
                for i in xrange(len(cal_df)):
                    yerr[5].append(cal_df['Pid5 Stddev'][i]/np.sqrt(len(pid5_chunks[i])))
                    
                if humid_correct == 'Y':
        
                        ydata5c = cal_dfc['Pid5 Voltage']    
                        slope_intercept5c,pcov5c = opt.curve_fit(linear_fit, xdata, ydata5c, sigma = yerr[5])
                        perr5c = np.sqrt(np.diag(pcov5c))    
                        Intercept_error5c = perr5c[0]/np.sqrt(cal_N)
                        Slope_Error5c = perr5c[1]/np.sqrt(cal_N)
        
                ydata5 = cal_df['Pid5 Voltage']
                slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr[5])
                
                perr5 = np.sqrt(np.diag(pcov5))    
                Intercept_error5 = perr5[0]/np.sqrt(cal_N)
                Slope_Error5 = perr5[1]/np.sqrt(cal_N)
                

                
        
        
                
        
        
        
        slope_values_string = ''
        
        if pid_3_on == 'Y': 
            slope_values_string = slope_values_string + '\t' + str(slope_intercept3[1]) + '\t' + str(Slope_Error3)
        else:
                slope_values_string = slope_values_string + '\t\t'   
                  
        if pid_4_on == 'Y': 
            slope_values_string = slope_values_string + '\t' +str(slope_intercept4[1]) + '\t' + str(Slope_Error4)
        else:
                slope_values_string = slope_values_string + '\t\t'  
                   
        if pid_5_on == 'Y':
            slope_values_string = slope_values_string + '\t' +str(slope_intercept5[1]) + '\t' + str(Slope_Error5)

            
        slopesfile.write(str(dataL.TheTime[len(dataL.TheTime)/2])+'\t'+RH_mean+slope_values_string+'\n')   
        
        if humid_correct == 'Y':
        
            slope_values_stringc = ''
            if pid_3_on == 'Y': 
                slope_values_stringc = slope_values_stringc + '\t' + str(slope_intercept3c[1]) + '\t' + str(Slope_Error3c)
            else:
                slope_values_stringc = slope_values_stringc + '\t\t'   
                
            if pid_4_on == 'Y': 
                slope_values_stringc = slope_values_stringc + '\t' + str(slope_intercept4c[1]) + '\t' + str(Slope_Error4c)
            else:
                slope_values_stringc = slope_values_stringc + '\t\t'    
                
            if pid_5_on == 'Y':
                slope_values_stringc = slope_values_stringc + '\t' + str(slope_intercept5c[1]) + '\t' + str(Slope_Error5c)

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
