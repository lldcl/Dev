import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

def file2date(x):
    return x[-6:-3]
    
def Isop_chunk_indexer(l1ist,spacing):
    cal_point_data = {}
    n = 0
    for i in np.arange(0,max(l1ist),spacing):
        cal_point_data[n] = list([x for x in xrange(0,len(l1ist)) if l1ist[x]<=i+spacing and l1ist[x] > i])
        n = n+1
    return cal_point_data   


cal_fit = 'Y'
Histograms = ''
mean_cals = 'Y'

binwidth = 2e-7


#Scipy Fits

lin_fit = 'Y'
quad_fit = ''
cube_fit = ''


#polynomial_order = 1

tolerance = 1e-5

comp = 'mat_e_000'


dataH = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\RH Cal Data Points.txt',sep='\t')
data = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep ='\t')

data3 = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep ='\t')
data3.drop([u'Pid4 Slope Value', u'Pid4 Slope Error', u'Pid5 Slope Value',u'Pid5 Slope Error'],1)

data4 = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep ='\t')
data3.drop([u'Pid3 Slope Value', u'Pid3 Slope Error', u'Pid5 Slope Value',u'Pid5 Slope Error'],1)

data5 = pd.read_csv('C:\Users\%s\Google Drive\Bursary\Data_Analysis\RH cals.txt' % (comp),sep ='\t')
data3.drop([u'Pid3 Slope Value', u'Pid3 Slope Error', u'Pid4 Slope Value',u'Pid4 Slope Error'],1)

    
    

 
    
data3 = data3[data3['Pid3 Slope Error'] < tolerance]
data4 = data4[data4['Pid4 Slope Error'] < tolerance]
data5 = data5[data5['Pid5 Slope Error'] < tolerance]

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

#fit3 = np.polyfit(Isop3,pid3,polynomial_order)
#y3 = np.polyval(fit3,x)
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
    
    #fit4 = np.polyfit(Isop4,pid4,polynomial_order)
    #y4 = np.polyval(fit4,x)
    
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
    
    #fit5 = np.polyfit(Isop5,pid5,polynomial_order)
    #y5 = np.polyval(fit5,x)
    
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
    
            
    
    if lin_fit == 'Y':
        fit_file.write('\tSlope\tIntercept\n')
        fit_file.write('Pid3'+'\t'+str(slope_int3[1])+'\t'+str(slope_int3[0])+'\n')
        fit_file.write('Pid4'+'\t'+str(slope_int4[1])+'\t'+str(slope_int4[0])+'\n')
        fit_file.write('Pid5'+'\t'+str(slope_int5[1])+'\t'+str(slope_int5[0])+'\n')
        
    if quad_fit == 'Y':
        fit_file.write('\t2A\t2B\t2C\t2D\n')
        fit_file.write('Pid3'+'\t'+str(roots3[0])+'\t'+str(roots3[1])+'\t'+str(roots3[2])+'\t'+str(roots3[3])+'\n')
        fit_file.write('Pid4'+'\t'+str(roots4[0])+'\t'+str(roots4[1])+'\t'+str(roots4[2])+'\t'+str(roots4[3])+'\n')
        fit_file.write('Pid5'+'\t'+str(roots5[0])+'\t'+str(roots5[1])+'\t'+str(roots5[2])+'\t'+str(roots5[3])+'\n')
    
    if cube_fit == 'Y':
        fit_file.write('\t3A\t3B\t3C\t3D\t3E\t3F\n')
        fit_file.write('Pid3'+'\t'+str(cube_params3[0])+'\t'+str(cube_params3[1])+'\t'+str(cube_params3[2])+'\t'+str(cube_params3[3])+'\t'+str(cube_params3[4])+'\t'+str(cube_params3[5])+'\n')
        fit_file.write('Pid4'+'\t'+str(cube_params4[0])+'\t'+str(cube_params4[1])+'\t'+str(cube_params4[2])+'\t'+str(cube_params4[3])+'\t'+str(cube_params4[4])+'\t'+str(cube_params4[5])+'\n')
        fit_file.write('Pid5'+'\t'+str(cube_params5[0])+'\t'+str(cube_params5[1])+'\t'+str(cube_params5[2])+'\t'+str(cube_params5[3])+'\t'+str(cube_params5[4])+'\t'+str(cube_params5[5])+'\n')
    
    
    fit_file.close()
    
    x_label = 'Isop / ppb'
    y_label = 'Pid/RH ( V )'
    
    fig3 = plt.figure()
    pid3ax = fig3.add_subplot(111)
    pid3ax.errorbar(Isop3,pid3, xerr = Isop_Error3, yerr = pid3_error,fmt ='bo')
    #pid3ax.plot(x,y3,'k',label = 'Order %s numpy fit'%(str(polynomial_order)))
    pid3ax.set_xlabel(x_label)
    pid3ax.set_ylabel(y_label)
    pid3ax.set_ylim([-0.000015,0.000045])
    pid3ax.set_title('Pid3 RH vs Isop Cal')
    
    
    
    fig4 = plt.figure()
    pid4ax = fig4.add_subplot(111)
    pid4ax.errorbar(Isop4,pid4, xerr = Isop_Error4, yerr = pid4_error,fmt ='bo' )
    #pid4ax.plot(x,y4,'k',label = 'Order %s, numpy fit'%(str(polynomial_order)))
    pid4ax.set_xlabel(x_label)
    pid4ax.set_ylabel(y_label)
    pid4ax.set_ylim([-0.000015,0.000045])
    pid4ax.set_title('Pid4 RH vs Isop Cal')
    
    
    
    fig5 = plt.figure()
    pid5ax = fig5.add_subplot(111)
    pid5ax.errorbar(Isop5,pid5, xerr = Isop_Error5, yerr = pid5_error,fmt ='bo')
    #pid5ax.plot(x,y5,'k',label = 'Order %s, numpy fit'%(str(polynomial_order)))
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
    
if mean_cals == 'Y':
        
    cal_point_data = Isop_chunk_indexer(dataH.Isop,0.25)
    
    isop_points = [np.nanmean(dataH.loc[cal_point_data[i],'Isop']) for i in xrange(1,len(cal_point_data))]    
    
    cal_points3 = [np.nanmean(dataH.loc[cal_point_data[i],'Pid3 Voltage']) for i in xrange(1,len(cal_point_data))]
    
    cal_points4 = [np.nanmean(dataH.loc[cal_point_data[i],'Pid4 Voltage']) for i in xrange(1,len(cal_point_data))]

    cal_points5 = [np.nanmean(dataH.loc[cal_point_data[i],'Pid5 Voltage']) for i in xrange(1,len(cal_point_data))]
    
    fig = plt.figure()
    plt.plot(isop_points,cal_points3,'o')
    fig = plt.figure()
    plt.plot(isop_points,cal_points4,'o')
    fig = plt.figure()
    plt.plot(isop_points,cal_points5,'o')
    
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
plt.show()    