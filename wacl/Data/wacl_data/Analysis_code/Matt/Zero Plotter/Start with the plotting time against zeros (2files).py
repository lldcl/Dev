import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
#from scipy import stats
#import time
import matplotlib.patches as mpatches

filename1 = '\d20150710_034'
filename2 = '\d20150713_015'
filename3 = '\d20150713_01'
filename4 = '\d20150713_02'

path = 'C:\Users\Matt\Python stuff and data\PID data\Calibration Graphs\Zeros'
path2 = 'C:\Users\Matt\Python stuff and data\PID data\Calibration Graphs'
'''filename1 = '\d2015' + raw_input('What date would you like to load from?\nPlease enter the date in the  form mmdd: ') + '_0' + raw_input('Which file would you like to load? ')
filename2 = '\d2015' + raw_input('What date would you like to load from?\nPlease enter the date in the  form mmdd: ') + '_0' + raw_input('Which file would you like to load? ')


def filechooser(n,m):
    data ={}
    while n<=m:
        filenamen = '\d20150713_0'+str(n)
        x = 'I:\PID data' + filenamen
        datan = pd.read_csv(x)
        data = [datan]
        return data
        n=n+1
filechooser(1,13)'''


cal = 'Y'
plots = 'Y'
print "\nThis is the file reference", path + filename1

data1 = pd.read_csv(path+filename1)
data2 = pd.read_csv(path+filename2) #reading both files
data3 = pd.read_csv(path2+filename3)
data4 = pd.read_csv(path2+filename4)

Time1 = pd.to_datetime(data1.TheTime,unit='D')
Time2 = pd.to_datetime(data2.TheTime,unit='D')
Time3 = pd.to_datetime(data3.TheTime,unit='D')
Time4 = pd.to_datetime(data4.TheTime,unit='D')

data1.TheTime = pd.to_datetime(data1.TheTime,unit='D') #converting the readings to a date and time
data2.TheTime = pd.to_datetime(data2.TheTime, unit='D')
data3.TheTime = pd.to_datetime(data3.TheTime, unit='D')
data4.TheTime = pd.to_datetime(data4.TheTime, unit='D')



tmp_pid1 = data1.pid1.notnull() #exludes any missing values
tmp_pid2 = data1.pid2.notnull() 
tmp_flow = data1.mfchiR.notnull()


tmp2_pid1 = data2.pid1.notnull() 
tmp2_pid2 = data2.pid2.notnull() 
tmp2_flow = data2.mfchiR.notnull()

tmp3_pid1 = data3.pid1.notnull()
tmp3_pid2 = data3.pid2.notnull()
tmp3_flow = data3.mfchiR.notnull()

tmp4_pid1 = data4.pid1.notnull()
tmp4_pid2 = data4.pid2.notnull()
tmp4_flow = data4.mfchiR.notnull()


#############################
## Plots
if (plots == 'Y'):

	pid_avg = pd.rolling_mean(data1.pid1,100)
	pid2_avg = pd.rolling_mean(data1.pid2,100)
	
	pid_avg2 = pd.rolling_mean(data2.pid1,100)
	pid2_avg2 = pd.rolling_mean(data2.pid2,100)
	
	pid_avg3 = pd.rolling_mean(data3.pid1,100)
	pid2_avg3 =pd.rolling_mean(data3.pid2,100)
	
	pid_avg4 = pd.rolling_mean(data4.pid1,100)
	pid2_avg4 =pd.rolling_mean(data4.pid2,100)

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	
	
	###Data Set 1 PID1
	pid = ax1.plot(Time1[tmp_pid1],data1.pid1[tmp_pid1], linewidth=1,color='r') #plotting the time from data 1 against the pid1 values that aren't null
	pid_10s = ax1.plot(Time1[tmp_pid1],pid_avg[tmp_pid1], linewidth=2,color='b') #plotting the time from data 1 against the rolling average for pid 1
	##PID 2
	pid2 = ax1.plot(Time1[tmp_pid2],data1.pid2[tmp_pid2], linewidth=1, color='g') #plotting the time from data 1 against the pid 2 values that aren't null
	pid2_10s = ax1.plot(Time1[tmp_pid2],pid2_avg[tmp_pid2], linewidth=2,color='b')

        ###Data Set 2 PID 1
	pidb = ax1.plot(Time2[tmp2_pid1],data2.pid1[tmp2_pid1], linewidth=1,color='r')
	pid_10sb = ax1.plot(Time2[tmp2_pid2],pid_avg2[tmp2_pid1], linewidth=2,color='b')
	##PID 2
	pidb2 = ax1.plot(Time2[tmp2_pid2],data2.pid2[tmp2_pid2],linewidth=1,color='g')
	pid2_10sb = ax1.plot(Time2[tmp2_pid2],pid2_avg2[tmp2_pid2], linewidth=2,color='b')
	
	###Data Set 3 PID 1
	pidc = ax1.plot(Time3[tmp3_pid1],data3.pid1[tmp3_pid1], linewidth=1, color = 'c')
	pid2_10sc = ax1.plot(Time3[tmp3_pid1],pid2_avg3[tmp3_pid1], linewidth=2,color='b')
	##PID 2
	pidc2 = ax1.plot(Time3[tmp3_pid2],data3.pid2[tmp3_pid2],linewidth=1,color='c')
	pid2_10sb = ax1.plot(Time3[tmp3_pid2],pid2_avg3[tmp3_pid2], linewidth=2,color='b')
	
	###Data Set 4 PID 1
	pidd = ax1.plot(Time4[tmp4_pid1],data4.pid1[tmp4_pid1], linewidth=1, color = 'c')
	pid2_10sd = ax1.plot(Time4[tmp4_pid1],pid2_avg4[tmp4_pid1], linewidth=2,color='b')
	##PID 2
	pidd2 = ax1.plot(Time4[tmp4_pid2],data4.pid2[tmp4_pid2],linewidth=1,color='c')
	pid2_10sc = ax1.plot(Time4[tmp4_pid2],pid2_avg4[tmp4_pid2], linewidth=2,color='b')
	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])


#plt.ylim(0,1e-4)

	plt.show()
