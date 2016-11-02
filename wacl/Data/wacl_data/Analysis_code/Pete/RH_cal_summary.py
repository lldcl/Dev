import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy.odr as odr
from RH_cal_fn import *

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'

cal_files = ['d20151021_01','d20151021_02','d20151021_04','d20151021_05','d20151021_06','d20151022_01','d20151022_02','d20151104_01','d20151104_02','d20151104_03','d20151109_03']

slopes = pd.DataFrame(columns=['pid4','pid5','pid6'])
slope_errs = pd.DataFrame(columns=['pid4','pid5','pid6'])
RH_stats = pd.DataFrame(columns=['median','min','max'])

for i in cal_files:
   folder = list(i)[1:7]
   filename = "".join(folder)+'/'+i
   RH_cal_data, raw_data = RH_cal_fn(path,filename,'30S')
   slope = pd.Series(RH_cal_data.loc['Slope (mV/%)',:],name=i)
   slopes = slopes.append(slope)
   slope_err = pd.Series(RH_cal_data.loc['Slope_err',:],name=i)
   slope_errs = slope_errs.append(slope_err)
   RH_stat = pd.Series([RH_cal_data.pid4['RH_median'],RH_cal_data.pid4['RH_min'],RH_cal_data.pid4['RH_max']],index = ['median','min','max'],name=i)
   RH_stats = RH_stats.append(RH_stat)

   try:
      data_concat = data_concat.append(raw_data)
      print ' concatenating'
   except NameError:
      data_concat = raw_data.copy(deep=True)
      print ' making data_concat'

slopefig = plt.figure()
ctr = 1
for p in slopes.columns:
	sfig = 'pax'+str(ctr)
	sfig = slopefig.add_subplot(3,1,ctr)
	sfig.errorbar(RH_stats['median'],slopes[p],color='b', yerr =slope_errs[p],  xerr = [RH_stats['median']-RH_stats['min'],RH_stats['max']-RH_stats['median']],fmt='o')
	sfig.set_ylabel(p+'RH cal slope / (mV/%)')
	sfig.set_xlabel("median RH / %")
	ctr+=1
slopefig.show()

datafig = plt.figure()
ctr = 1
for p in slopes.columns:
	dfig = 'pax'+str(ctr)
	dfig = datafig.add_subplot(3,1,ctr)
	dfig.errorbar(data_concat.RH,data_concat[p]*1e3,color='b',fmt='o')
	dfig.set_ylabel(p+'/ mV')
	dfig.set_xlabel("RH / %")
	ctr+=1
datafig.show()
