"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy.optimize import curve_fit

#path = '/Users/ks826/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_data_files/'
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

filename = '201510/d20151002_02'
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

#plot up the pid voltages without the correction
#Create a figure instance
pidfig = plt.figure()
#Create the three sub plots, so they all appear in the same window
ax1 = pidfig.add_subplot(3,1,1)
ax2 = pidfig.add_subplot(3,1,2)
ax3 = pidfig.add_subplot(3,1,3)
# I want the relative humidity to be plotted on the same graph as the PID voltages so must create 
#more axes for them.
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective graphs.
ax1.plot(data.TheTime, data.pid1, color="red",linewidth=3)
ax2.plot(data.TheTime, data.pid2, color = "green", linewidth=3)
ax3.plot(data.TheTime, data.pid3, color = "blue", linewidth=3)
ax4.plot(data.TheTime, data.RH, color="black", linewidth=3)
ax5.plot(data.TheTime, data.RH, color="black", linewidth=3)
ax6.plot(data.TheTime, data.RH, color="black",linewidth=3)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 1 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 2 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel('PID 3 /V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')
ax6.set_ylabel('RH %')
# Setting the title for the overall figure
pidfig.set_label('Uncalibrated PID data')


plt.show()
	


# To show the graph of PID vs RH.
# To remove the values that aren't numbers, it gets rid of the NaN things.
data = data.dropna()
# Create a figure instance
RHchart = plt.figure()
#Create an axis instance
ax1 = RHchart.add_subplot(1,1,1)
# Create the graph by telling the plot function to get the data from the columns pid# and RH
ax1.plot(data.RH, data.pid1, color="green", linewidth=3)

# Setiing a linear fit to the data
# Creating a function to model and create data. x, a and b are really odd...
def func(x, a, b):
    return a * x + b
    
# Executing curve fit on noisy data
popt, pcov = curve_fit(func, data.RH, data.pid1)
# popt returns the best fit values for the parameters of the given model.
x2 = np.linspace(min(data.RH),max(data.RH),100)
y2 = func(x2, popt[0], popt[1])
ax1.plot(x2,y2, color="black", linewidth=3)
print popt
 
ax1.set_xlabel('RH %')
ax1.set_ylabel('PID 1 /V')

plt.show()
	


# To ensure there is a good correlation between the isoprene concentration and the PID voltages
# I want to plot isoprene versus PID.
# These will print out the mean and standard deviation of the isoprene level.
#The mixing ratio of isoprene in the cylinder is 13.277 ppbv
isop_cyl = 13.277	
# The maximum flow rate of the mass flow controller (mfc) is 100 sccm  
mfchi_range = 100.
# The mfc data is recorded as a voltage, and this needs to be converted to a flow in sccm.
# mfchi_sccm is the flow in sccm, mfchiR is the mfc voltage from the mfc that controls the flow of dry air to
# to the PIDs. This is multiplied by the max mfc flow divided by the voltage range
# ( The mfc is controlled over a 5V range). 
mfchi_sccm = data.mfchiR*(mfchi_range/5.)
# Now for the mfc that controls the flow from the isoprene canister. Lower maximum flow.
mfclo_range = 20.	#sccm
mfclo_sccm = data.mfcloR*(mfclo_range/5.)
# The dilution factor needs to be determined, using the flow from the dry air and the isoprene can.
dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm)
# The isoprene mixing ratio can be determined by multiplying the dil. fac. by the cylinder [isoprene].
Isop_mr = dil_fac*isop_cyl
print 'Isoprene mixing ratio'
print 'mean =',np.mean(Isop_mr)
print 'stddev =',np.std(Isop_mr)
# Create a figure instance
isop = plt.figure()

# Create the three subplots for PIDs 1,2 and 3.
ax1 = isop.add_subplot(3,1,1)
ax2 = isop.add_subplot(3,1,2)
ax3 = isop.add_subplot(3,1,3)
# Create the graphs
ax1.plot(Isop_mr, data.pid1, color="purple", linewidth=3)
ax2.plot(Isop_mr, data.pid2, color= "green", linewidth=3)
ax3.plot(Isop_mr, data.pid3, color="blue", linewidth=3)
# Labelling axes
ax1.set_xlabel('Isoprene MR / ppbv')
ax1.set_ylabel('PID 1 /V')
ax2.set_xlabel('Isoprene MR / ppbv')
ax2.set_ylabel('PID 2 /V')
ax3.set_xlabel('Isoprene MR / ppbv')
ax3.set_ylabel('PID 3 /V')

plt.show()

# Trying to calibrate for RH
# Tell the program to get the data from the various columns then do the calculation on it

pid1 = data.pid1 - (0.061509 * data.RH)
pid2 = data.pid2 - (0.038940 * data.RH)	
pid3 = data.pid3 - (0.042824 * data.RH)
#plot up the pid voltages without the correction
#Create a figure instance
RHcorr = plt.figure()
#Create the three sub plots, so they all appear in the same window
plt1 = RHcorr.add_subplot(3,1,1)
plt2 = RHcorr.add_subplot(3,1,2)
plt3 = RHcorr.add_subplot(3,1,3)

colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective scatter graphs.
plt1.scatter(Isop_mr,data.pid1,color="purple",linewidth=3)
plt2.scatter(Isop_mr,data.pid2, color = "green", linewidth=3)
plt3.scatter(Isop_mr,data.pid3, color = "blue", linewidth=3)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
plt1.set_xlabel('Isoprene / ppbv')
plt1.set_ylabel('RH Corrected PID 1 /V')
plt1.axis([0, 2.6, 0.052, 0.054])
plt2.set_xlabel('Isoprene / ppbv')
plt2.set_ylabel('RH Corrected PID 2 /V')
plt2.axis([0, 2.6, 0.052, 0.054])
plt3.set_xlabel('Isoprene / ppbv')
plt3.set_ylabel('RH Corrected PID 3 /V')
plt3.axis([0, 2.6, 0.053, 0.055])

# Setting the title for the overall figure
RHcorr.set_label('Calibrated PID data')
plt.show()




