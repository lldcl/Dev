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
cal_file = os.listdir(path + f_date +'/MOS')
# The name of the MOS file to be analysed
data_concat = mr.readin(path, f_date, cal_file, 1, 5)
data_voc = voc_reader.extract_voc('../Data/', 'Detailed Compound Concentrations', 'Analyte vs Time') 
data_merge = data_concat.merge(data_voc, how = 'inner', on = ['Time'])

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
plt.show()