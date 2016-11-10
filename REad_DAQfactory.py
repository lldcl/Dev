"""Analysing the MOS files collected by running ambient air over the sensors. MOS refers to the metal oxide sensors, which 
are more sensitive towards VOCs but there are a few other sensors in the same air flow too. These include a Temp probe, an 
RH probe and electrochemical sensors monitoring CO, NO, NO2 and ozone becasue we are worried these might interfere with 
the MOS signal"""
import os
import pandas as pd
import operator
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import MOS_reader as mr
import pylab
import voc_reader
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText



# The path to where the raw files are stored
path = "../Data/wacl_data/Raw_data_files/"
f_date = '201610'
Time_avg = '300S'
cal_file = os.listdir(path + f_date +'/MOS')
# The name of the MOS file to be analysed
data_concat = mr.readin(path, f_date, cal_file, 1, 5, Time_avg)
data_voc = voc_reader.extract_voc('../Data/', 'Detailed Compound Concentrations', 'Analyte vs Time', Time_avg) 
data_merge = data_concat.merge(data_voc, how = 'inner', on = ['Time'])

# Find all the columns in the file that have these titles, as these are the MOS columns.
sub = 'MOS'
MOS=[ 'MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    #pylab.ylim([-0.09,0.09])
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    #plt.ylabel("MOS (V, differentiated)", size=20)
    plt.ylabel("MOS (V)", size=20)
    plt.xlabel("Time", size=20)	
MOSfig.show()

sub = 'MOSb'
MOS=[ 'MOS1b_Av','MOS2b_Av','MOS3b_Av','MOS4b_Av','MOS5b_Av','MOS6b_Av','MOS7b_Av','MOS8b_Av']
MOSbfig = plt.figure("MOSb data")
ax1 = MOSbfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("MOS (V)", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
MOSbfig.show()

sub = 'MOSc'
MOS=[ 'MOS1c_Av','MOS2c_Av','MOS3c_Av','MOS4c_Av','MOS5c_Av','MOS6c_Av','MOS7c_Av','MOS8c_Av']
MOScfig = plt.figure("MOSc data")
ax1 = MOScfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("MOS (V)", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
MOScfig.show()

sub = 'CO'
MOS=[ 'CO_ave1']
COfig = plt.figure("CO_ave1 data")
ax1 = COfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("CO", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
COfig.show()

sub = 'NO'
MOS=[ 'NO_ave1']
NOfig = plt.figure("NO_ave1 data")
ax1 = NOfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("NO", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
NOfig.show()


sub = 'Temperature'
MOS=[ 'LM65T1_Av']
Tmpfig = plt.figure("Temperature data")
ax1 = Tmpfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("Temperature", size=20)
    plt.xlabel("Time", size=20)	
plt.title(cal_file)	
Tmpfig.show()


#data_merge.to_csv('test3.csv')

sub = 'Humidity'
MOS=[ 'rh']
Hmdfig = plt.figure("Humidity data")
ax1 = Hmdfig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3)
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    plt.ylabel("Humidity", size=20)
    plt.xlabel("Time", size=20)	
Hmdfig.show()

sub = 'vocs1'
voc1=[ 'CH5O+ (methanol;H3O+) (ppb)',	'CH3CN.H+ (acetonitrile;H3O+) (ppb)',	'C3H7O+ (acetone;H3O+) (ppb)',	'C4H6O.H+ (3-buten-2-one;H3O+) (ppb)',	'C6H6.H+ (benzene;H3O+) (ppb)',	'C8H10.H+ (m-xylene;H3O+) (ppb)',	'C9H12.H+ (1,2,4-trimethylbenzene;H3O+) (ppb)',	'H3O+.C8H18 (octane;H3O+) (ppb)',	'C9H20.H3O+ (nonane;H3O+) (ppb)',	'H3O+.C10H22 (decane;H3O+) (ppb)',	'CH3O+ (formaldehyde;H3O+) (ppb)',	'MOS1c_Av']
VOCs1fig = plt.figure("voc1")
ax1 = VOCs1fig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
for n,c in zip(voc1,colors):
    if n == 'MOS1c_Av':
        ax = ax2.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax       
    else:
        ax = ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='large')    # the legend text fontsize
ax1.set_ylabel("vocs1", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
VOCs1fig.show()


sub = 'vocs2'
voc2=[ 'NO+.C3H6O (acetone;NO+) (ppb)','C5H8+ (isoprene;NO+) (ppb)',	'C4H6O.NO+ (3-buten-2-one;NO+) (ppb)',	'NO+.C4H8O (butanone;NO+) (ppb)',	'C6H6+ (benzene;NO+) (ppb)',	'NO.C6H6+ (benzene;NO+) (ppb)',	'C7H8+ (toluene;NO+) (ppb)',	'C8H10+ (m-xylene;NO+) (ppb)',	'C9H12+ (1,2,4-trimethylbenzene;NO+) (ppb)',	'C4H6+ (1,3-butadiene;NO+) (ppb)', 'MOS1c_Av']
VOCs2fig = plt.figure("vocs2")
ax1 = VOCs2fig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
for n,c in zip(voc2,colors):
    if n == 'MOS1c_Av':
        ax = ax2.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax       
    else:
        ax = ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='large')    # the legend text fontsize
ax1.set_ylabel("vocs2", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
VOCs2fig.show()

sub = 'vocs3'
voc3=[ 'C8H17+ (octane;NO+) (ppb)',	'C10H21+ (decane;NO+) (ppb)', 'C3H6O+ (acetone;O2+) (ppb)',	'C5H7+ (isoprene;O2+) (ppb)',	'C5H8+ (isoprene;O2+) (ppb)',	'C4H8O+ (butanone;O2+) (ppb)',	'C6H6+ (benzene;O2+) (ppb)',	'C7H8+ (toluene;O2+) (ppb)',	'C7H7+ (m-xylene;O2+) (ppb)', 'MOS1c_Av']
VOCs3fig = plt.figure("vocs3")
ax1 = VOCs3fig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
for n,c in zip(voc3,colors):
    if n == 'MOS1c_Av':
        ax = ax2.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax       
    else:
        ax = ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='large')    # the legend text fontsize
ax1.set_ylabel("vocs3", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
VOCs3fig.show()

sub = 'vocs4'
voc4=[ 'C8H10+ (m-xylene;O2+) (ppb)',	'C9H12+ (1,2,4-trimethylbenzene;O2+) (ppb)',	'C4H6+ (1,3-butadiene;O2+) (ppb)',	'C8H18+ (octane;O2+) (ppb)',	'C10H22+ (decane;O2+) (ppb)',	'C2H6O+ (ethanol;O2+) (ppb)', 'MOS1c_Av']
VOCs4fig = plt.figure("vocs4")
ax1 = VOCs4fig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
for n,c in zip(voc4,colors):
    if n == 'MOS1c_Av':
        ax = ax2.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax       
    else:
        ax = ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='large')    # the legend text fontsize
ax1.set_ylabel("vocs4", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
VOCs4fig.show()

sub = 'vocs5'
voc5 = ['C2H5O+ (ethanol;NO+) (ppb)',  'C2H5O+ (ethanol;O2+) (ppb)', 'MOS1c_Av']
VOCs5fig = plt.figure("vocs5")
ax1 = VOCs5fig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
for n,c in zip(voc5,colors):
    if n == 'MOS1c_Av':
        ax = ax2.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax       
    else:
        ax = ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='large')    # the legend text fontsize
ax1.set_ylabel("vocs5", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
VOCs5fig.show()

sub = 'vocs6'
voc6 = ['C3H3+ (1,3-butadiene;O2+) (ppb)', 'MOS1c_Av']
VOCs6fig = plt.figure("vocs6")
ax1 = VOCs6fig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
for n,c in zip(voc6,colors):
    if n == 'MOS1c_Av':
        ax = ax2.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax       
    else:
        ax = ax1.plot(data_merge.Time,data_merge[n],color=c,linewidth=3) + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='large')    # the legend text fontsize
ax1.set_ylabel("vocs6", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
VOCs6fig.show()

sub = 'VOC_total'
VOC = ['CH5O+ (methanol;H3O+) (ppb)',	'CH3CN.H+ (acetonitrile;H3O+) (ppb)',	'C3H7O+ (acetone;H3O+) (ppb)',	'C4H6O.H+ (3-buten-2-one;H3O+) (ppb)',	'C6H6.H+ (benzene;H3O+) (ppb)',	'C8H10.H+ (m-xylene;H3O+) (ppb)',	'C9H12.H+ (1,2,4-trimethylbenzene;H3O+) (ppb)',	'H3O+.C8H18 (octane;H3O+) (ppb)',	'C9H20.H3O+ (nonane;H3O+) (ppb)',	'H3O+.C10H22 (decane;H3O+) (ppb)',	'CH3O+ (formaldehyde;H3O+) (ppb)',
]
temp = matrix(data_voc["CH5O+ (methanol;H3O+) (ppb)"])
for i in VOC[1:]:
        temp = temp + matrix(data_voc[i])
temp = temp.transpose()
VOCsfig = plt.figure("VOC_total/MOS1c_AV")
ax1 = VOCsfig.add_subplot(111)
ax2 = ax1.twinx()
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax = []
ax = ax2.plot(data_merge.Time,data_merge['MOS1c_Av'],color='black',linewidth=3)       
ax = ax1.plot(data_merge.Time,temp,color=c,linewidth=3, label = 'VOC_total') + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
ax1.set_ylabel("vocs_total(H3O+)", size=20)
ax2.set_ylabel("MOSc1_Av", size=20)
plt.xlabel("Time", size=20)	
plt.show()
