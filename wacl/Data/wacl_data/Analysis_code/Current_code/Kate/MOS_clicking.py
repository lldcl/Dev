"""Universal MOS data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis

# Takes the file name and extracts the date then sticks this on the front to make the file path.""" 
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
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
	
	bitfig = plt.figure("Clicking to select a section of the data")
	ax1 = bitfig.add_subplot(111)
	colors = ["red", "blue" , "green", "orange", "purple"]
	for n,c in zip(MOS,colors):
		ax1.plot(data.index,data[n],color=c,linewidth=3)
	ax1.plot([xmin,xmin],[np.min(np.min(data[MOS]))*0.98,np.max(np.max(data[MOS]))*1.02],color='k',linewidth=3)
	ax1.plot([xmax,xmax],[np.min(np.min(data[MOS]))*0.98,np.max(np.max(data[MOS]))*1.02],color='k',linewidth=3)
	plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("MOS / V")
	plt.xlabel("Index")
	
	rangefig = plt.figure()
	ctr = 1
	for p,c in zip(MOS,colors):
		sfig = 'pax'+str(ctr)
		sfig = rangefig.add_subplot(len(MOS),1,ctr)
		sfig.plot(df_xrange.TheTime,df_xrange[p],color=c)
		sfig.set_ylabel(p+' / V')
		sfig.set_xlabel("Time")
	
		print p
		print 'mean =',np.mean(df_xrange[p])
		print 'stddev =',np.std(df_xrange[p])
		ctr+=1
	rangefig.show()
	
	isop_cyl = 685.4822	#ppbv
	mfchi_range = 2000.	#sccm
	mfchi_sccm = df_xrange.mfchiR*(mfchi_range/5.)
	mfcmid_range = 100 #sccm
	mfcmid_sccm = df_xrange.mfcmidR*(mfcmid_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = df_xrange.mfcloR*(mfclo_range/5.)
	dil_fac = mfclo_sccm/(mfclo_sccm+mfcmid_sccm+mfchi_sccm)
	isop_mr = dil_fac*isop_cyl
	print 'Isoprene mixing ratio'
	print 'mean =',np.mean(isop_mr)
	print 'stddev =',np.std(isop_mr)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)

#######################################
RH = (((data.RH1/4.96)-0.16)/0.0062)/(1.0546-0.00216*(data.Temp*100))
#plot up other variables
varfig = plt.figure("Plotting the rest of the variables")
#RH
rhax = varfig.add_subplot(3,1,1)
Tax = varfig.add_subplot(3,1,2)
isax = varfig.add_subplot(3,1,3)


rhax.plot(data.TheTime,RH,color='b',linewidth=3)
rhax.set_ylabel("RH %")

Tax.plot(data.TheTime,data.Temp*100.,color='r',linewidth=3)
Tax.set_ylabel("Temp / oC")

isax.plot(data.TheTime,data.isop_mr,color='k',linewidth=3, label = 'Isoprene')
isax.set_ylabel("Isoprene")

plt.xlabel("Time")
plt.show()