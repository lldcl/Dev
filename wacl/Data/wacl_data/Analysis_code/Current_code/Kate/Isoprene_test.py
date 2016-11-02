"""Just to check whether or not the 8 MOS respond to isoprene in new set up.

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats


"""path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201606/'

f = 'MOS_test_kate'

MOS_data = pd.read_csv(path+f)

isop_cyl = 723.	#ppbv
mfchi_range = 2000.	#100.	#sccm
mfclo_range = 20.	#sccm

dil_fac = mfclo_range/(mfclo_range+mfchi_range)
isop_mr = (dil_fac*isop_cyl )
print isop_mr

sub = 'MOS'
MOS = [s for s in MOS_data.columns if sub in s]

colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
#Use a counter to count through numbers in integers, beginning at one.
ctr=1
MOSloop = plt.figure("Raw MOS signal")
for n,c in zip(MOS,colors):
	ax = 'MOSraw'+str(ctr)
	ax = MOSloop.add_subplot(8,1,ctr)
	ax.scatter(MOS_data.index, MOS_data[n],color=c,linewidth=3)
	ax.set_xlim([MOS_data.index[0], MOS_data.index[len(MOS_data.index)-1]])
	ax.set_ylabel(n +"/ V")
	ax.set_xlabel("Index")
	ctr+=1
MOSloop.show()"""
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'
cal_file = ['d20151215_02']

for i in cal_file:
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
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	isop_cyl = 685.	#ppbv
	mfchi_range =2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100.	#sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)

	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
T3 = pd.datetime(2015,01,01,0)
# dt = pd.Series((mean_resampled.index - mean_resampled.index[0]),index=mean_resampled.index,name='dt')
dt = pd.Series((mean_resampled.index - T3),index=mean_resampled.index,name='dt')
dt = dt.astype('timedelta64[s]')
mean_resampled = pd.concat([mean_resampled,dt],axis=1,join_axes=[mean_resampled.index])

MOSfigall = plt.figure("MOS with all data vs time")

cor1ax = MOSfigall.add_subplot(2,1,1)
cor2ax = MOSfigall.add_subplot(2,1,2)
cor3 = cor1ax.twinx()
cor4 = cor2ax.twinx()

cor1ax.plot(mean_resampled.dt, mean_resampled.MOS1,color='b')
cor3.plot(mean_resampled.dt, mean_resampled.isop_mr, color='k')
cor2ax.plot(mean_resampled.dt, mean_resampled.MOS2,color='green')
cor4.plot(mean_resampled.dt, mean_resampled.isop_mr, color='k')

cor1ax.set_ylabel("MOS1 (V)")
cor2ax.set_ylabel("MOS2 (V)")

MOSfigall.show()

#join files
print 'mean_resampled shape = ',mean_resampled.shape
try:
	data_concat = data_concat.append(mean_resampled)
	print ' concatenating'
except NameError:
	data_concat = mean_resampled.copy(deep=False)
	print ' making data_concat'
	

	# filter out periods when isop changes rapidly (disopdt<0.1) and for 300 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	disopdt = pd.Series(np.absolute(data_concat.isop_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>0.1):
			disopdt_filt[disop_ctr:int(disop_ctr+nm_pts)] = 1
		disop_ctr+=1

	data_concat = pd.concat([data_concat,disopdt],axis=1,join_axes=[data_concat.index])
	data_concat = pd.concat([data_concat,disopdt_filt],axis=1,join_axes=[data_concat.index])
	data_concat = data_concat[data_concat.disopdt_filt == 0]

MOSfig = plt.figure("MOS vs time")

cor1ax = MOSfig.add_subplot(2,1,1)
cor2ax = MOSfig.add_subplot(2,1,2)
cor3 = cor1ax.twinx()
cor4 = cor2ax.twinx()

cor1ax.plot(data_concat.TheTime,data_concat.MOS1,color='b')
cor3.plot(data_concat.TheTime, data_concat.isop_mr, color='k')
cor2ax.plot(data_concat.TheTime, data_concat.MOS2,color='green')
cor4.plot(data_concat.TheTime, data_concat.isop_mr, color='k')

cor1ax.set_ylabel("MOS1 (V)")
cor2ax.set_ylabel("MOS2 (V)")

MOSfig.show()

# Determining the response time, subtract MOSall from MOS
disopfig = plt.figure("MOS vs time")

cor1ax = disopfig.add_subplot(1,1,1)
cor1ax.plot(data_concat.dt,data_concat.disopdt_filt,color='b')

cor1ax.set_ylabel("disop")


disopfig.show()

"""
### Need to plot up the isoprene sensitivity polts, with linear regression.
# Finding the isoprene sensitivity
# Bin the data into bins of 0.25ppb isoprene, get an average for this data and then plot this.

# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 0.25 ppb of isoprene sections
bin1 = stats.binned_statistic(data_concat.isop_mr, MOS1_cor, statistic='mean', bins=60, range=(0,15))
bin2 = stats.binned_statistic(data_concat.isop_mr, MOS2_cor, statistic='mean', bins=60, range=(0,15))
bin3 = stats.binned_statistic(data_concat.isop_mr, data_concat.isop_mr, statistic='mean', bins=60, range=(0,15))
bin4 = stats.binned_statistic(data_concat.isop_mr, MOS1_cor, statistic=stddev, bins=60, range=(0,15))
bin5 = stats.binned_statistic(data_concat.isop_mr, MOS2_cor, statistic=stddev, bins=60, range=(0,15))
bin6 = stats.binned_statistic(data_concat.isop_mr, data_concat.isop_mr, statistic=stddev, bins=60, range=(0,15))
# Turn into pandas to get rid of NaNs.
MOS1_cor = pd.Series(bin1[0])
MOS2_cor = pd.Series(bin2[0])
isop = pd.Series(bin3[0])
st1 = pd.Series(bin4[0])
st2 = pd.Series(bin5[0])
stIs = pd.Series(bin6[0])
# get rid of NaNs for both the data and the standard deviation.
MOS1_cor = MOS1_cor.dropna()
MOS2_cor = MOS2_cor.dropna()
isop = isop.dropna()
st1 = st1.dropna()
st2 = st2.dropna()
stIs = stIs.dropna()

isoprene = plt.figure(" Isoprene sensitivity with the general background removed")
ax1 = isoprene.add_subplot(2,1,1)
ax2 = isoprene.add_subplot(2,1,2)
ax1.scatter(isop, MOS1_cor, color="g")
ax1.errorbar(isop, MOS1_cor, xerr=stIs, yerr=st1, lw=1, fmt='o', color="g")
ax2.scatter(isop, MOS2_cor, color="b")
ax2.errorbar(isop, MOS2_cor, xerr=stIs, yerr=st2, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS1 signal (V)")
ax2.set_ylabel("MOS2 signal (V)")
ax1.set_xlabel("Isoprene (ppb)")
ax2.set_xlabel("Isoprene (ppb)")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(isop, MOS1_cor)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(isop, MOS2_cor)
ax1.plot([np.min(isop), np.max(isop)], [(slope3*np.min(isop))+intercept3, (slope3*np.max(isop))+intercept3])
ax2.plot([np.min(isop), np.max(isop)], [(slope4*np.min(isop))+intercept4, (slope4*np.max(isop))+intercept4])
print ("Gradient of isop vs MOS1", slope3)
print ("Intercept of isop vsMOS1", intercept3)
print ("R2 of isop vs MOS1", R2value3)
print ("Gradient of isop vs MOS2", slope4)
print ("Intercept of isop vs MOS2", intercept4)
print ("R2 of isop vs MOS2", R2value4)
print ("Average RH", np.mean(data_concat.RH1))
print ("Average temp", np.mean(data_concat.Temp*100))

plt.show()"""


