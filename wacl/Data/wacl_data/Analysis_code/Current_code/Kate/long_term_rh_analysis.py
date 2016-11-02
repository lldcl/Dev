"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis

#path = '/Users/ks826/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_data_files/'
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

filename = '201510/d20151021_05'
stat = 'Y'

#read file into dataframe
data = pd.read_csv(path+filename)

#dT = seconds since file start
dT = data.TheTime-data.TheTime[0]
dT*=60.*60.*24.

#convert daqfac time into real time pd.datetime object
data.TheTime = pd.to_datetime(data.TheTime,unit='D')
T1 = pd.datetime(1899,12,30,0)
T2 = pd.datetime(1970,1,1,0)
offset=T1-T2
data.TheTime+=offset

#find all pids in file
sub = 'pid'
pids = [s for s in data.columns if sub in s]

#plot up the pid voltages
pidfig = plt.figure()
ax1 = pidfig.add_subplot(1,1,1)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(data.TheTime,data[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Time")
plt.show()

#######################################
""" if (stat == 'Y'):
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
		sfig.set_xlabel("Time") """
		
#the code in the quotation marks is for selecting two points and getting a zoomed in version of the data. For the long term RH calibration this isn't very relevant.
	
# print p also for the two click thing
# I want to be able to see the values of the mean and stdev of the PID voltages on the terminal screen. 
# Print is the command, telling the screen to print, then the text in the ' marks will also appear. 
# The next bit tells numpy to use the mean function on the data in the file. The .pid4 tells the 
# code to only extract the data from the column called pid4. 
# Repeat for the other PIDs. 		
print 'total mean pid 4 =',np.mean(data.pid4)
print 'total stddev pid 4 =',np.std(data.pid4)		
print 'total mean pid5 =',np.mean(data.pid5)
print 'total stddev pid 5 =',np.std(data.pid5)
print 'total mean pid 6 =',np.mean(data.pid6)
print 'total stddev pid 6 =',np.std(data.pid6)

# For the next bit, I only want to calculate the mean from the first 100 data points from the file.
# Again, I need to tell the code to print the text in ' marks, followed by using the mean 
# function from numpy. The data[0:100] is telling the code to only use the first 100 points.

print 'Now for the first 100 points'

print '1st 100 mean pid 4 =',np.mean(data[0:100].pid4)
print '1st 100 std pid 4 =',np.std(data[0:100].pid4)
print '1st 100 mean pid 5 =',np.mean(data[0:100].pid5)
print '1st 100 std pid 5 =',np.std(data[0:100].pid5)
print '1st 100 mean pid 6 =',np.mean(data[0:100].pid6)
print '1st 100 std pid 6 =',np.mean(data[0:100].pid6)

# The last 100 points; this is a bit more tricky. Since using len(data.index) tells me the maximum 
# data point, I can use this as the last point. -100 tells the code to use the max minus 100 points.
print 'last 100 points'

print 'last 100 mean pid 4 =',np.mean(data[len(data.index)-100:len(data.index)]).pid4
print 'last 100 std pid 4 =',np.std(data[len(data.index)-100:len(data.index)]).pid4
print 'last 100 mean pid 5 =',np.mean(data[len(data.index)-100:len(data.index)]).pid5
print 'last 100 std pid 5 =',np.std(data[len(data.index)-100:len(data.index)]).pid5
print 'last 100 mean pid 6 =',np.mean(data[len(data.index)-100:len(data.index)]).pid6
print 'last 100 std pid 6 =',np.std(data[len(data.index)-100:len(data.index)]).pid6

# I want to plot a graph with the mean of each 100 points over time.
# Create a figure instance, called rhplot, using plt
rhplot = plt.figure()

# Create an axes instance for my plot called rhplot. The (1,1,1) tells the code to plot one
# figure with those co-ordinates.
ax1 = rhplot.add_subplot(1,1,1)

# Using the plot function on the axes with the data which was defined earlier. 
# plot(data.TheTime, data.RH, linewidth=3) is telling the code to use the data from the 
# TheTime column on the y-coodinates, the data from the RH column in the x-coordinate and make the 
# linewidth of the plot to have a thickness of 3. To determine which headings the data is under
#in the code (you should have previously labelled them) you can go to terminal and type in 
# dta.colums then after pressing enter the column headings will appear.
ax1.plot(data.TheTime, data.RH, linewidth = 3)
# Tells the code to use the plt function called xlabel to name the x axis RH.
plt.ylabel("RH")
# Tells the code to use the plt function called ylabel to name the y axis Time
plt.xlabel("Time")
# Type plt.show() to tell the code to make the finished graph appear after running.
plt.show()


#get the data for the box plot into collections

pid_4 = data.pid4
pid_5 = data.pid5
pid_6 = data.pid6
# to compare the first 100 data points
pid4_100 = data[0:100].pid4
pid5_100 = data[0:100].pid5
pid6_100 = data[0:100].pid5
# and the last 100 points
pid4_last = data[len(data.index)-100:len(data.index)].pid4
pid5_last = data[len(data.index)-100:len(data.index)].pid5
pid6_last = data[len(data.index)-100:len(data.index)].pid6 
# combine these collections into a list

data_to_plot = [pid_4, pid_5, pid_6, pid4_100, pid5_100, pid6_100, pid4_last, pid5_last, pid6_last]

# Create a figure instance

boxplot = plt.figure(1, figsize=(9,6))

#Create an axes instance
ax = boxplot.add_subplot(1,1,1)

#Create the box plot, then if I know that I want to make changes later, add the patch_artist=True
#as this will give me access to colours etc. 

bp = ax.boxplot(data_to_plot, patch_artist=True)

# To change the outline colour, fill colour and the line width of the boxes.
for box in bp['boxes' ]:
# changes the outline colour
    box.set( color='#7570b3', linewidth=3)
#changes the fill colour    
    box.set( facecolor = '#1b9e77') 
# change colour and line width of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='#7570b3', linewidth=2)
# change colour and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='#7570b3', linewidth=2)
# change colour and linewidth of the medians
for median in bp['medians']: 
    median.set(color='#b2df8a', linewidth=2)
#change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='#e7298a', alpha=0.5)    
        

# Custom x-axis labels
ax.set_xticklabels(['PID 4', 'PID 5', 'PID 6', 'PID 4 100', 'PID 5 100', 'PID 6 100', 'PID 4 LAST', 'PID 5 LAST', 'PID6 LAST'])
plt.ylabel(" PID / V")

# Show the plot when running the code.
plt.show()




# ctr+=1
#rangefig.show()
	
# isop_cyl = 13.277	#ppbv
# mfchi_range = 100.	#sccm
# mfchi_sccm = df_xrange.mfchiR*(mfchi_range/5.)
# mfclo_range = 20.	#sccm
# mfclo_sccm = df_xrange.mfcloR*(mfclo_range/5.)
# dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
# isop_mr = dil_fac*isop_cyl
# print 'Isoprene mixing ratio'
# print 'mean =',np.mean(isop_mr)
# print 'stddev =',np.std(isop_mr)
# 
# #######################################
# 
# #plot up other variables
# varfig = plt.figure()
# #RH
# rhax = varfig.add_subplot(3,1,1)
# RH = (((data.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data.Temp)
# rhax.plot(data.TheTime,RH,color='b',linewidth=3)
# rhax.set_ylabel("RH %")
# #Temp
# Tax = varfig.add_subplot(3,1,2)
# Tax.plot(data.TheTime,data.Temp*10.,color='r',linewidth=3)
# Tax.set_ylabel("Temp / oC")
# #MFC voltages
# mfcax = varfig.add_subplot(3,1,3)
# mfcax.plot(data.TheTime,data.mfcloR,color='g',linewidth=3, label = 'MFCLO')
# mfcax.plot(data.TheTime,data.mfchiR,color='k',linewidth=3, label = 'MFCHI')
# mfcax.set_ylabel("MFC / V")
# mfclegend = mfcax.legend()
# plt.xlabel("Time")
# plt.show()