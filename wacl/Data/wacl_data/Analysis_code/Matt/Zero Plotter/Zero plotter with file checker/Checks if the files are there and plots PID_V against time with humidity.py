import pandas as pd
from time import strftime
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def FileChecker(path,month1, month2, day1,day2,number_of_files):
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
    if day1 < 0:
        day1 = 0
    if day2 > 31:
        day2 = 31
    
    for month in range(month1, month2):
        if month < 10:
            month = '0'+str(month)
        path1 = path + '\\2015'+str(month)+'\\d2015'+str(month)
        for day in range (day1,day2):
            if day < 10:
                day = '0'+str(day)
            path2 = path1 + str(day)
            for filenumber in range(0,number_of_files):
                pfl.append(path2+'_0'+str(filenumber))
   
    p = []
    for i in range (0,len(pfl)):   
        p.append(os.path.exists(pfl[i]))
      
    for i in range(0,len(pfl)):
        if p[i] == True:
            filesl.append(pfl[i])
            
    return filesl
    
path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data'    
figRH = plt.figure()
 
ax1RH = figRH.add_subplot(311)
plt.title('Relative Humidity / %')
ax2RH= figRH.add_subplot(312)
plt.title('Pids Raw Data')
ax3RH = figRH.add_subplot(313)   

filesl = FileChecker(path,9,9,1,9,19)


for filei in filesl:
    datai = pd.read_csv(filei)
    if len(filei) == 91:
        date = filei[-7:-3]
        filenumber = filei[-2:]    
    elif len(filei) == 92:
        date = filei[-8:-4]
        filenumber = filei[-3:]
    print str(date)+'_'+str(filenumber)
    if int(date) < 904:
        pid_5_on = ''
        try:
            pid2d = datai.pid1.fillna(pd.rolling_mean(datai.pid1, 7, min_periods=1).shift(-3))
        except AttributeError:
            pid_2_on = ''  
        try:   
            pid3d = datai.pid2.fillna(pd.rolling_mean(datai.pid2, 7, min_periods=1).shift(-3))
        except AttributeError:
            pid_3_on = ''  
            
        try:    
            pid4d = datai.pid3.fillna(pd.rolling_mean(datai.pid3, 7, min_periods=1).shift(-3))
        except AttributeError:
            pid_4_on = ''    
                
    if int(date) >= 904:
        pid_2_on = ''
        try:
            pid5d = datai.pid5.fillna(pd.rolling_mean(datai.pid5, 7, min_periods=1).shift(-3))
        except AttributeError:
            pid_5_on = ''    

            
        try:   
            pid3d = datai.pid3.fillna(pd.rolling_mean(datai.pid3, 7, min_periods=1).shift(-3))
        except AttributeError:
            pid_3_on = ''     
                
        try:   
            pid4d = datai.pid4.fillna(pd.rolling_mean(datai.pid4, 7, min_periods=1).shift(-3))
        except AttributeError:
            pid_4_on = ''   
            
    
    
    RH = datai.RH
    RH /=4.9
    RH -= 0.16
    RH /= 0.0062
    RH *= 100
    RH /= 103
    
    Isop = datai.mfcloR
    Isop *= 0.7
    
    datai.TheTime = pd.to_datetime(datai.TheTime,unit='D')
    T1 = pd.datetime(1899,12,30,0)
    T2 = pd.datetime(1970,01,01,0)
    offset=T1-T2
    datai.TheTime+=offset
    
    #pid2_rolling_avg = pd.rolling_mean(datai.pid1,300)
    pid3_rolling_avg = pd.rolling_mean(pid3d,300)
    pid4_rolling_avg = pd.rolling_mean(pid4d,300)
    if pid_5_on == 'Y':
        pid5_rolling_avg = pd.rolling_mean(pid5d,300)
    
    
    

    ax1RH.plot(datai.TheTime,RH,color = 'b')

    
    
    

    
    #ax2RH.plot(datai.TheTime,datai.pid1,color = 'k')
    ax2RH.plot(datai.TheTime,pid3d,color = 'b')
    ax2RH.plot(datai.TheTime,pid4d,color = 'm')
    if pid_5_on == 'Y':
        ax2RH.plot(datai.TheTime,pid5d,color = 'k')
    
    pid3 = mpatches.Patch(label='Pid 3', color = 'b')
    pid4 = mpatches.Patch(label='Pid 4', color = 'm')
    if pid_5_on == 'Y':
        pid5 = mpatches.Patch(label='Pid 5', color = 'k')

    
    
    #ax3RH.plot(datai.TheTime,pid2_rolling_avg,color='k')
    ax3RH.plot(datai.TheTime,pid3_rolling_avg,color='b')
    ax3RH.plot(datai.TheTime,pid4_rolling_avg,color='m')
    if pid_5_on == 'Y':
        ax3RH.plot(datai.TheTime,pid5_rolling_avg,color='k')



plt.show()
    
    
    
    
    