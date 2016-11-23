import os
import pandas as pd
import operator
import numpy as np
import MOS_reader as mr
import pylab
import voc_reader
import matplotlib.pyplot as plt
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
dataset = pd.DataFrame(temp, columns = ['vocs'])
dataset['Time'] = data_merge['Time'].apply(lambda x: x.hour) *3600 + data_merge['Time'].apply(lambda x: x.minute)*60 + data_merge['Time'].apply(lambda x: x.second)
dataset['CO'] = data_merge['CO_ave1']
dataset['rh'] = data_merge['rh']
#dataset['MOS'] = data_merge['MOS1c_Av']
#print(dataset.Time)
#scaler = MinMaxScaler(feature_range=(0, 1))
#dataset = scaler.fit_transform(dataset)
#print(dataset.Time)
# split into train and test sets
train_X = dataset.as_matrix()
train_Y = data_merge['MOS1c_Av'].as_matrix()

# create model
model = Sequential()
model.add(Dense(8, input_dim=4, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
seed = 7
np.random.seed(seed)
# checkpoint
filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]
# Fit the model
model.fit(train_X, train_Y, validation_split=0.1, nb_epoch=50, batch_size=20, callbacks=callbacks_list, verbose=0)
trainPredictPlot = np.empty_like(train_Y)
trainPredictPlot[:] = np.nan
trainPredict = model.predict(train_X)
plt.plot(trainPredict)
plt.plot(train_Y)
print(model.get_weights())
plt.show()


