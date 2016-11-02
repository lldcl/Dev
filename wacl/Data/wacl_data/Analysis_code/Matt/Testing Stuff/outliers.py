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
            for i in range(0,len(y)):    
                print 'Cal number = ',i+1
                print 'mfc_setS = ',x[i]
                print 'mfc_setF = ',y[i]
                print 'difference = ',y[i]-x[i]
                print '\n'

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
arduino = ''

pid_2_on = 'Y'

pid_3_on = 'Y'

pid_4_on = ''

if cal_stuff == 'Y':
    if arduino == 'Y':
        arduino_cal_stuff = 'Y'
    else:    
        arduino_cal_stuff = ''
    questions = 'Y'
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
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\201507\\'
    filename1 = 'd20150713_02'
        
        
        
        
########################################
######Data Read  

dataL = pd.read_csv(pathL+filename1)
print 'Loading...'

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

if pid_2_on == 'Y':
    mean_pid2 = np.nanmean(dataL.pid1)
    translator_pid2  = mean_pid2
    scal_fac_pid2 =  2.5E-4
    isop_mr_raw_plot_pid2 = (isop_mr*scal_fac_pid2)+translator_pid2
if pid_3_on == 'Y':
    mean_pid3 = np.nanmean(dataL.pid2)
    translator_pid3  = mean_pid3
    scal_fac_pid3 = 2.5E-4
    isop_mr_raw_plot_pid3 = (isop_mr*scal_fac_pid3)+translator_pid3
if pid_4_on == 'Y':
    mean_pid4 = np.nanmean(dataL.pid3)
    scal_fac_pid4 =  2.5E-4
    translator_pid4  = mean_pid4+0.001*mean_pid4
    isop_mr_raw_plot_pid4 = (isop_mr*scal_fac_pid4)+translator_pid4

dataL['mfchi'] = [(5+((0*i)+1)) for i in range(0,len(dataL))] 
dataL = dataL.fillna({'mfchi':5})

#############################
## Signal vs Isop for calibration experiments

if arduino_cal_stuff == 'Y':
    
    pathA = 'C:\\Users\\mat_e_000\\Desktop\\arduino_PID_read\\'
    filenameA = 'USB_read.py.dat'
    dataA = pd.read_csv(pathA+filenameA,sep = '\t')
    dataA = dataA.dropna(subset=['Time'])
    

    
    
    
    dataA.Voltage*=1e-3
    
    mean_voltage = np.mean(dataA.Voltage)
    
    TimeA = map(timeconverter,dataA.Time)

   
if (cal == 'Y'):
    
    mfc_set = np.zeros((len(dataL.mfclo)),dtype=bool)
    for i in range(1,len(dataL.mfchi)):
        if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i-1],dataL.mfclo[i]!=dataL.mfclo[i-1]))):
                mfc_set[i] = "True"
                
    cal_N = np.sum(mfc_set) # number of changes in value for mfclo
        
    cal_pts = [range(0,cal_N)]
    
    ############################################################# PID 2 ################################################
    
    
    
    ######################  General Adjustments  ##################
    
    pinch = 200   # Makes the data range smaller at each side by the pinch amount 
    translate = 100 # A positive translate is a translation to the right
    
    
    mfc_setS = []
    for i in range(0,len(mfc_set)-1):
        if mfc_set[i] == True:
            mfc_setS.append(i)
    
    
    for i in range(0,len(mfc_setS)-2):
        
        mfc_setS[i] = mfc_setS[i] + pinch
    
    mfc_setS = [i+translate for i in mfc_setS]

   
    zero_time = 300 # how long the zero at the end will be

    
    mfc_setF = dataL.index[mfc_set]
    mfc_setF = [i-pinch for i in mfc_setF]
    mfc_setF = [i+translate for i in mfc_setF]
    
    if mfc_setF[-1]+zero_time < len(dataL):
        
    
        mfc_setF = np.append(mfc_setF,(mfc_setF[len(mfc_setF)-1]+zero_time))
        mfc_setF = np.delete(mfc_setF,0)
        mfc_setF-=11#Delay at end of cal step
    else:
        print '\n\nERROR MESSAGE:'
        zero_time = int(raw_input('\n\nThe zero time at the end was a bit big, please lower it to ' + str(len(dataL)-mfc_setF[-1] -1) + ' or below\n\nZero Time = '))
        mfc_setF = np.append(mfc_setF,(mfc_setF[len(mfc_setF)-1]+zero_time))
        mfc_setF = np.delete(mfc_setF,0)
        mfc_setF-=11#Delay at end of cal_L step
        
    
    #################### Individual Adjustments ##################
    
    ## Cal point 1 ##
    p2pinch1 = 100
    p2translate1 = 240
    
    mfc_setS[0] = mfc_setS[0] + p2pinch1 + p2translate1
    mfc_setF[0] = mfc_setF[0] - p2pinch1 + p2translate1
    
    ## Cal point 2 ##
    p2pinch2 = 150
    p2translate2 = 0
    
    mfc_setS[1] = mfc_setS[1] + p2pinch2 + p2translate2
    mfc_setF[1] = mfc_setF[1] - p2pinch2 + p2translate2
    
    ## Cal point 3 ##
    p2pinch3 = 150
    p2translate3 = 200
    
    mfc_setS[2] = mfc_setS[2] + p2pinch3 + p2translate3
    mfc_setF[2] = mfc_setF[2] - p2pinch3 + p2translate3
    
    ## Cal point 4 ##
    p2pinch4 = 100
    p2translate4 = 0

    mfc_setS[3] = mfc_setS[3] + p2pinch4 + p2translate4
    mfc_setF[3] = mfc_setF[3] - p2pinch4 + p2translate4
        
    ## Cal point 5 ##
    p2pinch5 = 175
    p2translate5 = -50
    
    mfc_setS[4] = mfc_setS[4] + p2pinch5 + p2translate5
    mfc_setF[4] = mfc_setF[4] - p2pinch5 + p2translate5
        
    ## Cal point 6 ##
    p2pinch6 = 125
    p2translate6 = 100
    
    mfc_setS[5] = mfc_setS[5] + p2pinch6 + p2translate6
    mfc_setF[5] = mfc_setF[5] - p2pinch6 + p2translate6 
    
    ## Cal point 7 ##
    p2pinch7 = 0
    p2translate7 = 0
    
    mfc_setS[6] = mfc_setS[6] + p2pinch7 + p2translate7
    mfc_setF[6] = mfc_setF[6] - p2pinch7 + p2translate7    
    
    ## Cal point 8 ##
    p2pinch8 = 100
    p2translate8 = 400
    
    mfc_setS[7] = mfc_setS[7] + p2pinch8 + p2translate8
    mfc_setF[7] = mfc_setF[7] - p2pinch8 + p2translate8 
    
    ## Cal point 9 ##
    p2pinch9 = 100
    p2translate9 = 300
    
    mfc_setS[8] = mfc_setS[8] + p2pinch9 + p2translate9
    mfc_setF[8] = mfc_setF[8] - p2pinch9 + p2translate9     
    
    ## Cal point 10 ##
    p2pinch10 = 75
    p2translate10 = 200
    
    mfc_setS[9] = mfc_setS[9] + p2pinch10 + p2translate10
    mfc_setF[9] = mfc_setF[9] - p2pinch10 + p2translate10     
    
    ## Cal point 11 ##
    p2pinch11 = 300
    p2translate11 = 400

    mfc_setS[10] = mfc_setS[10] + p2pinch11 + p2translate11
    mfc_setF[10] = mfc_setF[10] - p2pinch11 + p2translate11
    '''
    ## Cal point 12 ##
    p2pinch12 = 300
    p2translate12 = 400

    mfc_setS[11] = mfc_setS[11] + p2pinch12 + p2translate12
    mfc_setF[11] = mfc_setF[11] - p2pinch12 + p2translate12
    
    ## Cal point 13 ##
    p2pinch13 = 300
    p2translate13 = 400

    mfc_setS[12] = mfc_setS[12] + p2pinch13 + p2translate13
    mfc_setF[12] = mfc_setF[12] - p2pinch13 + p2translate13

    ## Cal point 14 ##
    p2pinch14 = 300
    p2translate14 = 400

    mfc_setS[13] = mfc_setS[13] + p2pinch14 + p2translate14
    mfc_setF[13] = mfc_setF[13] - p2pinch14 + p2translate14
    '''
    
    
    
    
    
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
        
    cal_df = pd.DataFrame(index=cal_pts, columns=cal_cols_new)
  
    
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

    cal_df_filtered = pd.DataFrame(columns=cal_cols_new)
    
    ########################## Zero Averaging #########################
    
    no_stds = 1.5
    
    isop_zero_indexes = []
    isop_zeros_avgs_pid2 =[]
    isop_zeros_avgs_pid3 = []
    isop_zeros_avgs_pid4 = []
        
    isop_zeros_stds = []
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
            
     

    if pid_2_on:    
        ######################### Zero Outliers Pid 2 ######################
        s_pid2 = np.nanstd(cal_df['Pid2 Voltage'][isop_zero_indexes])
        m_pid3 = np.nanmean(isop_zeros_avgs_pid2)        
                
        isop_zeros_avgs_pid2_filtered = []
        for i in range(0,len(isop_zeros_avgs_pid2)):
            if isop_zeros_avgs_pid2[i]> m_pid3-(no_stds*s_pid2) and isop_zeros_avgs_pid2[i] < m_pid3+(no_stds*s_pid2):       
                isop_zeros_avgs_pid2_filtered.append(isop_zeros_avgs_pid2[i])
        
        isop_zeros_avg_filtered_pid2 = np.nanmean(isop_zeros_avgs_pid2_filtered)
        isop_zeros_avg_pid2 = np.nanmean(isop_zeros_avgs_pid2)
        

        cal_df['Pid2 Voltage'][isop_zero_indexes] = isop_zeros_avg_pid2
        #cal_df1 = pd.DataFrame(columns=['Pid2 Voltage'])
        #cal_df1['Pid2 Voltage'] = cal_df['Pid2 Voltage'][range(0,10)[0:9]]
        
        avg_std_pid2 = np.mean(cal_df['Pid2 Stddev'])    
        
        non_outliers_pid2 = []
        for i in range(0,len(cal_df['Pid2 Voltage'])):
            if cal_df['Pid2 Voltage'][i] < mean_pid2+3*avg_std_pid2 and cal_df['Pid2 Voltage'][i] >mean_pid2-3*avg_std_pid2:    
                non_outliers_pid2.append(i)                              
        
        for i in cal_cols_new:
            for pt in non_outliers_pid2:
                cal_df_filtered[i] = cal_df[i][pt]

                
        
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
        cal_df1 = pd.DataFrame(columns=['Pid3 Voltage'])
        cal_df1['Pid3 Voltage'] = cal_df['Pid3 Voltage'][range(0,10)[0:9]] 
     
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
        cal_df1 = pd.DataFrame(columns=['Pid Voltage'])
        cal_df1['Pid4 Voltage'] = cal_df['Pid4 Voltage'][range(0,10)[0:9]] 







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
        


    ######## Error finding #######
    
    
    
    for i in range(0,len(cal_df)):
        if cal_df['Isop'][i] < 0.25:
            i = i
            
    xerrunfil = np.sqrt(cal_df['Isop Stddev'][i]/len(isop_chunks[i]))
            
        
    for i in range(len(cal_df)):
        xerr.append(cal_df['Isop Stddev'][i]/np.sqrt(len(isop_chunks[i+1])))

    #data = {'Slopes':[slope_intercept2[1],slope_intercept3[1]], 'Slope Error':[Slope_Error2,Slope_Error3],'Intercepts':[slope_intercept2[0], slope_intercept3[0]],'Intercept Error':[Intercept_error2,Intercept_error3]}  
    #frame = pd.DataFrame(data,index=['PID2','PID3'])
    #print frame










##########################################    Plotting   ##########################################  
if plots == 'Y':
    
    date = timestamp_convert(dataL.TheTime[0])[1:3]
    date = '/'.join(date)
    
    filenumber = filename1[-2:]
    
    times = list_multisplicer(dataL.TheTime,mfc_setS,mfc_setF)

    if pid_2_on == 'Y':
        ########################################### PID 2 ###########################################
        voltage_pid2 = list_multisplicer(dataL.pid1,mfc_setS,mfc_setF)
        
        
        
        
        
        fig2r = plt.figure()
        ###### Raw Data #######
        
        ax2r2 = fig2r.add_subplot(212)
        pid2_raw_data = ax2r2.plot(dataL.TheTime[tmp_pid2],dataL.pid1[tmp_pid2], linewidth=1,color='r')
        pid2_Isop = ax2r2.plot(dataL.TheTime[tmp_flow],isop_mr_raw_plot_pid2[tmp_flow], linewidth=1,color='g')
        #pid2_rolling_avg = ax2r2.plot(dataL.TheTime,pd.rolling_mean(dataL.pid1,300))
        # Making graph pretty #
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        
        #xy_coords = pyl.ginput(n=12)
        
        
        
        ####### Spliced graph #######
        
        ax2r1 = fig2r.add_subplot(211)
        spliced_graph_pid2 = ax2r1.plot(times,voltage_pid2, linewidth=1,color= 'b')
        #spliced_graph_pid2_limits = ax2r1.set_ylim([mean_pid2-2.5E-4,mean_pid2+2.5E-4])
        spliced_graph_rolling_avg = ax2r1.plot(dataL.TheTime,pd.rolling_mean(dataL.pid1,300), linewidth=1,color= 'r')
        # Making graph pretty 
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 2, Raw Data ('+date+') - '+filenumber)
        
        
        
        
        
        ###########################################
        
        
        ###### Cal Plot ######
        
        fig2c = plt.figure()
        ax2c1 = fig2c.add_subplot(111)
        pid2_cal_points = ax2c1.errorbar(cal_df.Isop,cal_df['Pid2 Voltage'], xerr = xerr, yerr = yerr2, fmt='o')
        pid2_cal_fit = ax2c1.plot(isop_fit,pid2_fit)
        
        # Adding a legend #
        slope_patch_pid2 = mpatches.Patch(label='Slope = '+str("%.2e" % slope_intercept2[1])+'+/-'+str("%.1e" % Slope_Error2))
        intecept_patch_pid2 = mpatches.Patch(label = 'Intercept = '+str("%.2e" % slope_intercept2[0])+'+/-'+str("%.1e" % Intercept_error2))
        plt.legend(handles=[slope_patch_pid2,intecept_patch_pid2],loc=2)
        
        # Making graph pretty #
        plt.ylabel('Pid 2 Voltage / V', fontsize = 13)
        plt.xlabel('Isoprene Concentration / ppb', fontsize = 13)
        plt.title('Pid 2, Cal plot ('+date+') - '+filenumber)
        
        
        
    

    if pid_3_on == 'Y':
        ########################################### PID 3 ###########################################
        voltage_pid3 = list_multisplicer(dataL.pid2,mfc_setS,mfc_setF)
        

        pid3_rolling_avg = pd.rolling_mean(dataL.pid2,300)
        
        fig3r = plt.figure()
        ax3r1 = fig3r.add_subplot(211)
        spliced_graph_pid3 = ax3r1.plot(times,voltage_pid3, linewidth=1,color= 'b')
        #spliced_graph_pid3_limits = ax3r1.set_ylim([mean_pid3-2.5E-4,mean_pid3+2.5E-4])
        spliced_graph_rolling_avg = ax3r1.plot(dataL.TheTime,pid3_rolling_avg, linewidth=1, color = 'r')
        
        # Making the Graph Pretty#
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 3, Raw Data ('+date+') - '+filenumber)
        
        ###### Raw Data #######
        
        ax3r2 = fig3r.add_subplot(212)
        pid3_raw_data = ax3r2.plot(dataL.TheTime[tmp_pid3],dataL.pid1[tmp_pid3], linewidth=1,color='b')
        pid3_Isop = ax3r2.plot(dataL.TheTime[tmp_flow],isop_mr_raw_plot_pid3[tmp_flow], linewidth=1,color='g')
        #pid3_rolling_avg_raw_plot = ax3r2.plot(dataL.TheTime,pid3_rolling_avg, linewidth=1,color = 'r')
        
        # Making graph pretty #
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        
        
        ###########################################
        
        
        ###### Cal Plot ######
        
        fig3c = plt.figure()
        ax3c1 = fig3c.add_subplot(111)
        #pid3_filtered_zero_point = ax3c1.errorbar(0,isop_zeros_avg_filtered_pid3,xerr = xerrunfil,fmt='x')
        pid3_cal_points = ax3c1.errorbar(cal_df.Isop,cal_df['Pid3 Voltage'], xerr = xerr, yerr = yerr3, fmt='o')
        pid3_cal_fit = ax3c1.plot(isop_fit,pid3_fit)
        
        # Adding a legend #
        slope_patch_pid3 = mpatches.Patch(label='Slope = '+str("%.2e" % slope_intercept3[1])+'+/-'+str("%.1e" % Slope_Error3))
        intecept_patch_pid3 = mpatches.Patch(label = 'Intercept = '+str("%.2e" % slope_intercept3[0])+'+/-'+str("%.1e" % Intercept_error3))
        plt.legend(handles=[slope_patch_pid3,intecept_patch_pid3],loc=2)
        
        # Making graph pretty #
        plt.ylabel('Pid 3 Voltage / V', fontsize = 13)
        plt.xlabel('Isoprene Concentration / ppb', fontsize = 13)
        plt.title('Pid 3, Cal plot ('+date+') - '+filenumber)


    
    
    
    
###########################################PID 4 ###########################################

        if pid_4_on == 'Y':
            ########################################### PID 4 ###########################################
            voltage_pid4 = list_multisplicer(dataL.pid2,mfc_setS,mfc_setF)
            

            pid4_rolling_avg = pd.rolling_mean(dataL.pid2,400)
            
            fig4r = plt.figure()
            ax4r1 = fig4r.add_subplot(211)
            spliced_graph_pid4 = ax4r1.plot(times,voltage_pid4, linewidth=1,color= 'b')
            #spliced_graph_pid4_limits = ax4r1.set_ylim([mean_pid4-2.5E-4,mean_pid4+2.5E-4])
            spliced_graph_rolling_avg = ax4r1.plot(dataL.TheTime,pid4_rolling_avg, linewidth=1, color = 'r')
            
            # Making the Graph Pretty#
            plt.ylabel("Isop / ppb")
            plt.xlabel('Time / s', fontsize = 20)
            plt.title('Pid 4, Raw Data ('+date+') - '+filenumber)
            
            ###### Raw Data #######
            
            ax4r2 = fig4r.add_subplot(212)
            pid4_raw_data = ax4r2.plot(dataL.TheTime[tmp_pid4],dataL.pid1[tmp_pid4], linewidth=1,color='b')
            pid4_Isop = ax4r2.plot(dataL.TheTime[tmp_flow],isop_mr_raw_plot_pid4[tmp_flow], linewidth=1,color='g')
            #pid4_rolling_avg_raw_plot = ax4r2.plot(dataL.TheTime,pid4_rolling_avg, linewidth=1,color = 'r')
            
            # Making graph pretty #
            plt.ylabel("Isop / ppb")
            plt.xlabel('Time / s', fontsize = 20)
            
            
            ###########################################
            
            
            ###### Cal Plot ######
            
            fig4c = plt.figure()
            ax4c1 = fig4c.add_subplot(111)
            #pid4_filtered_zero_point = ax4c1.errorbar(0,isop_zeros_avg_filtered_pid4,xerr = xerrunfil,fmt='x')
            pid4_cal_points = ax4c1.errorbar(cal_df.Isop,cal_df['Pid4 Voltage'], xerr = xerr, yerr = yerr4, fmt='o')
            pid4_cal_fit = ax4c1.plot(isop_fit,pid4_fit)
            
            # Adding a legend #
            slope_patch_pid4 = mpatches.Patch(label='Slope = '+str("%.2e" % slope_intercept4[1])+'+/-'+str("%.1e" % Slope_Error4))
            intecept_patch_pid4 = mpatches.Patch(label = 'Intercept = '+str("%.2e" % slope_intercept4[0])+'+/-'+str("%.1e" % Intercept_error4))
            plt.legend(handles=[slope_patch_pid4,intecept_patch_pid4],loc=2)
            
            # Making graph pretty #
            plt.ylabel('Pid 4 Voltage / V', fontsize = 14)
            plt.xlabel('Isoprene Concentration / ppb', fontsize = 14)
            plt.title('Pid 4, Cal plot ('+date+') - '+filenumber)
###########################################


print '\nShowing Graph'
plt.show()    


        


   
    
###############################################
############# Histogram Plotting

if hist == 'Y':
    
    pathH = 'E:\Bursary thing\Cal Stuff'

    filenameH1 = '\PID slope value'


    dataH1 = pd.read_csv(pathH+filenameH1)

    
    figH = plt.figure()
    
    ax1H = figH.add_subplot(211)
    ax1H.set_xlim([-0.00002, 0.0001])
    ax1H.set_ylim([0,90000])
    
    ax1H.set_xlabel('Bins')
    
     
    H1 = dataH1['PID2'].dropna()
    H2 = dataH1['PID3'].dropna()
    
        
    H1.hist(bins=20,alpha=0.3,color='k', normed = True)
    H1.plot(kind='kde', color='k')
    PID2_patch = mpatches.Patch(color='k',label='PID 2')
    plt.legend(handles=[PID2_patch])
       
    
    ax2H = figH.add_subplot(212)
    ax2H.set_xlim([-0.00002, 0.0001])
    ax2H.set_ylim([0,90000])

    ax2H.set_xlabel('Bins')
    
    H2.hist(bins=20,alpha=0.3,color='g', normed = True)
    H2.plot(kind='kde',color='g')
    PID3_patch = mpatches.Patch(color='g',label='PID 3')
    plt.legend(handles=[PID3_patch])
    plt.show()

    data = {'How many cals':[len(H1), len(H2)], 'Mean':[np.mean(H1),np.mean(H2)], 'Standard Deviation':[np.std(H1),np.std(H2)]}
    hist_frame = pd.DataFrame(data,index=['PID2','PID3'])
    print hist_frame
