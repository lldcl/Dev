import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from scipy import stats
import scipy.optimize as opt
import time
#from Tkinter import *
import datetime
import collections

################## Supposed to interpolate between NaN values
####
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


def timelist_convert(data):    
    time_listA = []
    time_listL = []
    try:
        for i in data.Time:
            b = timestamp_convert(i)[3:6]
            time_listA.append(b)
        return time_listA
    
    except AttributeError:
            for i in data['TheTime']:
                b = timestamp_convert(i)[3:6]
                time_listL.append(b)
            return time_listL
      
                  
def timeconverter(T):
    #	print T
    return (datetime.datetime.strptime(T,"%y-%m-%d-%H-%M-%S-%f"))


def troubleshooter(x,y):
            if y>len(mfc_setAS):
                y=len(mfc_setAS)
            if x>len(mfc_setAS):
                print 'That first value is too large, reduce it to '+len(mfc_setAS)-1+' or below'
                x = len(mfc_setAS)-1
            for i in range(x,y):    
                print 'Cal number = ',i+1
                print 'mfc_setAS = ',mfc_setAS[i]
                print 'mfc_setAF = ',mfc_setAF[i]
                print '\n'
                
                
def list_multisplicer(l1st,start_inidexes,end_indexes):
    new_lt = []
    for i in range(0,len(start_inidexes)):
        first = start_inidexes[i]
        last = end_indexes[i]
        for pt in range(0,len(l1st)):
            if pt >=first and pt <=last:
                new_lt.append(l1st[pt])
    return new_lt


def linear_fit(slope, intercept, x):
        return (slope*x)+intercept

pd.set_option('precision',9)

cal_stuff = 'Y'
arduino = 'Y'

pid_2_on = ''
pid_3_on = ''

if cal_stuff == 'Y':
    if arduino == 'Y':
        arduino_cal_stuff = 'Y'
    else:    
        arduino_cal_stuff = ''
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



npid2 = []
npid3 = []
nISop = []

cal_lengths = []

print '\nBefore you use this you\'ll have to check the path'



#############################
## User Interface
if questions == 'Y':
    #####Asking if the user would like to load from the memory stick
    pogk = 2
    while pogk == 2:
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
else:
    
    
    
    
    
    
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\201508\\'
    filename1 = 'd20150820_03'
    
pathA = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\201508\\'
filenameA = 'USB_read.py'        
ftype = 'dat' 
        
               
                      
                             
                                    
                                           
                                                  
                                                                
########################################
######Data Read  

dataL = pd.read_csv(pathL+filename1)
print '\n\nloading...\n'
TimeL = dataL.TheTime-dataL.TheTime[0]
#TimeL*=60.*60.*24.

dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
dataL.TheTime+=offset

tmp_pid2 = dataL.pid1.notnull()
tmp_pid3 = dataL.pid2.notnull()
tmp_flow = dataL.mfchiR.notnull()
    
isop_cyl = 13.277	#ppbv
mfchi_range = 100.	#sccm
mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)

mfclo_range = 20.	#sccm
mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)

dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = dil_fac*isop_cyl

dataL = dataL.fillna({'mfchi':5})



    
            




#############################
## Signal vs Isop for calibration experiments

if arduino_cal_stuff == 'Y':
    
    
    
    dataA = pd.read_csv(pathA+'\\'+filenameA+'.'+ftype,sep = '\t')
    dataA = dataA.dropna(subset=['Time'])
    dataA = dataA.dropna()
    dataL = dataL.dropna()
    A = timelist_convert(dataA)
    L = timelist_convert(dataL)

    start = L[0]
    end = A[-1]
    


    first_mutual_L = L.index(start)
    first_mutual_A = A.index(start)
    
    last_mutual_L = L.index(end)
    last_mutual_A = A.index(end)
    
    dataL_cut = dataL[first_mutual_L:]
    dataA_cut = dataA[first_mutual_A:]
    
    index_difference = 5 * abs(first_mutual_L-first_mutual_A)

    
    
    ### Converting the times in the .dat file to a form python can read

    TimeA = map(timeconverter,dataA.Time)
    
    
    dataA.Voltage*=1e-3
    
    mean_voltage = np.mean(dataA.Voltage)
    
    plt.plot(dataL.TheTime,dataL.pid1,color = 'g')
    plt.plot(TimeA,dataA.Voltage,color = 'r')
    
    
if (cal == 'Y'):

    mfc_setAS = []
    mfc_setAF = []
    mfc_setL = np.zeros((len(dataL.mfclo)),dtype=bool)

    for i in range(0,len(dataL)):
        try:
            dataL.TheTime[i]
            first_mutual_dataL = i
            break
        except KeyError:
            pass
    dataL.index = range(len(dataL))

    for i in range(first_mutual_L,last_mutual_L):
                if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i+1],dataL.mfclo[i]!=dataL.mfclo[i+1]))):
                        mfc_setL[i] = "True"

     
    cal_N = np.sum(mfc_setL) # number of changes in value for mfclo
    cal_L_cols = ['StartT','EndT','Isop','Isop_stddev','pid2_V','pid3_V','pid2_stddev','pid3_stddev'] # column titles for data frame
    cal_A_cols = ['StartT','EndT','Voltage','Voltage_stddev']
    
    cal_pts = [range(0,cal_N)] #(for index and things)
    delay = 300   #Delay at start of cal_L step
    cal_L_df = pd.DataFrame(index=cal_pts, columns=cal_L_cols) 
    cal_A_df = pd.DataFrame(index=[range(0,cal_N)],columns = cal_A_cols)
    
    
    mfc_setLS = []
    for i in range(0,len(mfc_setL)-1):
        if mfc_setL[i] == True:
            mfc_setLS.append(i)
    
    
    for i in range(0,len(mfc_setLS)-2):
        
        mfc_setLS[i] = mfc_setLS[i] + delay
     
    



        
    zero_time = 1 # how long the zero at the end will be


    mfc_setLF = dataL.index[mfc_setL]
    
    if mfc_setLF[-1]+zero_time < len(dataL):
        
    
        mfc_setLF = np.append(mfc_setLF,(mfc_setLF[len(mfc_setLF)-1]+zero_time))
        mfc_setLF = np.delete(mfc_setLF,0)
        mfc_setLF-=11#Delay at end of cal_L step
    else:
        print '\n\nERROR MESSAGE:'
        zero_time = int(raw_input('\n\nThe zero time at the end was a bit big, please lower it to ' + str(len(dataL)-mfc_setLF[-1] -1) + ' or below\n\nZero Time = '))
        mfc_setLF = np.append(mfc_setLF,(mfc_setLF[len(mfc_setLF)-1]+zero_time))
        mfc_setLF = np.delete(mfc_setLF,0)
        mfc_setLF-=11#Delay at end of cal_L step
    

    mfc_setAS = [5*i for i in mfc_setLS]
    
    

##############        General Adjustments to cal range      ###########

    stretch_left = 700
    stretch_right = 750
    
    end_cut_off = 1000
    translator = 1000
    
##############        Fine tuning of cal ranges            ###########    
    
    ## Cal Point 1 ##
    stretch_left_1 = 500
    stretch_right_1 = 35

    ## Cal Point 2 ##
    stretch_left_2 = -30
    stretch_right_2 = -300
    
    ## Cal Point 3 ##
    stretch_left_3 = -100
    stretch_right_3 = -1700
    
    ## Cal Point 4 ##
    stretch_left_4 = -5
    stretch_right_4 = 65
    
    ## Cal Point 5 ##
    stretch_left_5 = -400
    stretch_right_5 = -700
    
    ## Cal Point 6 ##
    stretch_left_6 = -1200
    stretch_right_6 = 70
    
    ## Cal Point 7 ##
    stretch_left_7 = -65
    stretch_right_7 = -35
    
    ## Cal Point 8 ##
    stretch_left_8 = -60
    stretch_right_8 = 40
    
    ## Cal Point 9 ##
    stretch_left_9 = -10
    stretch_right_9 = -30
    
    ## Cal Point 10 ##
    stretch_left_10 = 35
    stretch_right_10 = 25
    
    ## Cal Point 11 ##
    stretch_left_11 = -20
    stretch_right_11 = -25
    
    ## Cal Point 12 ##
    stretch_left_12 = -70
    stretch_right_12 = -30
    
    mfc_setAS = [i+stretch_left for i in mfc_setAS]
    
    mfc_setAS = [i+translator for i in mfc_setAS]
    if first_mutual_L>first_mutual_A:
        mfc_setAS = [i+index_difference for i in mfc_setAS]
    elif first_mutual_A>first_mutual_L:
        mfc_setAS = [i - index_difference for i in mfc_setAS]
        
        
        
    mfc_setAF = [5*i for i in mfc_setLF]
    mfc_setAF = [i+translator for i in mfc_setAF]
    mfc_setAF = [i+stretch_right for i in mfc_setAF]
    if mfc_setAF[-1]-end_cut_off > mfc_setAF[-2]:
        mfc_setAF[-1]=mfc_setAF[-1]-end_cut_off
    else:
        print 'The end cut off value is too large, it won\'t cut off anymore\n\nYou\'ll probably have to change cal point 10'

    
    if last_mutual_L>last_mutual_A:
        mfc_setAF = [i+index_difference for i in mfc_setAF]
    elif last_mutual_A>last_mutual_L:
        mfc_setAF = [i - index_difference for i in mfc_setAF]
        
        
    ######### FineTuning the cal points ###########
    mfc_setAS[0] = mfc_setAS[0] - stretch_left_1
    mfc_setAF[0] = mfc_setAF[0] + stretch_right_1
    
    mfc_setAS[1] = mfc_setAS[1] - stretch_left_2
    mfc_setAF[1] = mfc_setAF[1] + stretch_right_2
    
    mfc_setAS[2] = mfc_setAS[2] - stretch_left_3
    mfc_setAF[2] = mfc_setAF[2] + stretch_right_3
    
    mfc_setAS[3] = mfc_setAS[3] - stretch_left_4
    mfc_setAF[3] = mfc_setAF[3] + stretch_right_4
    
    mfc_setAS[4] = mfc_setAS[4] - stretch_left_5
    mfc_setAF[4] = mfc_setAF[4] + stretch_right_5
    
    mfc_setAS[5] = mfc_setAS[5] - stretch_left_6
    mfc_setAF[5] = mfc_setAF[5] + stretch_right_6
    
    mfc_setAS[6] = mfc_setAS[6] - stretch_left_7
    mfc_setAF[6] = mfc_setAF[6] + stretch_right_7
    
    mfc_setAS[7] = mfc_setAS[7] - stretch_left_8
    mfc_setAF[7] = mfc_setAF[7] + stretch_right_8
    
    mfc_setAS[8] = mfc_setAS[8] - stretch_left_9
    mfc_setAF[8] = mfc_setAF[8] + stretch_right_9
    
    mfc_setAS[9] = mfc_setAS[9] - stretch_left_10
    mfc_setAF[9] = mfc_setAF[9] + stretch_right_10
    
    mfc_setAS[10] = mfc_setAS[10] - stretch_left_11
    mfc_setAF[10] = mfc_setAF[10] +stretch_right_11
    
    mfc_setAS[11] = mfc_setAS[11] - stretch_left_12
    mfc_setAF[11] = mfc_setAF[11] + stretch_right_12
    

    
 
    ##################################################
    for pt in range(0,cal_N):
    #check that the flows are the same at the start and end of the range over which you are averaging
        if (np.logical_and(dataL.mfclo[mfc_setLS[pt]]==dataL.mfclo[mfc_setLF[pt]],dataL.mfchi[mfc_setLS[pt]]==dataL.mfchi[mfc_setLF[pt]])):
                
                #Labjack
                tpL_Isop = isop_mr[mfc_setLS[pt]:mfc_setLF[pt]] # Takes slices of the data everytime the value of mfclo changes
                tpL_pid2 = dataL.pid1[mfc_setLS[pt]:mfc_setLF[pt]]
                tpL_pid3 = dataL.pid2[mfc_setLS[pt]:mfc_setLF[pt]]
                tpL_lo = dataL.mfclo[mfc_setLS[pt]:mfc_setLF[pt]]
                
                cal_L_df.Isop[pt] = tpL_Isop.mean()
                cal_L_df.Isop_stddev[pt] = tpL_Isop.std()
                    
                
                cal_L_df.pid2_V[pt] = tpL_pid2.mean()
                cal_L_df.pid2_stddev[pt] = tpL_pid2.std()
        
                
                cal_L_df.pid3_V[pt] = tpL_pid3.mean()
                cal_L_df.pid3_stddev[pt] = tpL_pid3.std()
                
                
                cal_L_df.StartT[pt] = TimeL[mfc_setLS[pt]]
                cal_L_df.EndT[pt] = TimeL[mfc_setLF[pt]]
                
                cal_lengths.append(len(tpL_Isop))
                
                
                if avg_0 == 'Y':
            
                    pid2 = dataL.pid1
                    pid3 = dataL.pid2
                    lo = dataL.mfclo
            
                    pid2_zeros = []
                    pid3_zeros = []
            
                    for i in range (0,len(lo)):        
                        if lo[i] == 0:
                            pid2_zeros.append(pid2[i])
                            pid3_zeros.append(pid3[i])
            
                    mean_pid2 = np.nanmean(pid2_zeros)
                    mean_pid3 = np.nanmean(pid3_zeros)
                
                    if (np.any(tpL_lo)== 0):
                        cal_L_df.pid2_V[pt] = mean_pid2
                        cal_L_df.pid3_V[pt] = mean_pid3
                
                print '\nloading...\n'
                
                #Arduino
                tpA_Voltage = dataA.Voltage[mfc_setAS[pt]:mfc_setAF[pt]]

                cal_A_df.Voltage[pt] = tpA_Voltage.mean()
                cal_A_df.Voltage_stddev[pt] = tpA_Voltage.std()
                
                StartTime = timestamp_convert(dataA.Time[mfc_setAS[pt]])
                EndTime = timestamp_convert(dataA.Time[mfc_setAS[pt]])
                
                StartDate = '/'.join(timestamp_convert(dataA.Time[mfc_setAS[pt]])[:-4])
                StartTime = ':'.join(timestamp_convert(dataA.Time[mfc_setAS[pt]])[3:-1])
                    
                EndDate = '/'.join(timestamp_convert(dataA.Time[mfc_setAS[pt]])[:-4])
                EndTime = ':'.join(timestamp_convert(dataA.Time[mfc_setAS[pt]])[3:-1])
                                    
                cal_A_df.StartT[pt] = str(StartDate+''+StartTime)
                cal_A_df.EndT[pt] = str(EndDate+''+EndTime)

                    
                                        

################ Effectively finding the times isop = 0 and averaging (only for cal_A_df)
######

           
                                                                         
cal_L_df_repeated_voltage = [item for item, count in collections.Counter(cal_L_df['pid2_V']).items() if count > 1]
repeated_voltage_indexes =[]
for i in range(0,len(cal_L_df['pid2_V'])):
    if cal_L_df['pid2_V'][i] == cal_L_df_repeated_voltage[0]:
        repeated_voltage_indexes.append(i)
                    
voltagesA = []
for i in repeated_voltage_indexes:
    voltagesA.append(cal_A_df['Voltage'][i])
avg_voltageA = np.nanmean(voltagesA)
                          

for i in range(0,len(cal_A_df.Voltage)):
    if i in repeated_voltage_indexes:
        cal_A_df.Voltage[i] = avg_voltageA




##################################################################################################################################################################


    
voltage = list_multisplicer(dataA.Voltage,mfc_setAS,mfc_setAF)
times = list_multisplicer(TimeA,mfc_setAS,mfc_setAF)

fig00 = plt.figure()
ax00 = fig00.add_subplot(211)
ax00.plot(times,voltage)
ax00.set_ylim([np.mean(dataA.Voltage)-2.5E-4,np.mean(dataA.Voltage)+2.5E-4])
ax00.plot(TimeA,pd.rolling_mean(dataA.Voltage,300))

ax10 = fig00.add_subplot(212)
ax10.plot(TimeA,dataA.Voltage)
ax10.plot(TimeA,pd.rolling_mean(dataA.Voltage,300))
ax10.set_ylim([np.mean(dataA.Voltage)-2.5E-4,np.mean(dataA.Voltage)+2.5E-4])

plt.show()

voltageL = list_multisplicer(dataL.pid2,mfc_setLS,mfc_setLF)
timesL = list_multisplicer(dataL.TheTime,mfc_setLS,mfc_setLF)

fig01 = plt.figure()
ax01 = fig01.add_subplot(211)
ax01.plot(timesL,voltageL)
ax02 = fig01.add_subplot(212)
ax02.plot(dataL.TheTime,dataL.pid2)
ax02.plot(dataL.TheTime,pd.rolling_mean(dataL.pid2,300))
#ax02.set_ylim([np.mean(dataL.pid2)-2.5E-4,np.mean(dataL.pid2)+2.5E-4])
plt.show()



##################################################################################################################################################################

###################### Editing the dataframes to make them plottable 
##########



cal_L_df = cal_L_df.drop_duplicates(subset = ('pid2_V'))                                
cal_L_df = cal_L_df.dropna()                    
cal_L_df.index = np.arange(len(cal_L_df))

cal_A_df = cal_A_df.drop_duplicates(subset = ('Voltage'))
cal_A_df = cal_A_df.dropna()
cal_A_df.index = range(len(cal_A_df))

seen = set()
uniq = [x for x in cal_lengths if x not in seen and not seen.add(x) and x != 0] 


xerr = [cal_L_df.Isop_stddev[i]/np.sqrt(889) for i in range(len(cal_L_df))]

yerrL2 = [cal_L_df.pid2_stddev[i]/np.sqrt(889) for i in range(len(cal_L_df))]

yerrL3 = [cal_L_df.pid3_stddev[i]/np.sqrt(889) for i in range(len(cal_L_df))]

yerrA = [cal_A_df.Voltage_stddev[i]/np.sqrt(889) for i in range(len(cal_L_df))]




if (cal == 'Y'):
    
    cal_L_df.Isop = cal_L_df.Isop.astype(float) 
    cal_L_df.pid2_V = cal_L_df.pid2_V.astype(float)                
    cal_L_df.pid3_V = cal_L_df.pid3_V.astype(float)
    cal_A_df.Voltage = cal_A_df.Voltage.astype(float)
            
    ############# Fitting the data
    #######
    
    


    a = range(len(cal_L_df))
    
    ydata2 = cal_L_df.pid2_V        
    ydata3 = cal_L_df.pid3_V
    
    xdata = cal_L_df.Isop
    
    ydataA = cal_A_df.Voltage
            
    isop_fit = [0.,np.max(cal_L_df.Isop)]
                        
    ##### PID 2
    slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerrL2)
    pid2_fit = [slope_intercept2[0],(np.max(cal_L_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
    
    ##### PID 3
    slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerrL3)
    pid3_fit = [slope_intercept3[0],(np.max(cal_L_df.Isop)*slope_intercept3[1])+slope_intercept3[0]]
    
    ##### Arduino
    slope_interceptA,pcovA = opt.curve_fit(linear_fit, xdata,ydataA, sigma = yerrA)
    arduino_fit = [slope_interceptA[0],(np.max(cal_L_df.Isop)*slope_interceptA[1])+slope_interceptA[0]]
  	
    perr2 = np.sqrt(np.diag(pcov2))
    perr3 = np.sqrt(np.diag(pcov3))
    perrA = np.sqrt(np.diag(pcovA))
    
    Intercept_error2 = perr2[0]/np.sqrt(cal_N)
    Intercept_error3 = perr3[0]/np.sqrt(cal_N)
    Intercept_errorA = perrA[0]/np.sqrt(cal_N)
    
    Slope_Error2 = perr2[0]/np.sqrt(cal_N)
    Slope_Error3 = perr3[0]/np.sqrt(cal_N)
    Slope_ErrorA = perrA[0]/np.sqrt(cal_N)

    print slope_intercept2[0],'+-', Slope_Error2,' PID2'
    print slope_intercept3[0],'+-',Slope_Error3,' PID3'
    print slope_interceptA[0],'+-',Slope_ErrorA,' Arduino'
    
    
    ########## Arduino Cal Graph ####
    ####
    fig1 = plt.figure()

    plt.plot(isop_fit,arduino_fit)
    plt.errorbar(cal_L_df.Isop,cal_A_df.Voltage, xerr = xerr, yerr = yerrA, fmt='o')
    
    ####Making the graph prettier
    ##
    plt.ylabel('Pid 2 Voltage / V', fontsize = 13)
    plt.xlabel('Isoprene Concentration / ppb', fontsize = 13)
    plt.title('Arduino Cal')
    plt.show()

    ########### Pid 2 Cal Graph #####
    ####
    fig2 = plt.figure()
    plt.plot(isop_fit,pid2_fit)   
    plt.errorbar(cal_L_df.Isop,cal_L_df.pid2_V, xerr = xerr, yerr = yerrL2, fmt = 'o')
    plt.ylabel('Pid 2 Voltage / V', fontsize = 13)
    plt.xlabel('Isoprene Concentration / ppb', fontsize = 13)
    plt.title('Labjack Cal')
    
    fig3 = plt.figure()
    
    
    plt.show() 
    
#####################   Plotting
######	




if (plots == 'Y'):
    
    if pid_2_on == 'Y':
        pid2_avg = pd.rolling_mean(dataL.pid1,300)
        
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        
        pid2 = ax1.plot(L[tmp_pid2],dataL.pid1[tmp_pid2], linewidth=3,color='r')
        pid2_10s = ax1.plot(dataL.TheTime[tmp_pid2],pid2_avg[tmp_pid2], linewidth=3,color='b')
        Isop = ax1.plot(TimeL[tmp_flow],isop_mr[tmp_flow], linewidth=1,color='g')
        
        plt.ylabel("PID2 / V")
        ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
        isop = ax2.plot(L[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')
        
        
        ax2.plot([L[dataL.index[mfc_setLS]],L[dataL.index[mfc_setLS]]],[0.,2.],color='b',linestyle = '-')
        ax2.plot([L[dataL.index[mfc_setLF]],L[dataL.index[mfc_setLF]]],[0.,2.],color='g',linestyle = '-')
        
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 2, Raw Data')
        
        fig3 = plt.figure()
        plt.errorbar(cal_L_df.Isop,cal_L_df.pid2_V, xerr = xerr, yerr = yerrL2, fmt='o')
        plt.plot(isop_fit,pid2_fit)
        plt.ylabel('Pid 2 Voltage / V', fontsize = 13)
        plt.xlabel('Isoprene Concentration / ppb', fontsize = 13)
        plt.title('Pid 2, Cal plot')
    
    
    ###########################
    ######## Pid 3 plot
    
    if pid_3_on == 'Y':
        
        pid3_avg = pd.rolling_mean(dataL.pid2,300)
        
        fig1 = plt.figure()
        
        ax1 = fig1.add_subplot(111)
        
        pid3 = ax1.plot(TimeL[tmp_pid3],dataL.pid2[tmp_pid3], linewidth=3,color='r')
        pid3_10s = ax1.plot(TimeL[tmp_pid3],pid3_avg[tmp_pid3], linewidth=3,color='b')
        
        
        plt.ylabel("PID / V")
        
        ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
        
        isop = ax2.plot(TimeL[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')
        
        
        ax2.plot([TimeL[dataL.index[mfc_setLS]],TimeL[dataL.index[mfc_setLS]]],[0.,2.],color='b',linestyle = '-')
        ax2.plot([TimeL[dataL.index[mfc_setLF]],TimeL[dataL.index[mfc_setLF]]],[0.,2.],color='g',linestyle = '-')
        
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 3, Raw Data')
        
        fig3 = plt.figure()
        plt.errorbar(cal_L_df.Isop,cal_L_df.pid3_V, xerrL = xerr, yerrL = yerrL3, fmt='o')
        #plt.plot(isop_fit,pid3_fit)
        plt.ylabel('Pid 3 / V', fontsize = 20)
        plt.xlabel('[Isop] / ppb', fontsize = 20)
        plt.title('Pid 3, cal_L plot')	
    
    plt.show()

#if cal == 'Y':
    
#    perr2 = np.sqrt(np.diag(pcov2))
#    perr3 = np.sqrt(np.diag(pcov3))
    
#    Intercept_error2 = perr2[0]/np.sqrt(cal_N)
#    Intercept_error3 = perr3[0]/np.sqrt(cal_N)
    
#    Slope_Error2 = perr2[0]/np.sqrt(cal_N)
#    Slope_Error3 = perr3[0]/np.sqrt(cal_N)
    
#    data = {'Slopes':[slope_intercept2[1],slope_intercept3[1]], 'Slope Error':[Slope_Error2,Slope_Error3],'Intercepts':[slope_intercept2[0], slope_intercept3[0]],'Intercept Error':[Intercept_error2,Intercept_error3]}  
#    frame = pd.DataFrame(data,index=['PID2','PID3'])
#    print frame

   
    
###############################################
############# Histogram Plotting

if hist == 'Y':
    
    pathH = 'E:\Bursary thing\cal_L Stuff'

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

    data = {'How many cal_Ls':[len(H1), len(H2)], 'Mean':[np.mean(H1),np.mean(H2)], 'Standard Deviation':[np.std(H1),np.std(H2)]}
    hist_frame = pd.DataFrame(data,index=['PID2','PID3'])
    print hist_frame