import os
import pandas as pd
import operator
import numpy as np
import pylab
import voc_reader
import csv
import MOS_reader as mr
from pylab import *
from datetime import datetime
from sklearn import linear_model
from scipy import stats

# The path to where the raw files are stored
path = "../Data/wacl_data/Raw_data_files/"
f_date = '201610'
cal_file = os.listdir(path + f_date +'/MOS')
# The name of the MOS file to be analysed
data_concat = mr.readin(path, f_date, cal_file, 1, 5)
#correlation between MOSc and other signals

MOS=[ 'MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']
print('MOS/NO2_ave1')
corrcoef_data = []
for i in MOS:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave1']))
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave1'])[0][1])
df = pd.DataFrame(corrcoef_data, columns = ['MOSx/NO2_ave1'])
