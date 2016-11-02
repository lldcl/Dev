"""Universal MOS data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis

# Takes the file name and extracts the date then sticks this on the front to make the file path.""" 
stat = 'Y'

cal_files = ['d20151204_02']
for i in cal_files:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i

#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

#dT = seconds since file start
dT = data.TheTime-data.TheTime[0]
dT*=60.*60.*24.

#convert daqfac time into real time pd.datetime object
data.TheTime = pd.to_datetime(data.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,1,1,0)
offset=T1-T2
data.TheTime+=offset

#find all MOS data in file
sub = 'MOS'
MOS = [s for s in data.columns if sub in s]

#plot up the pid voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(MOS,colors):
	ax1.plot(data.index,data[n],color=c,linewidth=3)
plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("MOS / V")
plt.xlabel("Index")
plt.show()

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
#Temp
Tax = varfig.add_subplot(3,1,2)
Tax.plot(data.TheTime,data.Temp*10.,color='r',linewidth=3)
Tax.set_ylabel("Temp / oC")
#MFC voltages
mfcax = varfig.add_subplot(3,1,3)
mfcax.plot(data.TheTime,data.mfcloR,color='g',linewidth=3, label = 'MFCLO')
mfcax.plot(data.TheTime,data.mfchiR,color='k',linewidth=3, label = 'MFCHI')
mfcax.set_ylabel("MFC / V")
mfclegend = mfcax.legend()
plt.xlabel("Time")
plt.show()