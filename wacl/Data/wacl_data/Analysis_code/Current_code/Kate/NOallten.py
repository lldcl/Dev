
## Use a loop to extract all info from MOS ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats
from matplotlib.offsetbox import AnchoredText


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160422_03']


for i in cal_file:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i
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

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	#filter out periods when isop changes rapidly (disopdt<0.1) and for 60 seconds afterwards
	nm_pts = 600./float(Time_avg[:-1])
	dNOdt = pd.Series(np.absolute(mean_resampled.NO.diff()),name='dNOdt')
	dNOdt_filt = pd.Series(0, index=dNOdt.index,name='dNOdt_filt')
	dNO_ctr=0
	for dp in dNOdt:
		if (dp>0.01):
			dNOdt_filt[dNO_ctr:int(dNO_ctr+nm_pts)] = 1
		dNO_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dNOdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dNOdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.dNOdt_filt == 0]

# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

T3 = pd.datetime(2015,01,01,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('int')
#'timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])


#find all MOS average data in file. Wherever the term "MOS" appears in the column name, this will be picked up.
sub = 'MOS'
MOS = [s for s in data_concat.columns if sub in s]

# To work out the value to set for the differential to select data where the [NO] is not changing.
NOfig = plt.figure()
ax1 = NOfig.add_subplot(111)
ax1.plot(mean_resampled.index, mean_resampled.NO.diff())

#plot up the pid voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
	ax1.plot(data_concat.index,data_concat[n],color=c,linewidth=3)
	plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
	plt.ylabel("MOS / V")
	plt.xlabel("Index")	
# Give it something to count through at the same time as the MOS, so it changes color.
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
#Use a counter to count through numbers in integers, beginning at one.
ctr=1
MOSloop = plt.figure("Raw MOS signal")
for n,c in zip(MOS,colors):
	ax = 'MOSraw'+str(ctr)
	ax = MOSloop.add_subplot(11,1,ctr)
	ax.scatter(data_concat.index, data_concat[n],color=c,linewidth=3)
	ax.set_xlim([data_concat.index[0], data_concat.index[len(data_concat.index)-1]])
	ax.set_ylabel(n +"/ V")
	ax.set_xlabel("Index")
	ctr+=1
MOSloop.show()

numbers = range(1,11) 
# Extra stuff is there because I wanted to get a common axis for the subplots so that the could have a common label.
#In actual fact, this wasn't needed as the text in lines 124 and 125 do the trick, but complicated to change back...
ctr=1
MOSfigure, (MOS1_ax, MOS2_ax, MOSar1_ax, MOSar2_ax,MOSar3_ax,MOSar4_ax,MOSar5_ax,MOSar6_ax,MOSar7_ax,MOSar8_ax) = plt.subplots(10,sharex=True,sharey=True)
ax = [MOS1_ax, MOS2_ax, MOSar1_ax, MOSar2_ax,MOSar3_ax,MOSar4_ax,MOSar5_ax,MOSar6_ax,MOSar7_ax,MOSar8_ax]
# MOSfigure = plt.subplots(11,1,sharex=True,sharey=True)
for n,c,x in zip(MOS,colors,numbers):
	ax[x-1].scatter(data_concat.NO, data_concat[n], color = c, linewidth =3, label=n)	
	#ax[x-1].locator_params(axis='y',nbins=5) #to specify number of ticks on both or any single axes
	#ax[x-1].locator_params(axis='x',nbins=5)
	ax[x-1].set_xlim(np.min(data_concat.NO),np.max(data_concat.NO))
	slopex, interceptx, R2valuex, p_valuex, st_errx = stats.linregress(data_concat.NO,data_concat[n]) 
	slopex = ("%.3g" %slopex)
	interceptx = ("%.3g" %interceptx)
	anchored_text = AnchoredText(n+"y= "+slopex+ "x + " +interceptx , loc=2)
	ax[x-1].add_artist(anchored_text)
	ax[x-1].plot([data_concat.index[0], data_concat.index[len(data_concat.index)-1]], [(slopex*(data_concat.NO[0]))+interceptx, (slopex*(data_concat.NO[0]))+interceptx])
	ax[x-1].legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
	ctr+=1
MOSfigure.text(0.5, 0.04, 'common X', ha='center')
MOSfigure.text(0.04, 0.5, 'common Y', va='center', rotation='vertical')
MOSfigure.show()



#Use a counter to count through numbers in integers, beginning at one.
MOStwo = plt.figure("Two MOS vs NO")
ax1 = MOStwo.add_subplot(2,1,1)
ax2 = MOStwo.add_subplot(2,1,2)
ax1.scatter(data_concat.NO, data_concat.MOS1, color="green",linewidth=3)
ax2.scatter(data_concat.NO, data_concat.MOS2, color="royalblue",linewidth=3)
ax1.set_ylabel("MOS1 voltage / V")
ax1.set_xlabel("NO / ppb")
ax2.set_ylabel("MOS2 voltage / V")
ax2.set_xlabel("NO / ppb")
slopea, intercepta, R2valuea, p_valuea, st_erra = stats.linregress(data_concat.NO,data_concat.MOS1) 
slopeb, interceptb, R2valueb, p_valueb, st_errb = stats.linregress(data_concat.NO,data_concat.MOS2) 
ax1.plot([np.min(data_concat.NO), np.max(data_concat.NO)], [(np.min(data_concat.NO)*slopea+intercepta), (np.max(data_concat.NO)*slopea+intercepta)])
ax2.plot([np.min(data_concat.NO), np.max(data_concat.NO)], [(np.min(data_concat.NO)*slopeb+interceptb), (np.max(data_concat.NO)*slopeb+interceptb)])
slopea = ("%.3g" %slopea)
intercepta = ("%.3g" %intercepta)
anchored_text1 = AnchoredText("MOS1 y= "+slopea+ "x + " +intercepta , loc=2)
ax1.add_artist(anchored_text1)
slopeb = ("%.3g" %slopeb)
interceptb = ("%.3g" %interceptb)
anchored_text2 = AnchoredText("MOS2 y= "+slopeb+ "x + " +interceptb , loc=2)
ax2.add_artist(anchored_text2)
MOStwo.show()	
plt.show()