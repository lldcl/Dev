import os
import pandas as pd
import operator
import numpy as np
import MOS_reader as mr
import pylab
import voc_reader
import matplotlib.pyplot as plt
from pylab import *
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

path = "../Data/wacl_data/Raw_data_files/"
f_date = '201610'
Time_avg = '10S'
cal_file = os.listdir(path + f_date +'/MOS')
# The name of the MOS file to be analysed
data_concat = mr.readin(path, f_date, cal_file, 1, 5, Time_avg)
data_voc = voc_reader.extract_voc('../Data/', 'Detailed Compound Concentrations', 'Analyte vs Time', Time_avg) 
data_merge = data_concat.merge(data_voc, how = 'inner', on = ['Time'])

# Calculating the sum of vocs
VOC = ['CH5O+ (methanol;H3O+) (ppb)',	'CH3CN.H+ (acetonitrile;H3O+) (ppb)',	'C3H7O+ (acetone;H3O+) (ppb)',	'C4H6O.H+ (3-buten-2-one;H3O+) (ppb)',	'C6H6.H+ (benzene;H3O+) (ppb)',	'C8H10.H+ (m-xylene;H3O+) (ppb)',	'C9H12.H+ (1,2,4-trimethylbenzene;H3O+) (ppb)',	'H3O+.C8H18 (octane;H3O+) (ppb)',	'C9H20.H3O+ (nonane;H3O+) (ppb)',	'H3O+.C10H22 (decane;H3O+) (ppb)',	'CH3O+ (formaldehyde;H3O+) (ppb)',
]
temp = matrix(data_voc["CH5O+ (methanol;H3O+) (ppb)"])
for i in VOC[1:]:
        temp = temp + matrix(data_voc[i])
temp = temp.transpose()
data_merge['vocs'] = pd.DataFrame(temp)
dataset = pd.DataFrame({'Time' : []})
dataset['Time'] = data_merge['Time'].apply(lambda x: x.hour) *3600 + data_merge['Time'].apply(lambda x: x.minute)*60 + data_merge['Time'].apply(lambda x: x.second)
dataset['CO'] = data_merge['CO_ave1']
dataset['CO_square'] = data_merge['CO_ave1']**2
dataset['rh'] = data_merge['rh']
dataset['rh_square'] = data_merge['rh']**2
#dataset['vocs'] = data_merge['vocs']
#dataset['vocs_square'] = data_merge['vocs']**2
dataset['MOS'] = data_merge['MOS1c_Av']
dataset['MOS_square'] = data_merge['MOS1c_Av']**2
np.random.seed(1)
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train_X, test_X = dataset[0:train_size], dataset[train_size:len(dataset)]
train_y, test_y = data_merge.vocs[0:train_size], data_merge.vocs[train_size:len(data_merge)]
train_X, test_X = train_X.as_matrix(), test_X.as_matrix()
train_y, test_y = train_y.as_matrix(), test_y.as_matrix()
# Instanciate a Gaussian Process model
kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
# Fit to data using Maximum Likelihood Estimation of the parameters
gp.fit(train_X, train_y)
# Make the prediction
pred_y, pred_mse = gp.predict(test_X, return_std=True)

fig = plt.figure()
plt.plot(data_merge.Time[train_size:len(dataset)], pred_y, color="black",linewidth=2,label = 'Predicted vocs')
plt.plot(data_merge.Time[train_size:len(dataset)], test_y, color="firebrick",linewidth=2, label = 'Syft data')
plt.show()
print(pred_mse)