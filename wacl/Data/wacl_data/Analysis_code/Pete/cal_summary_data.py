"""Reads multiple cal files and averages data to give points for gpe
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *


########################################
#plotly graph code

py.sign_in("PeteEdwards","lz7j3ml8th")

def plot(data,  title = 'Plot',  filename = 'dash1' ) : 
    ########################################################################
    #3d graph
    #######################################################################   
    stats=data
    tracelist=[]  
    trace2=Scatter3d(
                    x=stats['V1'],
                    y=stats['V2'],
                    z=stats['V3'],
                   mode='markers',
                   name='Bins:         ',
                   marker=Marker(symbol='dot',
                                 size=10,
                                 color=[],
                                 showscale=True,
                                 colorscale= 'Portland',    #'Viridis',
                                 line=Line(color='rgb(50,50,50)', width=1.5)
                                 ),                
                    line=Line(color='rgb(125,125,125)', width=1
), 
                   hoverinfo='text'
                   ) 
    trace2['marker']['color']=stats.concentration  ##########SIZE VAR###########   
    axis=dict(showbackground=False,
              showline=True,  
              zeroline=False,
              showgrid=True,
              showticklabels=True,
              #title='Graph'
              ) 
    layout = Layout(
             title = title,
             width=1200,
             height=1100,
             showlegend=False,
             scene =Scene(  
                           xaxis=XAxis(axis, title = 'Temp'),
                           yaxis=YAxis(axis, title = 'RH'),
                           zaxis=ZAxis(axis, title = '[VOC]'),
                          ),
             margin=Margin( t=0  ),
            hovermode='closest',
            annotations=Annotations([
                   Annotation(
                    showarrow=False,
                    text="",
                    xref='paper',    
                    yref='paper',    
                    x=0,  
                    y=0.1,
                    xanchor='left',  
                    yanchor='bottom',                    
                    font=Font( size=11 )    
                    )                  
                ]),    )
               
    tracelist.append(trace2)
    data=Data(tracelist)
    fig=Figure(data=data, layout=layout) 
    return py.plot(fig, filename = filename , auto_open=True, sharing='public')

########################################
#main function

path = '/Users/Pete/Google Drive/Pete/AlFHoNSo/Data_Analysis/Raw_Data_Files/'
voc_cyl = 1040.	#total ppbv of VOC standard being used

cal_files = [
# 'd20160201_02',
# 'd20160201_06',
# 'd20160202_03',
# 'd20160202_04',
# 'd20160203_01',
# 'd20160203_02a',
# 'd20160203_02b',
# 'd20160204_01',
# 'd20160204_02',
# 'd20160205_02',
# 'd20160205_03',
# 'd20160205_04',
# 'd20160208_01',
'd20160211_03','d20160211_04','d20160212_02','d20160212_06','d20160215_02','d20160216_05']
for i in cal_files:
   folder = list(i)[1:7]
   filename = "".join(folder)+'/'+i
   print filename

   #read file into dataframe
   data = pd.read_csv(path+filename)

   #T_int = float of seconds since daqfac T0, to use as a long term drift metric
   T_int = data.TheTime
   T_int.name='T_int'
   data = pd.concat([data,T_int],axis=1)

   #convert daqfac time into real time pd.datetime object
   data.TheTime = pd.to_datetime(data.TheTime,unit='D')
   T1 = pd.datetime(1899,12,30,0)	#daqfac T0
   T2 = pd.datetime(1970,01,01,0)	#pandas datetime T0
   offset=T1-T2
   data.TheTime+=offset
   
   conc_change_date = pd.to_datetime(pd.datetime(2016,02,11,0))
   if (data.TheTime[0] < conc_change_date):
      voc_cyl = 40000.

   #find all sensors in file
   sub = 'MOS'
   sensors = [s for s in data.columns if sub in s]

   #convert mfc voltages into sccm and calculate [VOC]
   mfchi_range = 2000.	#sccm
   mfchi_sccm = data.mfchiR*(mfchi_range/5.)
   mfcmid_range = 100.	#sccm
   mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)
   mfclo_range = 20.	#sccm
   mfclo_sccm = data.mfcloR*(mfclo_range/5.)
   dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
   voc_mr = pd.Series(dil_fac*voc_cyl,name='voc_mr')
   data = pd.concat([data,voc_mr],axis=1)

   #convert T and RH from V into %
   data.Temp = data.Temp*100.
   data.RH1 = (((data.RH1/data.VS)-0.16)/0.0062)/(1.0546-0.00216*data.Temp)
   
   #select data to be used
   vars = ['TheTime','T_int','Temp','RH1','VS','voc_mr']+sensors
   data = data[vars]

   #remove Nan's and reindex
   data = data.dropna()
   
   Time_avg = '10S'

   data.TheTime = pd.to_datetime(data.TheTime,unit='L')
   data = data.set_index(data.TheTime,drop=False)
   data = data.resample(Time_avg, how='mean',fill_method='pad')
   
   ###############################################
   # dxdt filters
   nm_pts = 240./float(Time_avg[:-1])	#seconds to filter out after dxdt flagged

   #filter out periods when RH changes rapidly (dRHdt<0.2)
   dRHdt = pd.Series(np.absolute(data.RH1.diff()),name='dRHdt')
   dRHdt_filt = pd.Series(0, index=dRHdt.index,name='dRHdt_filt')

   dRH_ctr=0
   for dp in dRHdt:
      if (dp>0.2):
         dRHdt_filt[dRH_ctr:int(dRH_ctr+nm_pts)] = 1
      dRH_ctr+=1
   
   data = pd.concat([data,dRHdt],axis=1,join_axes=[data.index])
   data = data[dRHdt_filt == 0]

   #filter out periods when [VOC] changes rapidly (dvocdt<1)
   dvocdt = pd.Series(np.absolute(data.voc_mr.diff()),name='dvocdt')
   dvocdt_filt = pd.Series(0, index=dvocdt.index,name='dvocdt_filt')
   dvoc_ctr=0
   for dp in dvocdt:
      if (dp>1.):
         dvocdt_filt[dvoc_ctr:int(dvoc_ctr+nm_pts)] = 1
      dvoc_ctr+=1

   data = pd.concat([data,dvocdt],axis=1,join_axes=[data.index])
   data = data[dvocdt_filt == 0]
   
   try:
      data_concat = data_concat.append(data)
      print ' concatenating'
   except NameError:
      data_concat = data.copy(deep=True)
      print ' making data_concat'

#bin data by RH, T and [VOC]
RHbins = np.linspace(0,100,200)
Tbins  = np.linspace(15,30,200)
VOCbins = np.linspace(0,200,2000)

cRH = pd.cut(np.array(data_concat.RH1), RHbins, include_lowest=True)
cT = pd.cut(np.array(data_concat.Temp), Tbins, include_lowest=True)
cVOC = pd.cut(np.array(data_concat.voc_mr), VOCbins, include_lowest=True)

MOS1g = data_concat.MOS1.groupby([cRH.labels, cT.labels, cVOC.labels])
MOS2g = data_concat.MOS2.groupby([cRH.labels, cT.labels, cVOC.labels])

x=[]
y=[]
z=[]
v=[]

for bin,sig in MOS1g:
  x.append(Tbins[bin[1]])
  y.append(RHbins[bin[0]])
  z.append(VOCbins[bin[2]])
  v.append(sig.mean())

plot_data = pd.DataFrame([x,y,z,v]).T
plot_data.columns=['V1','V2','V3','concentration']
plot(plot_data,title = 'MOS1',filename='MOS1_test')

x=[]
y=[]
z=[]
v=[]

for bin,sig in MOS2g:
  x.append(Tbins[bin[1]])
  y.append(RHbins[bin[0]])
  z.append(VOCbins[bin[2]])
  v.append(sig.mean())

plot_data = pd.DataFrame([x,y,z,v]).T
plot_data.columns=['V1','V2','V3','concentration']
plot(plot_data,title = 'MOS2',filename='MOS2_test')
