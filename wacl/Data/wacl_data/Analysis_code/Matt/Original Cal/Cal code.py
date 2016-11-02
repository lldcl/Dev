import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from scipy import stats
import scipy.optimize as opt
import time
#from Tkinter import *
import datetime
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

#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept

############################################################################################################################################################


pd.set_option('precision',9)

cal_stuff = 'Y'
arduino = ''

pid_2_on = ''

pid_3_on = 'Y'

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



xerr = []
yerr3 = []
yerr2 = []

npid2 = []
npid3 = []
nISop = []

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
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\201507\\'
    filename1 = 'd20150710_014'
        
        
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
    cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid2_V','pid3_V','pid2_stddev','pid3_stddev'] # column titles for data frame
    
    
    cal_pts = [range(0,cal_N)] #(for index and things)
    delay = 400   #Delay at start of cal step
    cal_df = pd.DataFrame(index=cal_pts, columns=cal_cols) 
    
    
    mfc_setS = []
    for i in range(0,len(mfc_set)-1):
        if mfc_set[i] == True:
            mfc_setS.append(i)
    
    
    for i in range(0,len(mfc_setS)-2):
        
        mfc_setS[i] = mfc_setS[i] + delay
    

    #try:
    
    zero_time = 1200 # how long the zero at the end will be


    mfc_setF = dataL.index[mfc_set]
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
        
    
    
    
    for pt in range(0,cal_N):
    #check that the flows are the same at the start and end of the range over which you are averaging
        if (np.logical_and(dataL.mfclo[mfc_setS[pt]]==dataL.mfclo[mfc_setF[pt]],dataL.mfchi[mfc_setS[pt]]==dataL.mfchi[mfc_setF[pt]])):
            
                tp_Isop = isop_mr[mfc_setS[pt]:mfc_setF[pt]] # Takes slices of the data everytime the value of mfclo changes
                tp_pid2 = dataL.pid1[mfc_setS[pt]:mfc_setF[pt]]
                tp_pid3 = dataL.pid2[mfc_setS[pt]:mfc_setF[pt]]
                tp_lo = dataL.mfclo[mfc_setS[pt]:mfc_setF[pt]]

                
                
                cal_df.Isop[pt] = tp_Isop.mean()
                cal_df.Isop_stddev[pt] = tp_Isop.std()
                    
                
                cal_df.pid2_V[pt] = tp_pid2.mean()
                cal_df.pid2_stddev[pt] = tp_pid2.std()
        
                
                cal_df.pid3_V[pt] = tp_pid3.mean()
                cal_df.pid3_stddev[pt] = tp_pid3.std()
                
                
                cal_df.StartT[pt] = TimeL[mfc_setS[pt]]
                cal_df.EndT[pt] = TimeL[mfc_setF[pt]]
                
                
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
                
                    if (np.any(tp_lo)== 0):
                        cal_df.pid2_V[pt] = mean_pid2
                        cal_df.pid3_V[pt] = mean_pid3

    #except (KeyError,IndexError):
    #           pass
    
    cal_df = cal_df.drop_duplicates(subset = 'pid2_V')                              
    cal_df = cal_df.dropna()                    
    cal_df.index = np.arange(len(cal_df))

    for i in range(len(cal_df)):
        xerr.append(cal_df.Isop_stddev[i]/np.sqrt(889))
            
    for i in range(len(cal_df)):
        yerr2.append(cal_df.pid2_stddev[i]/np.sqrt(889))

    for i in range(len(cal_df)):
        yerr3.append(cal_df.pid3_stddev[i]/np.sqrt(889))






if (cal == 'Y'):
    
    cal_df.Isop = cal_df.Isop.astype(float) 
    cal_df.pid2_V = cal_df.pid2_V.astype(float)                
    cal_df.pid3_V = cal_df.pid3_V.astype(float)
            
    ############# Fitting the data
    #######
    
    


    
    ydata2 = cal_df.pid2_V        
    ydata3 = cal_df.pid3_V
    
    xdata = cal_df.Isop

            
    isop_fit = [0.,np.max(cal_df.Isop)]
                        
    ##### PID 2
    slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr2)
    pid2_fit = [slope_intercept2[0],(np.max(cal_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
    
    ##### PID 3
    slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr3)
    pid3_fit = [slope_intercept3[0],(np.max(cal_df.Isop)*slope_intercept3[1])+slope_intercept3[0]]
   	






#####################   Plotting
######	




if (plots == 'Y'):
    
    if pid_2_on == 'Y':
        pid2_avg = pd.rolling_mean(dataL.pid1,300)
        
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        
        pid2 = ax1.plot(TimeL[tmp_pid2],dataL.pid1[tmp_pid2], linewidth=3,color='r')
        pid2_10s = ax1.plot(TimeL[tmp_pid2],pid2_avg[tmp_pid2], linewidth=3,color='b')
        
        plt.ylabel("PID2 / V")
        ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
        isop = ax2.plot(TimeL[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')
        
        
        ax2.plot([TimeL[dataL.index[mfc_setS]],TimeL[dataL.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
        ax2.plot([TimeL[dataL.index[mfc_setF]],TimeL[dataL.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')
        
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 2, Raw Data')
        
        fig3 = plt.figure()
        plt.errorbar(cal_df.Isop,cal_df.pid2_V, xerr = xerr, yerr = yerr2, fmt='o')
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
        
        
        ax2.plot([TimeL[dataL.index[mfc_setS]],TimeL[dataL.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
        ax2.plot([TimeL[dataL.index[mfc_setF]],TimeL[dataL.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')
        
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 3, Raw Data')
        
        fig3 = plt.figure()
        plt.errorbar(cal_df.Isop,cal_df.pid3_V, xerr = xerr, yerr = yerr3, fmt='o')
        plt.plot(isop_fit,pid3_fit)
        plt.ylabel('Pid 3 / V', fontsize = 20)
        plt.xlabel('Isoprene Concentration / ppb', fontsize = 20)
        plt.title('Pid 3, Cal plot')	
    
    plt.show()

if cal == 'Y':
    
    perr2 = np.sqrt(np.diag(pcov2))
    perr3 = np.sqrt(np.diag(pcov3))
    
    Intercept_error2 = perr2[0]/np.sqrt(cal_N)
    Intercept_error3 = perr3[0]/np.sqrt(cal_N)
    
    Slope_Error2 = perr2[0]/np.sqrt(cal_N)
    Slope_Error3 = perr3[0]/np.sqrt(cal_N)
    
    data = {'Slopes':[slope_intercept2[1],slope_intercept3[1]], 'Slope Error':[Slope_Error2,Slope_Error3],'Intercepts':[slope_intercept2[0], slope_intercept3[0]],'Intercept Error':[Intercept_error2,Intercept_error3]}  
    frame = pd.DataFrame(data,index=['PID2','PID3'])
    print frame
        


   
    
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
