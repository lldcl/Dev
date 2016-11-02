import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_data_files/'

filename1 = '201506/Labview_files/20150609_03'
data1 = pd.read_csv(path+filename1)

data1.Time = data1.Date-data1.Date[0]
data1.Time*=60.*60.*24.
data1f = data1.dropna(how='all')

data1f.Date = pd.to_datetime(data1f.Date,unit='D')
T1 = pd.datetime(1904,01,01,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1f.Date+=offset

BgT1=25
BgT2=225

bg1 = data1f.PID1_Corrected_Voltage.loc[(data1f.Time > BgT1) & (data1f.Time < BgT2)]
print filename1
print ' Background mean = ',bg1.mean()
print ' Standard deviation = ',bg1.std()
print ' Standard variance = ',bg1.var()
print ' Number of points avareged = ',bg1.count()
print '################################'

# data2 = pd.read_csv('/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_data_files/201506/20150603_02')
# data2f = data2.dropna(how='all')
# 
# ts2 = pd.to_datetime(data2f.Date,unit='D')
# ts2+=offset
# exT2 = ts2 - ts2[0]

filename2 = '201506/DAQfac_files/d20150610_01'
data2 = pd.read_csv(path+filename2)
Time2 = data2.TheTime-data2.TheTime[0]
Time2*=60.*60.*24.

data2.TheTime = pd.to_datetime(data2.TheTime,unit='D')
T21 = pd.datetime(1899,12,30,0)
T22 = pd.datetime(1970,01,01,0)
offset2=T21-T22
data2.TheTime+=offset2

bg2 = data2.pid1.loc[(Time2 > BgT1) & (Time2 < BgT2)]
print filename2
print ' Background mean = ',bg2.mean()
print ' Standard deviation = ',bg2.std()
print ' Standard variance = ',bg2.var()
print ' Number of points avareged = ',bg2.count()

plt.figure()
plt.plot(data1f.Time,data1f.PID1_Corrected_Voltage,color='r',linewidth=3)
plt.plot(Time2,data2.pid1,color='g',linewidth=3)
plt.plot([BgT1,BgT1],[0.08,0.12],linewidth=3,color='b')
plt.plot([BgT2,BgT2],[0.08,0.12],linewidth=3,color='b')
plt.ylabel('voltage / v', fontsize = 20)
plt.xlabel('Time / s', fontsize = 20)
plt.show()


