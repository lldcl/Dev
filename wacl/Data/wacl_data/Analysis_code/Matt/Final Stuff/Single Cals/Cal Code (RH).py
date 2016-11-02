import pandas as pd
import matplotlib.pyplot as plt
from time import strftime
import numpy as np
import matplotlib.patches as mpatches
from operator import itemgetter
import scipy.odr as odr



Questions = 'Y' # 'Y' turns the questions on, 'N' lets you enter your own date and filenumber, and '' lets you enter your own filepath.




data_point_length = 1000 # If you want to cal with more data for each point adjust this. (If the code gives a ValueError becuase min() arg is an empty sequence lower this)
bad_cal_length = 500

pids_on = np.arange(0,1000)

############## ############## ##############  Defining Useful Functions ############## ############## ############## 
def plotter(num):
    
        fig1 = plt.figure()
        plt.suptitle('Pid%s, Isop = %s (%s/%s)'%(num,str(Isop),str(date[0:2]),str(date[2:])), fontsize = 14 )
        
        
        
        RH_Chunks = fig1.add_subplot(221)
        RH_Chunks.set_title('RH Chunks', fontsize=12)
        RH_Chunks.set_xlabel('Time / hh:mm:ss')
        RH_Chunks.set_ylabel('RH / %')
        
        
        
        
        Pid_Data = fig1.add_subplot(222)
        Pid_Data.set_title('Pid Data', fontsize=12)
        Pid_Data.set_xlabel('Time / hh:mm:ss')
        Pid_Data.set_ylabel('Pid Voltage / V')    
        
        
        
        RH_Raw_Data = fig1.add_subplot(223)
        PID_Raw_Data = RH_Raw_Data.twinx()
        RH_Raw_Data.set_title('Raw Data', fontsize=12)
        RH_Raw_Data.set_ylabel('RH / %')
        PID_Raw_Data.set_ylabel('Pid Voltage / V')
        RH_Raw_Data.set_xlabel('Time / hh:mm:ss')
        
        
        Cal_Plot = fig1.add_subplot (224)
        Cal_Plot.set_title('Cal Plot', fontsize=12)
        Cal_Plot.set_xlabel('RH / %')
        Cal_Plot.set_ylabel('Pid Voltage / V')
        
        
        
        ######### RH Chunks #########
        RH_Chunks.plot(dataL.TheTime,Rolling_Averages['Rolling Average']['RH'], color = 'b')
        RH_Chunks.plot(Spliced_Data['Times'][num],Spliced_Data['RH'][num],color='y')
        
        
        
        
        ######### Pid Data #########
        Pid_Data.plot(Spliced_Data['Times'][num],Spliced_Data['Pids'][num], 'g')
        Pid_Data.plot(dataL.TheTime,Rolling_Averages['Rolling Average'][num], 'r')
        
        
        
        
        ######### Raw Data #########
        RH_Raw_Data.plot(dataL.TheTime, RH,'b')
        PID_Raw_Data.plot(dataL.TheTime,pid_data[num],'g')
        
        
        
        
        ######### Cal Plot #########
        Cal_Plot.plot(RH_fit,pid_fits[num],'y')  
        Cal_Plot.errorbar(xdata,cal_df['Pid%s Voltage'%num], xerr = cal_df['RH Stderr'], yerr = cal_df['Pid%s Stderr'%num],color = 'b',fmt = 'none')
        slope_patch = mpatches.Patch(label = 'Slope = %s +/- %s'%(Values['Slopes'][num],Values['Slope Errors'][num]),color = 'b')
        plt.legend(handles = [slope_patch],loc = 'best',fontsize = 10)    
        
        
        
        
        plt.tight_layout()    
        plt.show()



### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation
def cal_point_ammender(data_set,bad_cal_length,S,F):
    shifter = (len(dataL)*1)/(20*(len(S)+2)*4)

    
    
    Snew = list(np.zeros(len(S)))
    Fnew = list(np.zeros(len(F)))    
    for i in xrange(0,len(S)):

        orig_std = np.nanstd(data_set[S[i]:F[i]])
        
        if orig_std > 0.7:
            S[i] = F[i] - bad_cal_length

        
        left_shift_stds = {k:[np.nanstd(data_set[S[i]-(k*shifter):F[i]-(k*shifter)])] for k in xrange(0,20) if S[i] - (k*shifter) >= 0}
        nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
        for t in nanL:
            del(left_shift_stds[t])
        
        print left_shift_stds
        
        
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
    
    # Checks if S and F are ever both zero and if they are delete them, the ODR function later doesn't like it if a cal point has zero error.
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


# Adds extra Cal points to bits that have a flat bit longer than the specified amount
#Not currenty used
def cal_adder(number_of_additions,S,F,tolerance_length,cal_length,cal_spacing):
    long_ones = [i for i in xrange(0,len(S)) if S[i] - S[i-1] > tolerance_length]
    
    for pt in xrange(0,(number_of_additions-1)):
        F = F + [F[i] for i in long_ones]
        S = S + [S[i] for i in long_ones]
        
    F.sort()
    S.sort()
    
    S_indexes = [i for i in xrange(0,len(S)) if S[i] == S[i-(number_of_additions-1)]]
    F_indexes = [i for i in xrange(0,len(F)) if F[i] == F[i-(number_of_additions-1)]]
    
    for i in F_indexes:
        for pt in xrange(0,number_of_additions):
            if pt >= 1:
                F[i-pt] = F[i-pt] - (pt*(cal_spacing))
    
    for i in S_indexes:
        for pt in xrange(0,number_of_additions):
            if pt >= 1:
                S[i-pt] = S[i-pt] - (pt*(cal_spacing))
    
        
    return S,F

# To interpolate between NaN values
def nan_helper(data,averagefreq,nanno):
    return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))

#Removes Duplicates
def remove_duplicates(l):
    return list(set(l))

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
                    
            return new_lt


#Returns a Linear Fit
def linear_fit(slope, intercept, x):
    return (slope*x)+intercept
    
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
############## ############## ############## ############## ############## ############## ############## ############## 


                      
    
    
############## ##############  Data Read ############## ##############     
if Questions == 'Y':
    date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
    if date == 'test':
#        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Isoprene = 0.0\\'    
        pathL = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data//201509//Humidity Cals/Isoprene = 0.0//'    

        filenameL = 'd2015test.txt'
        print '\nReading Data...'
        dataL = pd.read_csv(pathL+filenameL)
        
        date = 1
        
    elif date == 'bi' or date == 'bg' or date == 'big':
#        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\Isoprene = 0.0\\'    
        pathL = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data//201509//Humidity Cals/Isoprene = 0.0//'    

        filenameL = 'd20150904_0big(post 0903).txt'
        print '\nReading Data...'
        dataL = pd.read_csv(pathL+filenameL)
  
               
    elif date == 'both':
        pid_5_on = ''
        pid_2_on = ''
#        pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\\Humidity Cals\Isoprene = 0.0\\'
        pathL = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data//201509//Humidity Cals/Isoprene = 0.0//'    

        filenameL1 = 'd2015test.txt'
        filenameL2 = 'd20150904_0big(post 0903).txt'
        print '\nReading Data...'
        dataL1 = pd.read_csv(pathL+filenameL1)
        dataL2 = pd.read_csv(pathL+filenameL2)
        print '\nMerging DataFrames...'
        dataL1.columns = ['TheTime','pid2','pid3','pid4','mfcloR','mfchiR','mfclo','Temp','RH']
        dataL1 = dataL1.drop(['pid2'],1)

        dataL2.index = xrange(len(dataL1),len(dataL1)+len(dataL2))
        dataL = pd.concat([dataL1,dataL2])
        date = 905


    else:

        try:
            filenameL ='/d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
#            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals'+date[0:2]
            pathL = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data//201509//Humidity Cals'+date[0:2]
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)
            
        except IOError:
#            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
            pathL = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data//2015'+date[0:2]
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)
            
        except IOError:
#            pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
            pathL = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/RH_tests/Raw_Data//2015'+date[0:2]
            filenameL ='/d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
            print '\nReading Data...'
            dataL = pd.read_csv(pathL+filenameL)
            

elif Questions == 'N':
    date = '0924'
    filenameL = '2'
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\201509\Humidity Cals\\d2015'+date
    path = pathL+'_0'+filenameL
    print '\nReading Data...'
    dataL = pd.read_csv(path)
else:
    dataL = pd.read_csv('C:\\Users\\mat_e_000\\Google Drive\\Bursary\\Data_Analysis\\RH_tests\\Raw_Data\\201509\\Humidity Cals\\d20150917_04',sep=',')
    date = '0918'
print '\nCorrecting different Pid Labels and interpolating nans...'

if np.nanstd(dataL.mfcloR)/len(dataL) > 0.00003:
    proceed = raw_input('Sorry this doesn\'t look like an RH cal file, the isop level changes too much\n\nWould you like to proceed? ')
else:
    proceed = 'Y'
    
if proceed.upper() == 'Y' or proceed.upper() == 'YES':
    
    dataL.mfcloR = nan_helper(dataL.mfcloR,10,3)
    isop_cyl = 13.277	#ppbv
    mfchi_range = 100.	#sccm
    mfchi_sccm = dataL.mfchiR*(mfchi_range/5.)
    
    mfclo_range = 20.	#sccm
    mfclo_sccm = dataL.mfcloR*(mfclo_range/5.)
    
    dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
    isop_mr = dil_fac*isop_cyl
    
    Isop = np.nanmean(isop_mr)
    
    #Finds when the isoprene set point changes for a new cal.
    for i in xrange(0,len(isop_mr)):
        if isop_mr[i] > Isop + 0.25 or isop_mr[i] < Isop - 0.25:
            cal_cut_off = i + 50
        if isop_mr[i+1] < Isop + 0.25 and isop_mr[i+1] > Isop - 0.25:
            break
    try:
        if cal_cut_off > len(dataL)/2: 
            dataL = dataL[:cal_cut_off]
            dataL.index = xrange(0,len(dataL))  
        if cal_cut_off < len(dataL)/2:      
            dataL = dataL[cal_cut_off:]
            dataL.index = xrange(0,len(dataL)) 
    except NameError:
        pass
        
    Isop = np.nanmean(isop_mr)
    Isop_Error = np.nanstd(isop_mr)/np.sqrt(len(dataL)) 
    
    
    
    pids_on_new = []
    for num in pids_on:
        try:
            dataL['pid%s'%str(num)]
            pids_on_new.append(num)
        except KeyError:
            pass
            
    pids_on = pids_on_new
    pid_data = {num : nan_helper(dataL['pid%s'%(str(num))],10,3) for num in pids_on} # uses nan helper here

                    
    ############## ############## ############## ############## ############## 
    
    
    
    print '\nFormatting data...'
    
            
    ############## Formatting the Time ############## ##############   
    TimeL = dataL.TheTime-dataL.TheTime[0]
    TimeL*=60.*60.*24.
    
    dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
    T1 = pd.datetime(1899,12,30,0)
    T2 = pd.datetime(1970,01,01,0)
    offset=T1-T2
    dataL.TheTime+=offset
    ############## ############## ############## ############## 
    
    
    
    
    
    ############## Converting RH Voltage to RH % ############## 
    dataL.RH = nan_helper(dataL.RH,10,3) # RH correction
#     RH = dataL.RH
#     RH /=4.96
#     RH -= 0.16
#     RH /= 0.0062
#     
#     dataL.Temp *=10
#     RH /= (1.0546-(0.00216*dataL.Temp)) # Temperature correction
    
    RH = (((dataL.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*dataL.Temp*10.)
    ############## ############## ############## ############## 
    
    
    
    
    
    ############## ############## Trying to find where the RH changes Drastically (for new cal Points) ############## ############## 
    print '\nSelecting cal points...'
    
    RH_set = []
    
    timing = 150 

    sensitivity_mean = np.nanmean([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)]) # the mean of the rolling mean
    sensitivity_std = np.nanstd([abs(RH[i+timing]-RH[i]) for i in xrange(0,len(RH)-timing,timing)]) # the standard of the rolling standard

    
    #finds where the drastic changes are in the RH data        
    for i in xrange(0,len(RH)-timing,timing):
        if abs(RH[i]-RH[i+timing]) >= sensitivity_mean+sensitivity_std:
            RH_set.append(i)
            print 'appending',i

            
    
    Setters = []
    for i in xrange(0,len(RH_set)):
        if abs(RH_set[i-1]-RH_set[i]) > 300:
            Setters.append(i)
            
    
    RH_setF = [RH_set[i] for i in Setters]
    
    RH_setS = [i-data_point_length for i in RH_setF]
    
    if RH_setS[0]<0:
        SF = negative_remover(RH_setS,RH_setF)
        S = SF[0]
        F = SF[1]   
    else:
        S = RH_setS
        F = RH_setF
        
        
    print '\nAmmending bad cal points...' 
    
    
    
    
    RH_stds = [np.nanstd(RH[S[i]:F[i]]) for i in xrange(0,len(S))]
    
    
    # Ammends the bad cal points for all pids
    SF_indexes = pd.DataFrame(index = ['S','F'], columns = ['Pid%s'%num for num in pids_on])
    
    '''
    #SF = cal_point_ammender(RH,bad_cal_length,S,F)
    #SF_indexes['RH']['S'] = SF[0]
    #SF_indexes['RH']['F'] = SF[1]
    '''
    
    for num in pids_on:
        SF = cal_point_ammender(pid_data[num],bad_cal_length,S,F)
        SF_indexes['Pid%s'%num]['S'] = SF[0]
        SF_indexes['Pid%s'%num]['F'] = SF[1]
        
        
            
    diff = data_point_length   
    
    
    #Rolling Averages of the pids and RH
    Rolling_Averages = pd.DataFrame(index = pids_on+['RH'], columns = ['Rolling Average'])
    #Chunked up data for the pids and RH, for plotting
    Spliced_Data = pd.DataFrame(index = pids_on, columns = ['Pids','Pids listsout','Pid_Avgs','RH','RH listout','Isop listout','Times'])


    
    
    #filling the roling averages and spliced data dataframes
    

    
    Rolling_Averages['Rolling Average']['RH'] = pd.rolling_mean(RH,200,20)
    
    for num in pids_on:
            Rolling_Averages['Rolling Average'][num] = pd.rolling_mean(pid_data[num],200,20)
            
        
            Spliced_Data['Times'][num] = list_multisplicer(dataL.TheTime,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
            
            Spliced_Data['RH'][num] = list_multisplicer(RH,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
            Spliced_Data['RH listout'][num] = list_multisplicer_listsout(RH,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
            
            Spliced_Data['Isop listout'][num] = list_multisplicer_listsout(isop_mr,SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
            
            Spliced_Data['Pids'][num] = list_multisplicer(pid_data[num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
            Spliced_Data['Pids listsout'][num] = list_multisplicer_listsout(pid_data[num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
        
            Spliced_Data['Pid_Avgs'][num] = list_multisplicer(Rolling_Averages['Rolling Average'][num],SF_indexes['Pid%s'%num]['S'],SF_indexes['Pid%s'%num]['F'])
    
    print '\nCreating cal_df...'
    
    
    
    ############## ############## ############## ############## ############## ############## ############## ############## 
    #Calculating the mean of the data in the chunks for the cal points
    Voltages = pd.DataFrame({'Pid%s Voltage'%num : [np.nanmean(i) for i in Spliced_Data['Pids listsout'][num]] for num in pids_on})
    
    # Calculating the standard errors for the cal points
    Errors = pd.DataFrame({'Pid%s Stderr'%num : [np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['Pids listsout'][num]] for num in pids_on})
    
    #Finding time at Start and end of cal points
    Start_Times = pd.DataFrame({'Start Time': [TimeL[i] for i in S]})
    End_Times = pd.DataFrame({'End Time': [TimeL[i] for i in F]})
    
    #Finding the mean of the isoprene in the chunks and the standard error (like Voltages adn Errors)
    Isoprene_error = pd.DataFrame({'Isop Error': [np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['Isop listout'][num]]})
    Isoprene = pd.DataFrame({'Isop': [np.nanmean(i) for i in Spliced_Data['Isop listout'][num]]})

    #Average  RH for the chunks
    cal_RH = pd.DataFrame({'RH':[np.nanmean(i) for i in Spliced_Data['RH listout'][num]]})
    Error_RH = pd.DataFrame({'RH Stderr':[np.nanstd(i)/np.sqrt(data_point_length) for i in Spliced_Data['RH listout'][num]]})   
    #merges above dataframes into one (for corrected and uncorrected data)
    cal_df = pd.concat([Start_Times,End_Times,Isoprene,Isoprene_error,cal_RH,Error_RH,Voltages, Errors], axis=1, join='inner')

    ############## ############## Deciding the columns in cal_df and chunking the data ############## ############## 
        
    RH_fit = [0.,np.max(cal_df.RH)]

    

    xerr = [cal_df['RH Stderr'][i] for i in xrange(0,len(cal_df))]
    
    #Values of Slopes, Intercepts and errors
    Values = pd.DataFrame(index = pids_on, columns = ['Slopes','Slope Errors','Intercepts','Intercept Errors'])
    
    
    

    
    
    
    pid_fits = {num:[] for num in pids_on}
    
    print '\tFinding slope and intercepts...'
    
    xdata = [i for i in cal_df['RH']]
    
    for num in pids_on:
            
            yerr = [cal_df['Pid%s Stderr'%str(num)][i] for i in xrange(0,len(cal_df))]
            
            ydata = [i for i in cal_df['Pid%s Voltage'%num]] 
            
            initial_estimates = np.polyfit(cal_df['RH'],ydata,1)
            
            datac = odr.RealData(x = xdata,y =ydata,sx = cal_df['RH Stderr']*np.sqrt(data_point_length),sy = cal_df['Pid%s Stderr'%str(num)]*np.sqrt(data_point_length))
            fit = odr.ODR(datac,linear,initial_estimates)
            params = fit.run()
            
                
            pid_fits[num] = [params.beta[1],(np.max(cal_df.RH)*params.beta[0])+params.beta[1]]    
            
            
            
            
            Values['Intercepts'][num] = "%.2g" % params.beta[1]
            Values['Slopes'][num]= "%.3g" % params.beta[0]
            Values['Slope Errors'][num] = "%.1g" % params.sd_beta[0]
            Values['Intercept Errors'][num] = "%.1g" % params.sd_beta[1]


    
 
    
print '\nPlotting...'    
for num in pids_on:    
    plotter(num)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    