"""Universal pid data file reader/plotter to look at individual files
#Add an option to do stats on sections --> from matplotlib.widgets import SpanSelector
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.grid_search import GridSearchCV

###################################

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201511/'

train_filename = '10strain_1126_0204.csv'
test_filename = '10stest_1126_0204.csv'

train_data = pd.read_csv(path+train_filename,dtype='float32')
test_data = pd.read_csv(path+test_filename,dtype='float32')

#find all pids in file
sub = 'pid'
pids = [s for s in train_data.columns if sub in s]


X_var = ['RH1','Temp','pid5','pid6','pid7','pid8']
y_tr = train_data['isop_mr']
y_ts = test_data['isop_mr']

X_train, y_train = train_data[X_var], y_tr
X_test, y_test = test_data[X_var], y_ts

###Fit regression model
# params_grid = {'learning_rate': [0.01,0.05, 0.02, 0.01],
# 				'max_depth': [4,6],
# 				'min_samples_leaf': [3,5,9,17],
# 				'max_features': [1.0,0.3,0.1],
# 				'max_leaf_nodes': [2,3,4,5,6],
# 				'loss' : ['lad','ls','huber','quantile']}
# est = ensemble.GradientBoostingRegressor(n_estimators=3000)#,loss='lad')
# gs_cv = GridSearchCV(est,params_grid,n_jobs =2).fit(X_train,y_train)
# params = gs_cv.best_params_
# params['n_estimators']= 3000
# params['loss']='lad'

# #params for 25_03 pid5 calc (only rh,vs,T,isop predictors)
# params = {'learning_rate': 0.05,
#  'loss': 'quantile',
#  'max_depth': 6,
#  'max_features': 1.0,
#  'max_leaf_nodes': 5,
#  'min_samples_leaf': 17,
#  'n_estimators': 3000}

# #params for 25_03_T2 pid5 calc (only rh,vs,T,isop predictors)
# params = {'learning_rate': 0.02,
#  'loss': 'lad',
#  'max_depth': 6,
#  'max_features': 1.0,
#  'max_leaf_nodes': 4,
#  'min_samples_leaf': 3,
#  'n_estimators': 3000}

# #params for 25_03_T2 isop calc ('RH1','VS','Temp','pid5','pid6','pid7','pid8','MOS1','MOS2' predictors)
params = {'learning_rate': 0.05,
 'loss': 'ls',
 'max_depth': 6,
 'max_features': 1.0,
 'max_leaf_nodes': 3,
 'min_samples_leaf': 9,
 'n_estimators': 3000}
 
# params={'learning_rate': 0.02,
# 		'loss': 'lad',
# 		'max_depth': 4,
# 		'max_features': 0.1,
# 		'max_leaf_nodes': 2,
# 		'min_samples_leaf': 5,
# 		'n_estimators': 3000}
 
# 20151125_01
# params ={'learning_rate': 0.05,
#  'loss': 'lad',
#  'max_depth': 4,
#  'max_features': 0.3,
#  'max_leaf_nodes': 2,
#  'min_samples_leaf': 5,
#  'n_estimators': 3000}

# params = {'loss': 'lad','n_estimators': 3000, 'max_features': 0.3, 'learning_rate': 0.01, 'max_depth': 6, 'max_leaf_nodes': 2, 'min_samples_leaf': 5}
clf = ensemble.GradientBoostingRegressor(**params)
# clf = ensemble.GradientBoostingRegressor(loss='lad',n_estimators = 3000, max_features= 1.0, learning_rate= 0.01, max_depth= 4, max_leaf_nodes = 2,min_samples_leaf= 3)

clf.fit(X_train, y_train)
y_output = clf.predict(X_test)
mse = mean_squared_error(y_test, clf.predict(X_test))
print("MSE: %.6f" % mse)

# Plot training deviance 
# compute test set deviance
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

for i, y_output in enumerate(clf.staged_decision_function(X_test)):
    test_score[i] = clf.loss_(y_test, y_output)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

# ###############################################################################
# Plot feature importance
feature_importance = clf.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], align='center')
plt.yticks(pos, X_train.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()

from scipy import stats


Isop_fig= plt.figure()
sfig = Isop_fig.add_subplot(1,1,1)
sfig.plot(test_data.index,test_data.isop_mr,color='k',linewidth=3,label='Isoprene observation')
# sfig.plot(test_data.index,test_data.pid5*1e3,color='k',linewidth=3,label='PID observation')
# Tmodel = sfig.plot(test_data.index,y_output*1e3,color='b',linewidth=3,label='PID model')
Tmodel = sfig.plot(test_data.index,y_output,color='b',linewidth=3,label='isoprene model')
handles, labels = sfig.get_legend_handles_labels()
sfig.legend(handles, labels,loc=4)#, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0.)
sfig.tick_params(axis='both', which='major', labelsize=16)
# sfig.set_ylabel('PID/ mV', fontsize=20)
sfig.set_ylabel('Isoprene/ ppb', fontsize=20)
sfig.set_xlabel("Time", fontsize=20)
Isop_fig.show()

