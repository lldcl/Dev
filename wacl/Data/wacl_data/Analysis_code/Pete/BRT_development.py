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

filenames = [
# '5sconcat_1125.csv']
#'30sconcat_1013_1019.csv',

for f in filenames:
	print f
	data = pd.read_csv(path+f)

	#find all pids in file
	sub = 'pid'
	pids = [s for s in data.columns if sub in s]

	try:
		data_concat = data_concat.append(data)
		print ' concatenating'
	except NameError:
		data_concat = data.copy(deep=True)
		print ' making data_concat'

# X = data_concat[['pid6','RH','Temp']]
# y = data_concat['isop_mr']

# data_concat.TheTime = pd.to_datetime(data_concat.TheTime,unit='D')


X = data_concat[['RH1','VS','Temp','pid5']]#'MOS1','MOS2']]
y = data_concat['isop_mr']

offset = int(X.shape[0] * 0.75)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

###Fit regression model
# params_grid = {'learning_rate': [0.01,0.05, 0.02, 0.01],
# 				'max_depth': [4,6],
# 				'min_samples_leaf': [3,5,9,17],
# 				'max_features': [1.0,0.3,0.1],
# 				'max_leaf_nodes': [2,3,4,5,6]}
# est = ensemble.GradientBoostingRegressor(n_estimators=3000,loss='lad')
# gs_cv = GridSearchCV(est,params_grid,n_jobs =8).fit(X_train,y_train)
# params = gs_cv.best_params_
# params['n_estimators']= 3000
# params['loss']='lad'

params={'learning_rate': 0.02,
		'loss': 'lad',
		'max_depth': 4,
		'max_features': 0.1,
		'max_leaf_nodes': 2,
		'min_samples_leaf': 5,
		'n_estimators': 3000}
 
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
plt.yticks(pos, X.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()

from scipy import stats
rhcalfig = plt.figure()

slope, intercept, r_value, p_value, std_err = stats.linregress(X.RH1,y*1e3)

rfig = rhcalfig.add_subplot(1,1,1)
rfig.plot(X.RH1,y*1e3,'o',color='k')
rfig.set_ylabel('PID5 / mV')
rfig.set_xlabel("RH / %")

rhcalfig.show()

Isop_fig= plt.figure()
sfig = Isop_fig.add_subplot(1,1,1)

sfig.plot(data_concat.index[offset:],data_concat.isop_mr[offset:],color='k',linewidth=3,label='Isoprene observation')
Tmodel = sfig.plot(data_concat.index[offset:],y_output,color='b',linewidth=3,label='isoprene model')

# sfig.plot(data_concat.index[offset:],data_concat.pid5[offset:]*1e3,color='k',linewidth=3,label='PID observation')
# Tmodel = sfig.plot(data_concat.index[offset:],y_output*1e3,color='b',linewidth=3,label='PID model')

# Tlin = sfig.plot(data_concat.TheTime[offset:],(data_concat.RH[offset:]*slope)+intercept,color='r',linewidth=3,label='PID#5 RH linear reg')
handles, labels = sfig.get_legend_handles_labels()
sfig.legend(handles, labels,loc=4)#, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0.)
sfig.tick_params(axis='both', which='major', labelsize=16)

# sfig.set_ylabel('PID/ mV', fontsize=20)
sfig.set_ylabel('Isoprene/ ppb', fontsize=20)

sfig.set_xlabel("Time", fontsize=20)
Isop_fig.show()

#plot up the pid voltages
pidfig = plt.figure()
ax1 = pidfig.add_subplot(111)
colors = ["red", "blue" , "green", "orange", "purple"]
for n,c in zip(pids,colors):
	ax1.plot(data_concat.index,data_concat[n],color=c,linewidth=3)
plt.legend(pids, bbox_to_anchor=(0., 1.02, 1., .102),ncol=5, loc=8, mode="expand", borderaxespad=0.)
plt.ylabel("PID / V")
plt.xlabel("Index")
pidfig.show()

#plot up other variables
varfig = plt.figure()

rhax = varfig.add_subplot(3,1,1)
rhax.plot(data_concat.index,data_concat.RH1,color='b',linewidth=3)
rhax.set_ylabel("RH %")

isopax = varfig.add_subplot(3,1,2)
isopax.plot(data_concat.index,data_concat.isop_mr,color='g',linewidth=3)
isopax.set_ylabel("Isop / ppbv")

varfig.show()



