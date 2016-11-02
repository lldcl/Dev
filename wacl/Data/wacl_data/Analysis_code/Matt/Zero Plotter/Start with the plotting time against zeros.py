import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
import time
import matplotlib.patches as mpatches

#############################
## Data read

bss = '\ko'

path = 'E:\Bursary thing\PID Data\RAW'
filename1 = '\d20150818_03'
'''filename2 = '\d2015' + raw_input('What date would you like to load from?\nPlease enter the date in the  form mmdd: ') + '_0' + raw_input('Which file would you like to load? ')'''
 
cal = 'Y'
plots = 'Y'
print "\nThis is the file reference", path + filename1
data1 = pd.read_csv(path+filename1) #reading file
data2 = pd.read_csv


Time = pd.to_datetime(data1.TheTime,unit='D')
data1.TheTime = pd.to_datetime(data1.TheTime,unit='D') #converting the data to a date and time

T1 = pd.datetime(1899,12,30,0) 
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1.TheTime+=offset

tmp_pid = data1.pid1.notnull() #finds any missing PID values
tmp_pid2 = data1.pid2.notnull() 



std1 = np.std(data1.pid1)
mean1 = np.mean(data1.pid1)


print 'Standard Dev of pid1:', std1
print 'Mean of pid1:', mean1





#############################
## Plots
if (plots == 'Y'):

	pid_avg = pd.rolling_mean(data1.pid1,100)
	pid2_avg = pd.rolling_mean(data1.pid2,100)

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	pid = ax1.plot(Time[tmp_pid],data1.pid1[tmp_pid], linewidth=3,color='r')
	pid_10s = ax1.plot(Time[tmp_pid],pid_avg[tmp_pid], linewidth=3,color='b')
	pid2 = ax1.plot(Time[tmp_pid2],data1.pid2[tmp_pid2], linewidth  =3, color='g')
	pid2_10s = ax1.plot(Time[tmp_pid2],pid2_avg[tmp_pid2], linewidth=3,color='b')
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
