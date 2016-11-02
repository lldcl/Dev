"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis


path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'

filename = '201603/d20160329_01'
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
sub = 'MOS'
pids = [s for s in data.columns if sub in s]

# isop_cyl = 40000	#ppbv
# mfchi_range = 2000.	#100.	#sccm
# mfchi_sccm = data.mfchiR*(mfchi_range/5.)
# mfcmid_range = 100.
# mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
# mfclo_range = 20.	#sccm
# mfclo_sccm = data.mfcloR*(mfclo_range/5.)
# dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
# isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
# data = pd.concat([data,isop_mr],axis=1)

data.RH1 = (((data.RH1/data.VS)-0.16)/0.0062)/(1.0546-0.00216*data.Temp*100.)


#plot up the pid voltages
# pidfig = plt.figure()
# ax1 = pidfig.add_subplot(111)
# colors = ["red", "blue" , "green", "orange", "purple"]
# for n,c in zip(pids,colors):
# 	ax1.plot(data.index,data[n],color=c,linewidth=3,marker='o')
# plt.ylabel("MOS / V")
# plt.xlabel("Index")
# # ax2 = ax1.twinx()
# # ax2.plot(data.index,data.isop_mr, linewidth=3,color='k')
# # plt.ylabel("Isop / ppbv")
# plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# # ax1.set_ylim([0.0565,0.058])
# #plt.show()


#######################################
if (stat == 'Y'):
	#select points on graph
# 	print "Click at either end of range"
# 	x = ginput(2) 

	#slice df and calculate stats on selected range
	xmin = 0	#int(x[0][0])
	xmax = len(data.index)-1	#int(x[1][0])
# 	xmin = int(x[0][0])
# 	xmax = int(x[1][0])
	plt.close()
	print "The selected x (index) range is"
	print xmin,xmax

	df_xrange = data.iloc[xmin:xmax]
	df_xrange.set_index(df_xrange.TheTime,inplace=True)
	df_xrange = df_xrange.resample('1S',how='median')

	
# 	pidfig = plt.figure()
# 	ax1 = pidfig.add_subplot(111)
# 	colors = ["red", "blue" , "green", "orange", "purple"]
# 	for n,c in zip(pids,colors):
# 		ax1.plot(data.index,data[n],color=c,linewidth=3)
# 	ax1.plot([xmin,xmin],[np.min(np.min(data[pids]))*0.98,np.max(np.max(data[pids]))*1.02],color='k',linewidth=3)
# 	ax1.plot([xmax,xmax],[np.min(np.min(data[pids]))*0.98,np.max(np.max(data[pids]))*1.02],color='k',linewidth=3)
# 	plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# 	plt.ylabel("PID / V")
# 	plt.xlabel("Index")
# 	
# 	rangefig = plt.figure()
# 	ctr = 1
# 	for p,c in zip(pids,colors):
# 		sfig = 'pax'+str(ctr)
# 		sfig = rangefig.add_subplot(len(pids),1,ctr)
#  		sfig.plot(df_xrange.index,df_xrange[p],color=c)		
# 		ax2 = sfig.twinx()
# 		ax2.plot(df_xrange.index,df_xrange.RH1, linewidth=3,color='k')
# # 		ax2.plot(df_xrange.index,df_xrange.isop_mr, linewidth=3,color='k')
# 		ax2.yaxis.tick_right()
# 		ax2.yaxis.set_label_position("right")
# 		plt.ylabel("RH / %")
# # 		plt.ylabel("Isop / ppbv")
# 
# 		sfig.set_ylabel(p+' / V')
# 		sfig.set_xlabel("Time")
# 	
# 		print p
# 		print 'mean =',np.mean(df_xrange[p])
# 		print 'stddev =',np.std(df_xrange[p])
# 		ctr+=1
# 	rangefig.show()
	
	print 'Isoprene mixing ratio'
	print 'mean =',np.mean(df_xrange.isop_mr)
	print 'stddev =',np.std(df_xrange.isop_mr)
#######################################

#plot up other variables
varfig = plt.figure()
#RH
rhax = varfig.add_subplot(3,1,1)
rhax.plot(data.TheTime,data.RH1,color='b',linewidth=3)
rhax.set_ylabel("RH %")

tmp = pd.DataFrame(data.RH1.interpolate())
tmp.set_index(data.TheTime,inplace=True)
tmp = tmp.resample('30S',how='mean')
tmp = tmp.diff()
rhdax = varfig.add_subplot(3,1,2)
rhdax.plot(tmp.index,np.absolute(tmp),color='k',linewidth=3)
rhdax.set_ylabel("dRH/dt")

#Temp
Tax = varfig.add_subplot(3,1,2)
Tax.plot(data.TheTime,data.Temp*100.,color='r',linewidth=3,marker='o')
Tax.set_ylabel("Temp / oC")

Vax = varfig.add_subplot(3,1,3)
Vax.plot(data.TheTime,data.VOC,color='g',linewidth=3,marker='o')
Vax.set_ylabel("VOC / ppm")
#MFC voltages
# mfcax = varfig.add_subplot(3,1,3)
# # # mfcax.plot(RH,pd.rolling_mean(data.pid6,20),'o',label = 'PID6')
# # # mfcax.set_ylabel("PID / V")
# # plt.xlabel("RH / %")
# # mfcax.plot(df_xrange.index,df_xrange.isop_mr,color='g',linewidth=3, label = 'Isop')
# mfcax.plot(data.TheTime,data.mfcloR,color='k',linewidth=3, label = 'MFClo')
# mfcax.set_ylabel("Isop / ppbv")
# mfclegend = mfcax.legend()
# # plt.xlabel("Time")
# # plt.show()

mosdf = pd.concat([data.TheTime,data.VS,data.Temp,data.RH1,data.CO,data[pids]],axis=1)	#data.MOSar1,
mosdf = mosdf.dropna()

mosfig = plt.figure()
ctr = 1
for si in pids:

	mos1ax = mosfig.add_subplot(len(pids),1,ctr)
	mos1ax.plot(mosdf.TheTime,mosdf[si],color='b')
	mos1ax.set_ylabel(si)
	ax2 = mos1ax.twinx()
	ax2.plot(mosdf.TheTime,mosdf.CO,color='k')
	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	plt.ylabel("VOC")
	ctr+=1
# ax2 = mos1ax.twinx()
# ax2.plot(mosdf.TheTime,mosdf.Temp*100,color='k')
# ax2.plot(mosdf.TheTime,mosdf.RH2*100,color='g')
# ax2.yaxis.tick_right()
# ax2.yaxis.set_label_position("right")
# plt.ylabel("Temp")

# mos2ax = mosfig.add_subplot(3,1,2)
# mos2ax.plot(mosdf.TheTime,mosdf.MOS2,color='r')
# mos2ax.set_ylabel("MOS2 (V)")
# ax2 = mos2ax.twinx()
# ax2.plot(mosdf.TheTime,mosdf.Temp,color='k')
# ax2.yaxis.tick_right()
# ax2.yaxis.set_label_position("right")
# plt.ylabel("Temp")

# mos3ax = mosfig.add_subplot(3,1,3)
# mos3ax.plot(mosdf.TheTime,mosdf.MOSar1,color='g')
# mos3ax.set_ylabel("MOS3 (V)")

# mos3ax = mosfig.add_subplot(3,1,3)
# mos3ax.plot(mosdf.TheTime,mosdf.mfcloR,color='k')
# mos3ax.set_ylabel("MFClo")

# # ax2 = mos2ax.twinx()
# ax2.plot(mosdf.TheTime,mosdf.Temp,color='k')
# ax2.yaxis.tick_right()
# ax2.yaxis.set_label_position("right")
# plt.ylabel("Temp")

# vsax = mosfig.add_subplot(4,1,3)
# vsax.scatter(mosdf.Temp,mosdf.MOS1,color='b')
# # vsax.plot(mosdf.TheTime,mosdf.VS,color='k')
# # vsax.plot(mosdf.VS,mosdf.MOS1,color='k')
# vsax.set_ylabel("MOS1 (V)")
# 
# vssax = mosfig.add_subplot(4,1,4)
# # vsax.plot(mosdf.TheTime,mosdf.VS,color='k')
# # vssax.scatter(mosdf.VS,mosdf.MOS1,color='k')
# vssax.scatter(mosdf.Temp,mosdf.MOS2,color='r')
# vssax.set_ylabel("MOS2 (V)")

plt.show()