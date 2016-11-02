"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
import datetime


path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'

filename = '201510/d20151008_01'
stat = 'N'
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

#find all pids in file
sub = 'pid'
pids = [s for s in data.columns if sub in s]

data_10Hz = data.copy(deep=True)
data_10Hz.TheTime = pd.to_datetime(data_10Hz.TheTime,unit='L')
data_10Hz = data_10Hz.set_index(data_10Hz.TheTime,drop=True)
data_10Hz = data_10Hz.resample('100L', how='mean',fill_method='pad')


data_10s = data_10Hz.resample('10S', how='mean',fill_method='pad')

#plot up the pid voltages
pidfig = plt.figure()
ax1 = pidfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(data.index,data[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")
pidfig.show()

pidfig_10s = plt.figure()
ax1_10s = pidfig_10s.add_subplot(2,1,1)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1_10s.plot(data_10s.index,data_10s[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")

ax2_10s = pidfig_10s.add_subplot(2,1,2)
ax2_10s.plot(data_10s.index,np.absolute(pd.rolling_mean(data_10s.pid5, window=2).diff()),color='k',linewidth=3)
ax2_10s.set_ylabel("dpid5/dt")


pidfig_10s.show()

isop_cyl = 13.277	#ppbv
mfchi_range = 100.	#sccm
mfchi_sccm = data_10Hz.mfchiR*(mfchi_range/5.)
mfclo_range = 20.	#sccm
mfclo_sccm = data_10Hz.mfcloR*(mfclo_range/5.)
dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
isop_mr = dil_fac*isop_cyl

isop_diff = np.absolute(data_10s.diff())

isopfig = plt.figure()

isopax = isopfig.add_subplot(2,1,1)
isopax.plot(data_10Hz.index,isop_mr,color='g',linewidth=3)
isopax.plot(data_30s.index,isop_diff,color='k', linewidth=3)
isopax.set_ylabel("Isop / ppb")








#######################################
if (stat == 'Y'):
	#select points on graph
	print "Click at either end of range"
	x = ginput(2) 

	#slice df and calculate stats on selected range
	xmin = int(x[0][0])
	xmax = int(x[1][0])
	print "The selected x (index) range is"
	print xmin,xmax
	df_xrange = data.iloc[xmin:xmax]
	
	plt.close()
	pidfig = plt.figure()
	ax1 = pidfig.add_subplot(111)
	colors = ["red", "blue" , "green", "orange", "purple"]
	for n,c in zip(pids,colors):
		ax1.plot(data.index,data[n],color=c,linewidth=3)
	ax1.plot([xmin,xmin],[np.min(np.min(data[pids]))*0.98,np.max(np.max(data[pids]))*1.02],color='k',linewidth=3)
	ax1.plot([xmax,xmax],[np.min(np.min(data[pids]))*0.98,np.max(np.max(data[pids]))*1.02],color='k',linewidth=3)
	plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("PID / V")
	plt.xlabel("Index")
	
	rangefig = plt.figure()
	ctr = 1
	for p,c in zip(pids,colors):
		sfig = 'pax'+str(ctr)
		sfig = rangefig.add_subplot(len(pids),1,ctr)
		sfig.plot(df_xrange.TheTime,df_xrange[p],color=c)
		sfig.set_ylabel(p+' / V')
		sfig.set_xlabel("Time")
	
		print p
		print 'mean =',np.mean(df_xrange[p])
		print 'stddev =',np.std(df_xrange[p])
		ctr+=1
	rangefig.show()
	
	isop_cyl = 13.277	#ppbv
	mfchi_range = 100.	#sccm
	mfchi_sccm = df_xrange.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = df_xrange.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
	isop_mr = dil_fac*isop_cyl
	print 'Isoprene mixing ratio'
	print 'mean =',np.mean(isop_mr)
	print 'stddev =',np.std(isop_mr)
#######################################

#plot up other variables
varfig = plt.figure()
#RH
rhax = varfig.add_subplot(3,1,1)
RH = (((data.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data.Temp)
rhax.plot(data.TheTime,RH,color='b',linewidth=3)
rhax.set_ylabel("RH %")

tmp = pd.DataFrame(RH.interpolate())
tmp.set_index(data.TheTime,inplace=True)
tmp = tmp.resample('30S',how='mean')
tmp = tmp.diff()
rhdax = varfig.add_subplot(3,1,2)
rhdax.plot(tmp.index,np.absolute(tmp),color='k',linewidth=3)
rhdax.set_ylabel("dRH/dt")

# #Temp
# Tax = varfig.add_subplot(3,1,2)
# Tax.plot(data.TheTime,data.Temp*10.,color='r',linewidth=3)
# Tax.set_ylabel("Temp / oC")
#MFC voltages
mfcax = varfig.add_subplot(3,1,3)
mfcax.plot(data.TheTime,data.mfcloR,color='g',linewidth=3, label = 'MFCLO')
mfcax.plot(data.TheTime,data.mfchiR,color='k',linewidth=3, label = 'MFCHI')
mfcax.set_ylabel("MFC / V")
mfclegend = mfcax.legend()
plt.xlabel("Time")
plt.show()