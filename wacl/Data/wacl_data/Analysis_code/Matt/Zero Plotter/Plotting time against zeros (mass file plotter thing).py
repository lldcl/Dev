import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
#from scipy import stats
#import time
import matplotlib.patches as mpatches
stitch = 'Y'

############ Plotting the data together onto one graph
#########################################


filename1 = '\d20150710_034'
filename2 = '\d20150713_015'
path = 'E:\Bursary thing\PID Data\RAW'

data1 = pd.read_csv(path+filename1)
data2 = pd.read_csv(path+filename2) #reading both files

Time1 = pd.to_datetime(data1.TheTime,unit='D')
Time2 = pd.to_datetime(data2.TheTime,unit='D')

data1.TheTime = pd.to_datetime(data1.TheTime,unit='D') #converting the readings to a date and time
data2.TheTime = pd.to_datetime(data2.TheTime, unit='D')


filename3 = '\d20150713_01'
filename4 = '\d20150713_02'

tmp_pid1 = data1.pid1.notnull() #exludes any missing values
tmp_pid2 = data1.pid2.notnull() 
tmp_flow = data1.mfchiR.notnull()


tmp2_pid1 = data2.pid1.notnull() 
tmp2_pid2 = data2.pid2.notnull() 
tmp2_flow = data2.mfchiR.notnull()

if (stitch == 'Y'):
        
        fig1 = plt.figure()        
        ax1 = fig1.add_subplot(111)

	pid_avg = pd.rolling_mean(data1.pid1,100)
	pid2_avg = pd.rolling_mean(data1.pid2,100)
	
	pid_avg2 = pd.rolling_mean(data2.pid1,100)
	pid2_avg2 = pd.rolling_mean(data2.pid2,100)
	
        ###Data Set 1 PID1
	pid = ax1.plot(Time1[tmp_pid1],data1.pid1[tmp_pid1], linewidth=1,color='r') #plotting the time from data 1 against the pid1 values that aren't null
	pid_10s = ax1.plot(Time1[tmp_pid1],pid_avg[tmp_pid1], linewidth=1,color='b') #plotting the time from data 1 against the rolling average for pid 1
	##PID 2
	pid2 = ax1.plot(Time1[tmp_pid2],data1.pid2[tmp_pid2], linewidth=1, color='g') #plotting the time from data 1 against the pid 2 values that aren't null
	pid2_10s = ax1.plot(Time1[tmp_pid2],pid2_avg[tmp_pid2], linewidth=1,color='b')

        ###Data Set 2 PID 1
	pidb = ax1.plot(Time2[tmp2_pid1],data2.pid1[tmp2_pid1], linewidth=1,color='r')
	pid_10sb = ax1.plot(Time2[tmp2_pid2],pid_avg2[tmp2_pid1], linewidth=1,color='b')
	##PID 2
	pidb2 = ax1.plot(Time2[tmp2_pid2],data2.pid2[tmp2_pid2],linewidth=1,color='g')
	pid2_10sb = ax1.plot(Time2[tmp2_pid2],pid2_avg2[tmp2_pid2], linewidth=1,color='b')
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])


for i in range (1,15):
    filenamei = '\d20150713_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])



for i in range (3,18):
    filenamei = '\d20150710_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])

for i in range (1,10):
    filenamei = '\d20150714_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")

	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])

for i in range (1,14):
    filenamei = '\d20150715_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])

for i in range (1,9):
    filenamei = '\d20150716_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])

for i in range (1,6):
    filenamei = '\d20150717_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])
	
for i in range (1,10):
    filenamei = '\d20150720_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


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
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])
	
for i in range (1,2):
    filenamei = '\d20150721_0'+str(i)
    cal = 'Y'
    plots = 'Y'


    datai = pd.read_csv(path+filenamei)


    Timei = pd.to_datetime(datai.TheTime,unit='D')


    datai.TheTime = pd.to_datetime(datai.TheTime, unit='D')


    tmpi_pid1 = datai.pid1.notnull()
    tmpi_pid2 = datai.pid2.notnull()
    tmpi_flow = datai.mfchiR.notnull()



    #############################
    ## Plots
    if (plots == 'Y'):
    
	pid1_avgi = pd.rolling_mean(datai.pid1,100)
   	pid2_avgi =pd.rolling_mean(datai.pid2,100)

	
	

	
	###Data Set 3 PID 1
	pid = ax1.plot(Timei[tmpi_pid1],datai.pid1[tmpi_pid1], linewidth=1, color = 'c')
	pid1_10s = ax1.plot(Timei[tmpi_pid1],pid1_avgi[tmpi_pid1], linewidth=1,color='b')
	##PID 2
	pid2 = ax1.plot(Timei[tmpi_pid2],datai.pid2[tmpi_pid2],linewidth=1,color='c')
	pid2_10s = ax1.plot(Timei[tmpi_pid2],pid2_avgi[tmpi_pid2], linewidth=1,color='b')

	
	
	plt.ylabel("PID / V")
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)


	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)
	
	red_line = mpatches.Patch(color='red', label='Pid1 Data')
	green_line = mpatches.Patch(color='green', label='Pid2 Data')
	plt.legend(handles=[red_line, green_line])

plt.show()
