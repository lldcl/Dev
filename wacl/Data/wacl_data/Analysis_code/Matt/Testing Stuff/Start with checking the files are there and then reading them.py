import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal
from scipy import stats
#import time
import os


cal = 'Y'
plots = 'Y'

fl = []
il2 = []
il3 = []
sl2 = []
sl3 = []
r2 = []
r3 = []


filesl=[]
pfl = []

bss = '\ko'
for i in range (8,25):
    if i<10:
        path = 'C:\Users\Matt\Bursary thing\PID Data\Organised and or Edited'+bss[0]+'07-0'+str(i)
    else:
        path = 'C:\Users\Matt\Bursary thing\PID Data\Organised and or Edited'+bss[0]+'07-'+str(i)
        
    for pt in range(0,25):
        if i<10:
            filename = '\d2015070'+str(i)+'_0'+str(pt)
        else:
            filename = '\d201507'+str(i)+'_0'+str(pt)
        
        pfl.append(path+filename)

p = []
for i in range (0,len(pfl)):   
    p.append(os.path.exists(pfl[i]))

n=0    
for i in range(0,len(pfl)):
    if p[i] == True:
        filesl.append(pfl[i])
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
