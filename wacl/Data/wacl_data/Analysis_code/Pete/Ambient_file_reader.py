import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Ambient_experiments_june2016/'

filename = 'ambient_exp_20160628_02'
print filename
#read file into dataframe
data = pd.read_csv(path+filename)

#dT = seconds since file start
dT = data.TheTime-data.TheTime[0]
dT*=60.*60.*24.

#convert daqfac time into real time pd.datetime object
data.TheTime = pd.to_datetime(data.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data.TheTime+=offset

ave_time = ('30S')
data_av = data.copy(deep=True)
data_av = data_av.set_index(data_av.TheTime,drop=False)
data_av = data_av.resample(ave_time, how='mean',fill_method='pad')
ave_time = pd.Series(data_av.index,name='TheTime',index=data_av.index)
data_av = pd.concat([data_av,ave_time],axis=1)



#plot up the pid voltages
sensorfig = plt.figure()
ax1 = sensorfig.add_subplot(111)
sensor_av = ['MOSar1','MOSar2','MOSar3','MOSar4','MOSar5','MOSar6','MOSar7','MOSar8']
for s in sensor_av:
	ax1.plot(data_av.TheTime,data_av[s],linewidth=3)
plt.ylabel("Sensor / V")
plt.xlabel("The Time / GMT")


varfig = plt.figure()
ax1 = varfig.add_subplot(111)
var_av = ['Temp','RH']
for v in var_av:
	ax1.plot(data_av.index,data_av[v],linewidth=3)
plt.ylabel("Temp / RH")
plt.xlabel("Index")


plt.show()