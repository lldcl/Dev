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
data_concat = data_concat.merge(data_voc, how = 'inner', on = ['Time'])
# Find all the columns in the file that have these titles, as these are the MOS columns.
print(np.corrcoef(data_concat['CH5O+ (methanol;H3O+) (ppb)'], data_concat['HIH1_Av']))
sub = 'Diff'
MOS=[ 'MOS1c_Av','CH5O+ (methanol;H3O+) (ppb)',	'HIH1_Av']
Difffig = plt.figure("Diff")
ax1 = Difffig.add_subplot(111)
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
for n,c in zip(MOS,colors):
    temp = matrix(data_concat[n][1:]) - matrix(data_concat[n][0:-1])
    temp = pd.DataFrame(temp)
    temp = pd.DataFrame.transpose(temp)
    if n == 'MOS1c_Av' :
        ax1.plot(data_concat.Time[1:],temp*3500,color=c,linewidth=3)
    elif n == 'HIH1_Av':
        ax1.plot(data_concat.Time[1:],temp*1000,color=c,linewidth=3)
    else:
        ax1.plot(data_concat.Time[1:],temp,color=c,linewidth=3)
    #ax1.plot(data_concat.Time,data_concat[n],color=c,linewidth=3)
    #pylab.ylim([-0.09,0.09])
    plt.legend(MOS, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize='large')    # the legend text fontsize
    #plt.ylabel("MOS (V, differentiated)", size=20)
    plt.ylabel("MOS (V) & VOCs & Humidity", size=20)
    plt.xlabel("Time", size=20)	
plt.show()
