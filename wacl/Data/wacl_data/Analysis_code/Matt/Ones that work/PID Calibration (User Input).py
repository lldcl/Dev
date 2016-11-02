import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
import time

#############################
## Data read

backslashstring = '\ko'

#####Asking if the user would like to load from the memory stick
pogk = 2
while pogk == 2:
    memorystickq = raw_input('Are you loading from a your memory stick? ')
    if memorystickq == 'y' or memorystickq == 'yes' or memorystickq == 'YES' or memorystickq == 'Yes' or memorystickq == 'Y':
        print '\n\n(Okie doke, loading from E:\Bursary thing\PID Data\Organised and or Edited)'+backslashstring[0]
        path = "E:\Bursary thing\PID Data\Organised and or Edited"+backslashstring[0]
        pogk = 1
    elif memorystickq == 'no' or memorystickq == 'n' or memorystickq == 'No' or memorystickq =='NO' or memorystickq == 'N':
        print '\n\n(Okie doke, loading from C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited then)'
        path = 'C:\Users\mat_e_000\Documents\Bursary thing\PID Data\Organised and or Edited'+backslashstring[0]
        pogk = 1
    elif memorystickq == 'somewhere else' or memorystickq == 'elsewhere':
        path = raw_input('please enter where you would like to load from: ')
    else:
        print 'Please enter y or n...'


#####Asking if the user would like to load from today's data
while pogk == 1:
    dateq = raw_input('\nDo you want to load from today\'s data? ')
    if dateq == 'y' or dateq == 'yes' or dateq == 'YES' or dateq == 'Yes' or dateq == 'Y':
        print """\n(Okie doke, loading today's data)"""
        filename1 = str((time.strftime('%m-%d')))+'\d20' + str((time.strftime('%y%m%d'))) + '_0'+ raw_input('Which file would you like to load? ')
        pogk = 2
    elif dateq == 'n' or dateq == 'no' or dateq == 'No' or dateq == 'NO' or dateq == 'N':
        date = raw_input('\n\nOkie doke, what date would you like to load data from?\nInput date in format mmdd: ')
        filename1 =  date[0:2] + '-' + date[2:4] + '\d20' + str((time.strftime('%y'))) + date + '_0' + raw_input('\n\nWhich file would you like to load? ')
        pogk = 0
        print filename1
    else:
        print 'Please enter y or n...'
        
cal = 'Y'
plots = 'Y'

print "\n\nFile Reference = ", path + filename1

data1 = pd.read_csv(path+filename1) #reading file

Time = data1.TheTime-data1.TheTime[0] #retreiving the time data
Time*=60.*60.*24. #converting times
data1.TheTime = pd.to_datetime(data1.TheTime,unit='D') #converting the data to a date and time
T1 = pd.datetime(1899,12,30,0) 
T2 = pd.datetime(1970,01,01,0)
offset=T1-T2
data1.TheTime+=offset

tmp_pid = data1.pid1.notnull() #finds any missing PID values
tmp_flow = data1.mfchiR.notnull() #finds any missing mfchiR values

isop_cyl = 13.277	#how much isoprene in ppbv
mfchi_range = 100.	#sccm (100 as a float) finding the range of the mass flow controller high
mfchi_sccm = data1.mfchiR*(mfchi_range/5.) #mfchi 

mfclo_range = 20.	#sccm
mfclo_sccm = data1.mfcloR*(mfclo_range/5.) # finding range of the mass flow controller low

dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm) #finding how much the isoprene has been diluted by
isop_mr = dil_fac*isop_cyl #actual concentration of isoprene

#############################
## Signal vs Isop for calibration experiments
'''placing the blue and green lines (finding where the mfclo changes and placing the lines a set distance away)'''
if (cal == 'Y'):
   mfc_set = np.zeros((len(data1.mfclo)),dtype=bool) #creating an array for the time and mfclo data full of boolean values
   for i in range(1,len(data1.mfchi)): #iterating over the length of the data
      if (np.logical_and(np.logical_and(np.isfinite(data1.mfchi[i]),np.isfinite(data1.mfclo[i])),np.logical_or(data1.mfchi[i]!=data1.mfchi[i-1],data1.mfclo[i]!=data1.mfclo[i-1]))): #checking if mfchi and lo have been recorded properly and that the mfc data point is not equal to the one before it
         mfc_set[i] = "True" #if the conditions are met the code inputs a true value in the array, if it is true then the mfclo has changed
   cal_N = np.sum(mfc_set) #adding up the terms in mfc set
   cal_cols = ['StartT','EndT','Isop','Isop_stddev','pid_V','pid_stddev'] #giving the table headers
   cal_pts = [range(0,cal_N)] #making a list from 0 to the value of cal_N in steps of 1
   delay = 100     #Delay at start of cal step
   cal_df = pd.DataFrame(index=cal_pts, columns=cal_cols) #deciding where to put the blue line (the table gets values later)

   mfc_setS = data1.index[mfc_set] #finding the places mfc_set appears in the data
   mfc_setS+=delay #adding the delay and placing the blue line

   mfc_setF = data1.index[mfc_set] 
   mfc_setF = np.append(mfc_setF,len(data1.TheTime)) 
   mfc_setF = np.delete(mfc_setF,0) #deleting the first term in the mfc_set finish
   mfc_setF-=11      #Delay at end of cal step (placing green line)
   
   for pt in range(0,cal_N):
   #check that the flows are the same at the start and end of the range over which you are averaging
      if (np.logical_and(data1.mfclo[mfc_setS[pt]]==data1.mfclo[mfc_setF[pt]],data1.mfchi[mfc_setS[pt]]==data1.mfchi[mfc_setF[pt]])): 
         tp_Isop = isop_mr[mfc_setS[pt]:mfc_setF[pt]]
         tp_pid = data1.pid1[mfc_setS[pt]:mfc_setF[pt]]
         cal_df.Isop[pt] = tp_Isop.mean()
         cal_df.Isop_stddev[pt] = tp_Isop.std()
         cal_df.pid_V[pt] = tp_pid.mean()
         cal_df.pid_stddev[pt] = tp_pid.std()
         cal_df.StartT[pt] = Time[mfc_setS[pt]]
         cal_df.EndT[pt] = Time[mfc_setF[pt]]
      

#############################
## Plots
if (plots == 'Y'):

	pid_avg = pd.rolling_mean(data1.pid1,300)

	fig1 = plt.figure()
	
	ax1 = fig1.add_subplot(111)
	
	pid = ax1.plot(Time[tmp_pid],data1.pid1[tmp_pid], linewidth=3,color='r')
	pid_10s = ax1.plot(Time[tmp_pid],pid_avg[tmp_pid], linewidth=3,color='b')
	
	plt.ylabel("PID / V")
	
	ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
	
	isop = ax2.plot(Time[tmp_flow],isop_mr[tmp_flow], linewidth=3,color='g')

	if (cal == 'Y'):
		ax2.plot([Time[data1.index[mfc_setS]],Time[data1.index[mfc_setS]]],[0.,2.],color='b',linestyle = '-')
		ax2.plot([Time[data1.index[mfc_setF]],Time[data1.index[mfc_setF]]],[0.,2.],color='g',linestyle = '-')

	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")
	plt.ylabel("Isop / ppb")
	plt.xlabel('Time / s', fontsize = 20)

	if (cal == 'Y'):
		
		slope,intercept,r_value,p_value,std_err=stats.linregress(cal_df.Isop,cal_df.pid_V)
		isop_fit = [0.,np.max(cal_df.Isop)]
		pid_fit = [intercept,(np.max(cal_df.Isop)*slope)+intercept]
		fig3 = plt.figure()
		plt.plot(cal_df.Isop,cal_df.pid_V,"o")
		plt.plot(isop_fit,pid_fit)
		plt.ylabel('Pid / V', fontsize = 20)
		plt.xlabel('[Isop] / ppb', fontsize = 20)
#plt.ylim(0,1e-4)

	plt.show()

	
print '\n(graphs will appear in a new window)\n'
print 'intercept = ', intercept
print 'slope = ', slope
print 'R value =', r_value

start_time = 1
end_time = 3000

start_timea = 1
end_timea = 3000

pid1 = data1.pid1[start_time:end_time]
pid2 = data1.pid2[start_timea:end_timea]



print 'pid1 std = ', np.std(pid1)
print 'pid2 std = ', np.std(pid2)