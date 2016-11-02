# This Code plots graphs using the cal data that is in the big cal data text file.
#In the Control Panel you can change which graphs get plotted.
# big_cal will plot a cal graph of all the cal points, averaged. It displays a graph that looks the same as the single file cal graphs.
# time_vs_all_points plots time vs all the cal points in the cal data text files, it shows if there is any long term drift in the data.
# isop_vs_all_points is the colourful graph, it has isoprene on the x axis, and the pid voltage on the y axis. It also fits a line to find the slope. The size and redness of the circles shows the RH.
# isop_vs_all_points_time this plots the same data as isop_vs_all_points_RH however the points are coloured by the time, it looks like there might be some long term drift but the LTD plotter doesn't really show any.
# LTD_plots plots the cal data points vs time, this shows if the cals vary with time


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from matplotlib.dates import date2num
import matplotlib.patches as mpatches




########## Control Panel ###########


big_cal = ''
time_vs_all_points = ''
isop_vs_all_points_RH = ''
isop_vs_all_points_time = ''
LTD_plots = 'Y'


########## ########### ###########




def linear_fit(slope, intercept, x):
        return (slope*x)+intercept
def timeconverter2date(T):
   	return (pd.to_datetime(T))
   	
def timeconverter2num(T):
   	return (date2num(T))

data = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Cal Data.txt',sep = '\t')


data.loc[:,'The Time'] = data['The Time'].map(timeconverter2date)

datac = pd.read_csv('C:\Users\mat_e_000\Google Drive\Bursary\Data_Analysis\Cal Data Corrected.txt',sep = '\t')

datac.loc[:,'The Time'] = datac['The Time'].map(timeconverter2date)


xlim1 = np.min(data['The Time'])
xlim2 = np.max(data['The Time'])

yrange3 = [(np.max(data['Pid 3'])) - 110*(np.min(data['Pid 3'])/112),(np.max(datac['Pid 3'])) - 110*(np.min(datac['Pid 3'])/112)]  

yrange4 = [(np.max(data['Pid 4'])) - 110*(np.min(data['Pid 4'])/112),(np.max(datac['Pid 4'])) - 110*(np.min(datac['Pid 4'])/112)]

yrange5 = [(np.max(data['Pid 5'])) - 110*(np.min(data['Pid 5'])/112),(np.max(datac['Pid 5'])) - 110*(np.min(datac['Pid 5'])/112)]

yrange = np.max([np.max(yrange3),np.max(yrange4),np.max(yrange5)])

y3lim1 = 111*np.min(data['Pid 3'])/112
y3lim2 = y3lim1 + yrange

y4lim1 = 111*np.min(data['Pid 4'])/112
y4lim2 = y4lim1 + yrange

y5lim1 = 111*np.min(data['Pid 5'])/112
y5lim2 = y5lim1 + yrange

y3clim1 = 111*np.min(datac['Pid 3'])/112
y3clim2 = y3lim1 + yrange

y4clim1 = 111*np.min(datac['Pid 4'])/112
y4clim2 = y4lim1 + yrange

y5clim1 = 111*np.min(datac['Pid 5'])/112
y5clim2 = y5lim1 + yrange

Isop_indexes_dict = {}

Isop_indexes_dict[0.] = [i for i in xrange(0,len(data.Isop)) if np.around(data.Isop[i],1) == 0.0]

Isop_indexes_dict[0.5] = [i for i in xrange(0,len(data.Isop)) if np.around(data.Isop[i],1) == 0.5]

Isop_indexes_dict[1.0] = [i for i in xrange(0,len(data.Isop)) if np.around(data.Isop[i],1) == 1.0]

Isop_indexes_dict[1.5] = [i for i in xrange(0,len(data.Isop)) if np.around(data.Isop[i],1) == 1.4]

Isop_indexes_dict[2.0] = [i for i in xrange(0,len(data.Isop)) if np.around(data.Isop[i],1) == 1.8]

Isop_indexes_dict[2.5] = [i for i in xrange(0,len(data.Isop)) if np.around(data.Isop[i],1) == 2.2]

if LTD_plots == 'Y':
    
    figLTD3 = plt.figure()
    figLTD3.suptitle('Uncorrected Pid 3 Voltage vs Time, showing Long Term Drift')
    axLTD3 = figLTD3.add_subplot(111)
    axLTD3.plot(data.loc[Isop_indexes_dict[0],'The Time'],data.loc[Isop_indexes_dict[0],'Pid 3'],'co',label = 'Isop = 0')
    axLTD3.plot(data.loc[Isop_indexes_dict[0.5],'The Time'],data.loc[Isop_indexes_dict[0.5],'Pid 3'],'bo',label = 'Isop = 0.5')
    axLTD3.plot(data.loc[Isop_indexes_dict[1],'The Time'],data.loc[Isop_indexes_dict[1],'Pid 3'],'go',label = 'Isop = 1.0')
    axLTD3.plot(data.loc[Isop_indexes_dict[1.5],'The Time'],data.loc[Isop_indexes_dict[1.5],'Pid 3'],'ko',label = 'Isop = 1.5')
    axLTD3.plot(data.loc[Isop_indexes_dict[2.0],'The Time'],data.loc[Isop_indexes_dict[2.0],'Pid 3'],'mo',label = 'Isop = 2.0')
    axLTD3.plot(data.loc[Isop_indexes_dict[2.5],'The Time'],data.loc[Isop_indexes_dict[2.5],'Pid 3'],'ro',label = 'Isop = 2.5')
    axLTD3.set_ylim([y3lim1,y3lim2])
    axLTD3.set_xlim([xlim1,xlim2])
    plt.legend(loc = 'best')

    figLTD3c = plt.figure()
    figLTD3c.suptitle('Corrected Pid 3 Voltage vs Time, showing Long Term Drift')
    axLTD3c = figLTD3c.add_subplot(111)
    axLTD3c.plot(datac.loc[Isop_indexes_dict[0],'The Time'],datac.loc[Isop_indexes_dict[0],'Pid 3'],'co',label = 'Isop = 0')
    axLTD3c.plot(datac.loc[Isop_indexes_dict[0.5],'The Time'],datac.loc[Isop_indexes_dict[0.5],'Pid 3'],'bo',label = 'Isop = 0.5')
    axLTD3c.plot(datac.loc[Isop_indexes_dict[1],'The Time'],datac.loc[Isop_indexes_dict[1],'Pid 3'],'go',label = 'Isop = 1.0')
    axLTD3c.plot(datac.loc[Isop_indexes_dict[1.5],'The Time'],datac.loc[Isop_indexes_dict[1.5],'Pid 3'],'ko',label = 'Isop = 1.5')
    axLTD3c.plot(datac.loc[Isop_indexes_dict[2.0],'The Time'],datac.loc[Isop_indexes_dict[2.0],'Pid 3'],'mo',label = 'Isop = 2.0')
    axLTD3c.plot(datac.loc[Isop_indexes_dict[2.5],'The Time'],datac.loc[Isop_indexes_dict[2.5],'Pid 3'],'ro',label = 'Isop = 2.5')
    axLTD3c.set_ylim([y3clim1,y3clim2])
    axLTD3c.set_xlim([xlim1,xlim2])
    plt.legend(loc = 'best')
    
    
    
    
    
    figLTD4 = plt.figure()
    figLTD4.suptitle('Uncorrected Pid 4 Voltage vs Time, showing Long Term Drift')
    axLTD4 = figLTD4.add_subplot(111)
    axLTD4.plot(data.loc[Isop_indexes_dict[0],'The Time'],data.loc[Isop_indexes_dict[0],'Pid 4'],'co',label = 'Isop = 0')
    axLTD4.plot(data.loc[Isop_indexes_dict[0.5],'The Time'],data.loc[Isop_indexes_dict[0.5],'Pid 4'],'bo',label = 'Isop = 0.5')
    axLTD4.plot(data.loc[Isop_indexes_dict[1],'The Time'],data.loc[Isop_indexes_dict[1],'Pid 4'],'go',label = 'Isop = 1.0')
    axLTD4.plot(data.loc[Isop_indexes_dict[1.5],'The Time'],data.loc[Isop_indexes_dict[1.5],'Pid 4'],'ko',label = 'Isop = 1.5')
    axLTD4.plot(data.loc[Isop_indexes_dict[2.0],'The Time'],data.loc[Isop_indexes_dict[2.0],'Pid 4'],'mo',label = 'Isop = 2.0')
    axLTD4.plot(data.loc[Isop_indexes_dict[2.5],'The Time'],data.loc[Isop_indexes_dict[2.5],'Pid 4'],'ro',label = 'Isop = 2.5')
    axLTD4.set_ylim([y4lim1,y4lim2])
    axLTD4.set_xlim([xlim1,xlim2])
    plt.legend(loc = 'best')

    figLTD4c = plt.figure()
    figLTD4c.suptitle('Corrected Pid 4 Voltage vs Time, showing Long Term Drift')
    axLTD4c = figLTD4c.add_subplot(111)
    axLTD4c.plot(datac.loc[Isop_indexes_dict[0],'The Time'],datac.loc[Isop_indexes_dict[0],'Pid 4'],'co',label = 'Isop = 0')
    axLTD4c.plot(datac.loc[Isop_indexes_dict[0.5],'The Time'],datac.loc[Isop_indexes_dict[0.5],'Pid 4'],'bo',label = 'Isop = 0.5')
    axLTD4c.plot(datac.loc[Isop_indexes_dict[1],'The Time'],datac.loc[Isop_indexes_dict[1],'Pid 4'],'go',label = 'Isop = 1.0')
    axLTD4c.plot(datac.loc[Isop_indexes_dict[1.5],'The Time'],datac.loc[Isop_indexes_dict[1.5],'Pid 4'],'ko',label = 'Isop = 1.5')
    axLTD4c.plot(datac.loc[Isop_indexes_dict[2.0],'The Time'],datac.loc[Isop_indexes_dict[2.0],'Pid 4'],'mo',label = 'Isop = 2.0')
    axLTD4c.plot(datac.loc[Isop_indexes_dict[2.5],'The Time'],datac.loc[Isop_indexes_dict[2.5],'Pid 4'],'ro',label = 'Isop = 2.5')
    axLTD4c.set_ylim([y4clim1,y4clim2])
    axLTD4c.set_xlim([xlim1,xlim2])
    plt.legend(loc = 'best')
    
    
    
    
    
    figLTD5 = plt.figure()
    figLTD5.suptitle('Uncorrected Pid 5 Voltage vs Time, showing Long Term Drift')
    axLTD5 = figLTD5.add_subplot(111)
    axLTD5.plot(data.loc[Isop_indexes_dict[0],'The Time'],data.loc[Isop_indexes_dict[0],'Pid 5'],'co',label = 'Isop = 0')
    axLTD5.plot(data.loc[Isop_indexes_dict[0.5],'The Time'],data.loc[Isop_indexes_dict[0.5],'Pid 5'],'bo',label = 'Isop = 0.5')
    axLTD5.plot(data.loc[Isop_indexes_dict[1],'The Time'],data.loc[Isop_indexes_dict[1],'Pid 5'],'go',label = 'Isop = 1.0')
    axLTD5.plot(data.loc[Isop_indexes_dict[1.5],'The Time'],data.loc[Isop_indexes_dict[1.5],'Pid 5'],'ko',label = 'Isop = 1.5')
    axLTD5.plot(data.loc[Isop_indexes_dict[2.0],'The Time'],data.loc[Isop_indexes_dict[2.0],'Pid 5'],'mo',label = 'Isop = 2.0')
    axLTD5.plot(data.loc[Isop_indexes_dict[2.5],'The Time'],data.loc[Isop_indexes_dict[2.5],'Pid 5'],'ro',label = 'Isop = 2.5')
    axLTD5.set_ylim([y5lim1,y5lim2])
    axLTD5.set_xlim([xlim1,xlim2])
    plt.legend(loc = 'best')

    figLTD5c = plt.figure()
    figLTD5c.suptitle('Corrected Pid 5 Voltage vs Time, showing Long Term Drift')
    axLTD5c = figLTD5c.add_subplot(111)
    axLTD5c.plot(datac.loc[Isop_indexes_dict[0],'The Time'],datac.loc[Isop_indexes_dict[0],'Pid 5'],'co',label = 'Isop = 0')
    axLTD5c.plot(datac.loc[Isop_indexes_dict[0.5],'The Time'],datac.loc[Isop_indexes_dict[0.5],'Pid 5'],'bo',label = 'Isop = 0.5')
    axLTD5c.plot(datac.loc[Isop_indexes_dict[1],'The Time'],datac.loc[Isop_indexes_dict[1],'Pid 5'],'go',label = 'Isop = 1.0')
    axLTD5c.plot(datac.loc[Isop_indexes_dict[1.5],'The Time'],datac.loc[Isop_indexes_dict[1.5],'Pid 5'],'ko',label = 'Isop = 1.5')
    axLTD5c.plot(datac.loc[Isop_indexes_dict[2.0],'The Time'],datac.loc[Isop_indexes_dict[2.0],'Pid 5'],'mo',label = 'Isop = 2.0')
    axLTD5c.plot(datac.loc[Isop_indexes_dict[2.5],'The Time'],datac.loc[Isop_indexes_dict[2.5],'Pid 5'],'ro',label = 'Isop = 2.5')
    axLTD5c.set_ylim([y5clim1,y5clim2])
    axLTD5c.set_xlim([xlim1,xlim2])
    plt.legend(loc = 'best')
##################################################################################################
if time_vs_all_points == 'Y':   
    zero_mean3 = np.nanmean(data.loc[:,'Pid 3'])
    zero_mean4 = np.nanmean(data.loc[:,'Pid 4'])
    zero_mean5 = np.nanmean(data.loc[:,'Pid 5'])
        
    
    
    fig1 = plt.figure()
    plt.title('Cal Points')
    ax1a = fig1.add_subplot(311)
    ax1b = fig1.add_subplot(312)
    ax1c = fig1.add_subplot(313)
    
    
    ax1a.errorbar(data['The Time'],data['Pid 3'], yerr = data['Pid Error 3'], fmt='bo')
    ax1a.axhline(zero_mean3)
    ax1a.set_ylim([y3lim1,y3lim2])
    ax1a.set_xlim([xlim1,xlim2])
    
    
    ax1b.errorbar(data['The Time'],data['Pid 4'], yerr = data['Pid Error 4'], fmt='ko')
    ax1b.axhline(zero_mean4)
    ax1b.set_ylim([y4lim1,y4lim2])
    ax1b.set_xlim([xlim1,xlim2])
    
    
    
    ax1c.errorbar(data['The Time'],data['Pid 5'], yerr = data['Pid Error 5'], fmt='mo')
    ax1c.axhline(zero_mean5)
    ax1c.set_ylim([y5lim1,y5lim2])
    ax1c.set_xlim([xlim1,xlim2])
    
    
    

        
    zero_mean3 = np.nanmean(datac.loc[:,'Pid 3'])
    
    zero_mean4 = np.nanmean(datac.loc[:,'Pid 4'])
    zero_mean5 = np.nanmean(datac.loc[:,'Pid 5'])
    
    
    
    fig1 = plt.figure()
    plt.title('Cal Points Corrected')
    ax2a = fig1.add_subplot(311)
    ax2b = fig1.add_subplot(312)
    ax2c = fig1.add_subplot(313)
    
    ax2a.errorbar(data['The Time'],datac['Pid 3'], yerr = datac['Pid Error 3'], fmt='bo')
    ax2a.axhline(zero_mean3)
    ax2a.set_ylim([y3clim1,y3clim2])
    ax2a.set_xlim([xlim1,xlim2])
    
    
    ax2b.errorbar(data['The Time'],datac['Pid 4'], yerr = datac['Pid Error 4'], fmt='ko')
    ax2b.axhline(zero_mean4)
    ax2b.set_ylim([y4clim1,y4clim2])
    ax2b.set_xlim([xlim1,xlim2])
    
    ax2c.errorbar(data['The Time'],datac['Pid 5'], yerr = datac['Pid Error 5'], fmt='mo')
    ax2c.axhline(zero_mean5)
    ax2c.set_ylim([y5clim1,y5clim2])
    ax2c.set_xlim([xlim1,xlim2])


##################################################################################################

if isop_vs_all_points_RH == 'Y':
    
    isop_fit = [0.,np.max(data.Isop)]
    
    figiva3 = plt.figure()
    figiva3.suptitle('Uncorrected Isop vs All cal points for Septemeber, Pid 3')
    ax1iva3 = figiva3.add_subplot(111)    
    area = 10*(data.RH)
    ax1iva3.scatter(data['Isop'], data['Pid 3'], s=area, c = data.RH, alpha=0.5)
    ax1iva3.set_ylim([y3lim1,y3lim2])
    
    cal_points3 = [np.nanmean(data.loc[Isop_indexes_dict[i],'Pid 3']) for i in np.arange(0,3.0,0.5)]
    cal_points_error3 = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Pid 3']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept3,pcov3 = opt.curve_fit(linear_fit, data['Isop'], data['Pid 3'], sigma = data['Pid Error 3'])
    pid_fit3 = [slope_intercept3[0],(np.max(data.Isop)*slope_intercept3[1])+slope_intercept3[0]]  
    perr3 = np.sqrt(np.diag(pcov3))    
    Intercept_error3 = perr3[0]/np.sqrt(len(cal_points3))
    Slope_Error3 = perr3[1]/np.sqrt(len(cal_points3))
    
    slope_patch_pid3 = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept3[1])+'+/-'+str('%.1g' % Slope_Error3),color = 'b')
    intecept_patch_pid3 = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept3[0])+'+/-'+str('%.1g' % Intercept_error3),color = 'b')
    ax1iva3.legend(handles=[slope_patch_pid3,intecept_patch_pid3],loc='best')
    ax1iva3.plot(isop_fit,pid_fit3)
        
    ax1iva3.plot(isop_fit,pid_fit3)
    
    
    
    
    figiva3c = plt.figure()
    figiva3c.suptitle('Corrected Isop vs All cal points for Septemeber, Pid 3')
    ax1iva3c = figiva3c.add_subplot(111)    
    areac = 10*(datac.RH)
    ax1iva3c.scatter(datac['Isop'], datac['Pid 3'], s=areac, c = datac.RH, alpha=0.5)
    ax1iva3c.set_ylim([y3clim1,y3clim2])

            
    cal_points3c = [np.nanmean(datac.loc[Isop_indexes_dict[i],'Pid 3']) for i in np.arange(0,3.0,0.5)]
    cal_points_error3c = [(np.nanstd(datac.loc[Isop_indexes_dict[i],'Pid 3']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept3c,pcov3c = opt.curve_fit(linear_fit, datac['Isop'], datac['Pid 3'], sigma = datac['Pid Error 3'])
    pid_fit3c = [slope_intercept3c[0],(np.max(data.Isop)*slope_intercept3c[1])+slope_intercept3c[0]]  
    perr3c = np.sqrt(np.diag(pcov3c))    
    Intercept_error3c = perr3c[0]/np.sqrt(len(cal_points3c))
    Slope_Error3c = perr3c[1]/np.sqrt(len(cal_points3c))
    
    slope_patch_pid3c = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept3c[1])+'+/-'+str('%.1g' % Slope_Error3c),color = 'b')
    intecept_patch_pid3c = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept3c[0])+'+/-'+str('%.1g' % Intercept_error3c),color = 'b')
    ax1iva3c.legend(handles=[slope_patch_pid3c,intecept_patch_pid3c],loc='best')
    
    ax1iva3c.plot(isop_fit,pid_fit3c)
    
    
    
    
    
    
    
    
    
    figiva4 = plt.figure()
    figiva4.suptitle('Uncorrected Isop vs All cal points for Septemeber, Pid 4')
    ax1iva4 = figiva4.add_subplot(111)    
    area = 10*(data.RH)
    ax1iva4.scatter(data['Isop'], data['Pid 4'], s=area, c = data.RH, alpha=0.5)
    ax1iva4.set_ylim([y4lim1,y4lim2])
    
    cal_points4 = [np.nanmean(data.loc[Isop_indexes_dict[i],'Pid 4']) for i in np.arange(0,3.0,0.5)]
    cal_points_error4 = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Pid 4']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept4,pcov4 = opt.curve_fit(linear_fit, data['Isop'], data['Pid 4'], sigma = data['Pid Error 4'])
    pid_fit4 = [slope_intercept4[0],(np.max(data.Isop)*slope_intercept4[1])+slope_intercept4[0]]  
    perr4 = np.sqrt(np.diag(pcov4))    
    Intercept_error4 = perr4[0]/np.sqrt(len(cal_points4))
    Slope_Error4 = perr4[1]/np.sqrt(len(cal_points4))
    
    slope_patch_pid4 = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept4[1])+'+/-'+str('%.1g' % Slope_Error4),color = 'b')
    intecept_patch_pid4 = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept4[0])+'+/-'+str('%.1g' % Intercept_error4),color = 'b')
    ax1iva4.legend(handles=[slope_patch_pid4,intecept_patch_pid4],loc='best')
    ax1iva4.plot(isop_fit,pid_fit4)
        
    ax1iva4.plot(isop_fit,pid_fit4)
    
    
    
    
    figiva4c = plt.figure()
    figiva4c.suptitle('Corrected Isop vs All cal points for Septemeber, Pid 4')
    ax1iva4c = figiva4c.add_subplot(111)    
    areac = 10*(datac.RH)
    ax1iva4c.scatter(datac['Isop'], datac['Pid 4'], s=areac, c = datac.RH, alpha=0.5)
    ax1iva4c.set_ylim([y4clim1,y4clim2])

            
    cal_points4c = [np.nanmean(datac.loc[Isop_indexes_dict[i],'Pid 4']) for i in np.arange(0,3.0,0.5)]
    cal_points_error4c = [(np.nanstd(datac.loc[Isop_indexes_dict[i],'Pid 4']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept4c,pcov4c = opt.curve_fit(linear_fit, datac['Isop'], datac['Pid 4'], sigma = datac['Pid Error 4'])
    pid_fit4c = [slope_intercept4c[0],(np.max(data.Isop)*slope_intercept4c[1])+slope_intercept4c[0]]  
    perr4c = np.sqrt(np.diag(pcov4c))    
    Intercept_error4c = perr4c[0]/np.sqrt(len(cal_points4c))
    Slope_Error4c = perr4c[1]/np.sqrt(len(cal_points4c))
    
    slope_patch_pid4c = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept4c[1])+'+/-'+str('%.1g' % Slope_Error4c),color = 'b')
    intecept_patch_pid4c = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept4c[0])+'+/-'+str('%.1g' % Intercept_error4c),color = 'b')
    ax1iva4c.legend(handles=[slope_patch_pid4c,intecept_patch_pid4c],loc='best')
    
    ax1iva4c.plot(isop_fit,pid_fit4c)







    figiva5 = plt.figure()
    figiva5.suptitle('Uncorrected Isop vs All cal points for Septemeber, Pid 5')
    ax1iva5 = figiva5.add_subplot(111)    
    area = 10*(data.RH)
    ax1iva5.scatter(data['Isop'], data['Pid 5'], s=area, c = data.RH, alpha=0.5)
    ax1iva5.set_ylim([y5lim1,y5lim2])
    
    cal_points5 = [np.nanmean(data.loc[Isop_indexes_dict[i],'Pid 5']) for i in np.arange(0,3.0,0.5)]
    cal_points_error5 = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Pid 5']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept5,pcov5 = opt.curve_fit(linear_fit, data['Isop'], data['Pid 5'], sigma = data['Pid Error 5'])
    pid_fit5 = [slope_intercept5[0],(np.max(data.Isop)*slope_intercept5[1])+slope_intercept5[0]]  
    perr5 = np.sqrt(np.diag(pcov5))    
    Intercept_error5 = perr5[0]/np.sqrt(len(cal_points5))
    Slope_Error5 = perr5[1]/np.sqrt(len(cal_points5))
    
    slope_patch_pid5 = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept5[1])+'+/-'+str('%.1g' % Slope_Error5),color = 'b')
    intecept_patch_pid5 = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept5[0])+'+/-'+str('%.1g' % Intercept_error5),color = 'b')
    ax1iva5.legend(handles=[slope_patch_pid5,intecept_patch_pid5],loc='best')
    ax1iva5.plot(isop_fit,pid_fit5)
        
    ax1iva5.plot(isop_fit,pid_fit5)
    
    
    
    
    figiva5c = plt.figure()
    figiva5c.suptitle('Corrected Isop vs All cal points for Septemeber, Pid 5')
    ax1iva5c = figiva5c.add_subplot(111)    
    areac = 10*(datac.RH)
    ax1iva5c.scatter(datac['Isop'], datac['Pid 5'], s=areac, c = datac.RH, alpha=0.5)
    ax1iva5c.set_ylim([y5clim1,y5clim2])

            
    cal_points5c = [np.nanmean(datac.loc[Isop_indexes_dict[i],'Pid 5']) for i in np.arange(0,3.0,0.5)]
    cal_points_error5c = [(np.nanstd(datac.loc[Isop_indexes_dict[i],'Pid 5']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept5c,pcov5c = opt.curve_fit(linear_fit, datac['Isop'], datac['Pid 5'], sigma = datac['Pid Error 5'])
    pid_fit5c = [slope_intercept5c[0],(np.max(data.Isop)*slope_intercept5c[1])+slope_intercept5c[0]]  
    perr5c = np.sqrt(np.diag(pcov5c))    
    Intercept_error5c = perr5c[0]/np.sqrt(len(cal_points5c))
    Slope_Error5c = perr5c[1]/np.sqrt(len(cal_points5c))
    
    slope_patch_pid5c = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept5c[1])+'+/-'+str('%.1g' % Slope_Error5c),color = 'b')
    intecept_patch_pid5c = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept5c[0])+'+/-'+str('%.1g' % Intercept_error5c),color = 'b')
    ax1iva5c.legend(handles=[slope_patch_pid5c,intecept_patch_pid5c],loc='best')
    
    ax1iva5c.plot(isop_fit,pid_fit5c)

    
    
##################################################################################################





if isop_vs_all_points_time == 'Y':
    
    def circle_maker(dataset):
        return ((((((timeconverter2num(dataset)/700000)**100)/140)**200)/57000)**5)*100

    #data.loc[:,'The Time'] = data['The Time'].map(timeconverter2num)    
    #datac.loc[:,'The Time'] = datac['The Time'].map(timeconverter2num) 
    
    figiva3 = plt.figure()
    figiva3.suptitle('Uncorrected Isop vs All cal points for Septemeber, Pid 3')
    ax1iva3 = figiva3.add_subplot(111)    
    area = data['The Time'].map(circle_maker)


    ax1iva3.scatter(data['Isop'], data['Pid 3'], s=area, c = data['The Time'], alpha=0.5)
    ax1iva3.set_ylim([y3lim1,y3lim2])

    
    
    figiva3c = plt.figure()
    figiva3c.suptitle('Corrected Isop vs All cal points for Septemeber, Pid 3')
    ax1iva3c = figiva3c.add_subplot(111)    
    ax1iva3c.scatter(datac['Isop'], datac['Pid 3'], s=area, c = data['The Time'], alpha=0.5)
    ax1iva3c.set_ylim([y3clim1,y3clim2])
    

    
    
    figiva4 = plt.figure()
    figiva4.suptitle('Uncorrected Isop vs All cal points for Septemeber, Pid 4')
    ax1iva4 = figiva4.add_subplot(111)    
    ax1iva4.scatter(data['Isop'], data['Pid 4'], s=area, c = data['The Time'], alpha=0.5)
    ax1iva4.set_ylim([y4lim1,y4lim2])

    
    
    figiva4c = plt.figure()
    figiva4c.suptitle('Corrected Isop vs All cal points for Septemeber, Pid 4')
    ax1iva4c = figiva4c.add_subplot(111) 
    ax1iva4c.scatter(datac['Isop'], datac['Pid 4'], s=area, c = datac['The Time'], alpha=0.5)
    ax1iva4c.set_ylim([y4clim1,y4clim2])






    figiva5 = plt.figure()
    figiva5.suptitle('Uncorrected Isop vs All cal points for Septemeber, Pid 5')
    ax1iva5 = figiva5.add_subplot(111)     
    ax1iva5.scatter(data['Isop'], data['Pid 5'], s=area, c = data['The Time'], alpha=0.5)
    ax1iva5.set_ylim([y5lim1,y5lim2])

    
    
    figiva5c = plt.figure()
    figiva5c.suptitle('Corrected Isop vs All cal points for Septemeber, Pid 5')
    ax1iva5c = figiva5c.add_subplot(111)    
    ax1iva5c.scatter(datac['Isop'], datac['Pid 5'], s=area, c = datac.RH, alpha=0.5)
    ax1iva5c.set_ylim([y5clim1,y5clim2])

    
##################################################################################################





if big_cal == 'Y':
    
    
    Isop = [np.nanmean(data.loc[Isop_indexes_dict[i],'Isop']) for i in np.arange(0,3.0,0.5)]
    Isop_error = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Isop']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    
    
    
    
    
    cal_points3c = [np.nanmean(datac.loc[Isop_indexes_dict[i],'Pid 3']) for i in np.arange(0,3.0,0.5)]
    cal_points_error3c = [(np.nanstd(datac.loc[Isop_indexes_dict[i],'Pid 3']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept3c,pcov3c = opt.curve_fit(linear_fit, Isop, cal_points3c, sigma = cal_points_error3c)
    pid_fit3c = [slope_intercept3c[0],(np.max(data.Isop)*slope_intercept3c[1])+slope_intercept3c[0]]  
    perr3c = np.sqrt(np.diag(pcov3c))    
    Intercept_error3c = perr3c[0]/np.sqrt(len(cal_points3c))
    Slope_Error3c = perr3c[1]/np.sqrt(len(cal_points3c))
    
    
    
    
    cal_points4c = [np.nanmean(datac.loc[Isop_indexes_dict[i],'Pid 4']) for i in np.arange(0,3.0,0.5)]
    cal_points_error4c = [(np.nanstd(datac.loc[Isop_indexes_dict[i],'Pid 4']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept4c,pcov4c = opt.curve_fit(linear_fit, Isop, cal_points4c, sigma = cal_points_error4c)
    pid_fit4c = [slope_intercept4c[0],(np.max(data.Isop)*slope_intercept4c[1])+slope_intercept4c[0]]
    perr4c = np.sqrt(np.diag(pcov4c))    
    Intercept_error4c = perr4c[0]/np.sqrt(len(cal_points4c))
    Slope_Error4c = perr3c[1]/np.sqrt(len(cal_points4c))
    
    
    
    cal_points5c = [np.nanmean(datac.loc[Isop_indexes_dict[i],'Pid 5']) for i in np.arange(0,3.0,0.5)]
    cal_points_error5c = [(np.nanstd(datac.loc[Isop_indexes_dict[i],'Pid 5']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept5c,pcov5c = opt.curve_fit(linear_fit, Isop, cal_points5c, sigma = cal_points_error5c)
    pid_fit5c = [slope_intercept5c[0],(np.max(data.Isop)*slope_intercept5c[1])+slope_intercept5c[0]]  
    perr5c = np.sqrt(np.diag(pcov5c))    
    Intercept_error5c = perr5c[0]/np.sqrt(len(cal_points5c))
    Slope_Error5c = perr3c[1]/np.sqrt(len(cal_points5c))
    
    
    
    
    cal_points3 = [np.nanmean(data.loc[Isop_indexes_dict[i],'Pid 3']) for i in np.arange(0,3.0,0.5)]
    cal_points_error3 = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Pid 3']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept3,pcov3 = opt.curve_fit(linear_fit, Isop, cal_points3, sigma = cal_points_error3)
    pid_fit3 = [slope_intercept3[0],(np.max(data.Isop)*slope_intercept3[1])+slope_intercept3[0]]
    isop_fit = [np.min(data.Isop),np.max(data.Isop)]    
    perr3 = np.sqrt(np.diag(pcov3))    
    Intercept_error3 = perr3[0]/np.sqrt(len(cal_points3))
    Slope_Error3 = perr3[1]/np.sqrt(len(cal_points3))
            
            
            
    cal_points4 = [np.nanmean(data.loc[Isop_indexes_dict[i],'Pid 4']) for i in np.arange(0,3.0,0.5)]
    cal_points_error4 = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Pid 4']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept4,pcov4 = opt.curve_fit(linear_fit, Isop, cal_points4, sigma = cal_points_error4)
    pid_fit4 = [slope_intercept4[0],(np.max(data.Isop)*slope_intercept4[1])+slope_intercept4[0]]
    isop_fit = [np.min(data.Isop),np.max(data.Isop)]    
    perr4 = np.sqrt(np.diag(pcov4))    
    Intercept_error4 = perr4[0]/np.sqrt(len(cal_points4))
    Slope_Error4 = perr4[1]/np.sqrt(len(cal_points4))
    
    
    
    cal_points5 = [np.nanmean(data.loc[Isop_indexes_dict[i],'Pid 5']) for i in np.arange(0,3.0,0.5)]
    cal_points_error5 = [(np.nanstd(data.loc[Isop_indexes_dict[i],'Pid 5']))/np.sqrt(len(Isop_indexes_dict[i])) for i in np.arange(0,3.0,0.5)]
    slope_intercept5,pcov5 = opt.curve_fit(linear_fit, Isop, cal_points5, sigma = cal_points_error5)
    pid_fit5 = [slope_intercept5[0],(np.max(data.Isop)*slope_intercept5[1])+slope_intercept5[0]]
    isop_fit = [np.min(data.Isop),np.max(data.Isop)]    
    perr5 = np.sqrt(np.diag(pcov5))    
    Intercept_error5 = perr5[0]/np.sqrt(len(cal_points5))
    Slope_Error5 = perr5[1]/np.sqrt(len(cal_points5))    
    
    
    
    
    
    
    yrange3 = [(np.max(cal_points3)+np.max(cal_points_error3)) - (np.min(cal_points3)-np.max(cal_points_error3)),(np.max(cal_points3c)+np.max(cal_points_error3c)) - (np.min(cal_points3c)-np.max(cal_points_error3c))]
    yrange3 = np.max(yrange3)+(np.max(yrange3)/10)
    
    yrange4 = [(np.max(cal_points4)+np.max(cal_points_error4)) - (np.min(cal_points4)-np.max(cal_points_error4)),(np.max(cal_points4c)+np.max(cal_points_error4c)) - (np.min(cal_points4c)-np.max(cal_points_error4c))]
    yrange4 = np.max(yrange4)+(np.max(yrange4)/10)
    
    yrange5 = [(np.max(cal_points5)+np.max(cal_points_error5)) - (np.min(cal_points5)-np.max(cal_points_error5)),(np.max(cal_points5c)+np.max(cal_points_error5c)) - (np.min(cal_points5c)-np.max(cal_points_error5c))]
    yrange5 = np.max(yrange5)+(np.max(yrange5)/10)
    

    yrange = np.max([yrange3,yrange4,yrange5])


    
    
    
    fig_cal3 = plt.figure()
    plt.suptitle('Cal of all points from September Pid 3')
    ax3 = fig_cal3.add_subplot(211)
    ax3c = fig_cal3.add_subplot(212)
    
    
    ax3c.errorbar(Isop,cal_points3c,xerr = Isop_error, yerr = cal_points_error3c, fmt='o')
    slope_patch_pid3c = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept3c[1])+'+/-'+str('%.1g' % Slope_Error3c),color = 'b')
    intecept_patch_pid3c = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept3c[0])+'+/-'+str('%.1g' % Intercept_error3c),color = 'b')
    ax3c.set_title('Corrected')
    ax3c.set_ylim([(np.min(cal_points3c)-np.max(cal_points_error3c)),(np.min(cal_points3c)-np.max(cal_points_error3c))+yrange])
    ax3c.plot(isop_fit,pid_fit3c)
    ax3c.legend(handles=[slope_patch_pid3c,intecept_patch_pid3c],loc='best')
    
    ax3.errorbar(Isop,cal_points3,xerr = Isop_error, yerr = cal_points_error3, fmt='o')
    ax3.set_title('Uncorrected')
    ax3.set_ylim([(np.min(cal_points3)-np.max(cal_points_error3)),(np.min(cal_points3)-np.max(cal_points_error3))+yrange])
    ax3.plot(isop_fit,pid_fit3)
    slope_patch_pid3 = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept3[1])+'+/-'+str('%.1g' % Slope_Error3),color = 'b')
    intecept_patch_pid3 = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept3[0])+'+/-'+str('%.1g' % Intercept_error3),color = 'b')
    ax3.legend(handles=[slope_patch_pid3,intecept_patch_pid3],loc='best')
    

    
    fig_cal4 = plt.figure()
    plt.suptitle('Cal of all points from September Pid 4')
    ax4 = fig_cal4.add_subplot(211)
    ax4c = fig_cal4.add_subplot(212)
    
    
    ax4c.errorbar(Isop,cal_points4c,xerr = Isop_error, yerr = cal_points_error4c, fmt='o')
    ax4c.set_title('Corrected')
    ax4c.set_ylim([(np.min(cal_points4c)-np.max(cal_points_error4c)),(np.min(cal_points4c)-np.max(cal_points_error4c))+yrange])
    ax4c.plot(isop_fit,pid_fit4c)
    slope_patch_pid4c = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept4c[1])+'+/-'+str('%.1g' % Slope_Error4c),color = 'b')
    intecept_patch_pid4c = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept4c[0])+'+/-'+str('%.1g' % Intercept_error4c),color = 'b')
    ax4c.legend(handles=[slope_patch_pid4c,intecept_patch_pid4c],loc='best')
    
    ax4.errorbar(Isop,cal_points4,xerr = Isop_error, yerr = cal_points_error4, fmt='o')
    ax4.set_title('Uncorrected')
    ax4.set_ylim([(np.min(cal_points4)-np.max(cal_points_error4)),(np.min(cal_points4)-np.max(cal_points_error4))+yrange])
    ax4.plot(isop_fit,pid_fit4)
    slope_patch_pid4 = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept4[1])+'+/-'+str('%.1g' % Slope_Error4),color = 'b')
    intecept_patch_pid4 = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept4[0])+'+/-'+str('%.1g' % Intercept_error4),color = 'b')
    ax4.legend(handles=[slope_patch_pid4,intecept_patch_pid4],loc='best')
    
    
    
    fig_cal5 = plt.figure()
    plt.suptitle('Cal of all points from September Pid 5')
    ax5 = fig_cal5.add_subplot(211)
    ax5c = fig_cal5.add_subplot(212)
    
    
    ax5c.errorbar(Isop,cal_points5c,xerr = Isop_error, yerr = cal_points_error5c, fmt='o')
    ax5c.set_title('Corrected')
    ax5c.set_ylim([(np.min(cal_points5c)-np.max(cal_points_error5c)),(np.min(cal_points5c)-np.max(cal_points_error5c))+yrange])
    ax5c.plot(isop_fit,pid_fit5c)
    slope_patch_pid5c = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept5c[1])+'+/-'+str('%.1g' % Slope_Error5c),color = 'b')
    intecept_patch_pid5c = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept5c[0])+'+/-'+str('%.1g' % Intercept_error5c),color = 'b')
    ax5c.legend(handles=[slope_patch_pid5c,intecept_patch_pid5c],loc='best')
    
    ax5.errorbar(Isop,cal_points5,xerr = Isop_error, yerr = cal_points_error5, fmt='o')
    ax5.set_title('Uncorrected')
    ax5.set_ylim([(np.min(cal_points5)-np.max(cal_points_error5)),(np.min(cal_points5)-np.max(cal_points_error5))+yrange])
    ax5.plot(isop_fit,pid_fit5)
    slope_patch_pid5 = mpatches.Patch(label='Slope = '+str('%.2g' % slope_intercept5[1])+'+/-'+str('%.1g' % Slope_Error5),color = 'b')
    intecept_patch_pid5 = mpatches.Patch(label = 'Intercept = '+str('%.2g' % slope_intercept5[0])+'+/-'+str('%.1g' % Intercept_error5),color = 'b')
    ax5.legend(handles=[slope_patch_pid5,intecept_patch_pid5],loc='best')



plt.show()
