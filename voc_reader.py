"""This file is used to read the VOC measurements China method"""
import os
import pandas as pd
import operator
import numpy as np
import matplotlib.pyplot as plt
import pylab
import csv
from pylab import *
from sklearn import linear_model
from scipy import stats
from matplotlib.offsetbox import AnchoredText

#index is used for indicating the start and the end of the data that needs to be read in
def extract_voc(path, index1, index2, Time_avg):
        # The path to where the raw files are stored
        cal_file = os.listdir(path)
        for i in cal_file:
                if list(i)[0] != 'C':
                        cal_file.remove(i)
        print(cal_file)

        def find_row_kw(infile,kw):
                reader = csv.reader(infile)
                for num, row in enumerate(reader):
                        if kw in row[0]:
                                return num

                

        for i in cal_file:
                if list(i)[0] == 'C':
                        with open(path + i, mode = 'r') as infile:
                                data = pd.read_csv(path+i, skiprows = find_row_kw(infile, index1) + 1, nrows = find_row_kw(infile, index2) - 2)
                        date = str(i)[18:26]
                        time = str(i)[27:33]
                        #print(date)
                        #print(time)
                        T1 = pd.to_datetime(1970, 1, 1, 0, 0, 0)
                        T2 = pd.to_datetime(date + time, format = '%Y%m%d%H%M%S')
                        offset = T2 - T1
                        #print(data)
                        data['Time (ms)']= pd.to_datetime(data['Time (ms)'], unit = 'ms')
                        data['Time (ms)'] += offset
                        mean_resampled = data.copy(deep = True)
                        mean_resampled['Time (ms)'] = pd.to_datetime(mean_resampled['Time (ms)'], unit='L')
                        # Set the index to be the time column, when you do this it drops the index, even though it is set to False.
                        mean_resampled = mean_resampled.set_index(mean_resampled['Time (ms)'], drop=False)
                        mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
                        # Re-add the time index so that it can be plotted later
                        Time = pd.Series(mean_resampled.index,name = 'Time', index = mean_resampled.index)
                        mean_resampled = pd.concat([mean_resampled, Time],axis = 1)
                        # If there are more than one files to be read in together the data_concat function will join them together.
                        print ('mean_resampled shape = ', mean_resampled.shape)
                        try:
                                data_concat = data_concat.append(mean_resampled)
                                print (' concatenating')
                        except NameError:
                                data_concat = mean_resampled.copy(deep=True)
                                print (' making data_concat')
        data_concat.to_csv('test2.csv')
        return data_concat


