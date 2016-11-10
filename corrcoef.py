"""This program calculates the correlation coefficient between MOS signals and other signals such as O3 and temperature"""
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
Time_avg = '600S'
data_concat = mr.readin(path, f_date, cal_file, 1, 5, Time_avg)
data_voc = voc_reader.extract_voc('../Data/', 'Detailed Compound Concentrations', 'Analyte vs Time', Time_avg) 
data_merge = data_concat.merge(data_voc, how = 'inner', on = ['Time'])

#correlation between MOSc and other signals
MOS=[ 'MOS1_Av','MOS2_Av','MOS3_Av','MOS4_Av','MOS5_Av','MOS6_Av','MOS7_Av','MOS8_Av']
print('MOS/NO2_ave1')
corrcoef_data = []
for i in MOS:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave1'])[0][1])
df = pd.DataFrame(corrcoef_data, columns = ['MOSx/NO2_ave1'])

print('MOS/NO2_ave2')
corrcoef_data = []
for i in MOS:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave2'])[0][1])
df['MOSx/NO2_ave2'] = corrcoef_data

print('MOS/NO_ave1')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['NO_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO_ave1'])[0][1])
df['MOSx/NO_ave1'] = corrcoef_data

print('MOS/NO_ave2')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['NO_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO_ave2'])[0][1])
df['MOSx/NO_ave2'] = corrcoef_data

print('MOS/CO_ave1')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['CO_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['CO_ave1'])[0][1])
df['MOSx/CO_ave1'] = corrcoef_data

print('MOS/CO_ave2')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['CO_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['CO_ave2'])[0][1])
df['MOSx/CO_ave2'] = corrcoef_data

print('MOS/O3_ave1')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['O3_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['O3_ave1'])[0][1])
df['MOSx/O3_ave1'] = corrcoef_data

print('MOS/O3_ave2')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['O3_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['O3_ave2'])[0][1])
df['MOSx/O3_ave2'] = corrcoef_data

print('MOS/rh')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['rh'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['rh'])[0][1])
df['MOSx/rh'] = corrcoef_data

print('MOS/LM65T1_Av')
corrcoef_data = []
for i in MOS: 
    print(np.corrcoef(data_concat[i],data_concat['LM65T1_Av'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['LM65T1_Av'])[0][1])
df['MOSx/LM65T1_Av'] = corrcoef_data

#correlation between MOSc and other signals
MOSc=[ 'MOS1c_Av','MOS2c_Av','MOS3c_Av','MOS4c_Av','MOS5c_Av','MOS6c_Av','MOS7c_Av','MOS8c_Av']
print('MOSc/NO2_ave1')
corrcoef_data = []
for i in MOSc:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave1'])[0][1])
df['MOScx/NO2_ave1'] = corrcoef_data

print('MOSc/NO2_ave2')
corrcoef_data = []
for i in MOSc:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave2'])[0][1])
df['MOScx/NO2_ave2'] = corrcoef_data

print('MOSc/NO_ave1')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['NO_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO_ave1'])[0][1])
df['MOScx/NO_ave1'] = corrcoef_data

print('MOSc/NO_ave2')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['NO_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO_ave2'])[0][1])
df['MOScx/NO_ave2'] = corrcoef_data

print('MOSc/CO_ave1')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['CO_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['CO_ave1'])[0][1])
df['MOScx/CO_ave1'] = corrcoef_data

print('MOSc/CO_ave2')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['CO_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['CO_ave2'])[0][1])
df['MOScx/CO_ave2'] = corrcoef_data

print('MOSc/O3_ave1')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['O3_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['O3_ave1'])[0][1])
df['MOScx/O3_ave1'] = corrcoef_data

print('MOSc/O3_ave2')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['O3_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['O3_ave2'])[0][1])
df['MOScx/O3_ave2'] = corrcoef_data

print('MOSc/rh')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['rh'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['rh'])[0][1])
df['MOScx/rh'] = corrcoef_data

print('MOSc/LM65T1_Av')
corrcoef_data = []
for i in MOSc: 
    print(np.corrcoef(data_concat[i],data_concat['LM65T1_Av'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['LM65T1_Av'])[0][1])
df['MOScx/LM65T1_Av'] = corrcoef_data

#correlation between MOSb and other signals
MOSb=[ 'MOS1b_Av','MOS2b_Av','MOS3b_Av','MOS4b_Av','MOS5b_Av','MOS6b_Av','MOS7b_Av','MOS8b_Av']
print('MOSb/NO2_ave1')
corrcoef_data = []
for i in MOSb:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave1'])[0][1])
df['MOSbx/NO2_ave1'] = corrcoef_data

print('MOSb/NO2_ave2')
corrcoef_data = []
for i in MOSb:   
    print(np.corrcoef(data_concat[i],data_concat['NO2_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO2_ave2'])[0][1])
df['MOSbx/NO2_ave2'] = corrcoef_data

print('MOSb/NO_ave1')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['NO_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO_ave1'])[0][1])
df['MOSbx/NO_ave1'] = corrcoef_data

print('MOSb/NO_ave2')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['NO_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['NO_ave2'])[0][1])
df['MOSbx/NO_ave2'] = corrcoef_data

print('MOSb/CO_ave1')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['CO_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['CO_ave1'])[0][1])
df['MOSbx/CO_ave1'] = corrcoef_data

print('MOSb/CO_ave2')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['CO_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['CO_ave2'])[0][1])
df['MOSbx/CO_ave2'] = corrcoef_data

print('MOSb/O3_ave1')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['O3_ave1'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['O3_ave1'])[0][1])
df['MOSbx/O3_ave1'] = corrcoef_data

print('MOSb/O3_ave2')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['O3_ave2'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['O3_ave2'])[0][1])
df['MOSbx/O3_ave2'] = corrcoef_data

print('MOSb/rh')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['rh'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['rh'])[0][1])
df['MOSbx/rh'] = corrcoef_data

print('MOSb/LM65T1_Av')
corrcoef_data = []
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['LM65T1_Av'])[0][1])
    corrcoef_data.append(np.corrcoef(data_concat[i], data_concat['LM65T1_Av'])[0][1])
df['MOSbx/LM65T1_Av'] = corrcoef_data

"""MOSb=[ 'MOS1b_Av','MOS2b_Av','MOS3b_Av','MOS4b_Av','MOS5b_Av','MOS6b_Av','MOS7b_Av','MOS8b_Av']
print('MOSb/VOC')
for i in MOSb:   
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])
   
print('MOSb/VOC')
for i in MOSb:   
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])
   
print('MOSb/VOC')
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])

print('MOSb/VOC')
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])

print('MOSb/VOC')
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])

print('MOSb/VOC')
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])

print('MOSb/VOC')
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])

print('MOSb/VOC')
for i in MOSb: 
    print(np.corrcoef(data_concat[i],data_concat['VOC'])[0][1])"""


temp1 = matrix(data_concat['MOS1b_Av'][1:]) - matrix(data_concat['MOS1b_Av'][0:-1])
temp1 = pd.DataFrame(temp1)
temp2 = matrix(data_concat['MOS1c_Av'][1:]) - matrix(data_concat['MOS1c_Av'][0:-1])
temp2 = pd.DataFrame(temp2)
temp3 = matrix(data_concat['rh'][1:]) - matrix(data_concat['rh'][0:-1])
temp3 = pd.DataFrame(temp3)
print(np.corrcoef(data_concat['MOS1b_Av'],data_concat['MOS1c_Av']))
print(np.corrcoef(data_concat['MOS1_Av'][1:],temp3))
print(np.corrcoef(temp1, data_concat['rh'][1:]))


VOC = ['CH5O+ (methanol;H3O+) (ppb)',	'CH3CN.H+ (acetonitrile;H3O+) (ppb)',	'C3H7O+ (acetone;H3O+) (ppb)',	'C4H6O.H+ (3-buten-2-one;H3O+) (ppb)',	'C6H6.H+ (benzene;H3O+) (ppb)',	'C8H10.H+ (m-xylene;H3O+) (ppb)',	'C9H12.H+ (1,2,4-trimethylbenzene;H3O+) (ppb)',	'H3O+.C8H18 (octane;H3O+) (ppb)',	'C9H20.H3O+ (nonane;H3O+) (ppb)',	'H3O+.C10H22 (decane;H3O+) (ppb)',	'CH3O+ (formaldehyde;H3O+) (ppb)',	'NO+.C3H6O (acetone;NO+) (ppb)',	'C5H8+ (isoprene;NO+) (ppb)',	'C4H6O.NO+ (3-buten-2-one;NO+) (ppb)',	'NO+.C4H8O (butanone;NO+) (ppb)',	'C6H6+ (benzene;NO+) (ppb)',	'NO.C6H6+ (benzene;NO+) (ppb)',	'C7H8+ (toluene;NO+) (ppb)',	'C8H10+ (m-xylene;NO+) (ppb)',	'C9H12+ (1,2,4-trimethylbenzene;NO+) (ppb)',	'C4H6+ (1,3-butadiene;NO+) (ppb)',	'C8H17+ (octane;NO+) (ppb)',	'C10H21+ (decane;NO+) (ppb)',	'C2H5O+ (ethanol;NO+) (ppb)',	'C3H6O+ (acetone;O2+) (ppb)',	'C5H7+ (isoprene;O2+) (ppb)',	'C5H8+ (isoprene;O2+) (ppb)',	'C4H8O+ (butanone;O2+) (ppb)',	'C6H6+ (benzene;O2+) (ppb)',	'C7H8+ (toluene;O2+) (ppb)',	'C7H7+ (m-xylene;O2+) (ppb)',	'C8H10+ (m-xylene;O2+) (ppb)',	'C9H12+ (1,2,4-trimethylbenzene;O2+) (ppb)',	'C3H3+ (1,3-butadiene;O2+) (ppb)',	'C4H6+ (1,3-butadiene;O2+) (ppb)',	'C8H18+ (octane;O2+) (ppb)',	'C10H22+ (decane;O2+) (ppb)',	'C2H5O+ (ethanol;O2+) (ppb)',	'C2H6O+ (ethanol;O2+) (ppb)'
]
voc_corr = []

for i in VOC:
    print(i)
    print(np.corrcoef(data_merge['rh'],data_merge[i])[0][1])
for i, j, k in zip(MOS, MOSb, MOSc):
    print(i)
    print(np.corrcoef(data_merge['rh'],data_merge[i])[0][1])
    print(j)
    print(np.corrcoef(data_merge['rh'],data_merge[j])[0][1])
    print(k)
    print(np.corrcoef(data_merge['rh'],data_merge[k])[0][1])

for i in VOC:
    print(i + '/MOS1c_Av')
    voc_corr.append(i + '/MOS1c_Av')
    #print(data_merge['MOS1c_Av'],data_merge[i])
    print(np.corrcoef(data_merge['MOS1c_Av'],data_merge[i])[0][1])
    voc_corr.append(np.corrcoef(data_merge['MOS1c_Av'],data_merge[i])[0][1])

for i in VOC:
    j = VOC.index(i)
    for k in VOC[j+1:]:
        print(i + '/' + k)
        voc_corr.append(i + '/' + k)
        print(np.corrcoef(data_merge[i],data_merge[k])[0][1])
        voc_corr.append(np.corrcoef(data_merge[i],data_merge[k])[0][1])
 
voc_df = pd.DataFrame(voc_corr)
voc_df.to_csv('voc_corr_600s.csv')
print(np.corrcoef(data_merge['CH5O+ (methanol;H3O+) (ppb)'],data_merge['rh'])[0][1])
df.to_csv('corre_600s.csv')
"""with open('filename.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile,, quoting=csv.QUOTE_ALL)
    wr.writerow(voc_corr)
df.to_csv('coef.csv')"""
