import os
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

time = 86400*20

def sin_gen(Fs, f, sample, offset, noise):
        x = np.arange(0, time, 300)
        y = []
        for i in x:
                if noise == 1:
                        y.append(np.sin(2*np.pi*(f*i/Fs + offset))  + random.uniform(-0.3, 0.3))
                else:
                        y.append(np.sin(2*np.pi*(f*i/Fs + offset)))
        y = np.asarray(y)
        return y

def rh_mos(rh_value):
        mos_sen = []
        for i in rh_value:
                mos_sen.append(-0.786*np.log(i) + 4.2183 + random.uniform(-0.5, 0.5))
        mos_sen = np.asarray(mos_sen)
        return mos_sen

rh = 15*sin_gen(86400,3.3,time, 0.4*np.pi, 1) + 25
vocs = 150*sin_gen(86400,1.5,time,0, 0) + 200
mos_sen = rh_mos(rh)
mos = vocs * mos_sen
t = np.arange(0, time, 300)
dataset = pd.DataFrame({'Time' : []})
dataset['Time'] = t
dataset['rh'] = rh
dataset['mos'] = mos
dataset['vocs'] = vocs
dataset['mos_sen'] = mos_sen
dataset.to_csv('sig_gen.csv')
plt.plot(t, mos)
plt.plot(t, vocs)
plt.plot(t, rh)
plt.ylabel('voltage(mV)')
plt.xlabel('sample(n)')
plt.show()