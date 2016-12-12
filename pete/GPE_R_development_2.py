
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

import scipy
import rpy2.robjects as ro
import pandas.rpy.common as com
from rpy2.robjects import pandas2ri
pandas2ri.activate()

###################################

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201602/'

train_filename = '30strain_100216_1.csv'
test_filename = '30stest_100216_1.csv'

train_data = pd.read_csv(path+train_filename,dtype='float32')
test_data = pd.read_csv(path+test_filename,dtype='float32')

#find all sensors in file
sub = 'MOS'
mos = [s for s in train_data.columns if sub in s]

sensors = mos

X_var = ['RH1','Temp','VS','T_int']
y_var = ['isop_mr']

mean_pred = pd.DataFrame(index = test_data.index,columns=range(0,5))
for s in sensors:
 	X_var = X_var+[s]

trainvar_fig= plt.figure()
for v in range(0,len(X_var)):
	vfig = trainvar_fig.add_subplot(len(X_var),1,v)
	vfig.scatter(train_data[y_var],train_data[X_var[v]],color='k')
	vfig.set_ylabel(X_var[v])
	vfig.set_xlabel(y_var)	
trainvar_fig.show()

X=X_var+y_var

for m in mos:
	globals()[str(m)+'_fig']= plt.figure()
	for v in range(0,len(X)):
		vfig = globals()[str(m)+'_fig'].add_subplot(len(X),1,v)
		vfig.scatter(train_data[m],train_data[X[v]],color='k')
		vfig.set_ylabel(X[v])
		vfig.set_xlabel(m)	
	globals()[str(m)+'_fig'].show()



mean_pred = pd.DataFrame(index = test_data.index)	#,columns=range(0,5))
guedjdojdo=ughruhkdw
# r commands
ro.globalenv['grid']= train_data[X]
ro.r("save(grid,file='gridfile2')")
ro.globalenv['testgrid']= test_data[X]
ro.r("save(testgrid,file='testgridfile2')")
# guedjdojdo=ughruhkdw
ro.r("source('GPE_1.R')")
mean_pred[0] = com.load_data('mean')
ro.r("plot(grid)")


mean_pred.to_csv('Pred_100216'+test_filename)

### Train data skill

for x in X_var:
	globals()[str(m)+'_fig']= plt.figure()
	for v in range(0,len(X_var)):
		vfig = globals()[str(m)+'_fig'].add_subplot(len(X_var),1,v)
		vfig.scatter(train_data[X_var[v]],train_data[m],color='k')
		vfig.set_ylabel(X_var[v])
		vfig.set_xlabel(m)	
	globals()[str(m)+'_fig'].show()







### Test data comparisons

# Isop_fig= plt.figure()
# sfig = Isop_fig.add_subplot(1,1,1)
# Isop_obs = sfig.plot(test_data.index,test_data.isop_mr,color='g',linewidth=3,label='VOC observation')
# # for s in mean_pred:
# # 	if (s>0):
# # 		sfig.plot(test_data.index,mean_pred[s],color='k',label='isoprene model')		
# sfig.plot(test_data.index,mean_pred,color='k',label='VOC model')		
# handles, labels = sfig.get_legend_handles_labels()
# sfig.legend(handles, labels,loc=4)
# sfig.tick_params(axis='both', which='major', labelsize=16)
# sfig.set_ylabel('VOC/ ppb', fontsize=20)
# sfig.set_xlabel("Time", fontsize=20)
# Isop_fig.show()

MOS1_fig= plt.figure()
sfig = MOS1_fig.add_subplot(1,1,1)
MOS1_obs = sfig.plot(test_data.index,test_data.MOS1,color='g',linewidth=3,label='MOS1 obs')
sfig.plot(test_data.index,mean_pred,color='k',label='MOS1 model')		
handles, labels = sfig.get_legend_handles_labels()
sfig.legend(handles, labels,loc=4)
sfig.tick_params(axis='both', which='major', labelsize=16)
sfig.set_ylabel('MOS1/ v', fontsize=20)
sfig.set_xlabel("Time", fontsize=20)
MOS1_fig.show()
