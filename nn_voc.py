"""Neural network prediction for vocs"""
import os
import pandas as pd
import operator
import numpy as np
import MOS_reader as mr
import pylab
import voc_reader
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from pylab import *
from sklearn import linear_model
from scipy import stats
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping


path = "../Data/wacl_data/Raw_data_files/"
f_date = '201610'
Time_avg = '30S'
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
"""print(dataset.Time)
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
print(dataset.Time)"""
data_merge['vocs'].to_csv('voc_total.csv')
train_X = dataset.as_matrix()
train_Y = data_merge['vocs'].as_matrix()
scaler = MinMaxScaler(feature_range=(0, 1))
train_X = scaler.fit_transform(train_X)
train_Y = scaler.fit_transform(train_Y)
#np.savetxt('neuralnetworknorm.csv', train_X, delimiter=",")
#pd.DataFrame(train_Y).to_csv('vocsnorm')
# create model
model = Sequential()
model.add(Dense(8, input_dim=7, init='uniform', activation='relu'))
model.add(Dense(6, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
seed = 7
np.random.seed(seed)
# checkpoint
"""filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]"""
earlystopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=100, verbose=0, mode='auto')
# Fit the model
"""model.fit(train_X, train_Y, validation_split=0.3, nb_epoch=5000, batch_size=1, callbacks=callbacks_list, verbose=0)"""
ax = []
model.fit(train_X, train_Y, validation_split=0.33, nb_epoch=5000, batch_size=20, callbacks=[earlystopping], verbose=0)
trainPredictPlot = np.zeros_like(train_Y)
trainPredictPlot[:] = np.nan
trainPredictPlot = model.predict(train_X)
VOCpredict = plt.figure("vocs prediction")
colors = ["black","firebrick", "lightgreen" , "c", "darkblue", "purple","orange","forestgreen", "lightskyblue" , "indigo", "dimgrey", "fuchsia"]
ax1 = VOCpredict.add_subplot(111)
ax2 = ax1.twinx()
ax = []
ax = ax1.plot(data_merge.Time, trainPredictPlot, color="black",linewidth=2,label = 'Predicted vocs')
ax = ax1.plot(data_merge.Time, train_Y, color="firebrick",linewidth=2, label = 'Syft data') + ax
ax = ax2.plot(data_merge.Time, dataset['MOS'], color="lightgreen",linewidth=2, label = 'MOS') + ax
labs = [l.get_label() for l in ax]
plt.legend(ax, labs, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=2, mode="expand", borderaxespad=0.)
ax1.set_ylabel("Normalized vocs concentration", size=20)
ax2.set_ylabel("MOS reading (V)", size=20)
plt.xlabel("Time", size=20)	
print(model.get_weights())
#np.savetxt('predictedvocs.csv',trainPredictPlot,delimiter=",")
plt.show()

