"""Read Met Data"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

#path = '/Users/ks826/Google Drive/Data_Analysis/Met_Data/Met_01_04July2016.txt'
path = '/Users/ks826/Google Drive/Data_Analysis/Met_Data/Met_June2016.txt'

# The file's column titles take over two rows of text. Skip the first row and take the second one as the header.
# Column names=['date','time','Temp1','Temp2','Temp3','Humidity','Windspeed','Wind_dir','Wind_dir_text','Hi_spped','Winddir2','Heat_chill','THW','THSW','IndexA','Pressure_bar','S_rain','S_rate','Hi_solar_rad','UV_energy','UV','Hi_rad','Heat','IndexV','Cool_dose','InDD','In','AirTemp','Wind_dew','Wind_heat','ISS_emc','Arc','Sample','Tx','Recept'])
met_data = pd.read_csv(path, skiprows=0, header=0,sep='\t')

print(met_data.shape)
# Combine the date and time columns so that they can be read in python.
met_data.DATETIME = pd.to_datetime(met_data['Date'] + ' ' + met_data['Time'],unit='D')

Index = met_data.set_index([met_data.DATETIME])
#met_data.DATETIME = met_data.astype('int')
met_data = met_data.astype(int)

figure = plt.figure()
ax1 = figure.add_subplot(111)
ax1.plot( met_data.Chill, met_data.Out)
plt.show()