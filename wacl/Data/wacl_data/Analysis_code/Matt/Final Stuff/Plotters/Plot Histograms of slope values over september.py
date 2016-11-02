import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

ylim1 = -5e-4
ylim2 = 6e-4

xlim1 = np.datetime64('2015-09-02')
xlim2 = np.datetime64('2015-09-22')




def timeconverter(T):

   	return (datetime.strptime(T,"%Y-%m-%d %H:%M:%S.%f"))

humid_correct = 'Y'


path = 'C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis'
filename = '\Slopes'
filenamec = '\Slopes Corrected'

dataS = pd.read_csv(path+'\\'+filename+'.txt',sep='\t')

for i in xrange(0,len(dataS['The Time'])):
    if str(dataS['The Time'][i])[-3:] == '999':
        dataS.loc[i,'The Time'] = dataS.loc[i,'The Time'][:-3]


for x in xrange(0,len(dataS)):
    dataS.loc[x,'The Time'] = timeconverter(dataS.loc[x,'The Time'])



if humid_correct == 'Y':
    dataSc = pd.read_csv(path+filenamec+'.txt',sep='\t')

for i in xrange(0,len(dataSc['The Time'])):
    if str(dataSc['The Time'][i])[-3:] == '999':
        dataSc.loc[i,'The Time'] = dataSc.loc[i,'The Time'][:-3]
        
for x in xrange(0,len(dataSc)):
    dataSc.loc[x,'The Time'] = timeconverter(dataSc.loc[x,'The Time'])    
        
    
try:
    Slope3_mean = np.nanmean(dataS['Slope 3'][5:])
except:
    pass
    
try:
    Slope4_mean = np.nanmean(dataS['Slope 4'][5:])
except:
    pass
    
try:
    Slope5_mean = np.nanmean(dataS['Slope 5'][5:])
except:
    pass
if humid_correct == 'Y':
    Slope3c_mean = np.nanmean(dataSc['Slope 3'][5:])
    Slope4c_mean = np.nanmean(dataSc['Slope 4'][5:])
    Slope5c_mean = np.nanmean(dataSc['Slope 5'][5:])


fig1 = plt.figure()
plt.title('Raw')
ax1a = fig1.add_subplot(311)
ax1b = fig1.add_subplot(312)
ax1c = fig1.add_subplot(313)

ax1a.errorbar(dataS['The Time'],dataS['Slope 3'], yerr = dataS['Slope Error 3'], fmt='bo')
ax1a.axhline(Slope3_mean)
ax1a.set_ylim([ylim1,ylim2])
ax1a.set_xlim([xlim1,xlim2])

ax1b.errorbar(dataS['The Time'],dataS['Slope 4'], yerr = dataS['Slope Error 4'], fmt='ko')
ax1b.axhline(Slope4_mean)
ax1b.set_ylim([ylim1,ylim2])
ax1b.set_xlim([xlim1,xlim2])


ax1c.errorbar(dataS['The Time'],dataS['Slope 5'], yerr = dataS['Slope Error 5'], fmt='mo')
ax1c.axhline(Slope5_mean)
ax1c.set_ylim([ylim1,ylim2])
ax1c.set_xlim([xlim1,xlim2])

if humid_correct == 'Y':
    fig2 = plt.figure()
    plt.title('Corrected')
    ax2a = fig2.add_subplot(311)
    ax2b = fig2.add_subplot(312)
    ax2c = fig2.add_subplot(313)
    

    
    ax2a.errorbar(dataSc['The Time'],dataSc['Slope 3'], yerr = dataSc['Slope Error 3'], fmt='bo')
    ax2a.axhline(Slope3c_mean)
    ax2a.set_ylim([ylim1,ylim2])
    ax2a.set_xlim([xlim1,xlim2])
    
    ax2b.errorbar(dataSc['The Time'],dataSc['Slope 4'], yerr = dataSc['Slope Error 4'], fmt='ko')
    ax2b.axhline(Slope4c_mean)
    ax2b.set_ylim([ylim1,ylim2])
    ax2b.set_xlim([xlim1,xlim2])

    ax2c.errorbar(dataSc['The Time'],dataSc['Slope 5'], yerr = dataSc['Slope Error 5'], fmt='mo')
    ax2c.axhline(Slope5c_mean)
    ax2c.set_ylim([ylim1,ylim2])
    ax2c.set_xlim([xlim1,xlim2])
    
#    ax1a.set_ylim([-0.0001,0.00015])
#    ax2a.set_ylim([-0.0001,0.00015])
    
#    ax1b.set_ylim([-0.00001,0.00018])
#    ax2b.set_ylim([-0.00001,0.00018])
    
#    ax1c.set_ylim([0,0.00018])
#    ax2c.set_ylim([0,0.00018])

plt.show()
