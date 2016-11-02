# This will plot the data gathered from the RH cals.
# The cal_fit will plot the slopes from the RH cals against isoprene
# The Histograms will plot histograms for the individual points from the RH cal graphs
# mean_cals plots the same as cal_fit, however it groups pid voltages into bins determined by the isoprene concentration.


import scipy.odr as odr
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd


pids_on = [3,4,5]


def file2date(x):
    return x[-6:-3]
    
    
def Isop_chunk_indexer(l1ist,spacing):
    cal_point_data = {}
    n = 0
    for i in np.arange(0,max(l1ist),spacing):
        cal_point_data[n] = list([x for x in xrange(0,len(l1ist)) if l1ist[x]<=i+spacing and l1ist[x] > i])
        n = n+1
    return cal_point_data   
    
    
################  Control  Panel  ################

cal_fit = ''
Histograms = ''
mean_cals = ''
big_cal = 'Y'

binwidth = 2e-7


#Scipy Fits

lin_fit = 'Y'
quad_fit = ''
cube_fit = ''


tolerance = 1e-5

comp = 'mat_e_000'


background_colour = '#FFFAFA'

################ ################ ################

dataH = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH Cal Data Points.txt'% (comp),sep=',')
data = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep =',')

data3 = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep =',')
data3 = data3.drop(['Slope Error 4','Slope Error 5','Slope 5','Slope 4'],1)

data4 = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep =',')
data4 = data4.drop(['Slope Error 3','Slope Error 5','Slope 5','Slope 3'],1)


data5 = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep =',')
data5 = data5.drop(['Slope Error 4','Slope Error 3','Slope 3','Slope 4'],1)

    
    

 
    
data3 = data3[data3['Slope Error 3'] < tolerance]
data4 = data4[data4['Slope Error 4'] < tolerance]
data5 = data5[data5['Slope Error 5'] < tolerance]

mean_pid3 = np.nanmean(data3['Slope 3'])
mean_pid4 = np.nanmean(data4['Slope 4'])
mean_pid5 = np.nanmean(data5['Slope 5'])



'''
fit_file = open('C:\Users\%s\Google Drive\Bursary\Data_Analysis\\fit file.txt' % (comp),'w')


#Returns a linear Fit
def linear_fit(slope, intercept, Isoprene):
    return (slope*Isoprene)+intercept
    
#Returns a quadratic Fit
def quadratic_fit(Isoprene, root1, root2,xfac1,xfac2):
    return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)

#Returns a cubic Fit for pid4  
def cubic_fit4(Isoprene, root1, root2,root3,xfac1,xfac2,xfac3):
    return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)*((xfac3*Isoprene)+root3)

#Returns a cubic Fit    
def cubic_fit35(Isoprene, root1, root2,root3,xfac1,xfac2,xfac3):
    return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)*((xfac3*Isoprene)-root3)    
    


x = np.linspace(0.,2.5,10000)


############################
Isop3 = data3.Isop
Isop_Error3 = data3['Isop Error']

pid3 = data3['Pid3 Slope Value']
pid3_error = data3['Pid3 Slope Error']


if cal_fit == 'Y':
    if lin_fit == 'Y':
        slope_int3,pcov3 = curve_fit(linear_fit,Isop3,pid3, sigma = pid3_error)
        y3a= linear_fit(x,slope_int3[0],slope_int3[1])
    
    if quad_fit == 'Y':
        roots3,pcov3 = curve_fit(quadratic_fit,Isop3,pid3, sigma = pid3_error)
        y3b = quadratic_fit(x,roots3[0],roots3[1],roots3[2],roots3[3])
    
    if cube_fit == 'Y': 
        cube_params3,errors3 = curve_fit(cubic_fit4,Isop3,pid3, sigma = pid3_error)
        y3c = y3b = cubic_fit35(x,cube_params3[0],cube_params3[1],cube_params3[2],cube_params3[3],cube_params3[4],cube_params3[5])
        
    data.Filename = data.Filename.map(file2date)
    ############################
    
    Isop4 = data4.Isop
    Isop_Error4 = data4['Isop Error']
    
    pid4 = data4['Pid4 Slope Value']
    pid4_error = data4['Pid4 Slope Error']

    
    if lin_fit == 'Y':
        slope_int4,pcov4 = curve_fit(linear_fit,Isop4,pid4, sigma = pid4_error)
        y4a = linear_fit(x,slope_int4[0],slope_int4[1])
    
    if quad_fit == 'Y':
        roots4,pcov4 = curve_fit(quadratic_fit,Isop4,pid4, sigma = pid4_error)
        y4b = quadratic_fit(x,roots4[0],roots4[1],roots4[2],roots4[3])
    
    if cube_fit == 'Y':
        cube_params4,errors4 = curve_fit(cubic_fit35,Isop4,pid4, sigma = pid4_error)
        y4c = cubic_fit4(x,cube_params4[0],cube_params4[1],cube_params4[2],cube_params4[3],cube_params4[4],cube_params4[5])
    
    
    ############################
    Isop5 = data5.Isop
    Isop_Error5 = data5['Isop Error']
    
    pid5 = data5['Pid5 Slope Value']
    pid5_error = data5['Pid5 Slope Error']

    
    if lin_fit == 'Y':
        slope_int5,pcov5 = curve_fit(linear_fit,Isop5,pid5, sigma = pid5_error)
        y5a = linear_fit(x,slope_int5[0],slope_int5[1])
    
    if quad_fit == 'Y':
        roots5,pcov5 = curve_fit(quadratic_fit,Isop5,pid5, sigma = pid5_error)
        y5b = quadratic_fit(x,roots5[0],roots5[1],roots5[2],roots5[3])
    
    if cube_fit == 'Y':
        cube_params5,errors5 = curve_fit(cubic_fit35,Isop5,pid5, sigma = pid5_error)
        y5c = cubic_fit35(x,cube_params5[0],cube_params5[1],cube_params5[2],cube_params5[3],cube_params5[4],cube_params5[5])
    
    
    ############################
    
    x_label = 'Isop / ppb'
    y_label = 'Pid/RH ( V )'
    
    fig3 = plt.figure()
    pid3ax = fig3.add_subplot(111)
    pid3ax.errorbar(Isop3,pid3, xerr = Isop_Error3, yerr = pid3_error,fmt ='bo')
    pid3ax.set_xlabel(x_label)
    pid3ax.set_ylabel(y_label)
    pid3ax.set_ylim([-0.000015,0.000045])
    pid3ax.set_title('Pid3 RH vs Isop Cal')
    
    
    
    fig4 = plt.figure()
    pid4ax = fig4.add_subplot(111)
    pid4ax.errorbar(Isop4,pid4, xerr = Isop_Error4, yerr = pid4_error,fmt ='bo' )
    pid4ax.set_xlabel(x_label)
    pid4ax.set_ylabel(y_label)
    pid4ax.set_ylim([-0.000015,0.000045])
    pid4ax.set_title('Pid4 RH vs Isop Cal')
    
    
    
    fig5 = plt.figure()
    pid5ax = fig5.add_subplot(111)
    pid5ax.errorbar(Isop5,pid5, xerr = Isop_Error5, yerr = pid5_error,fmt ='bo')
    pid5ax.set_xlabel(x_label)
    pid5ax.set_ylabel(y_label)
    pid5ax.set_ylim([-0.000015,0.000045])
    pid5ax.set_title('Pid5 RH vs Isop Cal')
    
    
    
    
    
    if lin_fit == 'Y':
        pid4ax.plot(x,y4a,'g',label = 'Order 1, scipy fit')
        pid3ax.plot(x,y3a,'g',label = 'Order 1, scipy fit')
        pid5ax.plot(x,y5a,'g',label = 'Order 1, scipy fit')
        
        
    if quad_fit == 'Y':
        pid4ax.plot(x,y4b,'c',label = 'Order 2, scipy fit')
        pid5ax.plot(x,y5b,'c',label = 'Order 2, scipy fit')
        pid3ax.plot(x,y3b,'c',label = 'Order 2, scipy fit')
    
    
    if cube_fit == 'Y':
        pid3ax.plot(x,y3c,'r',label = 'Order 3, scipy fit')
        pid4ax.plot(x,y4c,'r',label = 'Order 3, scipy fit')
        pid5ax.plot(x,y5c,'r',label = 'Order 3, scipy fit')
    
    pid3ax.legend(loc = 'best')
    pid4ax.legend(loc = 'best')
    pid5ax.legend(loc = 'best')
















if Histograms == 'Y':
    
    cal_point_data = Isop_chunk_indexer(dataH.Isop,0.5)
 
    
    fig = plt.figure()
    plt.hist(dataH['Pid3 Voltage'],bins = np.arange(min(dataH['Pid3 Voltage']), max(dataH['Pid3 Voltage']) + binwidth, binwidth))
    plt.xlim([0,1e-5])
    plt.title('Pid3')
    
    fig1 = plt.figure()
    plt.hist(dataH['Pid4 Voltage'],bins = np.arange(min(dataH['Pid4 Voltage']), max(dataH['Pid4 Voltage']) + binwidth, binwidth))
    plt.xlim([0,1e-5])
    plt.title('Pid4')
    
    fig2 = plt.figure()
    plt.hist(dataH['Pid5 Voltage'],bins = np.arange(min(dataH['Pid5 Voltage']), max(dataH['Pid5 Voltage']) + binwidth, binwidth))
    plt.xlim([0,1e-5])
    plt.title('Pid5')
    
    
    for i in xrange(1,len(cal_point_data)):

        fig1 = plt.figure()
        plt.suptitle('Histograms of RH Cal Data')
        ax1 = fig1.add_subplot(311)
        ax1.hist(list(dataH.loc[cal_point_data[i],'Pid3 Voltage']), bins = np.arange(min(dataH.loc[cal_point_data[i],'Pid3 Voltage']), max(dataH.loc[cal_point_data[i],'Pid3 Voltage']) + binwidth/2, binwidth/2))
        ax1.set_title('Pid3')
        ax1.set_xlim([0,1e-5])
        ax1.set_ylim([0,10])
        
        ax2 = fig1.add_subplot(312)
        ax2.hist(list(dataH.loc[cal_point_data[i],'Pid4 Voltage']), bins= np.arange(min(dataH.loc[cal_point_data[i],'Pid4 Voltage']), max(dataH.loc[cal_point_data[i],'Pid4 Voltage']) + binwidth/2, binwidth/2))
        ax2.set_title('Pid4')
        ax2.set_xlim([0,1e-5])
        ax2.set_ylim([0,10])
        
        ax3 = fig1.add_subplot(313)
        ax3.hist(list(dataH.loc[cal_point_data[i],'Pid5 Voltage']), bins= np.arange(min(dataH.loc[cal_point_data[i],'Pid5 Voltage']), max(dataH.loc[cal_point_data[i],'Pid5 Voltage']) + binwidth/2, binwidth/2))
        ax3.set_title('Pid5')
        ax3.set_xlim([0,1e-5])
        ax3.set_ylim([0,10])
'''    
if mean_cals == 'Y':
        
    cal_point_data = Isop_chunk_indexer(dataH.Isop,0.1)
    
    isop_points = [np.nanmean(dataH.loc[cal_point_data[i],'Isop']) for i in xrange(1,len(cal_point_data))]    
    
    cal_points3 = [np.nanmean(dataH.loc[cal_point_data[i],'Pid3 Voltage']) for i in xrange(1,len(cal_point_data))]
    
    cal_points4 = [np.nanmean(dataH.loc[cal_point_data[i],'Pid4 Voltage']) for i in xrange(1,len(cal_point_data))]

    cal_points5 = [np.nanmean(dataH.loc[cal_point_data[i],'Pid5 Voltage']) for i in xrange(1,len(cal_point_data))]
    
    fig = plt.figure()
    fig.patch.set_facecolor(background_colour)
    fig.suptitle('RH Cal data points, grouped by isoprene',fontsize = 14)
    
    
    pid3 = fig.add_subplot(311)
    pid3.set_title('Pid 3',fontsize = 12)
    pid3.set_ylabel('Pid Voltage / V')
    pid3.set_xlabel('Isoprene / ppb')
    
    
    pid4 = fig.add_subplot(312)
    pid4.set_title('Pid 4',fontsize = 12)
    pid4.set_ylabel('Pid Voltage / V')
    pid4.set_xlabel('Isoprene / ppb')    
    
    pid5 = fig.add_subplot(313)
    pid5.set_title('Pid 5',fontsize = 12)
    pid5.set_ylabel('Pid Voltage / V')
    pid5.set_xlabel('Isoprene / ppb')    
    
    
    y_range = np.nanmax([(np.nanmax(cal_points3)-np.nanmin(cal_points3)),(np.nanmax(cal_points4)-np.nanmin(cal_points4)),(np.nanmax(cal_points5)-np.nanmin(cal_points5))])
    y_range = y_range*1.1

    pid3.plot(isop_points,cal_points3,'ro')
    pid3.plot([-0.5,3],[np.nanmean(cal_points3),np.nanmean(cal_points3)],'b-')
    pid3.set_ylim([np.nanmin(cal_points3)*0.99,np.nanmin(cal_points3) + y_range])  
    
    pid4.plot(isop_points,cal_points4,'go')
    pid4.plot([-0.5,3],[np.nanmean(cal_points4),np.nanmean(cal_points4)],'r-')
    pid4.set_ylim([np.nanmin(cal_points4)*0.99,np.nanmin(cal_points4) + y_range])
    
      
    pid5.plot(isop_points,cal_points5,'mo')
    pid5.plot([-0.5,3],[np.nanmean(cal_points5),np.nanmean(cal_points5)],'y-')
    pid5.set_ylim([np.nanmin(cal_points5)*0.99,np.nanmin(cal_points5) + y_range]) 
    
        
            
    plt.tight_layout()    
    plt.show()
    
    
if big_cal == 'Y': 
       
    def linear_fit_new(params, x):
        return ((params[0]*x)+params[1])  
          
    linear = odr.Model(linear_fit_new) 
    
        
    cal_point_indexes = Isop_chunk_indexer(dataH.Isop,0.5)
    
    slope_intercepts = {num:{x:()for x in xrange(0,len(cal_point_indexes))} for num in pids_on}
    
    Values = pd.DataFrame(index=pids_on,columns = ['Slope','Slope Error','Intercept','Intercept Error'])
    
    slopes = {num:{x:() for x in xrange(0,len(cal_point_indexes))} for num in pids_on}
    
    mean_slope_pid3 = np.nanmean([slopes[3][i] for i in slopes[3]])
    mean_slope_pid4 = np.nanmean([slopes[4][i] for i in slopes[4]])
    mean_slope_pid5 = np.nanmean([slopes[5][i] for i in slopes[5]])
    
    print mean_slope_pid3
    print mean_slope_pid4
    print mean_slope_pid5
    
    for x in xrange(0,len(cal_point_indexes)):
        for num in pids_on:
            datac = odr.RealData(x = dataH.loc[cal_point_indexes[x],'RH'],y =dataH.loc[cal_point_indexes[x],'Pid%s Voltage'%(str(num))],sx = dataH.loc[cal_point_indexes[x],'RH Error']*np.sqrt(360),sy = dataH.loc[cal_point_indexes[x],'Pid%s Voltage Error'%str(num)]*np.sqrt(360))
            fit = odr.ODR(datac,linear,[1e-5,0.05])
            params = fit.run()
        
            slope_intercepts[num][x] = params.beta
            
            slopes[num][x] = params.beta[0]

            
    


    
    
    
    figD = plt.figure()
    figD.suptitle('Pid Voltage vs RH, different colours indicate different isoprene concentrations', fontsize = 14)
    figD.patch.set_facecolor(background_colour)
    
    pid3 = figD.add_subplot(311)
    pid3.set_title('Pid 3',fontsize = 12)
    pid3.set_ylabel('Pid Voltage / V')
    pid3.set_xlabel('RH / %')
    
    
    pid4 = figD.add_subplot(312)
    pid4.set_title('Pid 4',fontsize = 12)
    pid4.set_ylabel('Pid Voltage / V')
    pid4.set_xlabel('RH / %')    
    
    pid5 = figD.add_subplot(313)
    pid5.set_title('Pid 5',fontsize = 12)
    pid5.set_ylabel('Pid Voltage / V')
    pid5.set_xlabel('RH / %')   
    
    
    for i in xrange(0,len(cal_point_indexes)):
        pid3.plot(dataH.loc[cal_point_indexes[i],'RH'],dataH.loc[cal_point_indexes[i],'Pid3 Voltage'],'o')
        
        
        pid4.plot(dataH.loc[cal_point_indexes[i],'RH'],dataH.loc[cal_point_indexes[i],'Pid4 Voltage'],'o')
        
        
        pid5.plot(dataH.loc[cal_point_indexes[i],'RH'],dataH.loc[cal_point_indexes[i],'Pid5 Voltage'],'o')
    
    
    plt.tight_layout()
    
    
    
    
    
    figL = plt.figure() 
    figL.suptitle('Pid Voltage vs RH, different colours indicate different isoprene concentrations', fontsize = 14)
    figL.patch.set_facecolor(background_colour)
    
    pid3 = figL.add_subplot(311)
    pid3.set_title('Pid 3',fontsize = 12)
    pid3.set_ylabel('Pid Voltage / V')
    pid3.set_xlabel('RH / %')    
    
    
    pid4 = figL.add_subplot(312)
    pid4.set_title('Pid 4',fontsize = 12)
    pid4.set_ylabel('Pid Voltage / V')
    pid4.set_xlabel('RH / %')    
    
      
    pid5 = figL.add_subplot(313)
    pid5.set_title('Pid 5',fontsize = 12)
    pid5.set_ylabel('Pid Voltage / V')
    pid5.set_xlabel('RH / %') 
    
      
    for i in xrange(0,len(cal_point_indexes)):
        Isop = np.nanmean(dataH.loc[cal_point_indexes[i],'Isop'])
        RH_fit = [min(dataH.loc[cal_point_indexes[i],'RH']),max(dataH.loc[cal_point_indexes[i],'RH'])]
        pid3_fit = [slope_intercepts[3][i][1],slope_intercepts[3][i][1]+(slope_intercepts[3][i][0]*max(dataH.loc[cal_point_indexes[i],'RH']))]
        pid3.plot(RH_fit,pid3_fit,label = 'Isop = %s'%Isop)
        pid3.legend(loc='best',fontsize = 9)


        RH_fit = [min(dataH.loc[cal_point_indexes[i],'RH']),max(dataH.loc[cal_point_indexes[i],'RH'])]
        pid4_fit = [slope_intercepts[4][i][1],slope_intercepts[4][i][1]+(slope_intercepts[4][i][0]*max(dataH.loc[cal_point_indexes[i],'RH']))]
        pid4.plot(RH_fit,pid4_fit,label = 'Isop = %s'%Isop)    
        pid4.legend(loc='best',fontsize = 9)    
    

        RH_fit = [min(dataH.loc[cal_point_indexes[i],'RH']),max(dataH.loc[cal_point_indexes[i],'RH'])]
        pid5_fit = [slope_intercepts[5][i][1],slope_intercepts[5][i][1]+(slope_intercepts[5][i][0]*max(dataH.loc[cal_point_indexes[i],'RH']))]
        pid5.plot(RH_fit,pid5_fit,label = 'Isop = %s'%Isop)    
        pid5.legend(loc='best',fontsize = 9)    
        plt.tight_layout()    
      
        plt.show()    

   
         
plt.figure()
Isop = np.nanmean(dataH.loc[cal_point_indexes[0],'Isop'])
RH_fit = [min(dataH.loc[cal_point_indexes[0],'RH']),max(dataH.loc[cal_point_indexes[0],'RH'])]
pid3_fit = [slope_intercepts[3][0][1],slope_intercepts[3][0][1]+(slope_intercepts[3][0][0]*max(dataH.loc[cal_point_indexes[0],'RH']))]
plt.plot(RH_fit,pid3_fit,label = 'Isop = %s'%Isop)
pid3.legend(loc='best',fontsize = 9)

plt.figure()
RH_fit = [min(dataH.loc[cal_point_indexes[0],'RH']),max(dataH.loc[cal_point_indexes[0],'RH'])]
pid4_fit = [slope_intercepts[4][0][1],slope_intercepts[4][0][1]+(slope_intercepts[4][0][0]*max(dataH.loc[cal_point_indexes[0],'RH']))]
plt.plot(RH_fit,pid4_fit,label = 'Isop = %s'%Isop)    
pid4.legend(loc='best',fontsize = 9)    

plt.figure()
RH_fit = [min(dataH.loc[cal_point_indexes[0],'RH']),max(dataH.loc[cal_point_indexes[0],'RH'])]
pid5_fit = [slope_intercepts[5][0][1],slope_intercepts[5][0][1]+(slope_intercepts[5][0][0]*max(dataH.loc[cal_point_indexes[0],'RH']))]
plt.plot(RH_fit,pid5_fit,label = 'Isop = %s'%Isop)    
pid5.legend(loc='best',fontsize = 9)    
    
    
    
   
    
    
    
    
    
plt.figure()    
plt.plot(dataH.loc[cal_point_indexes[0],'RH'],dataH.loc[cal_point_indexes[0],'Pid3 Voltage'],'o')

plt.figure()
plt.plot(dataH.loc[cal_point_indexes[0],'RH'],dataH.loc[cal_point_indexes[0],'Pid4 Voltage'],'o')

plt.figure()
plt.plot(dataH.loc[cal_point_indexes[0],'RH'],dataH.loc[cal_point_indexes[0],'Pid5 Voltage'],'o')  
    
    
    
plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
plt.show() 