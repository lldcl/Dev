import pandas as pd
import matplotlib.pyplot as plt
from time import strftime
import matplotlib.patches as mpatches


date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')

try:
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Raw_data_files\\2015'+date[0:2]
    filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
    dataL = pd.read_csv(pathL+filenameL)
    
except IOError:
    pathL = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
    dataL = pd.read_csv(pathL+filenameL)
    



RH = dataL.RH
RH /=4.9
RH -= 0.16
RH /= 0.0062
RH *= 100
RH /= 103

Isop = dataL.mfcloR
Isop *= 0.7

dataL.TheTime = pd.to_datetime(dataL.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
dataL.TheTime+=offset

#pid2_rolling_avg = pd.rolling_mean(dataL.pid1,300)
pid3_rolling_avg = pd.rolling_mean(dataL.pid3,300)
pid4_rolling_avg = pd.rolling_mean(dataL.pid4,300)
pid5_rolling_avg = pd.rolling_mean(dataL.pid5,300)


figRH = plt.figure()
ax1RH = figRH.add_subplot(311)
plt.title('Relative Humidity / %')
ax1RH.plot(dataL.TheTime,RH,color = 'b')
ax1RH.plot(dataL.TheTime,Isop)



ax2RH= figRH.add_subplot(312)
plt.title('Pids Raw Data')

#ax2RH.plot(dataL.TheTime,dataL.pid1,color = 'k')
ax2RH.plot(dataL.TheTime,dataL.pid3,color = 'b')
ax2RH.plot(dataL.TheTime,dataL.pid4,color = 'm')
ax2RH.plot(dataL.TheTime,dataL.pid5,color = 'k')

pid3 = mpatches.Patch(label='Pid 3', color = 'b')
pid4 = mpatches.Patch(label='Pid 4', color = 'm')
pid5 = mpatches.Patch(label='Pid 5', color = 'k')
plt.legend(handles=[pid3,pid4,pid5],loc=2)

ax3RH = figRH.add_subplot(313)
#ax3RH.plot(dataL.TheTime,pid2_rolling_avg,color='k')
ax3RH.plot(dataL.TheTime,pid3_rolling_avg,color='b')
ax3RH.plot(dataL.TheTime,pid4_rolling_avg,color='m')
ax3RH.plot(dataL.TheTime,pid5_rolling_avg,color='k')
plt.legend(handles=[pid3,pid4,pid5],loc=2)


plt.show()