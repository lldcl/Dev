
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

import scipy
import sklearn
from sklearn.gaussian_process import GaussianProcess


###################################

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'

filenames = ['201511/10sconcat_1112.csv']

for f in filenames:
	print f
	data = pd.read_csv(path+f)
# 	data=data.dropna()

	#find all pids in file
	sub = 'pid'
	pids = [s for s in data.columns if sub in s]

	try:
		data_concat = data_concat.append(data)
		print ' concatenating'
	except NameError:
		data_concat = data.copy(deep=True)
		print ' making data_concat'


data_concat.TheTime = pd.to_datetime(data_concat.TheTime,unit='D')


X = data_concat[['RH','pid5','Temp','VS','pid4']]
y = data_concat['isop_mr']

offset = int(X.shape[0] * 0.8)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

gp = GaussianProcess(regr='quadratic',corr='linear',theta0=0.1,nugget=0.5)
gp.fit(X_train, y_train)
y_output,mean_squared_error = gp.predict(X_test,eval_MSE=True)

plt.figure(figsize=(16, 12))
plt.plot(data_concat.TheTime[offset:], y_test, color='k', label='Observations')
plt.plot(data_concat.TheTime[offset:], y_output, 'o',color='b', label='Predictions')
plt.title('Observations and Predictions');
#plt.xlim([np.min(x), 120]);
plt.legend(loc='upper right')

y_toutput = gp.predict(X_train)

plt.figure(figsize=(16, 12))
plt.plot(data_concat.TheTime[:offset], y_train, color='k', label='Observations')
plt.plot(data_concat.TheTime[:offset], y_toutput, 'o',color='b', label='Predictions')
plt.title('Observations and Predictions');
#plt.xlim([np.min(x), 120]);
plt.legend(loc='upper right')

plt.show()