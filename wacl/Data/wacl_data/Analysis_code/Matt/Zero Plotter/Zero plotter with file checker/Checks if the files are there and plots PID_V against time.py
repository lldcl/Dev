import pandas as pd
import matplotlib.pyplot as plt
from time import strftime
import os
import matplotlib.patches as mpatches
stitch = 'Y'




filesl=[]
pfl = []
day = strftime('%d')
day = int(day)



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
            print path2
            for filenumber in range(0,number_of_files):
                pfl.append(path2+'_0'+str(filenumber))

        
    p = []
    for i in range (0,len(pfl)):   
        p.append(os.path.exists(pfl[i]))
      
    for i in range(0,len(pfl)):
        if p[i] == True:
            filesl.append(pfl[i])
            
    return filesl
        
filesl = FileChecker('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files',9,9,0,10,15)        

fig1 = plt.figure()        
ax1 = fig1.add_subplot(111)


for i in range(0,len(filesl)):
    filenamei = filesl[i]
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(filenamei, engine = 'c')
    
    try:


        Timei = pd.to_datetime(datai.TheTime,unit='D')
    
    
        datai.TheTime = pd.to_datetime(datai.TheTime, unit='D')
    
    
        tmpi_pid1 = datai.pid1.notnull()
        tmpi_pid2 = datai.pid2.notnull()
        tmpi_flow = datai.mfchiR.notnull()
    
    
    
        #############################
        ## Plots
        if (stitch == 'Y'):
    
           	pid1_avgi = pd.rolling_mean(datai.pid1,100)
               	pid2_avgi =pd.rolling_mean(datai.pid2,100)
           	
            
           	
           	###Data Set 3 PID 1
           	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'r')
           	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
           	##PID 2
           	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='g')
           	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')
            
           	
           	
           	plt.ylabel("PID / V")
           	ax1.set_ylim([0.052, 0.074])
           	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
            
            
           	ax2.yaxis.tick_right()
           	ax2.yaxis.set_label_position("right")
           	
           	plt.ylabel("Isop / ppb")
           	plt.xlabel('Time / s', fontsize = 20)
           	
           	red_line = mpatches.Patch(color='red', label='Pid1 Data')
           	green_line = mpatches.Patch(color='green', label='Pid2 Data')
           	plt.legend(handles=[red_line, green_line])
	
        plt.show()
    except:
        pass


