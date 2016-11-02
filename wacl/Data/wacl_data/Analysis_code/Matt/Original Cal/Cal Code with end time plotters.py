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
from time import strftime

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


pid3_correction = 1.11E-5
pid4_correction = 1.36E-5
pid5_correction = 2.97E-5


pd.set_option('precision',9)

cal_stuff = 'Y'
arduino = ''

data_point_length = 300 # how many data points used for the cals



pid_2_on = ''

pid_3_on = 'Y'

pid_4_on = 'Y'

pid_5_on = 'Y'


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
yerr5 = []

npid2 = []
npid3 = []
npid4 = []
npid5 = []
nISop = []




#############################
## User Interface
if questions == 'Y':
    date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
    try:
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
        filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
        dataL = pd.read_csv(pathL+filenameL)
        
    except IOError:
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
        dataL = pd.read_csv(pathL+filenameL)
else:
    pathL = ''
    filenameL = ''
    
    
  
if int(date) < 904:
        pid_5_on = ''
if int(date)>=904:
    pid_2_on = ''       
        
########################################
######Data Read  
print 'Reading Data...'
dataL = pd.read_csv(pathL+filenameL)
print 'Analysing and Adjusting...'

##   Sorting out the Times   ##
TimeL = dataL.TheTime-dataL.TheTime[0]
TimeL*=60.*60.*24.

dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
dataL.TheTime+=offset

#### Relative Humidity ###

if int(date) >= 903:
    RH = dataL.RH
    RH /=4.9
    RH -= 0.16
    RH /= 0.0062
    RH *= 100
    RH /= 103


##  Sorting data and correcting for humidity  ##
if int(date) < 904:
    if pid_2_on == 'Y':
        pid2d = dataL.pid1.fillna(pd.rolling_mean(dataL.pid1, 7, min_periods=1).shift(-3))
        
    if pid_3_on == 'Y':    
        pid3d = dataL.pid2.fillna(pd.rolling_mean(dataL.pid2, 7, min_periods=1).shift(-3))
        pid3dc = pid3d - RH*pid3_correction
        
    if pid_4_on == 'Y':    
        pid4d = dataL.pid3.fillna(pd.rolling_mean(dataL.pid3, 7, min_periods=1).shift(-3))
        pid4dc = pid4d - RH*pid4_correction
        
if int(date) >= 904:
    if pid_5_on == 'Y':
        pid5d = dataL.pid5.fillna(pd.rolling_mean(dataL.pid5, 7, min_periods=1).shift(-3))
        pid5dc = pid5d - RH*pid5_correction
        
    if pid_3_on == 'Y':    
        pid3d = dataL.pid3.fillna(pd.rolling_mean(dataL.pid3, 7, min_periods=1).shift(-3))
        pid3dc = pid3d - RH*pid3_correction
        
    if pid_4_on == 'Y':    
        pid4d = dataL.pid4.fillna(pd.rolling_mean(dataL.pid4, 7, min_periods=1).shift(-3))
        pid4dc = pid4d - RH*pid4_correction


if pid_2_on == 'Y':
    tmp_pid2 = pid2d.notnull()

if pid_3_on == 'Y':
    tmp_pid3 = pid3dc.notnull()

    
if pid_4_on == 'Y':
    tmp_pid4 = pid4dc.notnull()

if pid_5_on == 'Y':
    tmp_pid5 = pid5d.notnull()


    
    
    
tmp_flow = dataL.mfchiR.notnull()
    
isop_cyl = 13.277	#ppbv
mfchi_range = 100.	#sccm
mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)

mfclo_range = 20.	#sccm
mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)

dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = dil_fac*isop_cyl





    
##########################


if pid_2_on == 'Y':
    mean_pid2 = np.nanmean(pid2d)
    translator_pid2  = mean_pid2
    scal_fac_pid2 =  6E-5
    isop_mr_raw_plot_pid2 = (isop_mr*scal_fac_pid2)+translator_pid2
if pid_3_on == 'Y':
    mean_pid3 = np.nanmean(pid3dc)
    translator_pid3  = mean_pid3
    scal_fac_pid3 = 1.2E-4
    isop_mr_raw_plot_pid3 = (isop_mr*scal_fac_pid3)+translator_pid3
if pid_4_on == 'Y':
    mean_pid4 = np.nanmean(pid4dc)
    scal_fac_pid4 =  1E-4
    translator_pid4  = mean_pid4+0.001*mean_pid4
    isop_mr_raw_plot_pid4 = (isop_mr*scal_fac_pid4)+translator_pid4
if pid_5_on == 'Y':
    mean_pid5 = np.nanmean(pid5d)
    translator_pid5  = mean_pid5
    scal_fac_pid5 =  6E-5
    isop_mr_raw_plot_pid5 = (isop_mr*scal_fac_pid5)+translator_pid5




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
    
    
    
    
    
    end_cut_off = 10
    


    
    mfc_setF = dataL.index[mfc_set]
    
    mfc_setF = mfc_setF[1:]
    mfc_setF -= end_cut_off #taking some data points away from the end to give a bit of a tolerance
    
    
    mfc_setS = [i-data_point_length for i in mfc_setF]    

            
    S = mfc_setS
    F = mfc_setF
  
    print 'Splicing the Data...'
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
        pid2_chunks = list_multisplicer_listsout(pid2d,mfc_setS,mfc_setF)
    
        pid2_avgs = [np.nanmean(i) for i in pid2_chunks]
        pid2_stds = [np.nanstd(i) for i in pid2_chunks]
        
        cal_df['Pid2 Voltage'] = pid2_avgs
        cal_df['Pid2 Stddev'] = pid2_stds
        
    if pid_3_on == 'Y':
        
        pid3_chunks = list_multisplicer_listsout(pid3dc,mfc_setS,mfc_setF)
        
        pid3_avgs = [np.nanmean(i) for i in pid3_chunks]
        pid3_stds = [np.nanstd(i) for i in pid3_chunks]
        
        cal_df['Pid3 Voltage'] = pid3_avgs
        cal_df['Pid3 Stddev']= pid3_stds 
           
    if pid_4_on =='Y':
        pid4_chunks = list_multisplicer_listsout(pid4dc,mfc_setS,mfc_setF)
        
        pid4_avgs = [np.nanmean(i) for i in pid4_chunks]
        pid4_stds = [np.nanstd(i) for i in pid4_chunks] 
    
        cal_df['Pid4 Voltage'] = pid4_avgs
        cal_df['Pid4 Stddev'] = pid4_stds
        
    if pid_5_on =='Y':
        pid5_chunks = list_multisplicer_listsout(pid5dc,mfc_setS,mfc_setF)
        
        pid5_avgs = [np.nanmean(i) for i in pid5_chunks]
        pid5_stds = [np.nanstd(i) for i in pid5_chunks] 
    
        cal_df['Pid5 Voltage'] = pid5_avgs
        cal_df['Pid5 Stddev'] = pid5_stds
        
        
    isop_chunks = list_multisplicer_listsout(isop_mr,mfc_setS,mfc_setF)
    
    isop_avgs = [np.nanmean(i) for i in isop_chunks]
    isop_stds = [np.nanstd(i) for i in isop_chunks]
    
    
    start_times = [TimeL[i] for i in mfc_setS]
    end_times = [TimeL[i] for i in mfc_setF]
    


    cal_df['Isop'] = isop_avgs
    cal_df['Isop Stddev'] = isop_stds
    cal_df['Start Times'] = start_times
    cal_df['End Times'] = end_times
    
    cal_df_orig = cal_df # Saving an unaltered cal_df

    
    cal_df = cal_df.dropna()
    cal_df.index = range(0,len(cal_df))


    print 'Averaging the Zeros...'
    ########################## Zero Averaging #########################
    
    
    isop_zero_indexes = []
    for i in range(0,len(cal_df.Isop)):
        if cal_df.Isop[i] < 0.2:
            isop_zero_indexes.append(i)

    
    
    if pid_2_on:
        cal_df['Pid2 Voltage'][isop_zero_indexes] = np.nanmean(cal_df['Pid2 Voltage'][isop_zero_indexes])

    if pid_3_on:
        cal_df['Pid3 Voltage'][isop_zero_indexes] = np.nanmean(cal_df['Pid3 Voltage'][isop_zero_indexes])

    if pid_4_on:
        cal_df['Pid4 Voltage'][isop_zero_indexes] = np.nanmean(cal_df['Pid4 Voltage'][isop_zero_indexes])

    if pid_5_on:
        cal_df['Pid5 Voltage'][isop_zero_indexes] = np.nanmean(cal_df['Pid5 Voltage'][isop_zero_indexes])

    
    
    if pid_2_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid2 Voltage')
    elif pid_3_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid3 Voltage')
    elif pid_4_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid4 Voltage')
    elif pid_5_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid5 Voltage')



    cal_df.index = range(0,len(cal_df))

    ########################## Improving Cal ########################## 
    
    
    dodgy_indexes_pid3 = []
    m3 = np.nanmean(cal_df['Pid3 Stddev'])
    s3 = np.nanstd(cal_df['Pid3 Stddev'])
    for i in range(0,len(cal_df['Pid3 Stddev'])):
        if cal_df['Pid3 Stddev'][i] > s3+m3 or cal_df['Pid3 Stddev'][i] < m3-s3:
            dodgy_indexes_pid3.append(i)

        
    
    
    ########################## ########################## ########################## 
    print 'Just Tidying Up and Fitting the Data...'
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
        
    if pid_5_on: 
        cal_df = cal_df.drop_duplicates(subset = ['Pid5 Voltage'])
        cal_df.index = range(0,len(cal_df))
        for i in range(len(cal_df)):
            yerr5.append(cal_df['Pid5 Stddev'][i]/np.sqrt(len(pid5_chunks[i+1])))
            
        xdata = cal_df.Isop
        ydata5 = cal_df['Pid5 Voltage']
        slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr5)
        pid5_fit = [slope_intercept5[0],(np.max(cal_df.Isop)*slope_intercept5[1])+slope_intercept5[0]]
        
        perr5 = np.sqrt(np.diag(pcov5))    
        Intercept_error5 = perr5[0]/np.sqrt(cal_N)
        Slope_Error5 = perr5[0]/np.sqrt(cal_N)

    
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








print 'Plotting the Ammended Data...'

##########################################    Plotting   ##########################################  
if plots == 'Y':
    
    date = timestamp_convert(dataL.TheTime[0])[1:3]
    date = '/'.join(date)
    
    filenumber = filenameL[-2:]
    
    times = list_multisplicer(dataL.TheTime,mfc_setS,mfc_setF)
    
    
    

    if pid_2_on == 'Y':
        ########################################### PID 2 ###########################################
        voltage_pid2 = list_multisplicer(pid2d,mfc_setS,mfc_setF)
        isop_chunks_data_pid2 = list_multisplicer(isop_mr_raw_plot_pid2,mfc_setS,mfc_setF)
        
        
        
        
        fig2r = plt.figure()
        ###### Raw Data #######
        
        ax2r2a = fig2r.add_subplot(212)
        ax2r2b = ax2r2a.twinx()
        pid2_raw_data = ax2r2a.plot(dataL.TheTime[tmp_pid2],pid2d[tmp_pid2], linewidth=1,color='r')
        pid2_Isop = ax2r2b.plot(dataL.TheTime[tmp_flow],isop_mr_raw_plot_pid2[tmp_flow], linewidth=1,color='g')
        #pid2_rolling_avg = ax2r2.plot(dataL.TheTime,pd.rolling_mean(pid2d,300))
        # Making graph pretty #
        ax2r2a.set_ylabel("Pid Voltage / V")
        ax2r2b.set_ylabel('Isop / ppb')
        plt.xlabel('Time / s', fontsize = 20)
        
        #xy_coords = pyl.ginput(n=12)
        
        
        
        ####### Spliced graph #######
        
        ax2r1a = fig2r.add_subplot(211)
        ax2r1b = ax2r1a.twinx()
        spliced_graph_pid2 = ax2r1a.plot(times,voltage_pid2, linewidth=1,color= 'b')
        #spliced_graph_pid2_limits = ax2r1.set_ylim([mean_pid2+3E-4,mean_pid2-3E-4])
        #spliced_graph_pid2_limits = ax2r1.set_ylim([mean_pid2-2.5E-4,mean_pid2+2.5E-4])
        spliced_graph_rolling_avg = ax2r1a.plot(dataL.TheTime,pd.rolling_mean(pid2d,300,30), linewidth=1,color= 'r')
        isop_data_pid2 = ax2r1b.plot(times,isop_chunks_data_pid2,linewidth = 1,color='k')
        
        # Making graph pretty 
        ax2r2a.set_ylabel("Pid Voltage / V")
        ax2r2b.set_ylabel('Isop / ppb')
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
        voltage_pid3 = list_multisplicer(pid3dc,mfc_setS,mfc_setF)
        isop_chunks_data_pid3 = list_multisplicer(isop_mr_raw_plot_pid3,mfc_setS,mfc_setF)
        

        pid3_rolling_avg = pd.rolling_mean(pid3dc,300,60)
        
        fig3r = plt.figure()
        ax3r1 = fig3r.add_subplot(211)
        spliced_graph_pid3 = ax3r1.plot(times,voltage_pid3, linewidth=1,color= 'b')
        #spliced_graph_pid3_limits = ax3r1.set_ylim([mean_pid3-3E-4,mean_pid3+3E-4])
        spliced_graph_rolling_avg = ax3r1.plot(dataL.TheTime,pid3_rolling_avg, linewidth=1, color = 'r')
        isop_data_pid3 = ax3r1.plot(times,isop_chunks_data_pid3,linewidth = 1,color='k')
        
        # Making the Graph Pretty#
        plt.ylabel("Isop / ppb")
        plt.xlabel('Time / s', fontsize = 20)
        plt.title('Pid 3, Raw Data ('+date+') - '+filenumber)
        
        ###### Raw Data #######
        
        ax3r2 = fig3r.add_subplot(212)
        pid3_raw_data = ax3r2.plot(dataL.TheTime[tmp_pid3],pid3dc[tmp_pid3], linewidth=1,color='b')
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
            voltage_pid4 = list_multisplicer(pid4dc,mfc_setS,mfc_setF)
            isop_chunks_data_pid4 = list_multisplicer(isop_mr_raw_plot_pid4,mfc_setS,mfc_setF)
            

            pid4_rolling_avg = pd.rolling_mean(pid4dc,300,60)
            
            fig4r = plt.figure()
            ax4r1 = fig4r.add_subplot(211)
            spliced_graph_pid4 = ax4r1.plot(times,voltage_pid4, linewidth=1,color= 'b')
            #spliced_graph_pid4_limits = ax4r1.set_ylim([mean_pid4-3E-4,mean_pid4+3E-4])
            spliced_graph_rolling_avg = ax4r1.plot(dataL.TheTime,pid4_rolling_avg, linewidth=1, color = 'r')
            isop_data_pid4 = ax4r1.plot(times,isop_chunks_data_pid4,linewidth = 1,color='k')
            
            # Making the Graph Pretty#
            plt.ylabel("Isop / ppb")
            plt.xlabel('Time / s', fontsize = 20)
            plt.title('Pid 4, Raw Data ('+date+') - '+filenumber)
            
            ###### Raw Data #######
            
            ax4r2 = fig4r.add_subplot(212)
            #sf = (np.nanmean(RH)/mean_pid4)

            #RH_plot_pid4 = ax4r2.plot(dataL.TheTime,(RH/sf)*0.8+0.01)
            pid4_raw_data = ax4r2.plot(dataL.TheTime[tmp_pid4],pid4d[tmp_pid4], linewidth=1,color='b')

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

    if pid_5_on == 'Y':
            ########################################### PID 4 ###########################################
            voltage_pid5 = list_multisplicer(pid5dc,mfc_setS,mfc_setF)
            isop_chunks_data_pid5 = list_multisplicer(isop_mr_raw_plot_pid5,mfc_setS,mfc_setF)
            

            pid5_rolling_avg = pd.rolling_mean(pid5dc,300,60)
            
            fig5r = plt.figure()
            ax5r1 = fig5r.add_subplot(211)
            spliced_graph_pid5 = ax5r1.plot(times,voltage_pid5, linewidth=1,color= 'b')
            #spliced_graph_pid5_limits = ax5r1.set_ylim([mean_pid5-3E-5,mean_pid5+3E-5])
            spliced_graph_rolling_avg = ax5r1.plot(dataL.TheTime,pid5_rolling_avg, linewidth=1, color = 'r')
            isop_data_pid5 = ax5r1.plot(times,isop_chunks_data_pid5,linewidth = 1,color='k')
            
            # Making the Graph Pretty#
            plt.ylabel("Isop / ppb")
            plt.xlabel('Time / s', fontsize = 20)
            plt.title('Pid 5, Raw Data ('+date+') - '+filenumber)
            
            ###### Raw Data #######
            
            ax5r2 = fig5r.add_subplot(212)
            #sf = (np.nanmean(RH)/mean_pid5)

            #RH_plot_pid5 = ax5r2.plot(dataL.TheTime,(RH/sf)*0.8+0.01)
            pid5_raw_data = ax5r2.plot(dataL.TheTime[tmp_pid5],pid5d[tmp_pid5], linewidth=1,color='b')
            pid5_corrected_for_humid = ax5r2.plot(dataL.TheTime[tmp_pid5],pid5dc[tmp_pid5],linewidth=1,color = 'k')
            pid5_Isop = ax5r2.plot(dataL.TheTime[tmp_flow],isop_mr_raw_plot_pid5[tmp_flow], linewidth=1,color='g')
            #pid5_rolling_avg_raw_plot = ax5r2.plot(dataL.TheTime,pid5_rolling_avg, linewidth=1,color = 'r')
            
            # Making graph pretty #
            plt.ylabel("Isop / ppb")
            plt.xlabel('Time / s', fontsize = 20)
            
            
            ###########################################
            
            
            ###### Cal Plot ######
            
            fig5c = plt.figure()
            ax5c1 = fig5c.add_subplot(111)
            #pid5_filtered_zero_point = ax5c1.errorbar(0,isop_zeros_avg_filtered_pid5,xerr = xerrunfil,fmt='x')
            pid5_cal_points = ax5c1.errorbar(cal_df.Isop,cal_df['Pid5 Voltage'], xerr = xerr, yerr = yerr5, fmt='o')
            pid5_cal_fit = ax5c1.plot(isop_fit,pid5_fit)
            
            # Adding a legend #
            slope_patch_pid5 = mpatches.Patch(label='Slope = '+str("%.2e" % slope_intercept5[1])+'+/-'+str("%.1e" % Slope_Error5))
            intecept_patch_pid5 = mpatches.Patch(label = 'Intercept = '+str("%.2e" % slope_intercept5[0])+'+/-'+str("%.1e" % Intercept_error5))
            plt.legend(handles=[slope_patch_pid5,intecept_patch_pid5],loc=2)
            
            # Making graph pretty #
            plt.ylabel('Pid 5 Voltage / V', fontsize = 15)
            plt.xlabel('Isoprene Concentration / ppb', fontsize = 15)
            plt.title('Pid 5, Cal plot ('+date+') - '+filenumber)
###########################################


print '\nShowing Graph...'
plt.show()    


        


   
    
###############################################
############# Histogram Plotting

if hist == 'Y':
    print 'Creating Histograms...'
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
