import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from scipy import stats
import scipy.optimize as opt
import time
#from Tkinter import *
import datetime
#import pylab as pyl


##################################################### Defining Functions For Use Later #################################################

# To interpolate between NaN values
def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]
    
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
        time
        
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





pd.set_option('precision',9)

cal_stuff = 'Y'

pid_2_on = ''

pid_3_on = ''

pid_4_on = 'Y'

if cal_stuff == 'Y':

    questions = ''
    plots = 'Y'
    cal = 'Y'
    avg_0 = 'Y'
else:
    questions = ''
    plots = ''
    cal = ''
    avg_0 = ''
    arduino_cal_stuff = ''
    
hist = ''


slopesqwe_pid2 = []
slopes_errorqwe_pid2 = []

slopesqwe_pid3 = []
slopes_errorqwe_pid3 = []

slopesqwe_pid4 = []
slopes_errorqwe_pid4 = []

d=15
a = 1
n = 150
while n <= 850:
    
    xerr = []
    yerr2 = []
    yerr3 = []
    yerr4 = []
    
    npid2 = []
    npid3=[]
    npid4= []
    nISop = []
    
    
    
    
    #############################
    ## User Interface
    if questions == 'Y':
        #####Asking if the user would like to load from the memory stick
        pogk = 2
        '''while pogk == 2:
            memorystickq = raw_input('Are you loading from a your memory stick? ')
            if memorystickq == 'y' or memorystickq == 'yes' or memorystickq == 'YES' or memorystickq == 'Yes' or memorystickq == 'Y':
                print '\n\n(Okie doke, loading from E:\Bursary thing\PID Data\Organised and or Edited\\)'
                pathL = "E:\Bursary thing\PID Data\Organised and or Edited\\"
                pogk = 1
            elif memorystickq == 'no' or memorystickq == 'n' or memorystickq == 'No' or memorystickq =='NO' or memorystickq == 'N':
                print '\n\n(Okie doke, loading from C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited then)'
                pathL = 'C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited\\'
                pogk = 1
            elif memorystickq == 'somewhere else' or memorystickq == 'elsewhere':
                pathL = raw_input('please enter where you would like to load from: ')
            else:
                print 'Please enter y or n...'
        
        
        #####Asking if the user would like to load from today's data
        while pogk == 1:
            dateq = raw_input('\nDo you want to load from today\'s data? ')
            if dateq == 'y' or dateq == 'yes' or dateq == 'YES' or dateq == 'Yes' or dateq == 'Y':
                print """\n(Okie doke, loading today's data)"""
                filename1 = str((time.strftime('%m-%d')))+'\d20' + str((time.strftime('%y%m%d'))) + '_0'+ raw_input('Which file would you like to load? ')
                pogk = 2
            elif dateq == 'n' or dateq == 'no' or dateq == 'No' or dateq == 'NO' or dateq == 'N':
                date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
                filename1 =  date[0:2] + '-' + date[2:4] + '\d20' + str((time.strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
                pogk = 0
                print filename1
            else:
                print 'Please enter y or n...'
        '''        
        date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
        filename1 ='\d20' + str((time.strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
        pogk = 0
        print filename1
    else:
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\201509\\'
        filename1 = 'd20150902_010'
            
            
            
            
    ########################################
    ######Data Read  
    
    print a
    dataL = pd.read_csv(pathL+filename1)

    
    TimeL = dataL.TheTime-dataL.TheTime[0]
    TimeL*=60.*60.*24.
    
    dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
    T1 = pd.datetime(1899,12,30,0)
    T2 = pd.datetime(1970,01,01,0)
    offset=T1-T2
    dataL.TheTime+=offset
    
    tmp_pid2 = dataL.pid1.notnull()
    
    try:
        tmp_pid3 = dataL.pid2.notnull()
    except AttributeError:
        pass
        
    try:
        tmp_pid4 = dataL.pid3.notnull()
    except AttributeError:
        pass
        
    tmp_flow = dataL.mfchiR.notnull()
        
    isop_cyl = 13.277	#ppbv
    mfchi_range = 100.	#sccm
    mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
    
    mfclo_range = 20.	#sccm
    mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
    
    dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
    isop_mr = dil_fac*isop_cyl
    
    
    #### Relative Humidity ###
    
    try:
        RH = dataL.RH
        RH -= 0.826
        RH /= 31.482E-3
        
    
    except AttributeError:
        pass
        
    ##########################
    
    
    if pid_2_on == 'Y':
        mean_pid2 = np.nanmean(dataL.pid1)
        translator_pid2  = mean_pid2
        scal_fac_pid2 =  6E-5
        isop_mr_raw_plot_pid2 = (isop_mr*scal_fac_pid2)+translator_pid2
    if pid_3_on == 'Y':
        mean_pid3 = np.nanmean(dataL.pid2)
        translator_pid3  = mean_pid3
        scal_fac_pid3 = 1.2E-4
        isop_mr_raw_plot_pid3 = (isop_mr*scal_fac_pid3)+translator_pid3
    if pid_4_on == 'Y':
        mean_pid4 = np.nanmean(dataL.pid3)
        scal_fac_pid4 =  1E-4
        translator_pid4  = mean_pid4+0.001*mean_pid4
        isop_mr_raw_plot_pid4 = (isop_mr*scal_fac_pid4)+translator_pid4
    
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
        
        
        
        
        data_point_length = n # how many data points used for the cals
        end_cut_off = 10
        
    
    
        
        mfc_setF = dataL.index[mfc_set]
        
        mfc_setF = mfc_setF[1:]
        mfc_setF -= end_cut_off #taking some data points away from the end to give a bit of a tolerance
        
        
        mfc_setS = [i-data_point_length for i in mfc_setF]    
    
                
        S = mfc_setS
        F = mfc_setF
    

        cal_cols_new = ['Start Times','End Times','Isop','Isop Stddev']
        
        if pid_2_on == 'Y':
            cal_cols_new.append('Pid2 Voltage')
            cal_cols_new.append('Pid2 Stddev')
            
        if pid_3_on == 'Y':
            cal_cols_new.append('Pid3 Voltage')
            cal_cols_new.append('Pid3 Stddev')
            
        if pid_4_on == 'Y':
            cal_cols_new.append('Pid4 Voltage')
            cal_cols_new.append('Pid4 Stddev')
            
        cal_df = pd.DataFrame(index=range(0,len(S)), columns=cal_cols_new)
    
        
        if pid_2_on == 'Y':
            pid2_chunks = list_multisplicer_listsout(dataL.pid1,mfc_setS,mfc_setF)
        
            pid2_avgs = [np.nanmean(i) for i in pid2_chunks]
            pid2_stds = [np.nanstd(i) for i in pid2_chunks]
            
            cal_df['Pid2 Voltage'] = pid2_avgs
            cal_df['Pid2 Stddev'] = pid2_stds
            
        if pid_3_on == 'Y':
            
            pid3_chunks = list_multisplicer_listsout(dataL.pid2,mfc_setS,mfc_setF)
            
            pid3_avgs = [np.nanmean(i) for i in pid3_chunks]
            pid3_stds = [np.nanstd(i) for i in pid3_chunks]
            
            cal_df['Pid3 Voltage'] = pid3_avgs
            cal_df['Pid3 Stddev']= pid3_stds 
            
        if pid_4_on =='Y':
            pid4_chunks = list_multisplicer_listsout(dataL.pid3,mfc_setS,mfc_setF)
            
            pid4_avgs = [np.nanmean(i) for i in pid4_chunks]
            pid4_stds = [np.nanstd(i) for i in pid4_chunks] 
        
            cal_df['Pid4 Voltage'] = pid4_avgs
            cal_df['Pid4 Stddev'] = pid4_stds
            
            
        isop_chunks = list_multisplicer_listsout(isop_mr,mfc_setS,mfc_setF)
        
        isop_avgs = [np.nanmean(i) for i in isop_chunks]
        isop_stds = [np.nanstd(i) for i in isop_chunks]
        
        
        start_times = [TimeL[i] for i in mfc_setS]
        end_times = [TimeL[i] for i in mfc_setF]
        
    
    
        cal_df['Isop'] = isop_avgs
        cal_df['Isop Stddev'] = isop_stds
        cal_df['Start Times'] = start_times
        cal_df['End Times'] = end_times
    
    
        
        cal_df = cal_df.dropna()
        cal_df.index = range(0,len(cal_df))
    
        cal_df_filtered = cal_df

        ########################## Zero Averaging #########################
        
        no_stds = 1.5
        
        isop_zero_indexes = []
        isop_zeros_avgs_pid2 =[]
        isop_zeros_avgs_pid3 = []
        isop_zeros_avgs_pid4 = []
        isop_zeros_stds = []
        
        isop_05_indexes = []
        isop_05_avgs_pid2 =[]
        isop_05_avgs_pid3 =[]
        isop_05_avgs_pid4 =[]
        isop_05_stds = []
        
        isop_10_indexes = []
        isop_10_avgs_pid2 =[]
        isop_10_avgs_pid3 =[]
        isop_10_avgs_pid4 =[]
        isop_10_stds = []
        
        isop_15_indexes = []
        isop_15_avgs_pid2 =[]
        isop_15_avgs_pid3 =[]
        isop_15_avgs_pid4 =[]
        isop_15_stds = []
        
        isop_20_indexes = []
        isop_20_avgs_pid2 =[]
        isop_20_avgs_pid3 =[]
        isop_20_avgs_pid4 =[]
        isop_20_stds = []
        
        isop_25_indexes = []
        isop_25_avgs_pid2 =[]
        isop_25_avgs_pid3 =[]
        isop_25_avgs_pid4 =[]
        isop_25_stds = [] 
    
        isop_30_indexes = []
        isop_30_avgs_pid2 =[]
        isop_30_avgs_pid3 =[]
        isop_30_avgs_pid4 =[]
        isop_30_stds = []  
        
        isop_35_indexes = []
        isop_35_avgs_pid2 =[]
        isop_35_avgs_pid3 =[]
        isop_35_avgs_pid4 =[]
        isop_35_stds = []     
        
        
        for i in range(0,len(cal_df.Isop)):
            if cal_df.Isop[i] < 0.2:
                if pid_3_on:
                    isop_zeros_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_zeros_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_zeros_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_zero_indexes.append(i)
                isop_zeros_stds.append(cal_df['Isop Stddev'][i])
        '''       
            elif cal_df.Isop[i] >0.35 and cal_df.Isop[i] < 0.65:
                if pid_3_on:
                    isop_05_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_05_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_05_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_05_indexes.append(i)
                isop_05_stds.append(cal_df['Isop Stddev'][i])
                
            elif cal_df.Isop[i] >0.85 and cal_df.Isop[i] < 1.15:
                if pid_3_on:
                    isop_10_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_10_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_10_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_10_indexes.append(i)
                isop_10_stds.append(cal_df['Isop Stddev'][i])
                
            elif cal_df.Isop[i] >1.35 and cal_df.Isop[i] < 1.65:
                if pid_3_on:
                    isop_15_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_15_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_15_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_15_indexes.append(i)
                isop_15_stds.append(cal_df['Isop Stddev'][i])
    
            elif cal_df.Isop[i] >1.85 and cal_df.Isop[i] < 2.15:
                if pid_3_on:
                    isop_20_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_20_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_20_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_20_indexes.append(i)
                isop_20_stds.append(cal_df['Isop Stddev'][i])
                
            elif cal_df.Isop[i] >2.35 and cal_df.Isop[i] < 2.65:
                if pid_3_on:
                    isop_25_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_25_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_25_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_25_indexes.append(i)
                isop_25_stds.append(cal_df['Isop Stddev'][i])
            
            elif cal_df.Isop[i] >2.85 and cal_df.Isop[i] < 3.15:
                if pid_3_on:
                    isop_30_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_30_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_30_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_30_indexes.append(i)
                isop_30_stds.append(cal_df['Isop Stddev'][i])
            
            elif cal_df.Isop[i] >3.35 and cal_df.Isop[i] < 3.65:
                if pid_3_on:
                    isop_35_avgs_pid3.append(cal_df['Pid3 Voltage'][i])
                
                if pid_2_on:
                    isop_35_avgs_pid2.append(cal_df['Pid2 Voltage'][i])
                
                if pid_4_on: 
                    isop_35_avgs_pid4.append(cal_df['Pid4 Voltage'][i])
                
                isop_35_indexes.append(i)
                isop_35_stds.append(cal_df['Isop Stddev'][i])
                
            '''
        
        if pid_2_on:    
            ######################### Zero Outliers Pid 2 ######################
            s0_pid2 = np.nanstd(cal_df['Pid2 Voltage'][isop_zero_indexes])
            m0_pid3 = np.nanmean(isop_zeros_avgs_pid2)        
                    
            isop_zeros_avgs_pid2_filtered = []
            for i in range(0,len(isop_zeros_avgs_pid2)):
                if isop_zeros_avgs_pid2[i]> m0_pid3-(no_stds*s0_pid2) and isop_zeros_avgs_pid2[i] < m0_pid3+(no_stds*s0_pid2):       
                    isop_zeros_avgs_pid2_filtered.append(isop_zeros_avgs_pid2[i])
            
            isop_zeros_avg_filtered_pid2 = np.nanmean(isop_zeros_avgs_pid2_filtered)
            isop_zeros_avg_pid2 = np.nanmean(isop_zeros_avgs_pid2)
            isop_05_avg_pid2 = np.nanmean(isop_05_avgs_pid2)
            isop_10_avg_pid2 = np.nanmean(isop_10_avgs_pid2)
            isop_15_avg_pid2 = np.nanmean(isop_15_avgs_pid2)        
            isop_20_avg_pid2 = np.nanmean(isop_20_avgs_pid2)
            isop_25_avg_pid2 = np.nanmean(isop_25_avgs_pid2)
            isop_30_avg_pid2 = np.nanmean(isop_30_avgs_pid2)
            isop_35_avg_pid2 = np.nanmean(isop_35_avgs_pid2)
            
            
            cal_df['Pid2 Voltage'][isop_zero_indexes] = isop_zeros_avg_pid2
            '''
            cal_df['Pid2 Voltage'][isop_05_indexes] = isop_05_avg_pid2
            cal_df['Pid2 Voltage'][isop_10_indexes] = isop_10_avg_pid2
            cal_df['Pid2 Voltage'][isop_15_indexes] = isop_15_avg_pid2                                      
            cal_df['Pid2 Voltage'][isop_20_indexes] = isop_20_avg_pid2
            cal_df['Pid2 Voltage'][isop_25_indexes] = isop_25_avg_pid2
            cal_df['Pid2 Voltage'][isop_30_indexes] = isop_30_avg_pid2
            cal_df['Pid2 Voltage'][isop_35_indexes] = isop_35_avg_pid2
            '''
    
        if pid_3_on:
            ######################### Zero Outliers Pid 3 ######################
            s_pid3 = np.nanstd(cal_df['Pid3 Voltage'][isop_zero_indexes])
            m_pid3 = np.nanmean(isop_zeros_avgs_pid3)        
                    
            isop_zeros_avgs_filtered_pid3 = []
            for i in range(0,len(isop_zeros_avgs_pid3)):
                if isop_zeros_avgs_pid3[i]> m_pid3-(no_stds*s_pid3) and isop_zeros_avgs_pid3[i] < m_pid3+(no_stds*s_pid3):       
                    isop_zeros_avgs_filtered_pid3.append(isop_zeros_avgs_pid3[i])
            
            isop_zeros_avg_filtered_pid3 = np.nanmean(isop_zeros_avgs_filtered_pid3)
            isop_zeros_avg_pid3 = np.nanmean(isop_zeros_avgs_pid3)
            
            cal_df['Pid3 Voltage'][isop_zero_indexes] = isop_zeros_avg_pid3
    
        
        if pid_4_on:                                                                                               
            ######################### Zero Outliers Pid 4 ######################
            s_pid4 = np.nanstd(cal_df['Pid4 Voltage'][isop_zero_indexes])
            m_pid4 = np.nanmean(isop_zeros_avgs_pid4) 
            
                        
                    
            isop_zeros_avgs_filtered_pid4 = []
            for i in range(0,len(isop_zeros_avgs_pid4)):
                if isop_zeros_avgs_pid4[i]> m_pid4-(no_stds*s_pid4) and isop_zeros_avgs_pid4[i] < m_pid4+(no_stds*s_pid4):       
                    isop_zeros_avgs_filtered_pid4.append(isop_zeros_avgs_pid4[i])
            
            isop_zeros_avg_filtered_pid4 = np.nanmean(isop_zeros_avgs_filtered_pid4)
            isop_zeros_avg_pid4 = np.nanmean(isop_zeros_avgs_pid4)
            
            cal_df['Pid4 Voltage'][isop_zero_indexes] = isop_zeros_avg_pid4
    
    
    
    
    

        ########## Tidying up and fitting #########
        
    
        
        isop_fit = [0.,np.max(cal_df.Isop)]    
        
        if pid_2_on:
            
            cal_df = cal_df.drop_duplicates(subset = ['Pid2 Voltage'])
            cal_df.index = range(0,len(cal_df))
            
            for i in range(len(cal_df)):
                    yerr2.append(cal_df['Pid2 Stddev'][i]/np.sqrt(len(pid2_chunks[i+1])))
                    
            xdata = cal_df.Isop
            ydata2 = cal_df['Pid2 Voltage'] 
            slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr2)
            pid2_fit = [slope_intercept2[0],(np.max(cal_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
            
            perr2 = np.sqrt(np.diag(pcov2))
            Intercept_error2 = perr2[0]/np.sqrt(cal_N)
            Slope_Error2 = perr2[0]/np.sqrt(cal_N)        
            
            slopesqwe_pid2.append(slope_intercept2[1])
            slopes_errorqwe_pid2.append(Slope_Error2) 
            
                    
        if pid_3_on: 
            cal_df = cal_df.drop_duplicates(subset = ['Pid3 Voltage'])
            cal_df.index = range(0,len(cal_df))
            
            for i in range(len(cal_df)):
                yerr3.append(cal_df['Pid3 Stddev'][i]/np.sqrt(len(pid3_chunks[i+1]))) 
                
            xdata = cal_df.Isop     
            ydata3 = cal_df['Pid3 Voltage']
            slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
            pid3_fit = [slope_intercept3[0],(np.max(cal_df.Isop)*slope_intercept3[1])+slope_intercept3[0]]
    
            perr3 = np.sqrt(np.diag(pcov3))    
            Intercept_error3 = perr3[0]/np.sqrt(cal_N)
            Slope_Error3 = perr3[0]/np.sqrt(cal_N)        
            
            slopesqwe_pid3.append(slope_intercept3[1])
            slopes_errorqwe_pid3.append(Slope_Error3)
            
                
        if pid_4_on: 
            cal_df = cal_df.drop_duplicates(subset = ['Pid4 Voltage'])
            cal_df.index = range(0,len(cal_df))
            for i in range(len(cal_df)):
                yerr4.append(cal_df['Pid4 Stddev'][i]/np.sqrt(len(pid4_chunks[i+1])))
                
            xdata = cal_df.Isop
            ydata4 = cal_df['Pid4 Voltage']
            slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr4)
            pid4_fit = [slope_intercept4[0],(np.max(cal_df.Isop)*slope_intercept4[1])+slope_intercept4[0]]
            
            perr4 = np.sqrt(np.diag(pcov4))    
            Intercept_error4 = perr4[0]/np.sqrt(cal_N)
            Slope_Error4 = perr4[0]/np.sqrt(cal_N)
            
            slopesqwe_pid4.append(slope_intercept4[1])
            slopes_errorqwe_pid4.append(Slope_Error4)
     
    
    
    
    
                
    n=n+d
    a=a+1     



x = range(150,850)[::d]
y2 = slopes_errorqwe_pid2
y3 = slopes_errorqwe_pid3
y4 = slopes_errorqwe_pid4

if pid_2_on:
    figH = plt.figure()
    plt.plot(x,y2,color='b')
    plt.plot(x,slopesqwe_pid2,color='r')
    slope_patch = mpatches.Patch(label='Slope Errors',color = 'b')
    slope_error_patch = mpatches.Patch(label = 'Slope Values',color = 'r')
    plt.legend(handles=[slope_patch,slope_error_patch],loc=2)
    plt.title('Pid 2 - ('+str(filename1[5:-5])+'\\'+str(filename1[-5:-3])+') Run '+str(filename1[-2:]))
    

if pid_3_on:
    
    figH1 = plt.figure()
    plt.plot(x,y3,color='b')
    plt.plot(x,slopesqwe_pid3,color='r')
    plt.legend(handles=[slope_patch,slope_error_patch],loc=2)
    plt.title('Pid 3 - ('+str(filename1[5:-5])+'\\'+str(filename1[-5:-3])+') Run '+str(filename1[-2:]))
    
if pid_4_on:
    figH2 = plt.figure()
    plt.plot(x,y4,color='b')
    plt.plot(x,slopesqwe_pid4,color='r')
    plt.legend(handles=[slope_patch,slope_error_patch],loc=2)
    plt.title('Pid 4 - ('+str(filename1[5:-5])+'\\'+str(filename1[-5:-3])+') Run '+str(filename1[-2:]))
    
plt.show()