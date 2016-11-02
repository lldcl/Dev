"""Ozone MOS data file reader/plotter to look at individual files run with the dilute VOC mix.
There are no corrections for the baseline in this code"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

cal_file = ['d20160414_02']


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
	
	#filter out periods when ozone changes rapidly (dO3_6dt<0.1) and for 60 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	dO3_6dt = pd.Series(np.absolute(mean_resampled.O3_6.diff()),name='dO3_6dt')
	dO3_6dt_filt = pd.Series(0, index=dO3_6dt.index,name='dO3_6dt_filt')
	dO3_6_ctr=0
	for dp in dO3_6dt:
		if (dp>5.0):
			dO3_6dt_filt[dO3_6_ctr:int(dO3_6_ctr+nm_pts)] = 1
		dO3_6_ctr+=1

	mean_resampled = pd.concat([mean_resampled,dO3_6dt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,dO3_6dt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.dO3_6dt_filt == 0]
	
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
sub = 'MOS'
MOS = [s for s in data_concat.columns if sub in s]

#Determine the value of differentiating the data for filtering.
diff_fig = plt.figure()
ax1 = diff_fig.add_subplot(211)
ax2 = diff_fig.add_subplot(212)
ax1.plot(mean_resampled.index, mean_resampled.O3_6.diff())
ax2.plot(mean_resampled.index, mean_resampled.dO3_6dt_filt)

# To work out the value to set for the differential to select data where the [O3] is not changing.
# O3fig = plt.figure()
# ax1 = O3fig.add_subplot(111)
# ax1.plot(mean_resampled.index, mean_resampled.O3.diff())
# O3fig.show()

#plot up the MOS voltages
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

# The median MOS signal
data_concat['Median_MOS_signal'] = data_concat[['MOSar1','MOSar2','MOSar3','MOSar4','MOSar5','MOSar6','MOSar7','MOSar8']].median(axis=1)
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.index, data_concat.Median_MOS_signal, color="green")
#Plot the ozone conc from the 2B monitor.
ax2.plot(data_concat.index, data_concat.O3_6, color = "blue")
ax1.set_xlabel("Index",size =18)
ax2.set_ylabel("2B Ozone conc (ppb)", size=18)
ax1.set_ylabel('Median MOS signal (V)',size=18)
plt.title(cal_file, size=20)

ozne_cal = plt.figure()
ax1 = ozne_cal.add_subplot(111)
ax1.scatter(data_concat.O3_6, data_concat.Median_MOS_signal, color = "black")
ax1.set_xlabel("2B Ozone concentration (ppb)", size=18)
ax1.set_ylabel("Median MOS signal (V)", size=18)
slope, intercept, R2value, p_value, st_err = stats.linregress(data_concat.O3_6, data_concat.Median_MOS_signal)
ax1.plot([np.min(data_concat.O3_6), np.max(data_concat.O3_6)], [(np.min(data_concat.O3_6)*slope+intercept), (np.max(data_concat.O3_6)*slope+intercept)])
slope = ("%.3g" %slope)
intercept = ("%.3g" %intercept)
R2value = ("%.3g" %R2value)
anchored_text1 = AnchoredText("MOS y= "+slope+ "x + " +intercept , prop=dict(size=15),loc=2)
ax1.add_artist(anchored_text1)
anchored_text2 = AnchoredText("R2 value ="+R2value, prop=dict(size=15),loc=3)
ax1.add_artist(anchored_text2)
plt.title("Ozone calibration", size=20)

"""
# Create an empty table called table
table=[]
# Count from 1 to 10
numbers = range(1,11) 
# Start a counter
ctr=1
MOSfigure = plt.figure("MOS vs [O3]")
for n,c,x in zip(MOS,colors,numbers):
	ax = 'MOSfigure'+str(ctr)
	ax = MOSfigure.add_subplot(11,1,ctr)
	ax.scatter(data_concat.O3_6, data_concat[n], color = c, linewidth =3)	
	slopex, interceptx, R2valuex, p_valuex, st_errx = stats.linregress(data_concat.O3_6,data_concat[n]) 
	slopex = ("%.3g" %slopex)
	interceptx = ("%.3g" %interceptx)
	anchored_text = AnchoredText(n+"y= "+slopex+ "x + " +interceptx , loc=2)
	ax.add_artist(anchored_text)
	#ax.plot([np.min(data_concat.O3_6), np.max(data_concat.O3_6)], [(np.min(data_concat.O3_6)*slopex+interceptx), (np.max(data_concat.O3_6)*slopex+interceptx)])
	#ax.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
	ctr+=1
	table.append([n, slopex, interceptx, R2valuex])
MOSfigure.text(0.5, 0.04, 'Ozone from 2B monitor (ppb)', ha='center')
MOSfigure.text(0.04, 0.5, 'MOS voltage (V)', va='center', rotation='vertical')
MOSfigure.show()
# Convert the table called table to a pandas data frame and then make this into a CSV file.
pd.DataFrame(table,  columns=('MOS','Sensitivity','Intercept','R2 value')).to_csv('Data_from_ozone_file.csv', index=False)
#This returns a file located in the same file as this code that has the values from the linear regression of each MOS sensor as an Excel sheet.	"""

print(np.mean(data_concat.RH1))
variables = plt.figure()
ax1 = variables.add_subplot(4,1,1)
ax2 = variables.add_subplot(4,1,2)
ax3 = variables.add_subplot(4,1,3)
ax4 = variables.add_subplot(4,1,4)
ax1.plot(data_concat.index, data_concat.RH1, color="skyblue", linewidth =3)
ax2.plot(data_concat.index, data_concat.Temp*100, color="red", linewidth =3)
ax3.plot(data_concat.index, data_concat.O3, color="k", linewidth=3)
ax4.plot(data_concat.index, data_concat.O3_6, color = "forestgreen", linewidth = 3)
ax1.set_ylabel("Relative humidity (%)", size=14)
ax2.set_ylabel("Temperature (oC)", size=14)
ax3.set_ylabel("Ozone (ppb)", size=14)
ax4.set_ylabel("Ozone box (ppb)", size=14)

plt.show()


# For my presentation I just want to view two of the MOS
"""
#Use a counter to count through numbers in integers, beginning at one.
MOStwo = plt.figure("Two MOS vs ozone")
ax1 = MOStwo.add_subplot(2,1,1)
ax2 = MOStwo.add_subplot(2,1,2)
ax1.scatter(data_concat.O3_6, data_concat.MOS1, color="green",linewidth=3)
ax2.scatter(data_concat.O3_6, data_concat.MOS2, color="royalblue",linewidth=3)
ax1.set_ylabel("MOS1 voltage / V")
ax1.set_xlabel("Ozone / ppb")
ax2.set_ylabel("MOS2 voltage / V")
ax2.set_xlabel("Ozone / ppb")
slopea, intercepta, R2valuea, p_valuea, st_erra = stats.linregress(data_concat.O3_6,data_concat.MOS1) 
slopeb, interceptb, R2valueb, p_valueb, st_errb = stats.linregress(data_concat.O3_6,data_concat.MOS2) 
ax1.plot([np.min(data_concat.O3_6), np.max(data_concat.O3_6)], [(np.min(data_concat.O3_6)*slopea+intercepta), (np.max(data_concat.O3_6)*slopea+intercepta)])
ax2.plot([np.min(data_concat.O3_6), np.max(data_concat.O3_6)], [(np.min(data_concat.O3_6)*slopeb+interceptb), (np.max(data_concat.O3_6)*slopeb+interceptb)])
slopea = ("%.3g" %slopea)
intercepta = ("%.3g" %intercepta)
anchored_text1 = AnchoredText("MOS1 y= "+slopea+ "x + " +intercepta , loc=2)
ax1.add_artist(anchored_text1)
slopeb = ("%.3g" %slopeb)
interceptb = ("%.3g" %interceptb)
anchored_text2 = AnchoredText("MOS2 y= "+slopeb+ "x + " +interceptb , loc=2)
ax2.add_artist(anchored_text2)
MOStwo.show()"""

"""# Make a new dataframe which excludes the broken MOS.
GoodMOS = pd.DataFrame(data_concat, data_concat.index, columns=['MOS1','MOS2','MOSar1','MOSar4','MOSar5','MOSar6','MOSar8','MOSar9','O3','RH1','Temp','VS'])

sub = 'MOS'
MOSnew = [r for r in GoodMOS.columns if sub in r]
# Plot the new dataframe with the colours.
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
#Use a counter to count through numbers in integers, beginning at one.
# Filter out times when the RH dropped to 0.4 as this indicates the ozone conc was being remeasured.
GoodMOS = GoodMOS[GoodMOS.RH1 > 0.1]
ctr=1
MOSwork = plt.figure("Raw MOS signal for new dataframe")
for n,c in zip(MOSnew,colors):
	ax = 'MOSwork'+str(ctr)
	ax = MOSwork.add_subplot(9,1,ctr)
	ax.scatter(GoodMOS.index, GoodMOS[n],color=c,linewidth=3)
	#ax.set_xlim([GoodMOS.index[0], GoodMOS.index[len(GoodMOS.index)-1]])
	ax.set_ylabel(n +"/ V")
	ax.set_xlabel("Index")
	ctr+=1
ax8 = MOSwork.add_subplot(9,1,8)
ax8.plot(GoodMOS.index, GoodMOS.RH1, color = "skyblue", linewidth=3)
ax8.set_ylabel("RH (%)")
ax10 = ax8.twinx()
ax10.plot(GoodMOS.index, GoodMOS.O3, color= "silver", linewidth = 3)
major_ticks = np.arange(0, 400, 100)                                                                                        
ax10.set_yticks(major_ticks)      
ax_ticks = np.arange(-200, 1000, 500)     
ax8.set_xticks(ax_ticks)                                           
ax10.set_ylabel("Ozone (ppb)")
ax9 = MOSwork.add_subplot(9,1,9)
ax9.plot(GoodMOS.index, GoodMOS.Temp*100, color = "red", linewidth=3)
ax9.set_ylabel("Temperature (oC)")
ax9.set_xticks(ax_ticks) 
MOSwork.show()

numbers1 = range(1,8) 
ctr=1

table=[]

MOSvs = plt.figure("MOS vs [O3] for working MOS")
for n,c,k in zip(MOSnew,colors,numbers1):
	ax = 'MOSvs'+str(ctr)
	ax = MOSvs.add_subplot(7,1,ctr)
	ax.scatter(GoodMOS.O3, GoodMOS[n], color = c, linewidth =3, label=n)	
	slopek, interceptk, R2k, p_valuek, st_errk = stats.linregress(GoodMOS.O3,GoodMOS[n]) 
	slopek = ("%.3g" %slopek)
	interceptk = ("%.3g" %interceptk)
	R2k = ("%.3g" %R2k)
	#ax.plot([np.min(data_concat.O3), np.max(data_concat.O3)], [(np.min(data_concat.O3)*slopek+interceptk), (np.max(data_concat.O3)*slopek+interceptk)])
	#ax.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
	ax.set_ylabel(n +" (V)")
	ax.set_xlabel("Ozone (ppb)")
	anchored_text = AnchoredText(n+" y= "+slopek+ "x + " +interceptk , loc=1)
	ax.add_artist(anchored_text)
	ctr+=1
	table.append([n, slopek, interceptk, R2k])
#MOSvs.text(0.5, 0.04, 'Ozone (ppb)', ha='center')	
MOSvs.show()
"""














