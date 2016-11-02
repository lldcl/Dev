import pandas as pd
import matplotlib.pyplot as plt
from time import strftime



google_drive_path = 'C:\Users\mat_e_000\Google Drive\Bursary'





date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')

try:
    pathL = google_drive_path+'\Data_Analysis\Raw_data_files\\2015'+date[0:2]
    filenameL ='\d20' + str((strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
    dataL = pd.read_csv(pathL+filenameL)
    
except IOError:
    pathL = google_drive_path+'\Data_Analysis\RH_tests\Raw_Data\\2015'+date[0:2]
    dataL = pd.read_csv(pathL+filenameL)
    



RH = dataL.RH
RH -= 0.826
RH /= 31.482E-3

Isop = dataL.mfcloR
Isop *= 0.2

pid2_rolling_avg = pd.rolling_mean(dataL.pid1,300)
pid3_rolling_avg = pd.rolling_mean(dataL.pid2,300)
pid4_rolling_avg = pd.rolling_mean(dataL.pid3,300)

figRH = plt.figure()
ax1RH = figRH.add_subplot(211)
plt.title('Relative Humidity / %')
ax1RH.plot(dataL.TheTime,RH)
ax1RH.plot(dataL.TheTime,Isop)



ax2RH= figRH.add_subplot(212)
plt.title('Pids\' Rolling Means')
ax2RH.plot(dataL.TheTime,pid2_rolling_avg,color='b')
ax2RH.plot(dataL.TheTime,pid3_rolling_avg,color='r')
ax2RH.plot(dataL.TheTime,pid4_rolling_avg,color='g')

plt.show()