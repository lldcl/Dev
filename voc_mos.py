import os
import pandas as pd
import operator
import numpy as np
import pylab
import voc_reader
import MOS_reader as mr
from pylab import *
from sklearn import linear_model
from scipy import stats

# The path to where the raw files are stored
path = 'D:/WACL/Data/wacl_data/Raw_data_files/'
f_date = '201610'
cal_file = os.listdir(path + f_date +'/MOS')
# The name of the MOS file to be analysed
data_concat = mr.readin(path, f_date, cal_file, 1, 5)
#correlation between MOSc and other signals

data_voc = voc_reader.extract_voc('D:/WACL/Data/', 'Detailed Compound Concentrations', 'Analyte vs Time') 
data_merge = data_concat.merge(data_voc, how = 'inner', on = ['Time'])
print(np.corrcoef(data_merge['MOS1c_Av'], data_merge['CH5O+ (methanol;H3O+) (ppb)']))
print(np.corrcoef(data_merge['MOS1c_Av'], data_merge['CH3CN.H+ (acetonitrile;H3O+) (ppb)']))
print(np.corrcoef(data_merge['MOS1c_Av'], data_merge['C3H7O+ (acetone;H3O+) (ppb)']))
print(np.corrcoef(data_merge['MOS1c_Av'], data_merge['C4H6O.H+ (3-buten-2-one;H3O+) (ppb)']))
print(np.corrcoef(data_merge['MOS1c_Av'], data_merge['C6H6.H+ (benzene;H3O+) (ppb)']))