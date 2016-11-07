"""total voc concentration(syft)"""
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
import heapq

# The path to where the raw files are stored
path = "../Data/wacl_data/Raw_data_files/"
f_date = '201610'
cal_file = os.listdir(path + f_date +'/MOS')
# The name of the MOS file to be analysed
data_concat = mr.readin(path, f_date, cal_file, 1, 5)

data_voc = voc_reader.extract_voc('../Data/', 'Detailed Compound Concentrations', 'Analyte vs Time') 
data_merge = data_concat.merge(data_voc, how = 'inner', on = ['Time'])

print(max(data_concat["rh"]), min(data_concat["rh"]))
VOC = ['CH5O+ (methanol;H3O+) (ppb)',	'CH3CN.H+ (acetonitrile;H3O+) (ppb)',	'C3H7O+ (acetone;H3O+) (ppb)',	'C4H6O.H+ (3-buten-2-one;H3O+) (ppb)',	'C6H6.H+ (benzene;H3O+) (ppb)',	'C8H10.H+ (m-xylene;H3O+) (ppb)',	'C9H12.H+ (1,2,4-trimethylbenzene;H3O+) (ppb)',	'H3O+.C8H18 (octane;H3O+) (ppb)',	'C9H20.H3O+ (nonane;H3O+) (ppb)',	'H3O+.C10H22 (decane;H3O+) (ppb)',	'CH3O+ (formaldehyde;H3O+) (ppb)',
]

temp = matrix(data_voc["CH5O+ (methanol;H3O+) (ppb)"])
for i in VOC[1:]:
        temp = temp + matrix(data_voc[i])
temp = temp.transpose()
print(max(temp), min(temp))
print(min(data_voc['CH5O+ (methanol;H3O+) (ppb)']))