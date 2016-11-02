# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.optimize as opt
import datetime
from time import strftime
from operator import itemgetter


################  Control  Panel  ################

pid_corrections = {3:(1.8664285714285712e-05),4:(9.2661904761904766e-06),5:(2.6714285714285718e-05)}

pd.set_option('precision',8)


data_point_length = 360 # how many data points used for the cals
bad_cal_length = data_point_length



humid_correct = 'Y'


pids_on = [5]



questions = ''


################ ################ ################







##################################################### Defining Functions For Use Later #################################################

def plotter(pidxd,pidxdc,num):
    
    pid_number = num
    #Making seperate integer and str variables for the pid number and the string 3 shaves some time of the function, and assigning dataL.TheTime to tim may do as well
    pid_number_str = str(num)
    tim =  dataL.TheTime 

    Sc = list(SF_indexes_corrected[num][0])
    Fc = list(SF_indexes_corrected[num][1])
  
    
    # Need the date for titles of graphs
    date = str(tim[0])[5:10]
    
    #Also need this for the titles of the graphs
    filenumber = filenameL[-2:]

       
    
    pid_rolling_avg = pd.rolling_mean(pidxd,300,60)
    #Fig for the raw plots (That's why it's figure r)
    figr = plt.figure()
    figr.suptitle('Pid'+pid_number_str+' , Data Plot ('+date+') - '+filenumber,fontsize = 16)
    # Creating 2 axes on the same subplot for Isoprene and pid voltage (I named the axes according to whether they were a raw plot or not so axr or axc, which axis they were, so axr1, axr2, axr3 or axc1 and the a and b at the end refers to the left and right scale respectively, so axr1a would have the pid voltage, and axr1b would have the isoprene)
    if humid_correct == 'Y':
        x1 = 221 #Posistion of the Uncorrected Raw Data
        x2 = 222 #Posistion of RH Graph
        x3 = 223 #Posistion of the Corrected Spliced graph
        x4 = 224 #Posistion of the Cal Graph
    else:
        x1 = 211
        x3 = 212
    

    ##################### Raw Data Plot #####################
    axr1a = figr.add_subplot(x1)
    axr1b = axr1a.twinx()
    
    #The raw PID Data.
    axr1a.plot(tim,pidxd, linewidth=1,color='b')
    #The Isoprene data.
    axr1b.plot(tim,isop_mr, linewidth=1,color='g')

    ##################### Uncorrected Spliced Plot #########################

    ### Uncorrected Rolling Average
    axr1a.plot(tim,pid_rolling_avg, linewidth=1, color = 'b')

    # Adding labels
    axr1a.set_ylabel('Pid'+pid_number_str+' Voltage / V')
    axr1b.set_ylabel('Isop / ppb')
    plt.xlabel('Time / s', fontsize = 20)
    
    # Plotting a Line at the zero point to show variation of the zero
    for zero_index in xrange(0,len(cal_df)):
        if np.around(cal_df.loc[zero_index,'Isop'],1) == 0.0:
            y0 = cal_df.loc[zero_index,'Pid'+pid_number_str+' Voltage']
            if humid_correct == 'Y':
                y0c = cal_dfc.loc[zero_index,'Pid'+pid_number_str+' Voltage']
            break    
    axr1a.plot([min(tim),max(tim)],[y0,y0],'k-')
    
    ##################### Corrected Spliced Plot #########################
    if humid_correct == 'Y':
        isop_chunks_data_pidc = list_multisplicer(isop_mr,Sc,Fc)
        timesc = list_multisplicer(tim,Sc,Fc)
        ### Splicing the corrected Voltages
        voltage_pidc = list_multisplicer(pidxdc,Sc,Fc)
        ### Calculating a Rolling Average of the corrected Voltages
        pidc_rolling_avg = pd.rolling_mean(pidxdc,300,60)
        
        # Creating Subplot for the corrected graph
        axr2a = figr.add_subplot(x3)
        axr2b = axr2a.twinx()

        # Corrected plot of Spliced Voltage
        axr2a.plot(timesc,voltage_pidc, linewidth=1,color= 'r')
        axr2a.plot(tim,pidc_rolling_avg, linewidth=1, color = 'b')
        
        # This is the Black Line (the Isoprene concentrations at the spliced bits)
        axr2b.plot(timesc,isop_chunks_data_pidc,linewidth = 1,color='k')
        
        #Setting axes Labels
        axr2a.set_ylabel('Pid'+pid_number_str+' Voltage / V')
        plt.xlabel('Time / s', fontsize = 20)
        
        # Plotting a Line at the zero point to show variation of the zero
        axr2a.plot([min(tim),max(tim)],[y0c,y0c],'k-')
        
        ########################### RH Plot ############################
        
        axr4a = figr.add_subplot(x2)
        axr4b = axr4a.twinx()
        
        #Plotting Time against RH
        axr4a.plot(tim,RH,color='b')

        #Plotting Rolling Averages
        axr4b.plot(tim,pid_rolling_avg, linewidth=1, color = 'r')
        axr4b.plot(tim,pidc_rolling_avg, linewidth=1, color = 'g')
        
        # Plotting a Line at the zero point to show variation of the zero
        axr4b.plot([min(tim),max(tim)],[y0,y0],'k-')
        if humid_correct == 'Y':
            axr4b.plot([min(tim),max(tim)],[y0c,y0c],'-k')
        
        #Setting the title
        axr4b.set_title('red = uncorrected, green = corrected, blue =  humidity',fontsize = 13)
    
    
    

    
    

    ##################### Cal Plot #########################

    axc1a = figr.add_subplot(x4)
    axc1a.set_title('Pid'+pid_number_str+' , Cal plot ('+date+') - '+filenumber,fontsize = 13)

    
    # Setting axes labels
    axc1a.set_ylabel('Pid Voltage / V')
    plt.xlabel('Isop / ppb')
    
    #Plotting Cal Points with Errorbars
    axc1a.errorbar(cal_df.Isop,cal_df['Pid'+pid_number_str+' Voltage'], xerr = xerr, yerr = cal_df['Pid%s Stderr' %(pid_number)], fmt='bo')
    #Plotting Lines of Best Fit
    axc1a.plot(isop_fit,pid_fits[pid_number],color = 'b')

    
    if humid_correct == 'Y':
        # Creating a new scale for the corrected cal line
        axc1b = axc1a.twinx()
        axc1b.errorbar(cal_df.Isop,cal_dfc['Pid'+pid_number_str+' Voltage'], xerr = xerr, yerr = cal_dfc['Pid%s Stderr' %(pid_number)], fmt='mx')
        axc1b.plot(isop_fit, pidc_fits[pid_number],color = 'm')
        axc1b.set_ylabel('Pid Voltage / V')
        
    # Adding a legend #
    # Information for the legends, values are given to 2 d.p. and intercepts are given to 1 d.p. (to change this just change the '%.Xg' number)
    slope_patch_pid = mpatches.Patch(label='Slope = '+str('%.2g' % Values['Slope'][pid_number])+'+/-'+str('%.1g' % Values['Slope Error'][pid_number]),color = 'b')
    intecept_patch_pid = mpatches.Patch(label = 'Intercept = '+str('%.2g' % Values['Intercept'][pid_number])+'+/-'+str('%.1g' % Values['Intercept'][pid_number]),color = 'b')
    
    if humid_correct == 'Y':
        slope_patch_pid_corrected = mpatches.Patch(label = 'Slopec = '+str("%.2g" % Corrected_Values['Slope'][pid_number])+'+/-'+str("%.1g" % Corrected_Values['Slope Error'][pid_number]),color = 'm')
        intecept_patch_pid_corrected = mpatches.Patch(label = 'Interceptc = '+str("%.2g" % Corrected_Values['Intercept'][pid_number])+'+/-'+str("%.1g" % Corrected_Values['Intercept Error'][pid_number]),color = 'm')
        #Popping the legend on the graph in the 'best'location
        plt.legend(handles=[slope_patch_pid,intecept_patch_pid,slope_patch_pid_corrected,intecept_patch_pid_corrected],loc='best',fontsize = 10)
    
    else:
        plt.legend(handles=[slope_patch_pid,intecept_patch_pid],loc='best',fontsize = 10)
    # Setting Labels
    plt.ylabel('Pid'+pid_number_str+' Voltage / V')
    plt.xlabel('Isoprene Concentration / ppb')

    plt.tight_layout()
    plt.show()
            
            
            
            
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

### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation

def cal_point_ammender(data_set,bad_cal_length,S,F,*args):
    shifter = len(dataL)/(20*len(S)*11)
    if args == ():
        if S[0]/22 >= shifter:
            shifter = len(dataL)/(20*len(S)*4)
        elif S[0]/22 <= shifter:
            shifter = S[0]/22
    else:
        if args[0] <= 1:
            print 'Are you sure you want to use a shifter that high?'
            shifter = len(dataL)/(20*len(S)*args[0])
        else:
            shifter = len(dataL)/(20*len(S)*args[0])
    Snew = np.zeros(len(S))
    Fnew = np.zeros(len(F))    
    for i in xrange(0,len(S)):

        orig_std = np.nanstd(data_set[S[i]:F[i]])
        
        if orig_std > 0.7:
            S[i] = F[i] - bad_cal_length

        
        left_shift_stds = {k:[np.nanstd(data_set[S[i]-(k*shifter):F[i]-(k*shifter)])] for k in xrange(0,20)}
        nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
        for t in nanL:
            del(left_shift_stds[t])
            
        minPairL = min(left_shift_stds.iteritems(), key=itemgetter(1))


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
               
    if S[0] < 0:
        SF = negative_remover(Snew,Fnew)
        Snew = SF[0]
        Fnew = SF[1]
        
    return Snew,Fnew
        


# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))
    
#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept
        
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


pid_fits = {i:[] for i in pids_on}
pidc_fits = {i:[] for i in pids_on}





#############################
## User Interface
if questions == 'Y':
    date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
    filenumber = raw_input('\n\nWhich file would you like to load? ')
    try:
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
        filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + filenumber
        dataL = pd.read_csv(pathL+filenameL)
        
    except IOError:
        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
        dataL = pd.read_csv(pathL+filenameL)
else:
    date = '0907'
    filenumber = '3'
    
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+str(date[0:2])
    filenameL ='\d20' + str((strftime('%y'))) + date + '_0'+str(filenumber)
    dataL = pd.read_csv(pathL+filenameL)

            
          
########################################
######Data Read  
print 'Reading Data...'



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


        

    xerr = [cal_df['Isop Error'][i]/np.sqrt(data_point_length) for i in xrange(len(cal_df))]    

    
    for num in pids_on:
        plotter(pid_data[num],pid_data_corrected[num],num)

else:
    print 'Okie Doke, I won\'t cal %s then'%(filenameL[1:])
