
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

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/201512/'

train_filename = '10strain_1203_06.csv'
test_filename = '10stest_1203_06.csv'

train_data = pd.read_csv(path+train_filename,dtype='float32')
test_data = pd.read_csv(path+test_filename,dtype='float32')

#find all pids in file
sub = 'pid'
pids = ['pid5','pid6','pid7']
# [s for s in train_data.columns if sub in s]

sub2 = 'MOS'
mos = [s for s in train_data.columns if sub2 in s]

sensors = pids+mos

X_var = ['RH1','Temp','VS']
y_var = ['isop_mr']

mean_pred = pd.DataFrame(index = test_data.index,columns=range(0,5))
# for s in sensors:
# 	X = X_var+[s]+y_var
for i in range(0,5):

#	X = X_var+sensors+y_var
	X = X_var+mos+y_var

# r commands
	ro.globalenv['grid']= train_data[X]
	ro.globalenv['testgrid']= test_data[X] 
	ro.r("source('GPE_1.R')")
	mean_pred[i] = com.load_data('mean')


mean_pred.to_csv('Pred_MOSonly2'+test_filename)

Isop_fig= plt.figure()
sfig = Isop_fig.add_subplot(1,1,1)
Isop_obs = sfig.plot(test_data.index,test_data.isop_mr,color='g',linewidth=3,label='Isoprene observation')
for s in mean_pred:
	if (s>0):
		sfig.plot(test_data.index,mean_pred[s],color='k',label='isoprene model')		
handles, labels = sfig.get_legend_handles_labels()
sfig.legend(handles, labels,loc=4)
sfig.tick_params(axis='both', which='major', labelsize=16)
sfig.set_ylabel('Isoprene/ ppb', fontsize=20)
sfig.set_xlabel("Time", fontsize=20)
Isop_fig.show()

