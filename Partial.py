
# Median MOS signal
#data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']].median(axis=1)
# Without the broken MOS 4 and 6
data_concat['Median_MOS_signal'] = data_concat[['MOS1_Av','MOS2_Av','MOS3_Av','MOS5_Av','MOS7_Av','MOS8_Av']].median(axis=1)
# Plot the median MOS signal with temperature, over time.
median = plt.figure()
ax1 = median.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green", linewidth=5, label="MOS")
ax2.plot(data_concat.Time, data_concat.Temp2_Av, color="pink", label="Temp 2 (oC)")
ax1.set_ylabel("Median MOS signal (V)")
ax1.set_xlabel("Time")
ax2.set_ylabel("Temperature")
median.show()

# Plot up temperature and humidity which are recorded in the same air flow as the MOS.
Variables = plt.figure("Temp and humidity")
ax1 = Variables.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Temp1_Av, color="red", label="Temp 1 (oC)")
ax1.plot(data_concat.Time, data_concat.Temp2_Av, color="pink", label="Temp 2 (oC)")
#ax1.plot(data_concat.Time, data_concat.Temp3_Av, color="purple", label="Temp 3 (oC)")
ax1.plot(data_concat.Time, data_concat.RH1_Av, color="blue", label="RH 1 (%)")
#ax2.plot(data_concat.Time, data_concat.RH2_Av, color="navy", label="RH 2 (%)")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="green",linewidth = 3, label="Median MOS")
ax1.set_ylabel("Temperature (oC) and RH (%)",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=1)
ax2.legend(loc=2)
Variables.show()

# Correlation plot
correlation = plt.figure("Temp and humidity correlated")
ax1a = correlation.add_subplot(111)
#ax2 = ax1a.twinx()
ax1a.scatter(data_concat.Temp1_Av, data_concat.Median_MOS_signal, color="red", label="Temp 1 (oC)")
#ax1a.scatter(data_concat.RH1_Av, data_concat.Median_MOS_signal , color="blue", label="RH 1 (%)")
ax1a.set_ylabel("Median MOS (V)",size=16)
ax1a.set_xlabel(" Temperature (oC) and RH (%)",size=16)
ax1a.legend(loc=1)
#ax2.legend(loc=2)
correlation.show()


##########################################################################################
#Other electrochemical sensprs in line with the MOS

Variables1 = plt.figure("CO, ozone and NOx")

# Find all the columns in the file that have these titles, as these are the MOS columns.
CO=['CO_OP1_Av','CO_OP2_Av']
# Plot up the CO data
ax1 = Variables1.add_subplot(311)
colors = ["black","firebrick"]
for u,v in zip(CO,colors):
    ax1.plot(data_concat.Time,data_concat[u],color=v,linewidth=3)
    plt.legend(CO, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("Carbon monoxide", size=20)
    plt.xlabel("Time", size=20)	

ozo=['O3_OP1_Av','O3_OP2_Av']
# Plot up the ozone data
ax2 = Variables1.add_subplot(312)
colors = ["blue","darkblue"]
for w,x in zip(ozo,colors):
    ax2.plot(data_concat.Time,data_concat[w],color=x,linewidth=3)
    plt.legend(ozo, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("Ozone", size=20)
    plt.xlabel("Time", size=20)	

NOx=['NO2_OP1_Av','NO2_OP2_Av', 'NO_OP1_Av','NO_OP2_Av']
# Plot up the NOx data
ax3 = Variables1.add_subplot(313)
colors = ["green","darkgreen"]
for y,z in zip(NOx,colors):
    ax3.plot(data_concat.Time,data_concat[y],color=z,linewidth=3, label=[y])
    plt.legend(NOx, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("NOx", size=20)
    plt.xlabel("Time", size=20)	
Variables1.show()


# MOS versus in-line electrochemical ozone and NO data 
MOSozone = plt.figure("MOS and in-line ozone and NO sensor")
ax1 = MOSozone.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.O3_OP1_Av, color="blue", label="Ozone (ppb)")
ax1.plot(data_concat.Time, data_concat.NO2_OP1_Av, color="green", label="NO2 (ppb)")
ax1.plot(data_concat.Time, data_concat.CO_OP1_Av, color="orange", label="CO")
ax1.plot(data_concat.Time, data_concat.NO_OP1_Av, color="purple", label="NO (ppb)")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="black",linewidth = 3, label="Median MOS")
ax1.set_ylabel("Ozone and NO2",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=2)
ax2.legend(loc=1)
MOSozone.show()

# The MOS sensors are (supposedly) more sensitive towards VOCs and CO is the closest to this class of compound out of 
# the electrochemical sensors so this is plotted up separately. 
MOSCO = plt.figure("MOS and in-line CO sensor")
ax1 = MOSCO.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot(data_concat.Time, data_concat.CO_OP1_Av, color="orange", label="CO")
ax2.plot(data_concat.Time, data_concat.Median_MOS_signal, color="black",linewidth = 3, label="Median MOS")
ax1.set_ylabel("CO",size=16)
ax2.set_ylabel(" Median MOS (V)",size=16)
ax1.set_xlabel("Time")
ax1.legend(loc=2)
ax2.legend(loc=1)
MOSCO.show()


# A plot to see if there is a strong correlation between the two. 
COdep = plt.figure("MOS and CO linked?")
ax1 = COdep.add_subplot(111)
ax1.scatter(data_concat.CO_OP1_Av, data_concat.Median_MOS_signal,  color="silver", label="CO")
ax1.set_xlabel("CO",size=16)
ax1.set_ylabel(" Median MOS (V)",size=16)
slope1, intercept1, R2value1, p_value1, st_err1 = stats.linregress(data_concat.CO_OP1_Av, data_concat.Median_MOS_signal)
ax1.plot([np.min(data_concat.CO_OP1_Av), np.max(data_concat.CO_OP1_Av)], [(slope1*np.min(data_concat.CO_OP1_Av))+intercept1, (slope1*np.max(data_concat.CO_OP1_Av))+intercept1])
# Get the linear regression paramenters to have 3 sig figs.
slope1 = ("%.3g" %slope1)
intercept1 = ("%.3g" % (intercept1))
R2value1 = ("%.3g" % (R2value1))
# Add these to the plot, and specify the location of the text using co-ordinates based on the axis.
ax1.text(1,2,'y = ' +str(slope1)+'x +' +str(intercept1)+ 'R2='+str(R2value1), style='italic', fontsize = 15) 
plt.show()