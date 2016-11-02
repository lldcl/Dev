import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.optimize as opt
import datetime
from time import strftime

##################################################### Defining Functions For Use Later #################################################

def plotter(pidxd,pidxdc):
    
    pid_number = int(pidxd.name[-1])
    #Making seperate integer and str variables for the pid number and the string 3 shaves some time of the function, and assigning dataL.TheTime to tim may do as well
    pid_number_str = pidxd.name[-1]
    tim =  dataL.TheTime 
    
    
    # Need the date for titles of graphs
    date = str(tim[0])[5:10]
    
    #Also need this for the titles of the graphs
    filenumber = filenameL[-2:]
    
    
    times = list_multisplicer(tim,S,F)
                                                            
    voltage_pid = list_multisplicer(pidxd,S,F)
            
    isop_chunks_data_pid = list_multisplicer(isop_mr,S,F)
    
       
    
    pid_rolling_avg = pd.rolling_mean(pidxd,300,60)
    #Fig for the raw plots (That's why it's figure r)
    figr = plt.figure()
    figr.suptitle('Pid'+pid_number_str+' , Data Plot ('+date+') - '+filenumber,fontsize = 16)
    # Creating 2 axes on the same subplot for Isoprene and pid voltage (I named the axes according to whether they were a raw plot or not so axr or axc, which axis they were, so axr1, axr2, axr3 or axc1 and the a and b at the end refers to the left and right scale respectively, so axr1a would have the pid voltage, and axr1b would have the isoprene)
    if humid_correct == 'Y':
        x1 = 221 #Posistion of the Uncorrected Spliced graph
        x2 = 223 #Posistion of the Corrected Spliced graph
        x3 = 224 #Posistion of the Raw Data graph
        x4 = 222 #Posistion of the RH graph
    else:
        x1 = 211
        x3 = 212
    axr1a = figr.add_subplot(x1)
    axr1b = axr1a.twinx()
    
    
    ##################### Uncorrected Spliced Plot #########################
    
    ### Uncorrected spliced voltage
    axr1a.plot(times,voltage_pid, linewidth=1,color= 'r')
    ### Uncorrected Rolling Average
    axr1a.plot(tim,pid_rolling_avg, linewidth=1, color = 'b')
    ### Isoprene concentration
    axr1b.plot(times,isop_chunks_data_pid,linewidth = 1,color='k')
    # Adding labels
    axr1a.set_ylabel('Pid'+pid_number_str+' Voltage / V')
    axr1b.set_ylabel('Isop / ppb')
    plt.xlabel('Time / s', fontsize = 20)
    
    
    
    ##################### Corrected Spliced Plot #########################
    if humid_correct == 'Y':
        
        ### Splicing the corrected Voltages
        voltage_pidc = list_multisplicer(pidxdc,S,F)
        ### Calculating a Rolling Average of the corrected Voltages
        pidc_rolling_avg = pd.rolling_mean(pidxdc,300,60)
        
        # Creating Subplot for the corrected graph
        axr2a = figr.add_subplot(x2)
        axr2b = axr2a.twinx()

        # Corrected plot of Spliced Voltage
        axr2a.plot(times,voltage_pidc, linewidth=1,color= 'r')
        axr2a.plot(tim,pidc_rolling_avg, linewidth=1, color = 'b')
        
        # This is the Black Line (the Isoprene concentrations at the spliced bits)
        axr2b.plot(times,isop_chunks_data_pid,linewidth = 1,color='k')
        
        #Setting axes Labels
        axr2a.set_ylabel('Pid'+pid_number_str+' Voltage / V')
        plt.xlabel('Time / s', fontsize = 20)
        
        
        
        ########################### RH Plot ############################
        
        axr4a = figr.add_subplot(x4)
        axr4b = axr4a.twinx()
        
        axr4a.plot(tim,RH,color='b')
        axr4b.plot(tim,pid_rolling_avg, linewidth=1, color = 'r')
        axr4b.plot(tim,pidc_rolling_avg, linewidth=1, color = 'g')
        axr4b.set_title('red = uncorrected, green = corrected, blue =  humidity')
    
    
    
    ##################### Raw Data Plot #####################
    
    axr3a = figr.add_subplot(x3)
    axr3b = axr3a.twinx()
    #The raw PID Data.
    axr3a.plot(tim,pidxd, linewidth=1,color='b')
    #The Isoprene data.
    axr3b.plot(tim,isop_mr, linewidth=1,color='g')
            
    # Setting axes labels
    axr3b.set_ylabel('Isop / ppb')
    plt.xlabel('Time / s', fontsize = 20)
    
    

    ##################### Cal Plot #########################

    figc = plt.figure()
    figc.suptitle('Pid'+pid_number_str+' , Cal plot ('+date+') - '+filenumber,fontsize = 16)
    axc1a = figc.add_subplot(111)
    
    
    # Setting axes labels
    axc1a.set_ylabel('Pid Voltage / V')
    plt.xlabel('Isop / ppb')
    
    #Plotting Cal Points with Errorbars
    axc1a.errorbar(cal_df.Isop,cal_df['Pid'+pid_number_str+' Voltage'], xerr = xerr, yerr = yerr[pid_number], fmt='bo')
    #Plotting Lines of Best Fit
    axc1a.plot(isop_fit,pid_fits[pid_number],color = 'b')

    
    if humid_correct == 'Y':
        # Creating a new scale for the corrected cal line
        axc1b = axc1a.twinx()
        axc1b.errorbar(cal_df.Isop,cal_dfc['Pid'+pid_number_str+' Voltage c'], xerr = xerr, yerr = yerr[pid_number], fmt='mx')
        axc1b.plot(isop_fit, pidc_fits[pid_number],color = 'm')
        axc1b.set_ylabel('Pid Voltage / V')
        
    # Adding a legend #
    # Information for the legends, values are given to 2 d.p. and intercepts are given to 1 d.p. (to change this just change the '%.Xg' number)
    slope_patch_pid = mpatches.Patch(label='Slope = '+str('%.2g' % Values['Slope'][pid_number])+'+/-'+str('%.1g' % Values['Slope Error'][pid_number]),color = 'b')
    intecept_patch_pid = mpatches.Patch(label = 'Intercept = '+str('%.2g' % Values['Intercept'][pid_number])+'+/-'+str('%.1g' % Values['Intercept'][pid_number]),color = 'b')
    
    if humid_correct == 'Y':
        slope_patch_pid_corrected = mpatches.Patch(label = 'Slopec = '+str("%.2e" % Corrected_Values['Slope'][pid_number])+'+/-'+str("%.1e" % Corrected_Values['Slope Error'][pid_number]),color = 'm')
        intecept_patch_pid_corrected = mpatches.Patch(label = 'Interceptc = '+str("%.2e" % Corrected_Values['Intercept'][pid_number])+'+/-'+str("%.1e" % Corrected_Values['Intercept Error'][pid_number]),color = 'm')
        #Popping the legend on the graph in the 'best'location
        plt.legend(handles=[slope_patch_pid,intecept_patch_pid,slope_patch_pid_corrected,intecept_patch_pid_corrected],loc='best')
    
    else:
        plt.legend(handles=[slope_patch_pid,intecept_patch_pid],loc='best')
    # Setting Labels
    plt.ylabel('Pid'+pid_number_str+' Voltage / V')
    plt.xlabel('Isoprene Concentration / ppb')

    
    plt.show()
            
            
            
            
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
    
    
#To convert timestamps to a string
def timeconverter(T):
    #	print T
   	return (datetime.datetime.strptime(T,"%y-%m-%d-%H-%M-%S-%f"))


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
            non_blank = []
            for i in new_lt:
                   if i != []:
                       non_blank.append(i)     
            return non_blank

             
                   
#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept

#Returns a quadratic Fit
def quadratic_fit(Isoprene, root1, root2,xfac1,xfac2):
    return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)
    
#Returns a cubic Fit for pid4  
def cubic_fit4(Isoprene, root1, root2,root3,xfac1,xfac2,xfac3):
    return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)*((xfac3*Isoprene)+root3)

#Returns a cubic Fit for pids 3 & 5
def cubic_fit35(Isoprene, root1, root2,root3,xfac1,xfac2,xfac3):
    return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)*((xfac3*Isoprene)-root3) 
         
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




pd.set_option('precision',9)

cal_stuff = 'Y'
arduino = ''

data_point_length = 300 # how many data points used for the cals


humid_correct = 'Y'

if humid_correct == 'Y':
    linear_fitter = ''
    quadratic_fitter = ''
    cubic_fitter = ''
    
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
    cal = 'Y'
else:
    questions = ''
    avg_0 = ''
    arduino_cal_stuff = ''
    
hist = ''



##############################################################################################################################
##############################################################################################################################


xerr = []
yerr = {1:[],2:[],3:[],4:[],5:[]}
pid_fits = {2:[],3:[],4:[],5:[]}
pidc_fits = {2:[],3:[],4:[],5:[]}





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

          
if humid_correct == 'Y':
    dataL.mfcloR = nan_helper(dataL.mfcloR,10,3)
    x = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\\fit file.txt', sep = '\t')
    names = [i for i in x['Unnamed: 0']]
    x.index = names
    x = x.drop('Unnamed: 0',1)
    pid3_correction = 1.8664285714285712e-05
    pid4_correction = 9.2661904761904766e-06
    pid5_correction = 2.6714285714285718e-05
    
    if linear_fitter == 'Y':
        pid3_correction = [((x['Slope']['Pid3']*i)+x['Intercept']['Pid3']) for i in dataL.mfcloR]
        pid3_correction = pid3_correction = np.nanmean(pid3_correction)
        
        pid4_correction = [((x['Slope']['Pid4']*i)+x['Intercept']['Pid4']) for i in dataL.mfcloR]
        pid4_correction = pid4_correction = np.nanmean(pid4_correction)
        
        pid5_correction = [((x['Slope']['Pid5']*i)+x['Intercept']['Pid5']) for i in dataL.mfcloR]
        pid5_correction = pid5_correction = np.nanmean(pid5_correction)
        
    if quadratic_fitter == 'Y':
        pid3_correction = quadratic_fit(dataL.mfcloR,x['2A']['Pid3'],x['2B']['Pid3'],x['2C']['Pid3'],x['2D']['Pid3'])
        pid4_correction = quadratic_fit(dataL.mfcloR,x['2A']['Pid4'],x['2B']['Pid4'],x['2C']['Pid4'],x['2D']['Pid4'])
        pid5_correction = quadratic_fit(dataL.mfcloR,x['2A']['Pid5'],x['2B']['Pid5'],x['2C']['Pid5'],x['2D']['Pid5'])
        
        pid3_correction = pid3_correction = np.nanmean(pid3_correction)
        pid4_correction = pid4_correction = np.nanmean(pid4_correction)
        pid5_correction = pid5_correction = np.nanmean(pid5_correction)    
    if cubic_fitter == 'Y':
        pid3_correction = cubic_fit35(dataL.mfcloR,x['3A']['Pid3'],x['3B']['Pid3'],x['3C']['Pid3'],x['3D']['Pid3'],x['3E']['Pid3'],x['3F']['Pid3'])
        pid4_correction = cubic_fit4(dataL.mfcloR,x['3A']['Pid4'],x['3B']['Pid4'],x['3C']['Pid4'],x['3D']['Pid4'],x['3E']['Pid4'],x['3F']['Pid4'])
        pid5_correction = cubic_fit35(dataL.mfcloR,x['3A']['Pid5'],x['3B']['Pid5'],x['3C']['Pid5'],x['3D']['Pid5'],x['3E']['Pid5'],x['3F']['Pid5'])
        
        pid3_correction = pid3_correction = np.nanmean(pid3_correction)
        pid4_correction = pid4_correction = np.nanmean(pid4_correction)
        pid5_correction = pid5_correction = np.nanmean(pid5_correction)               
          
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
    dataL.RH = nan_helper(dataL.RH,10,3)
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
dataL['mfchi'] = [(5+((0*i)+1)) for i in xrange(0,len(dataL))] 
dataL = dataL.fillna({'mfchi':5})


print 'Correcting different Pid Labels and interpolating nans...'
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
print 'Setting Cal Points...'   
if (cal == 'Y'):
    
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
    
 
            
            
    print 'Splicing the Data and Filling cal_df...'
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

    cal_df = pd.DataFrame(index=xrange(0,len(S)), columns=cal_cols_new)
  
    
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
    cal_df.index = xrange(0,len(cal_df))


    print 'Averaging the Zeros...'
    ########################## Zero Averaging #########################
    

    isop_zero_indexes = []
    for i in xrange(0,len(cal_df.Isop)):
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



    cal_df.index = xrange(0,len(cal_df))

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
    
    
    cal_df.index = xrange(0,len(cal_df))    
    
    
    
    if humid_correct == 'Y':
        cal_dfc = pd.DataFrame(index=xrange(0,len(cal_df)), columns=cal_cols_c)
            
    
    isop_fit = [0.,np.max(cal_df.Isop)]    
    
    xdata = cal_df.Isop
    
    

    Values = {'Slope':{3:[],4:[],5:[]},'Intercept':{3:[],4:[],5:[]},'Slope Error':{3:[],4:[],5:[]},'Intercept Error':{3:[],4:[],5:[]}}
    Corrected_Values = {'Slope':{3:[],4:[],5:[]},'Intercept':{3:[],4:[],5:[]},'Slope Error':{3:[],4:[],5:[]},'Intercept Error':{3:[],4:[],5:[]}}
    
    
    
    if pid_2_on:
        
        for i in xrange(len(cal_df)):
                yerr[2].append(cal_df['Pid2 Stddev'][i]/np.sqrt(len(pid2_chunks[i+1])))
                
        
        ydata2 = cal_df['Pid2 Voltage'] 
        slope_intercept2,pcov2 = opt.curve_fit(linear_fit, xdata, ydata2, sigma = yerr[2])
        pid_fits[2] = [slope_intercept2[0],(np.max(cal_df.Isop)*slope_intercept2[1])+slope_intercept2[0]]
        
        perr2 = np.sqrt(np.diag(pcov2))
        Intercept_error2 = perr2[0]/np.sqrt(cal_N)
        Slope_Error2 = perr2[1]/np.sqrt(cal_N)        
        
        Values['Slope'][2] = slope_intercept2[1]
        Values['Intercept'][2] = slope_intercept2[0]
        Values['Slope Error'][2] = Slope_Error2
        Values['Intercept Error'][2] =Intercept_error2
                
    if pid_3_on:        
        
        for i in xrange(len(cal_df)):
            yerr[3].append(cal_df['Pid3 Stddev'][i]/np.sqrt(len(pid3_chunks[i]))) 
            
            
        if humid_correct == 'Y':
                    cal_dfc['Pid3 Voltage c'] = cal_df['Pid3 Voltage']-cal_df['RH']*pid3_correction
                    ydata3c = cal_dfc['Pid3 Voltage c']    
                    slope_intercept3c,pcov3c = opt.curve_fit(linear_fit, xdata, ydata3c, sigma = yerr[3])
                    pidc_fits[3] = [slope_intercept3c[0],(np.max(cal_df.Isop)*slope_intercept3c[1])+slope_intercept3c[0]]
                    perr3c = np.sqrt(np.diag(pcov3c))    
                    Intercept_error3c = perr3c[0]/np.sqrt(cal_N)
                    Slope_Error3c = perr3c[1]/np.sqrt(cal_N)
                        
                    Corrected_Values['Slope'][3] = slope_intercept3c[1]
                    Corrected_Values['Intercept'][3] = slope_intercept3c[0]
                    Corrected_Values['Slope Error'][3] = Slope_Error3c
                    Corrected_Values['Intercept Error'][3] = Intercept_error3c
  
  
        ydata3 = cal_df['Pid3 Voltage']
        slope_intercept3,pcov3 = opt.curve_fit(linear_fit, xdata, ydata3, sigma = yerr[3])
        pid_fits[3] = [slope_intercept3[0],(np.max(cal_df.Isop)*slope_intercept3[1])+slope_intercept3[0]]

        perr3 = np.sqrt(np.diag(pcov3))    
        Intercept_error3 = perr3[0]/np.sqrt(cal_N)
        Slope_Error3 = perr3[1]/np.sqrt(cal_N)        
        
        Values['Slope'][3] = slope_intercept3[1]
        Values['Intercept'][3] = slope_intercept3[0]
        Values['Slope Error'][3] = Slope_Error3
        Values['Intercept Error'][3] =Intercept_error3
                    
if pid_4_on: 
        
                            
        for i in xrange(len(cal_df)):
            yerr[4].append(cal_df['Pid4 Stddev'][i]/np.sqrt(len(pid4_chunks[i])))
        
        if humid_correct == 'Y':
                    cal_dfc['Pid4 Voltage c'] = cal_df['Pid4 Voltage']-cal_df['RH']*pid4_correction
                    ydata4c = cal_dfc['Pid4 Voltage c']    
                    slope_intercept4c,pcov4c = opt.curve_fit(linear_fit, xdata, ydata4c, sigma = yerr[4])
                    pidc_fits[4] = [slope_intercept4c[0],(np.max(cal_df.Isop)*slope_intercept4c[1])+slope_intercept4c[0]]
                    perr4c = np.sqrt(np.diag(pcov4c))    
                    Intercept_error4c = perr4c[0]/np.sqrt(cal_N)
                    Slope_Error4c = perr4c[1]/np.sqrt(cal_N)

                    Corrected_Values['Slope'][4] = slope_intercept4c[1]
                    Corrected_Values['Intercept'][4] = slope_intercept4c[0]
                    Corrected_Values['Slope Error'][4] = Slope_Error4c
                    Corrected_Values['Intercept Error'][4] = Intercept_error4c
                                

        ydata4 = cal_df['Pid4 Voltage']
        slope_intercept4,pcov4 = opt.curve_fit(linear_fit, xdata, ydata4, sigma = yerr[4])
        pid_fits[4] = [slope_intercept4[0],(np.max(cal_df.Isop)*slope_intercept4[1])+slope_intercept4[0]]
        
        perr4 = np.sqrt(np.diag(pcov4))    
        Intercept_error4 = perr4[0]/np.sqrt(cal_N)
        Slope_Error4 = perr4[1]/np.sqrt(cal_N)
        
        Values['Slope'][4] = slope_intercept4[1]
        Values['Intercept'][4] = slope_intercept4[0]
        Values['Slope Error'][4] = Slope_Error4
        Values['Intercept Error'][4] = Intercept_error4
        
if pid_5_on: 
    
        for i in xrange(len(cal_df)):
            yerr[5].append(cal_df['Pid5 Stddev'][i]/np.sqrt(len(pid5_chunks[i])))
            
        if humid_correct == 'Y':
                cal_dfc['Pid5 Voltage c'] = cal_df['Pid5 Voltage']-cal_df['RH']*pid5_correction
                ydata5c = cal_dfc['Pid5 Voltage c']    
                slope_intercept5c,pcov5c = opt.curve_fit(linear_fit, xdata, ydata5c, sigma = yerr[5])
                pidc_fits[5] = [slope_intercept5c[0],(np.max(cal_df.Isop)*slope_intercept5c[1])+slope_intercept5c[0]]
                perr5c = np.sqrt(np.diag(pcov5c))    
                Intercept_error5c = perr5c[0]/np.sqrt(cal_N)
                Slope_Error5c = perr5c[1]/np.sqrt(cal_N)

                Corrected_Values['Slope'][5] = slope_intercept5c[1]
                Corrected_Values['Intercept'][5] = slope_intercept5c[0]
                Corrected_Values['Slope Error'][5] = Slope_Error5c
                Corrected_Values['Intercept Error'][5] = Intercept_error5c           

        ydata5 = cal_df['Pid5 Voltage']
        slope_intercept5,pcov5 = opt.curve_fit(linear_fit, xdata, ydata5, sigma = yerr[5])
        pid_fits[5] = [slope_intercept5[0],(np.max(cal_df.Isop)*slope_intercept5[1])+slope_intercept5[0]]
        
        perr5 = np.sqrt(np.diag(pcov5))    
        Intercept_error5 = perr5[0]/np.sqrt(cal_N)
        Slope_Error5 = perr5[1]/np.sqrt(cal_N)
        
        Values['Slope'][5] = slope_intercept5[1]
        Values['Intercept'][5] = slope_intercept5[0]
        Values['Slope Error'][5] = Slope_Error5
        Values['Intercept Error'][5] =Intercept_error5

    ######## Error finding #######
    
    
    
for i in xrange(0,len(cal_df)):
    if cal_df['Isop'][i] < 0.25:
        i = i
        
xerrunfil = np.sqrt(cal_df['Isop Stddev'][i]/len(isop_chunks[i]))
        
    
for i in xrange(len(cal_df)):
    xerr.append(cal_df['Isop Stddev'][i]/np.sqrt(len(isop_chunks[i])))

    #data = {'Slopes':[slope_intercept2[1],slope_intercept3[1]], 'Slope Error':[Slope_Error2,Slope_Error3],'Intercepts':[slope_intercept2[0], slope_intercept3[0]],'Intercept Error':[Intercept_error2,Intercept_error3]}  
    #frame = pd.DataFrame(data,index=['PID2','PID3'])
    #print frame








print 'Plotting the Ammended Data...'

##########################################    Plotting   ##########################################  

# To Edit the Plots Please Edit the plotter function at the top of the code.
    

   
plotter(pid3d,pid3dc)
plotter(pid4d,pid4dc)
plotter(pid5d,pid5dc)
