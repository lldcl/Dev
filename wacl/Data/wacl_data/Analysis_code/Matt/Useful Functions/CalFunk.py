class functions(object):
    from operator import itemgetter
    left_shift_stds = {}
    right_shift_stds = {}
    nanL = []
    nanR = []

    
    def cal_point_ammender(self,data_set,bad_cal_length,shifter,S,F):
        S = list(S)
        F = list(F)
        for i in xrange(0,len(S)):
            orig_std = np.nanstd(data_set[S[i]:F[i]])
            
            if orig_std > 0.7:
                S[i] = F[i] - bad_cal_length
    
            
            left_shift_stds = {}
            for k in xrange(1,20):
                x_shiftL = k*shifter
                left_shift_stds[k] = np.nanstd(data_set[S[i]-x_shiftL:F[i]-x_shiftL])
            nanL = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
            for t in nanL:
                del(left_shift_stds[t])
                
            minPairL = min(left_shift_stds.iteritems(), key=self.itemgetter(1))
    
    
            right_shift_stds = {}
            for k in xrange(1,20):
                x_shiftR = k*shifter
                right_shift_stds[k] = np.nanstd(data_set[S[i]+x_shiftR:F[i]+x_shiftR])
                
            nanR = [q for q in right_shift_stds if np.isnan(right_shift_stds[q])]
            for t in nanR:
                del(right_shift_stds[t])
                
            minPairR = min(right_shift_stds.iteritems(), key=self.itemgetter(1))
    
            
            
            if minPairL[1] < orig_std and minPairL[1] < minPairR[1]:
                S[i] = S[i]-minPairL[0]*shifter
                F[i] = F[i]-minPairL[0]*shifter
            elif minPairR[1] < orig_std and minPairR[1] < minPairL[1]:
                S[i] = S[i]+minPairR[0]*shifter
                F[i] = F[i]+minPairR[0]*shifter  

        if S[0] < 0:
            SF = negative_remover(S,F)
            S = SF[0]
            F = SF[1]
            
        return S,F  
        
    def negative_remover(self,list1,list2):
        negative_removerF = []
        negative_removerS = []
    
        
        if list1[0] < 0:
            for i in xrange(0,len(list1)):
                if list2[i]<0:
                    negative_removerF.append(i)
                if list1[i] < 0:
                    negative_removerS.append(i)
    
            if negative_removerF < negative_removerS:
                negative_removerF = max(negative_removerS)
                negative_removerS = max(negative_removerS)+1         
            
                A = [0] + list1[negative_removerS:]
                B = list2[negative_removerF:]
            else:
                A = list1[max(negative_removerS)+1:]
                B = list2[max(negative_removerF)+1:]
            return A,B
    
    def plotter(pidxd,pidxdc):
    
        pid_number = int(pidxd.name[-1])
        #Making seperate integer and str variables for the pid number and the string 3 shaves some time of the function, and assigning dataL.TheTime to tim may do as well
        pid_number_str = pidxd.name[-1]
        tim =  dataL.TheTime 
        
        
        # Need the date for titles of graphs
        date = str(tim[0])[5:10]
        
        #Also need this for the titles of the graphs
        filenumber = filenameL[-2:]
        
        
        times = self.list_multisplicer(tim,S,F)
                                                                
        voltage_pid = self.list_multisplicer(pidxd,S,F)
                
        isop_chunks_data_pid = self.list_multisplicer(isop_mr,S,F)
        
        
        
        pid_rolling_avg = pd.rolling_mean(pidxd,300,60)
        #Fig for the raw plots (That's why it's figure r)
        figr = plt.figure()
        figr.suptitle('Pid'+pid_number_str+' , Data Plot ('+date+') - '+filenumber,fontsize = 16)
        # Creating 2 axes on the same subplot for Isoprene and pid voltage (I named the axes according to whether they were a raw plot or not so axr or axc, which axis they were, so axr1, axr2, axr3 or axc1 and the a and b at the end refers to the left and right scale respectively, so axr1a would have the pid voltage, and axr1b would have the isoprene)
        if humid_correct == 'Y':
            x1 = 221 #Posistion of the Uncorrected Spliced graph
            x2 = 223 #Posistion of the Corrected Spliced graph
            x3 = 224 #Posistion of the Raw Data graph
            x4 = 222 #Posistion of the RH graph
        else:
            x1 = 211
            x3 = 212
        axr1a = figr.add_subplot(x1)
        axr1b = axr1a.twinx()
        
        
        ##################### Uncorrected Spliced Plot #########################
        
        ### Uncorrected spliced voltage
        axr1a.plot(times,voltage_pid, linewidth=1,color= 'r')
        ### Uncorrected Rolling Average
        axr1a.plot(tim,pid_rolling_avg, linewidth=1, color = 'b')
        ### Isoprene concentration
        axr1b.plot(times,isop_chunks_data_pid,linewidth = 1,color='k')
        # Adding labels
        axr1a.set_ylabel('Pid'+pid_number_str+' Voltage / V')
        axr1b.set_ylabel('Isop / ppb')
        plt.xlabel('Time / s', fontsize = 20)
        
        # Plotting a Line at the zero point to show variation of the zero
        for zero_index in xrange(0,len(cal_df)):
            if np.around(cal_df.loc[zero_index,'Isop'],1) == 0.0:
                y0 = cal_df.loc[zero_index,'Pid'+pid_number_str+' Voltage']
                if humid_correct == 'Y':
                    y0c = cal_dfc.loc[zero_index,'Pid'+pid_number_str+' Voltage']
                break    
        axr1a.plot([min(tim),max(tim)],[y0,y0],'k-')
        ##################### Corrected Spliced Plot #########################
        if humid_correct == 'Y':
            
            ### Splicing the corrected Voltages
            voltage_pidc = self.list_multisplicer(pidxdc,S,F)
            ### Calculating a Rolling Average of the corrected Voltages
            pidc_rolling_avg = pd.rolling_mean(pidxdc,300,60)
            
            # Creating Subplot for the corrected graph
            axr2a = figr.add_subplot(x2)
            axr2b = axr2a.twinx()
    
            # Corrected plot of Spliced Voltage
            axr2a.plot(times,voltage_pidc, linewidth=1,color= 'r')
            axr2a.plot(tim,pidc_rolling_avg, linewidth=1, color = 'b')
            
            # This is the Black Line (the Isoprene concentrations at the spliced bits)
            axr2b.plot(times,isop_chunks_data_pid,linewidth = 1,color='k')
            
            #Setting axes Labels
            axr2a.set_ylabel('Pid'+pid_number_str+' Voltage / V')
            plt.xlabel('Time / s', fontsize = 20)
            
            # Plotting a Line at the zero point to show variation of the zero
            axr2a.plot([min(tim),max(tim)],[y0c,y0c],'k-')
            
            ########################### RH Plot ############################
            
            axr4a = figr.add_subplot(x4)
            axr4b = axr4a.twinx()
            
            #Plotting Time against RH
            axr4a.plot(tim,RH,color='b')
    
            #Plotting Rolling Averages
            axr4b.plot(tim,pid_rolling_avg, linewidth=1, color = 'r')
            axr4b.plot(tim,pidc_rolling_avg, linewidth=1, color = 'g')
            
            # Plotting a Line at the zero point to show variation of the zero
            axr4b.plot([min(tim),max(tim)],[y0,y0],'k-')
            if humid_correct == 'Y':
                axr4b.plot([min(tim),max(tim)],[y0c,y0c],'-k')
            
            #Setting the title
            axr4b.set_title('red = uncorrected, green = corrected, blue =  humidity')
        
        
        
        ##################### Raw Data Plot #####################
        
        axr3a = figr.add_subplot(x3)
        axr3b = axr3a.twinx()
        #The raw PID Data.
        axr3a.plot(tim,pidxd, linewidth=1,color='b')
        #The Isoprene data.
        axr3b.plot(tim,isop_mr, linewidth=1,color='g')
                
        # Setting axes labels
        axr3b.set_ylabel('Isop / ppb')
        plt.xlabel('Time / s', fontsize = 20)
        
        
    
        ##################### Cal Plot #########################
    
        figc = plt.figure()
        figc.suptitle('Pid'+pid_number_str+' , Cal plot ('+date+') - '+filenumber,fontsize = 16)
        axc1a = figc.add_subplot(111)
        
        
        # Setting axes labels
        axc1a.set_ylabel('Pid Voltage / V')
        plt.xlabel('Isop / ppb')
        
        #Plotting Cal Points with Errorbars
        axc1a.errorbar(cal_df.Isop,cal_df['Pid'+pid_number_str+' Voltage'], xerr = xerr, yerr = yerr[pid_number], fmt='bo')
        #Plotting Lines of Best Fit
        axc1a.plot(isop_fit,pid_fits[pid_number],color = 'b')
    
        
        if humid_correct == 'Y':
            # Creating a new scale for the corrected cal line
            axc1b = axc1a.twinx()
            axc1b.errorbar(cal_df.Isop,cal_dfc['Pid'+pid_number_str+' Voltage'], xerr = xerr, yerr = yerr[pid_number], fmt='mx')
            axc1b.plot(isop_fit, pidc_fits[pid_number],color = 'm')
            axc1b.set_ylabel('Pid Voltage / V')
            
        # Adding a legend #
        # Information for the legends, values are given to 2 d.p. and intercepts are given to 1 d.p. (to change this just change the '%.Xg' number)
        slope_patch_pid = mpatches.Patch(label='Slope = '+str('%.2g' % Values['Slope'][pid_number])+'+/-'+str('%.1g' % Values['Slope Error'][pid_number]),color = 'b')
        intecept_patch_pid = mpatches.Patch(label = 'Intercept = '+str('%.2g' % Values['Intercept'][pid_number])+'+/-'+str('%.1g' % Values['Intercept'][pid_number]),color = 'b')
        
        if humid_correct == 'Y':
            slope_patch_pid_corrected = mpatches.Patch(label = 'Slopec = '+str("%.2g" % Corrected_Values['Slope'][pid_number])+'+/-'+str("%.1g" % Corrected_Values['Slope Error'][pid_number]),color = 'm')
            intecept_patch_pid_corrected = mpatches.Patch(label = 'Interceptc = '+str("%.2g" % Corrected_Values['Intercept'][pid_number])+'+/-'+str("%.1g" % Corrected_Values['Intercept Error'][pid_number]),color = 'm')
            #Popping the legend on the graph in the 'best'location
            plt.legend(handles=[slope_patch_pid,intecept_patch_pid,slope_patch_pid_corrected,intecept_patch_pid_corrected],loc='best')
        
        else:
            plt.legend(handles=[slope_patch_pid,intecept_patch_pid],loc='best')
        # Setting Labels
        plt.ylabel('Pid'+pid_number_str+' Voltage / V')
        plt.xlabel('Isoprene Concentration / ppb')
    
        
        plt.show()
        
    # To interpolate between NaN values
    def nan_helper(data,averagefreq,nanno):
        return data.fillna(pd.rolling_mean(data, averagefreq, min_periods=nanno).shift(-3))
        
        
    #To convert timestamps to a string
    def timeconverter(T):
        #	print T
       	return (datetime.datetime.strptime(T,"%y-%m-%d-%H-%M-%S-%f"))
    
    
    #Splices list at indexes given by 2 lists
    def list_multisplicer(l1st,start_inidexes,end_indexes):
        new_lt = []
        for i in xrange(0,len(start_inidexes)):
            first = start_inidexes[i]
            last = end_indexes[i]
            for pt in xrange(0,len(l1st)):
                if pt >=first and pt <=last:
                    new_lt.append(l1st[pt])
        return new_lt
        
    def list_multisplicer_listsout(l1st,start_indexes,end_indexes):
                new_lt = []
                for i in xrange(0,len(start_indexes)):
                    segments = []
                    first = start_indexes[i]
                    last = end_indexes[i]
                    for pt in xrange(0,len(l1st)):
                        if pt >=first and pt<=last:
                            segments.append(l1st[pt])
                    new_lt.append(segments)
                non_blank = []
                for i in new_lt:
                    if i != []:
                        non_blank.append(i)     
                return non_blank
    
                
                    
    #Returns a Linear Fit
    def linear_fit(slope, intercept, x):
        return (slope*x)+intercept
    
    #Returns a quadratic Fit
    def quadratic_fit(Isoprene, root1, root2,xfac1,xfac2):
        return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)
        
    #Returns a cubic Fit for pid4  
    def cubic_fit4(Isoprene, root1, root2,root3,xfac1,xfac2,xfac3):
        return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)*((xfac3*Isoprene)+root3)
    
    #Returns a cubic Fit for pids 3 & 5
    def cubic_fit35(Isoprene, root1, root2,root3,xfac1,xfac2,xfac3):
        return ((xfac1*Isoprene)+root1)*((xfac2*Isoprene)+root2)*((xfac3*Isoprene)-root3) 
            
    # Converts a timestamp to a list
    def timestamp_convert(timestamp):
        
        if type(timestamp) == pd.tslib.Timestamp:
            timestamp = str(timestamp)
            
            
        elif len(timestamp.split('-')) >= 5:
            c = timestamp.split('-')
            return c
            
        b = timestamp.split('-')
        year = b[0]
        month = b[1]
        c = b[2].split(' ')
        day = c[0]
        d = c[1].split(':')
        hour = d[0]
        minute = d[1]
        e = d[2].split('.')
        second = e[0]
        try:
            millisecond = e[1]
        except IndexError:
            pass
            
        time_list_final = [year,month,day,hour,minute,second]
        try:
            time_list_final.append(millisecond)
        except UnboundLocalError:
            pass
        return time_list_final