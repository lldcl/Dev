"""Sulphur dioxide MOS data file reader/plotter to look at individual files.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160420_03']


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

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
	
	#filter out periods when isop changes rapidly (disopdt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	dSO2dt = pd.Series(np.absolute(mean_resampled.SO2.diff()),name='dSO2dt')
	dSO2dt_filt = pd.Series(0, index=dSO2dt.index,name='dSO2dt_filt')
	dSO2_ctr=0
	for dp in dSO2dt:
		if (dp>0.01):
			dSO2dt_filt[dSO2_ctr:int(dSO2_ctr+nm_pts)] = 1
		dSO2_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dSO2dt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dSO2dt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.dSO2dt_filt == 0]
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
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)


# Find all the columns with MOS in the title for use in loops.
sub = 'MOSar'
MOS = [s for s in data_concat.columns if sub in s]

diff_fig = plt.figure()
ax1 = diff_fig.add_subplot(211)
ax2 = diff_fig.add_subplot(212)
ax1.plot(mean_resampled.index, mean_resampled.SO2.diff())
ax2.plot(mean_resampled.index, mean_resampled.dSO2dt_filt)

# To work out the value to set for the differential to select data where the [SO2] is not changing.
# SO2fig = plt.figure()
# ax1 = SO2fig.add_subplot(111)
# ax1.plot(mean_resampled.index, mean_resampled.SO2.diff())
# SO2fig.show()

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

table=[]
numbers = range(1,11) 
ctr=1
MOSfigure = plt.figure("MOS vs [SO2]")
for n,c,x in zip(MOS,colors,numbers):
	ax = 'MOSfigure'+str(ctr)
	ax = MOSfigure.add_subplot(11,1,ctr)
	ax.scatter(data_concat.SO2, data_concat[n], color = c, linewidth =3)	
	slopex, interceptx, R2valuex, p_valuex, st_errx = stats.linregress(data_concat.SO2,data_concat[n]) 
	slopex = ("%.3g" %slopex)
	interceptx = ("%.3g" %interceptx)
	anchored_text = AnchoredText(n+"y= "+slopex+ "x + " +interceptx , loc=2)
	ax.add_artist(anchored_text)
	#ax.plot([np.min(data_concat.SO2), np.max(data_concat.SO2)], [(np.min(data_concat.SO2)*slopex+interceptx), (np.max(data_concat.SO2)*slopex+interceptx)])
	#ax.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
	ctr+=1
	table.append([n, slopex, interceptx, R2valuex])
MOSfigure.text(0.5, 0.04, 'SO2 from generator (ppb)', ha='center')
MOSfigure.text(0.04, 0.5, 'MOS voltage (V)', va='center', rotation='vertical')
MOSfigure.show()

pd.DataFrame(table,  columns=('MOS','Sensitivity','Intercept','R2 value')).to_csv('Data_from_SO2_file.csv', index=False)
#This returns a file located in the same file as this code that has the values from the linear regression of each MOS sensor as an Excel sheet.	
data_concat['Median_MOS_signal'] = data_concat[['MOSar1','MOSar2','MOSar3','MOSar4','MOSar5','MOSar6','MOSar7','MOSar8']].median(axis=1)
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.index, data_concat.Median_MOS_signal, color="green")
#Plot the SO2 conc from the SO2 box.
ax2.plot(data_concat.index, data_concat.SO2, color = "blue")
ax1.set_xlabel("Index",size =18)
ax2.set_ylabel("SO2 conc (ppb)", size=18)
ax1.set_ylabel('Median MOS signal (V)',size=18)
plt.title(cal_file, size=20)

SO2_cal = plt.figure()
ax1 = SO2_cal.add_subplot(111)
ax1.scatter(data_concat.SO2, data_concat.Median_MOS_signal, color = "black")
ax1.set_xlabel("SO2 concentration (ppb)", size=18)
ax1.set_ylabel("Median MOS signal (V)", size=18)
slope, intercept, R2value, p_value, st_err = stats.linregress(data_concat.SO2, data_concat.Median_MOS_signal)
ax1.plot([np.min(data_concat.SO2), np.max(data_concat.SO2)], [(np.min(data_concat.SO2)*slope+intercept), (np.max(data_concat.SO2)*slope+intercept)])
slope = ("%.3g" %slope)
intercept = ("%.3g" %intercept)
anchored_text1 = AnchoredText("MOS y= "+slope+ "x + " +intercept , prop=dict(size=15),loc=2)
ax1.add_artist(anchored_text1)
plt.title("SO2 calibration", size=20)

print(np.mean(data_concat.RH1))
variables = plt.figure()
ax1 = variables.add_subplot(3,1,1)
ax2 = variables.add_subplot(3,1,2)
ax3 = variables.add_subplot(3,1,3)
ax1.plot(data_concat.index, data_concat.RH1, color="skyblue", linewidth =3)
ax2.plot(data_concat.index, data_concat.Temp*100, color="red", linewidth =3)
ax3.plot(data_concat.index, data_concat.SO2, color="k", linewidth=3)
ax1.set_ylabel("Relative humidity (%)")
ax2.set_ylabel("Temperature (oC)")
ax3.set_ylabel("Sulfur dioxide (ppb)")
plt.show()
