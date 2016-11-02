## The aim of this code is to select a certain amount of data and find an equation for the RH vs PID slope.
## then, plot the different intercepts over time.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats



path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201511/'

#filenames = ['d20151021_02','d20151021_03','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151023_01','d20151023_02','d20151023_03']
#filenames = ['d20151026_05']
#filenames = ['d20151023_02', 'd20151023_03', 'd20151022_04']
filenames = ['d20151111_03']
stat = 'Y'


for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

	#dT = seconds since file start
	dT = data.TheTime-data.TheTime[0]
	dT*=60.*60.*24.

	#convert daqfac time into real time pd.datetime object
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	#find all pids in file
	sub = 'pid'
	pids = [s for s in data.columns if sub in s]

	isop_cyl = 723.	#13.277	#ppbv
	mfchi_range = 2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	#mfcmid_range = 100. #sccm
	#mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
	#dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm + mfcmid_sccm)
	dil_fac = mfclo_sccm/(mfclo_sccm + mfchi_sccm)  ### Use for the files before the third mfc was introduced
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)
	
	

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH = (mean_resampled.RH)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

dRHdt = pd.Series(np.absolute(data_concat.RH.diff()),name='dRHdt')
dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')
nm_pts = 120./float(Time_avg[:-1])
dRH_ctr=0
for dp in dRHdt:
	if (dp>0.02):
		dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
	dRH_ctr+=1

data_concat = pd.concat([data_concat,dRHdt],axis=1,join_axes=[data_concat.index])
data_concat = pd.concat([data_concat,dRHdt_filt],axis=1,join_axes=[data_concat.index])
data_concat = data_concat.dropna()
#filter out periods when RH changes rapidly (dRHdt<0.2)
data_concat = data_concat[data_concat.dRHdt_filt == 0]

#plot up the pid voltages
# Create a figure instance
pidfig = plt.figure("PID voltage over time")
#Create the three subplots to appear in the same window
ax1 = pidfig.add_subplot(3,1,1)
ax2 = pidfig.add_subplot(3,1,2)
ax3 = pidfig.add_subplot(3,1,3)
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
RH = (((data_concat.RH/data_concat.VS)-0.16)/0.0062)/(1.0546-0.00216*data_concat.Temp)
ax1.plot(data_concat.index,data_concat.pid4, color="red",linewidth=3)
ax2.plot(data_concat.index, data_concat.pid5, color="green", linewidth=3)
ax3.plot(data_concat.index, data_concat.pid6, color="blue", linewidth=3)
ax4.plot(data_concat.index, RH, color="black", linewidth=2)
ax5.plot(data_concat.index, RH, color="black", linewidth=2)
ax6.plot(data_concat.index, RH, color="black", linewidth=2)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel('PID 6 / V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')
ax6.set_ylabel('RH %')



a = data_concat[0:2000]
b = data_concat[2001:4000]
c = data_concat[4001:6000]
d = data_concat[6001:8000]
e = data_concat[8001:10000]
f = data_concat[10001:12000]
g = data_concat[12001:14000]
h = data_concat[14001:16000]
i = data_concat[16001:18000]
j = data_concat[18001:20000]
k = data_concat[20001:22000]
l = data_concat[22001:]

RH = (((a.RH/a.VS)-0.16)/0.0062)/(1.0546-0.00216*a.Temp*10)
pid4 = a.pid4*1000
pid5 = a.pid5*1000
pid6 = a.pid6*1000

#### a
RHfig = plt.figure("Sections of the above data")
ax1 = RHfig.add_subplot(1,1,1)
ax1.scatter(RH, pid4, color='purple', linewidth=3)
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(RH, pid4)
ax1.set_xlabel(' RH %')
ax1.set_ylabel(' PID 4 / mv')
print ("Gradient PID 4:", slope1)
print ("R2 value pid 4:", R2value1)
print ("intercept pid 4:", intercept1)
ax1.plot([np.min(RH), np.max(RH)], [(slope1*np.min(RH))+intercept1, (slope1*np.max(RH))+intercept1])

RH = (((b.RH/b.VS)-0.16)/0.0062)/(1.0546-0.00216*b.Temp*10)
pid4 = b.pid4*1000
pid5 = b.pid5*1000
pid6 = b.pid6*1000

#### b
RHfigb = plt.figure("Sections of the above data b")
ax2 = RHfigb.add_subplot(1,1,1)
ax2.scatter(RH, pid4, color='purple', linewidth=3)
slope2, intercept2, R2value2, p_value2, st_err2 = stats.linregress(RH, pid4)
ax2.set_xlabel(' RH %')
ax2.set_ylabel(' PID 4 / mv')
print ("Gradient b PID 4:", slope2)
print ("R2 value b pid 4:", R2value2)
print ("intercept b pid 4:", intercept2)
ax2.plot([np.min(RH), np.max(RH)], [(slope2*np.min(RH))+intercept2, (slope2*np.max(RH))+intercept2])

##### c

RH = (((c.RH/c.VS)-0.16)/0.0062)/(1.0546-0.00216*c.Temp*10)
pid4 = c.pid4*1000
pid5 = c.pid5*1000
pid6 = c.pid6*1000


RHfigc = plt.figure("Sections of the above data c")
ax3 = RHfigc.add_subplot(1,1,1)
ax3.scatter(RH, pid4, color='purple', linewidth=3)
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(RH, pid4)
ax3.set_xlabel(' RH %')
ax3.set_ylabel(' PID 4 / mv')
print ("Gradient c PID 4:", slope3)
print ("R2 value c pid 4:", R2value3)
print ("intercept c pid 4:", intercept3)
ax3.plot([np.min(RH), np.max(RH)], [(slope3*np.min(RH))+intercept3, (slope3*np.max(RH))+intercept3])


#### d

RH = (((d.RH/d.VS)-0.16)/0.0062)/(1.0546-0.00216*d.Temp*10)
pid4 = d.pid4*1000
pid5 = d.pid5*1000
pid6 = d.pid6*1000


RHfigd = plt.figure("Sections of the above data d")
ax4 = RHfigd.add_subplot(1,1,1)
ax4.scatter(RH, pid4, color='purple', linewidth=3)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(RH, pid4)
ax4.set_xlabel(' RH %')
ax4.set_ylabel(' PID 4 / mv')
print ("Gradient d PID 4:", slope4)
print ("R2 value d pid 4:", R2value4)
print ("intercept d pid 4:", intercept4)
ax4.plot([np.min(RH), np.max(RH)], [(slope4*np.min(RH))+intercept4, (slope4*np.max(RH))+intercept4])

#### e

RH = (((e.RH/e.VS)-0.16)/0.0062)/(1.0546-0.00216*e.Temp*10)
pid4 = e.pid4*1000
pid5 = e.pid5*1000
pid6 = e.pid6*1000


RHfige = plt.figure("Sections of the above data e")
ax5 = RHfige.add_subplot(1,1,1)
ax5.scatter(RH, pid4, color='purple', linewidth=3)
slope5, intercept5, R2value5, p_value5, st_err5 = stats.linregress(RH, pid4)
ax5.set_xlabel(' RH %')
ax5.set_ylabel(' PID 4 / mv')
print ("Gradient e PID 4:", slope5)
print ("R2 value e pid 4:", R2value5)
print ("intercept e pid 4:", intercept5)
ax5.plot([np.min(RH), np.max(RH)], [(slope5*np.min(RH))+intercept5, (slope5*np.max(RH))+intercept5])

#### f

RH = (((f.RH/f.VS)-0.16)/0.0062)/(1.0546-0.00216*f.Temp*10)
pid4 = f.pid4*1000
pid5 = f.pid5*1000
pid6 = f.pid6*1000

RHfigf = plt.figure("Sections of the above data f")
ax6 = RHfigf.add_subplot(1,1,1)
ax6.scatter(RH, pid4, color='purple', linewidth=3)
slope6, intercept6, R2value6, p_value6, st_err6 = stats.linregress(RH, pid4)
ax6.set_xlabel(' RH %')
ax6.set_ylabel(' PID 4 / mv')
print ("Gradient f PID 4:", slope6)
print ("R2 value f pid 4:", R2value6)
print ("intercept f pid 4:", intercept6)
ax6.plot([np.min(RH), np.max(RH)], [(slope6*np.min(RH))+intercept6, (slope6*np.max(RH))+intercept6])

###### g

RH = (((g.RH/g.VS)-0.16)/0.0062)/(1.0546-0.00216*g.Temp*10)
pid4 = g.pid4*1000
pid5 = g.pid5*1000
pid6 = g.pid6*1000

RHfigg = plt.figure("Sections of the above data g")
ax7 = RHfigg.add_subplot(1,1,1)
ax7.scatter(RH, pid4, color='purple', linewidth=3)
slope7, intercept7, R2value7, p_value7, st_err7 = stats.linregress(RH, pid4)
ax7.set_xlabel(' RH %')
ax7.set_ylabel(' PID 4 / mv')
print ("Gradient g PID 4:", slope7)
print ("R2 value g pid 4:", R2value7)
print ("intercept g pid 4:", intercept7)
ax7.plot([np.min(RH), np.max(RH)], [(slope7*np.min(RH))+intercept7, (slope7*np.max(RH))+intercept7])


###### h

RH = (((h.RH/h.VS)-0.16)/0.0062)/(1.0546-0.00216*h.Temp*10)
pid4 = h.pid4*1000
pid5 = h.pid5*1000
pid6 = h.pid6*1000

RHfigh = plt.figure("Sections of the above data h")
ax8 = RHfigh.add_subplot(1,1,1)
ax8.scatter(RH, pid4, color='purple', linewidth=3)
slope8, intercept8, R2value8, p_value8, st_err8 = stats.linregress(RH, pid4)
ax8.set_xlabel(' RH %')
ax8.set_ylabel(' PID 4 / mv')
print ("Gradient h PID 4:", slope8)
print ("R2 value h pid 4:", R2value8)
print ("intercept h pid 4:", intercept8)
ax8.plot([np.min(RH), np.max(RH)], [(slope8*np.min(RH))+intercept8, (slope8*np.max(RH))+intercept8])


###### i

RH = (((i.RH/i.VS)-0.16)/0.0062)/(1.0546-0.00216*i.Temp*10)
pid4 = i.pid4*1000
pid5 = i.pid5*1000
pid6 = i.pid6*1000

RHfigi = plt.figure("Sections of the above data i")
ax9 = RHfigi.add_subplot(1,1,1)
ax9.scatter(RH, pid4, color='purple', linewidth=3)
slope9, intercept9, R2value9, p_value9, st_err9 = stats.linregress(RH, pid4)
ax9.set_xlabel(' RH %')
ax9.set_ylabel(' PID 4 / mv')
print ("Gradient i PID 4:", slope9)
print ("R2 value i pid 4:", R2value9)
print ("intercept 9 pid 4:", intercept9)
ax9.plot([np.min(RH), np.max(RH)], [(slope9*np.min(RH))+intercept9, (slope9*np.max(RH))+intercept9])


###### j

RH = (((j.RH/j.VS)-0.16)/0.0062)/(1.0546-0.00216*j.Temp*10)
pid4 = j.pid4*1000
pid5 = j.pid5*1000
pid6 = j.pid6*1000

RHfigj = plt.figure("Sections of the above data j")
ax10 = RHfigj.add_subplot(1,1,1)
ax10.scatter(RH, pid4, color='purple', linewidth=3)
slope10, intercept10, R2value10, p_value10, st_err10 = stats.linregress(RH, pid4)
ax10.set_xlabel(' RH %')
ax10.set_ylabel(' PID 4 / mv')
print ("Gradient j PID 4:", slope10)
print ("R2 value j pid 4:", R2value10)
print ("intercept j pid 4:", intercept10)
ax10.plot([np.min(RH), np.max(RH)], [(slope10*np.min(RH))+intercept10, (slope10*np.max(RH))+intercept10])


###### k

RH = (((k.RH/k.VS)-0.16)/0.0062)/(1.0546-0.00216*k.Temp*10)
pid4 = k.pid4*1000
pid5 = k.pid5*1000
pid6 = k.pid6*1000

RHfigk = plt.figure("Sections of the above data k")
ax11 = RHfigk.add_subplot(1,1,1)
ax11.scatter(RH, pid4, color='purple', linewidth=3)
slope11, intercept11, R2value11, p_value11, st_err11 = stats.linregress(RH, pid4)
ax11.set_xlabel(' RH %')
ax11.set_ylabel(' PID 4 / mv')
print ("Gradient k PID 4:", slope11)
print ("R2 value k pid 4:", R2value11)
print ("intercept k pid 4:", intercept11)
ax11.plot([np.min(RH), np.max(RH)], [(slope11*np.min(RH))+intercept11, (slope11*np.max(RH))+intercept11])


###### l

RH = (((l.RH/l.VS)-0.16)/0.0062)/(1.0546-0.00216*l.Temp*10)
pid4 = l.pid4*1000
pid5 = l.pid5*1000
pid6 = l.pid6*1000

RHfigl = plt.figure("Sections of the above data l")
ax12 = RHfigl.add_subplot(1,1,1)
ax12.scatter(RH, pid4, color='purple', linewidth=3)
slope12, intercept12, R2value12, p_value12, st_err12 = stats.linregress(RH, pid4)
ax12.set_xlabel(' RH %')
ax12.set_ylabel(' PID 4 / mv')
print ("Gradient l PID 4:", slope12)
print ("R2 value l pid 4:", R2value12)
print ("intercept l pid 4:", intercept12)
ax12.plot([np.min(RH), np.max(RH)], [(slope12*np.min(RH))+intercept12, (slope12*np.max(RH))+intercept12])

slopfig = plt.figure("Intercept over time")
x = [1,2,3,4,5,6,7,8,9,10,11,12]
y = [intercept1, intercept2, intercept3, intercept4, intercept5, intercept6, intercept7, intercept8, intercept9, intercept10, intercept11, intercept12]
z = [slope1, slope2, slope3, slope4, slope5, slope6, slope7, slope8, slope9, slope10, slope11, slope12]
ax1a = slopfig.add_subplot(1,1,1)
ax2a = ax1a.twinx()
ax1a.plot(x, y, color="red", linewidth=3, label="Intercept")
ax2a.plot(x, z, color="green", linewidth=3, label = "Gradient")
plt.legend(bbox_to_anchor=(0,1), loc=2)
ax1a.set_xlabel("Every 2000 data points")
ax1a.set_ylabel("intercept of pid vs RH ") 
ax2a.set_ylabel("Slope of pid vs RH")

plt.show()




