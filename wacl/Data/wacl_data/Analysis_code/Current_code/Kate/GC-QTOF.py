# File to read the GC-QTOF results. 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText


path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/'

filename = 'mos_data_050516_02.txt'

#read file into dataframe
data = pd.read_csv(path+filename)

# Turn the time into a number:
new_time = pd.to_datetime(data.TheTime)

#plot up the MOS voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
ax1.plot(new_time,data.Sensor_ave,color="green",linewidth=3)
ax1.set_ylabel("MOS voltage (V)")
ax1.set_xlabel("Time")
plt.show()



