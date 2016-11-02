"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from scipy import stats


#path = '/Users/ks826/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_data_files/'
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/'

filename ='201511/d20151111_03b'
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

#plot up the pid voltages over time (without the RH correction)
#Create a figure instance
pidfig = plt.figure()
#Create the three sub plots, so they all appear in the same window
ax1 = pidfig.add_subplot(3,1,1)
ax2 = pidfig.add_subplot(3,1,2)
ax3 = pidfig.add_subplot(3,1,3)
# I want the relative humidity to be plotted on the same graph as the PID voltages so must create 
# secondary axes for each graph.
RH = (((data.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data.Temp*100)
pid4 = data.pid4*1000
pid5 = data.pid5*1000
pid6 = data.pid6*1000
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective graphs.
ax1.plot(data.TheTime, pid4, color = "red",linewidth=3)
ax2.plot(data.TheTime, pid5, color = "green", linewidth=3)
ax3.plot(data.TheTime, pid6, color = "blue", linewidth=3)
ax4.plot(data.TheTime, RH, color="black", linewidth=3)
ax5.plot(data.TheTime, RH, color="black", linewidth=3)
ax6.plot(data.TheTime, RH, color="black",linewidth=3)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1.set_xlabel('Time')
ax1.set_ylabel('PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel('PID 5 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel('PID 6 /V')
ax4.set_ylabel('RH %')
ax5.set_ylabel('RH %')
ax6.set_ylabel('RH %')



	
########################
# The second set of graphs plot the relative humidity (RH) against the PID voltages
# To remove the values that aren't numbers, it gets rid of the NaN things.

RHplot = plt.figure("RH vs PID")
data = data.dropna()
#Create the three sub plots, so they all appear in the same window
ax1a = RHplot.add_subplot(3,1,1)
ax2a = RHplot.add_subplot(3,1,2)
ax3a = RHplot.add_subplot(3,1,3)
# data.RH gives the relative humidity as a voltage, so need to turn this into a n absolute value:
RH = (((data.RH/4.96)-0.16)/0.0062)/(1.0546-0.00216*data.Temp)
colors = ["red", "blue" , "green", "orange", "purple"]
pid4 = data.pid4*1000
pid5 = data.pid5*1000
pid6 = data.pid6*1000
#for n,c in zip(pids,colors):
# Creating the three respective scatter graphs. The 'o' command tells the code to plot with dots, not as a line graph.
ax1a.plot(RH, pid4, 'o', color= "purple", linewidth=1)
ax2a.plot(RH, pid5, 'o', color = "green", linewidth=1)
ax3a.plot(RH, pid6, 'o', color = "blue", linewidth=1)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1a.set_xlabel('RH (%)')
ax1a.set_ylabel('PID 4 / mV')
ax2a.set_xlabel('RH (%)')
ax2a.set_ylabel(' PID 5 / mV')
ax3a.set_xlabel('RH (%)')
ax3a.set_ylabel('PID 6 /V')
# The linear regression of the data points.

# Linear regression using scipy. The function will return the following 5 parameters in that order.
slope1, intercept1, R2_value1, p_value1, st_err1 = stats.linregress(RH, pid4)
slope2, intercept2, R2_value2, p_value2, st_err2 = stats.linregress(RH, pid5)
slope3, intercept3, R2_value3, p_value3, st_err3 = stats.linregress(RH, pid6)
print ("Gradient pid 4:", slope1)
print ("R2 value pid 4:", R2_value1)
print ("Gradient pid 5:", slope2)
print ("R2 value pid 5:", R2_value2)
print ("Gradient pid 6:", slope3)
print ("R2 value pid 6:", R2_value3)

ax1a.plot([np.min(RH), np.max(RH)], [(slope1*np.min(RH))+intercept1, (slope1*np.max(RH))+intercept1])
ax2a.plot([np.min(RH), np.max(RH)], [(slope2*np.min(RH))+intercept2, (slope2*np.max(RH))+intercept2])
ax3a.plot([np.min(RH), np.max(RH)], [(slope3*np.min(RH))+intercept3, (slope3*np.max(RH))+intercept3])

print ("Start time:", np.min(data.TheTime))
print ("End time:", np.max(data.TheTime))
print ("RH range:", (np.max(RH) - np.min(RH)))
print ("RH max:", np.max(RH))


predpid5 = RH*(1.9707*10**(-3))+54.1911
pid5 = data.pid5 - predpid5

RHcal = plt.figure("Correct for RH")
ax1 = RHcal.add_subplot(2,1,1)
ax2 = ax1.twinx()
ax1.plot(data.TheTime, predpid5, color="red")
ax2.plot(data.TheTime, pid5, color="blue")
plt.show()

############################

"""For now the isoprene conc doesn't need to be determined as only the RH is changing.

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
isop_mr = dil_fac*isop_cyl
print 'Isoprene mixing ratio'
print 'mean =',np.mean(isop_mr)
print 'stddev =',np.std(isop_mr)
# Plotting isoprene over time
# Tell the program to get the data from the various columns then do the calculation on it



#Create a figure instance
RHcorr = plt.figure()
#Create the three sub plots, so they all appear in the same window
ax1 = RHcorr.add_subplot(3,1,1)
ax2 = RHcorr.add_subplot(3,1,2)
ax3 = RHcorr.add_subplot(3,1,3)
# I want the relative humidity to be plotted on the same graph as the PID voltages so must create 
#more axes for them.
ax4 = ax1.twinx()
ax5 = ax2.twinx()
ax6 = ax3.twinx()
colors = ["red", "blue" , "green", "orange", "purple"]
#for n,c in zip(pids,colors):
# Creating the three respective graphs.
ax1.plot(data.TheTime,data.pid4,color="purple",linewidth=3)
ax2.plot(data.TheTime,data.pid5, color = "green", linewidth=3)
ax3.plot(data.TheTime,data.pid6, color = "blue", linewidth=3)
ax4.plot(data.TheTime,isopr_mr, color="black", linewidth=3)
ax5.plot(data.TheTime,isop_mr, color="black", linewidth=3)
ax6.plot(data.TheTime,isop_mr, color="black",linewidth=3)
#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
ax1.set_xlabel('Time')
ax1.set_ylabel(' PID 4 /V')
ax2.set_xlabel('Time')
ax2.set_ylabel(' PID 5 /V')
ax3.set_xlabel('Time')
ax3.set_ylabel(' PID 6 /V')
ax4.set_ylabel('Isoprene / ppb')
ax5.set_ylabel('Isoprene / ppb')
ax6.set_ylabel('Isoprene / ppb')
# Setting the title for the overall figure
RHcorr.set_label('Isoprene and PID data')



# Trying to calibrate for RH
# Tell the program to get the data from the various columns then do the calculation on it

pid4 = data.pid4 - (0.061509 * data.RH)
pid5 = data.pid5 - (0.038940 * data.RH)	
pid6 = data.pid6 - (0.042824 * data.RH)
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
plt1.scatter(isop_mr,data.pid4,color="purple",linewidth=3)
plt2.scatter(isop_mr,data.pid5, color = "green", linewidth=3)
plt3.scatter(isop_mr,data.pid6, color = "blue", linewidth=3)

#plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
# Labelling the x and y axis for each plot
plt1.set_xlabel('Isoprene / ppbv')
plt1.set_ylabel('RH Corrected PID 3 /V')
#plt1.axis([0, np.nanmax(isop_mr)+1, np.nanmin(data.pid4)-0.01, np.nanmax(data.pid4)+0.01])
plt2.set_xlabel('Isoprene / ppbv')
plt2.set_ylabel('RH Corrected PID 4 /V')
#plt2.axis([0, np.nanmax(isop_mr)+1, np.nanmin(data.pid5)-0.01, np.nanmax(data.pid5)+0.01])
plt3.set_xlabel('Isoprene / ppbv')
plt3.set_ylabel('RH Corrected PID 5 /V')
#plt3.axis([0, np.nanmax(isop_mr)+1, np.nanmin(data.pid6)-0.01, np.nanmax(data.pid6)+0.01])
# Setting the title for the overall figure
RHcorr.set_label('Calibrated PID data')
plt.show()
"""