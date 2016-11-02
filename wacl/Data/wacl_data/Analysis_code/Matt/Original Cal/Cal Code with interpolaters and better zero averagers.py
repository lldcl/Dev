import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.optimize as opt
import datetime
from time import strftime

##################################################### Defining Functions For Use Later #################################################

def plotter(pidxd,pidxdc):
    
    pid_number = int(pidxd[len(pidxd)])
    
    pidxd = pidxd[:len(pidxd)-1]
                    
    voltage_pid = list_multisplicer(pidxd,S,F)
            
    isop_chunks_data_pid = list_multisplicer(isop_mr,S,F)
    

    pid_rolling_avg = pd.rolling_mean(pidxd,300,60)
    
    figr = plt.figure()
    
    axr1a = figr.add_subplot(311)
    axr1b = axr1a.twinx()
    
    
    spliced_graph_pid = axr1a.plot(times,voltage_pid, linewidth=1,color= 'r')
    spliced_graph_rolling_avg = axr1a.plot(dataL.TheTime,pid_rolling_avg, linewidth=1, color = 'r')
    
    isop_data_pid = axr1b.plot(times,isop_chunks_data_pid,linewidth = 1,color='k')
    axr1a.set_ylabel('Pid'+str(pid_number)+' Voltage / V')
    axr1b.set_ylabel('Isop / ppb')
    plt.xlabel('Time / s', fontsize = 20)
    
    
    if humid_correct == 'Y':
        voltage_pidc = list_multisplicer(pidxdc,S,F)
        pidc_rolling_avg = pd.rolling_mean(pidxdc,300,60)
        
        axr2a = figr.add_subplot(312)
        axr2b = axr2a.twinx()

        
        spliced_graph_pid3_corrected = axr2a.plot(times,voltage_pidc, linewidth=1,color= 'b')
        spliced_graph_rolling_avg = axr2a.plot(dataL.TheTime[0:len(pd.rolling_mean(pid3dc,300,60))],pidc_rolling_avg[0:len(dataL.TheTime)], linewidth=1, color = 'b')
        
        isop_data_pid3 = axr2b.plot(times,isop_chunks_data_pid,linewidth = 1,color='k')

        axr2a.set_ylabel('Pid'+str(pid_number)+' Voltage / V')
        axr2b.set_ylabel('Isop / ppb')
        plt.xlabel('Time / s', fontsize = 20)
        
    
    ###### Raw Data #######
    
    axr3a = figr.add_subplot(313)
    axr3b = axr3a.twinx()
    pid_raw_data = axr3a.plot(dataL.TheTime,pidxd, linewidth=1,color='b')
    pid_Isop = axr3b.plot(dataL.TheTime,isop_mr, linewidth=1,color='g')
            
    # Making graph pretty #
    axr3a.set_ylabel('Pid'+str(pid_number)+' Voltage / V')
    axr3b.set_ylabel('Isop / ppb')
    plt.xlabel('Time / s', fontsize = 20)
    
    
    ###########################################
    

    ###### Cal Plot ######
    
    figc = plt.figure()
    axc1a = figc.add_subplot(111)
    axc1b = axc1a.twinx()
    axr1a.set_ylabel('Pid Voltage / V')
    plt.xlabel('Isop / ppb')
    
    pid_cal_points = axc1a.errorbar(cal_df.Isop,cal_df['Pid'+str(pid_number)+' Voltage'], xerr = xerr, yerr = yerr[pid_number], fmt='bo')
    pid_cal_fit = axc1a.plot(isop_fit,pid_fits[pid_number],color = 'b')
    
    if humid_correct == 'Y':
        axc1b.errorbar(cal_df.Isop,cal_dfc['Pid'+str(pid_number)+' Voltage c'], xerr = xerr, yerr = yerr[pid_number], fmt='mx')
        pid_cal_fit_corrected = axc1b.plot(isop_fit, pidc_fits[pid_number],color = 'm')
        axc1b.set_ylabel('Pid Voltage / V')

    # Adding a legend #
    slope_patch_pid = mpatches.Patch(label='Slope = '+str("%.2e" % Values['Slope'][int(pid_number)])+'+/-'+str("%.1e" % Values['Slope Error'][int(pid_number)]),color = 'b')
    intecept_patch_pid = mpatches.Patch(label = 'Intercept = '+str("%.2e" % Values['Intercept'][int(pid_number)])+'+/-'+str("%.1e" % Values['Intercept'][int(pid_number)]),color = 'b')
    if humid_correct == 'Y':
        slope_patch_pid_corrected = mpatches.Patch(label = 'Slopec = '+str("%.2e" % Corrected_Values['Slope'][int(pid_number)])+'+/-'+str("%.1e" % Corrected_Values['Slope Error'][int(pid_number)]),color = 'm')
        intecept_patch_pid_corrected = mpatches.Patch(label = 'Interceptc = '+str("%.2e" % Corrected_Values['Intercept'][int(pid_number)])+'+/-'+str("%.1e" % Corrected_Values['Intercept Error'][int(pid_number)]),color = 'm')
    plt.legend(handles=[slope_patch_pid,intecept_patch_pid,slope_patch_pid_corrected,intecept_patch_pid_corrected],loc='best')
    
    # Making graph pretty #
    plt.ylabel('Pid'+str(pid_number)+' Voltage / V')
    plt.xlabel('Isoprene Concentration / ppb')
    plt.title('Pid'+str(pid_number)+' , Cal plot ('+date+') - '+filenumber)
    plt.show()
            
            
            
            
###### Removes the negative values if they appear at the begining of the selection indexes (mfc_setS and mfc_setF)
def negative_remover(list1,list2):
    negative_removerF = []
    negative_removerS = []

    
    if list1[0] < 0:
        for i in range(0,len(list1)):
            if list2[i]<0:
                negative_removerF.append(i)
            if list1[i] < 0:
                negative_removerS.append(i)
        
        if negative_removerF < negative_removerS:
            negative_removerF = max(negative_removerS)
            negative_removerS = max(negative_removerS)+1         
        
        A = [0] + list1[negative_removerS:]
        B = list2[negative_removerF:]
        return A,B




# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))
    
    
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
            non_blank = []
            for i in new_lt:
                   if i != []:
                       non_blank.append(i)     
            return non_blank

             
                   
#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept


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


pid3_correction = 2.59E-05
pid4_correction = 1.36E-5
pid5_correction = 3.03E-5


pd.set_option('precision',9)

cal_stuff = 'Y'
arduino = ''

data_point_length = 300 # how many data points used for the cals


humid_correct = 'Y'

pid_2_on = 'Y'

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
yerr = {1:[],2:[],3:[],4:[],5:[]}
pid_fits = {2:[],3:[],4:[],5:[]}
pidc_fits = {2:[],3:[],4:[],5:[]}

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
     
                   
          
########################################
######Data Read  
print 'Reading Data...'
dataL = pd.read_csv(pathL+filenameL)
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
    RH = dataL.RH
    RH /=4.9
    RH -= 0.16
    RH /= 0.0062
    RH *= 100
    RH /= 103
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

print 'Filling in missing mfchi values...'
dataL['mfchi'] = [(5+((0*i)+1)) for i in range(0,len(dataL))] 
dataL = dataL.fillna({'mfchi':5})


print 'Correcting different Pid Labels and interpolating nans...'
if int(date) < 904:
    pid_5_on = ''
    try:
        pid2d = nan_helper(dataL.pid1,10,3)
    except AttributeError:
        pid_2_on = ''  
    
    try:   
        pid3d = nan_helper(dataL.pid2,10,3)
        pid3d[len(pid3d)+1] = 3

        if humid_correct == 'Y':
            pid3dc = pid3d - RH*pid4_correction
    except AttributeError:
        pid_3_on = ''  
        
    try:    
        pid4d = nan_helper(dataL.pid3,10,3)
        pid4d[len(pid3d)+1] = 4

        if humid_correct == 'Y':
            pid4dc = pid4d - RH*pid4_correction
    except AttributeError:
        pid_4_on = ''    
            
if int(date) >= 904:
    pid_2_on = ''
    try:
        pid5d = nan_helper(dataL.pid5,10,3)
        pid5d[len(pid5d)+1] = 5

        if humid_correct == 'Y':
            pid5dc = pid5d - RH*pid5_correction
    except AttributeError:
        pid_5_on = ''    
         
    try:   
        pid3d = nan_helper(dataL.pid3,10,3)
        pid3d[len(pid3d)+1] = 3
        if humid_correct == 'Y':
            pid3dc = pid3d - RH*pid3_correction
    except AttributeError:
        pid_3_on = ''     
            
    try:   
        pid4d = nan_helper(dataL.pid4,10,3)
        pid4d[len(pid4d)+1] = 4
        if humid_correct == 'Y':
            pid4dc = pid4d - RH*pid4_correction
    except AttributeError:
                pid_4_on = '' 
 
         





#############################
## Signal vs Isop for calibration experiments
   
if (cal == 'Y'):
    
    mfc_set = np.zeros((len(dataL.mfclo)),dtype=bool)
    for i in range(1,len(dataL.mfchi)):
        if (np.logical_and(np.logical_and(np.isfinite(dataL.mfchi[i]),np.isfinite(dataL.mfclo[i])),np.logical_or(dataL.mfchi[i]!=dataL.mfchi[i-1],dataL.mfclo[i]!=dataL.mfclo[i-1]))):
                mfc_set[i] = "True"
                
    cal_N = np.sum(mfc_set) # number of changes in value for mfclo
        
    cal_pts = [range(0,cal_N)]
    

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
     
            
    print 'Splicing the Data...'
    cal_cols_new = ['Start Times','End Times','Isop','Isop Stddev']
    cal_cols_c = []
    
    if pid_2_on == 'Y':
        cal_cols_new.append('Pid2 Voltage')
        cal_cols_new.append('Pid2 Stddev')
        if humid_correct == 'Y':
            cal_cols_c.append('Pid2 Voltage c')
    
        
    if pid_3_on == 'Y':
        cal_cols_new.append('Pid3 Voltage')
        cal_cols_new.append('Pid3 Stddev')
        if humid_correct == 'Y':
            cal_cols_c.append('Pid3 Voltage c')
    
                
    if pid_4_on == 'Y':
        cal_cols_new.append('Pid4 Voltage')
        cal_cols_new.append('Pid4 Stddev')
        if humid_correct == 'Y':
            cal_cols_c.append('Pid4 Voltage c')
    
    if pid_5_on == 'Y':
        cal_cols_new.append('Pid5 Voltage')
        cal_cols_new.append('Pid5 Stddev')
        if humid_correct == 'Y':
            cal_cols_c.append('Pid5 Voltage c') 

    cal_df = pd.DataFrame(index=range(0,len(S)), columns=cal_cols_new)
  
    
    if pid_2_on == 'Y':
        pid2_chunks = list_multisplicer_listsout(pid2d,S,F)
    
        pid2_avgs = [np.nanmean(i) for i in pid2_chunks]
        pid2_stds = [np.nanstd(i) for i in pid2_chunks]
        
        cal_df['Pid2 Voltage'] = pid2_avgs
        cal_df['Pid2 Stddev'] = pid2_stds
        
    if pid_3_on == 'Y':
        
        pid3_chunks = list_multisplicer_listsout(pid3d[:len(pid3d)-1],S,F)
        
        pid3_avgs = [np.nanmean(i) for i in pid3_chunks]
        pid3_stds = [np.nanstd(i) for i in pid3_chunks]
        
        cal_df['Pid3 Voltage'] = pid3_avgs
        cal_df['Pid3 Stddev']= pid3_stds 
           
    if pid_4_on =='Y':
        pid4_chunks = list_multisplicer_listsout(pid4d[:len(pid4d)-1],S,F)
        
        pid4_avgs = [np.nanmean(i) for i in pid4_chunks]
        pid4_stds = [np.nanstd(i) for i in pid4_chunks] 
    
        cal_df['Pid4 Voltage'] = pid4_avgs
        cal_df['Pid4 Stddev'] = pid4_stds
        
    if pid_5_on =='Y':
        pid5_chunks = list_multisplicer_listsout(pid5d[:len(pid5d)-1],S,F)
        
        pid5_avgs = [np.nanmean(i) for i in pid5_chunks]
        pid5_stds = [np.nanstd(i) for i in pid5_chunks] 
    
        cal_df['Pid5 Voltage'] = pid5_avgs
        cal_df['Pid5 Stddev'] = pid5_stds
        
        
    isop_chunks = list_multisplicer_listsout(isop_mr,S,F)
    
    isop_avgs = [np.nanmean(i) for i in isop_chunks]
    isop_stds = [np.nanstd(i) for i in isop_chunks]
    
    
    start_times = [TimeL[i] for i in S]
    end_times = [TimeL[i] for i in F]
    
    if humid_correct == 'Y':
        RH_chunks = list_multisplicer_listsout(RH,S,F)
        RH_avgs = [np.nanmean(i) for i in RH_chunks]
        cal_df['RH'] = RH_avgs

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
        if cal_df['Pid3 Stddev'][i] > s3+m3:
            dodgy_indexes_pid3.append(i)

        
    
    
    ########################## ########################## ########################## 
    print 'Just Tidying Up and Fitting the Data...'
    ########## Tidying up and fitting #########
    
    if pid_2_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid2 Voltage')
    elif pid_3_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid3 Voltage')
    elif pid_4_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid4 Voltage')
    elif pid_5_on:
        cal_df = cal_df.drop_duplicates(subset = 'Pid5 Voltage')
    
    
    cal_df.index = range(0,len(cal_df))    
    
    
    
    if humid_correct == 'Y':
        cal_dfc = pd.DataFrame(index=range(0,len(cal_df)), columns=cal_cols_c)
            
    
    isop_fit = [0.,np.max(cal_df.Isop)]    
    
    xdata = cal_df.Isop
    
    

    Values = {'Slope':{3:[],4:[],5:[]},'Intercept':{3:[],4:[],5:[]},'Slope Error':{3:[],4:[],5:[]},'Intercept Error':{3:[],4:[],5:[]}}
    Corrected_Values = {'Slope':{3:[],4:[],5:[]},'Intercept':{3:[],4:[],5:[]},'Slope Error':{3:[],4:[],5:[]},'Intercept Error':{3:[],4:[],5:[]}}
    
    
    
    if pid_2_on:
        
        for i in range(len(cal_df)):
                yerr[2].append(cal_df['Pid2 Stddev'][i]/np.sqrt(len(pid2_chunks[i+1])))
                
        
        ydata2 = cal_df['Pid2 Voltage'] 
        slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr[2])
        pid2_fit = [slope_intercept2[0],(np.max(cal_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
        
        perr2 = np.sqrt(np.diag(pcov2))
        Intercept_error2 = perr2[0]/np.sqrt(cal_N)
        Slope_Error2 = perr2[0]/np.sqrt(cal_N)        
        
                
    if pid_3_on:        
        
        for i in range(len(cal_df)):
            yerr[3].append(cal_df['Pid3 Stddev'][i]/np.sqrt(len(pid3_chunks[i]))) 
            
            
        if humid_correct == 'Y':
                    cal_dfc['Pid3 Voltage c'] = cal_df['Pid3 Voltage']-cal_df['RH']*pid3_correction
                    ydata3c = cal_dfc['Pid3 Voltage c']    
                    slope_intercept3c,pcov3c = opt.curve_fit(linear_fit, xdata, ydata3c, sigma = yerr[3])
                    pidc_fits[3] = [slope_intercept3c[0],(np.max(cal_df.Isop)*slope_intercept3c[1])+slope_intercept3c[0]]
                    perr3c = np.sqrt(np.diag(pcov3c))    
                    Intercept_error3c = perr3c[0]/np.sqrt(cal_N)
                    Slope_Error3c = perr3c[0]/np.sqrt(cal_N)
                        
                    Corrected_Values['Slope'][3] = slope_intercept3c[1]
                    Corrected_Values['Intercept'][3] = slope_intercept3c[0]
                    Corrected_Values['Slope Error'][3] = Slope_Error3c
                    Corrected_Values['Intercept Error'][3] = Intercept_error3c
  
  
        ydata3 = cal_df['Pid3 Voltage']
        slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr[3])
        pid_fits[3] = [slope_intercept3[0],(np.max(cal_df.Isop)*slope_intercept3[1])+slope_intercept3[0]]

        perr3 = np.sqrt(np.diag(pcov3))    
        Intercept_error3 = perr3[0]/np.sqrt(cal_N)
        Slope_Error3 = perr3[0]/np.sqrt(cal_N)        
        
        Values['Slope'][3] = slope_intercept3[1]
        Values['Intercept'][3] = slope_intercept3[0]
        Values['Slope Error'][3] = Slope_Error3
        Values['Intercept Error'][3] =Intercept_error3
                    
if pid_4_on: 
        
                            
        for i in range(len(cal_df)):
            yerr[4].append(cal_df['Pid4 Stddev'][i]/np.sqrt(len(pid4_chunks[i])))
        
        if humid_correct == 'Y':
                    cal_dfc['Pid4 Voltage c'] = cal_df['Pid4 Voltage']-cal_df['RH']*pid4_correction
                    ydata4c = cal_dfc['Pid4 Voltage c']    
                    slope_intercept4c,pcov4c = opt.curve_fit(linear_fit, xdata, ydata4c, sigma = yerr[4])
                    pidc_fits[4] = [slope_intercept4c[0],(np.max(cal_df.Isop)*slope_intercept4c[1])+slope_intercept4c[0]]
                    perr4c = np.sqrt(np.diag(pcov4c))    
                    Intercept_error4c = perr4c[0]/np.sqrt(cal_N)
                    Slope_Error4c = perr4c[0]/np.sqrt(cal_N)

                    Corrected_Values['Slope'][4] = slope_intercept4c[1]
                    Corrected_Values['Intercept'][4] = slope_intercept4c[0]
                    Corrected_Values['Slope Error'][4] = Slope_Error4c
                    Corrected_Values['Intercept Error'][4] = Intercept_error4c
                                

        ydata4 = cal_df['Pid4 Voltage']
        slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr[4])
        pid_fits[4] = [slope_intercept4[0],(np.max(cal_df.Isop)*slope_intercept4[1])+slope_intercept4[0]]
        
        perr4 = np.sqrt(np.diag(pcov4))    
        Intercept_error4 = perr4[0]/np.sqrt(cal_N)
        Slope_Error4 = perr4[0]/np.sqrt(cal_N)
        
        Values['Slope'][4] = slope_intercept4[1]
        Values['Intercept'][4] = slope_intercept4[0]
        Values['Slope Error'][4] = Slope_Error4
        Values['Intercept Error'][4] = Intercept_error4
        
if pid_5_on: 
    
        for i in range(len(cal_df)):
            yerr[5].append(cal_df['Pid5 Stddev'][i]/np.sqrt(len(pid5_chunks[i])))
            
        if humid_correct == 'Y':
                cal_dfc['Pid5 Voltage c'] = cal_df['Pid5 Voltage']-cal_df['RH']*pid5_correction
                ydata5c = cal_dfc['Pid5 Voltage c']    
                slope_intercept5c,pcov5c = opt.curve_fit(linear_fit, xdata, ydata5c, sigma = yerr[5])
                pidc_fits[5] = [slope_intercept5c[0],(np.max(cal_df.Isop)*slope_intercept5c[1])+slope_intercept5c[0]]
                perr5c = np.sqrt(np.diag(pcov5c))    
                Intercept_error5c = perr5c[0]/np.sqrt(cal_N)
                Slope_Error5c = perr5c[0]/np.sqrt(cal_N)

                Corrected_Values['Slope'][5] = slope_intercept5c[1]
                Corrected_Values['Intercept'][5] = slope_intercept5c[0]
                Corrected_Values['Slope Error'][5] = Slope_Error5c
                Corrected_Values['Intercept Error'][5] = Intercept_error5c           

        ydata5 = cal_df['Pid5 Voltage']
        slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr[5])
        pid_fits[5] = [slope_intercept5[0],(np.max(cal_df.Isop)*slope_intercept5[1])+slope_intercept5[0]]
        
        perr5 = np.sqrt(np.diag(pcov5))    
        Intercept_error5 = perr5[0]/np.sqrt(cal_N)
        Slope_Error5 = perr5[0]/np.sqrt(cal_N)
        
        Values['Slope'][5] = slope_intercept5[1]
        Values['Intercept'][5] = slope_intercept5[0]
        Values['Slope Error'][5] = Slope_Error5
        Values['Intercept Error'][5] =Intercept_error5

    ######## Error finding #######
    
    
    
for i in range(0,len(cal_df)):
    if cal_df['Isop'][i] < 0.25:
        i = i
        
xerrunfil = np.sqrt(cal_df['Isop Stddev'][i]/len(isop_chunks[i]))
        
    
for i in range(len(cal_df)):
    xerr.append(cal_df['Isop Stddev'][i]/np.sqrt(len(isop_chunks[i])))

    #data = {'Slopes':[slope_intercept2[1],slope_intercept3[1]], 'Slope Error':[Slope_Error2,Slope_Error3],'Intercepts':[slope_intercept2[0], slope_intercept3[0]],'Intercept Error':[Intercept_error2,Intercept_error3]}  
    #frame = pd.DataFrame(data,index=['PID2','PID3'])
    #print frame








print 'Plotting the Ammended Data...'

##########################################    Plotting   ##########################################  
if plots == 'Y':
    
    date = timestamp_convert(dataL.TheTime[0])[1:3]
    date = '/'.join(date)
    
    filenumber = filenameL[-2:]
    
    times = list_multisplicer(dataL.TheTime,S,F)
    
    
    


        
        
    plotter(pid3d,pid3dc)
    plotter(pid4d,pid4dc)
    plotter(pid5d,pid5dc)
'''    
###########################################PID 4 ###########################################

    if pid_4_on == 'Y':
            ########################################### PID 4 ###########################################
            voltage_pid4 = list_multisplicer(pid4d,S,F)
            isop_chunks_data_pid4 = list_multisplicer(isop_mr,S,F)
            

            pid4_rolling_avg = pd.rolling_mean(pid4d,300,60)
            
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
            pid4_raw_data = ax4r2.plot(dataL.TheTime,pid4d, linewidth=1,color='b')

            pid4_Isop = ax4r2.plot(dataL.TheTime,isop_mr, linewidth=1,color='g')
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

    if pid_5_on == '':
            ########################################### PID 4 ###########################################
            voltage_pid5 = list_multisplicer(pid5d,S,F)
            isop_chunks_data_pid5 = list_multisplicer(isop_mr,S,F)
            

            pid5_rolling_avg = pd.rolling_mean(pid5d,300,60)
            
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

             
            pid5_raw_data = ax5r2.plot(dataL.TheTime,pid5d, linewidth=1,color='b')
            pid5_Isop = ax5r2.plot(dataL.TheTime,isop_mr, linewidth=1,color='g')
            #pid5_rolling_avg_raw_plot = ax5r2.plot(dataL.TheTime,pid5_rolling_avg, linewidth=1,color = 'r')
            
            # Making graph pretty #
            plt.ylabel("Isop / ppb")
            plt.xlabel('Time / s', fontsize = 20)
            
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
            
            
            
            
            ############################### Humidity Correction Checker ###############################
            fig_s = plt.figure()
            ax1s = fig_s.add_subplot(211)
            RH_plot = ax1s.plot(dataL.TheTime,RH)
            ax2s = fig_s.add_subplot(212)
            RH_plot_corrected = ax2s.plot(dataL.TheTime, pid3_rolling_avg,color='m')
            RH_plot_corrected = ax2s.plot(dataL.TheTime, pid4_rolling_avg,color='b')
            RH_plot_corrected = ax2s.plot(dataL.TheTime, pid5_rolling_avg,color='k')
            plt.title('magenta = pid3, blue = pid4, black = pid5')
            ########################################### ################################################
            
            
            
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
'''