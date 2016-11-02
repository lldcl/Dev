#Create a simple R file to look at data

## set working directory to find the files and call it 'path'.
path <- setwd("/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/201602/")

## List all the files I have in the working directory.
files <- list.files(path)

# Call on one csv file:
#filename <- read.csv("d20160201_01","d20160201_02","d20160202_03", header=TRUE, sep = ",")
# To concatenate files
for (file in files) {
  # if the merged dataset doesn't exist, create it
  if (!exists("data_concat")){
    data_concat <- read.csv(file, header = TRUE, sep=",")
  }
  # if the merged dataset does exist, append to it
  if (exists("data_concat")){
    temp_dataset <- read.csv(file, header = TRUE, sep=",")
    data_concat <- rbind(data_concat, temp_dataset)
    rm(temp_dataset)
  }
}
## look at dimensions of the data, returns the vaules in box below.
print(dim(data_concat))
# Trying to get the code to print out the right date and time of the run.
data_concat$TimeDate <- as.POSIXlt(data_concat$TheTime-24*60*60*4+60*60*2.15,format='%H', origin = "1900-01-01", tz = "GMT")

#mydata <- do.call(rbind,lapply(files[1:7], read.txt))
# Choosing files which are VOC calibrations
#d20160201_01 <- read.csv(file.choose(), header = TRUE)
#d20160201_02 <- read.csv(file.choose(), header = TRUE)
#d20160202_03 <- read.csv(file.choose(), header = TRUE)

#Merges all the files that I have identified as cal files into one, and called the new data frame VOC_cal.
#VOC_cal <- rbind(d20160201_01, d20160201_02, d20160202_03)

library(ggplot2)
library(openair)

# Add a new column, whuich calculates the correct temperature, instead of the voltage that the Temp sensor reads.
data_concat$Temp1 <- VOC_cal$Temp *10
# Create another column to calculate the relative humidity in the dataframe.
data_concat$RH <- (((VOC_cal$RH1/VOC_cal$VS)-0.16)/0.0062)/(1.0546-0.00216*VOC_cal$Temp1*10.)

# Calculating VOC conc.
VOC_cyl <- 40000.	#ppbv
mfchi_range <- 2000.	#sccm
mfchi_sccm <- data_concat$mfchiR*(mfchi_range/5.)
mfclo_range <- 20.	#sccm
mfclo_sccm <- data_concat$mfcloR*(mfclo_range/5.)
mfcmid_range <- 100.	#sccm
mfcmid_sccm <- data_concat$mfcmidR*(mfcmid_range/5.)

dil_fac <- mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
data_concat$VOC_mr <- (dil_fac*VOC_cyl)
# Plot a histogram of all the MOS1 signal data.
hist(data_concat$MOS1, main = "Histogram of MOS1 data", xlab="MOS (v)")
# First 500 data points
plot(data_concat$TimeDate[1:500], data_concat$MOS1[1:500], type =1, xlab="date", ylab = "MOS1 / V")


aggregate(list(time = dT$TheTime), cut(dT,"10 seconds")),mean)
		#convert daqfac time into real time pd.datetime object
	VOC_cal$TheTime <- datetime(VOC_cal.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset
	Time_avg = '10S'
	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
		
	# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

	T3 = pd.datetime(2015,01,01,0)
	# dt = pd.Series((data_concat.index - data_concat.index[0]),index=data_concat.index,name='dt')
	dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
	dt = dt.astype('timedelta64[s]')
	data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])

	mosdf = pd.concat([data_concat.dt,data_concat.MOS1,data_concat.MOS2,data_concat.RH1],axis=1)
	mosdf = mosdf.dropna()
	x_var = ['RH1','dt']
	x_train = mosdf[x_var]
	y_train = mosdf.MOS1

	linear_MOS1 = linear_model.LinearRegression()
	linear_MOS1.fit(x_train, y_train)
	linear_MOS1.score(x_train, y_train)
# 	print 'MOS1'
# 	print('Coefficient: \n', linear_MOS1.coef_)
# 	print('Intercept: \n', linear_MOS1.intercept_)
	MOS1_pred = linear_MOS1.predict(x_train)

	y_train = mosdf.MOS2
	linear_MOS2 = linear_model.LinearRegression()
	linear_MOS2.fit(x_train, y_train)
	linear_MOS2.score(x_train, y_train)
# 	print 'MOS2'
# 	print('Coefficient: \n', linear_MOS2.coef_)
# 	print('Intercept: \n', linear_MOS2.intercept_)
	MOS2_pred = linear_MOS2.predict(x_train)


# Plots
	mosfig = plt.figure()
	mos1ax = mosfig.add_subplot(2,1,1)
	mos1ax.plot(mosdf.dt,mosdf.MOS1,color='b',marker='o')
	mos1ax.plot(mosdf.dt,MOS1_pred)
	mos1ax.set_ylabel("MOS1 (V)")

	mos1ax = mosfig.add_subplot(2,1,2)
	mos1ax.plot(mosdf.dt,mosdf.MOS2,color='r',marker='o')
	mos1ax.plot(mosdf.dt,MOS2_pred)
	mos1ax.set_ylabel("MOS2 (V)")
	#plt.show()
	
	return(linear_MOS1.coef_,linear_MOS2.coef_,linear_MOS1.intercept_,linear_MOS2.intercept_)

#################################
# File(s) put in to be the baseline, this can be a number of overnight runs.
baseline_file = ['d20160128_03b']
#baseline_file = ['d20151211_03b']
a1,a2,b1,b2 = baseline_cor(baseline_file)
# File with the isoprene in to plot the isoprene sensitivity.
#cal_file = ['d20151210_07','d20151211_01','d20151211_02','d20151214_01','d20151215_01','d20151215_02','d20151216_01','d20151217_01','d20151218_02','d20151218_03']
cal_file = ['d20160129_02']

for i in cal_file:
	folder = list(i)[1:7]
	f = "".join(folder)+'/'+i

#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(path+f)

	#dT = seconds since file start
	dT = data.TheTime-data.TheTime[0]
	dT*=60.*60.*24.

	#convert daqfac time into real time pd.datetime object
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')
	T1 = pd.datetime(1899,12,30,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset

	isop_cyl = 40000.	#ppbv
	mfchi_range =2000.	#100.	#sccm
	mfchi_sccm = data.mfchiR*(mfchi_range/5.)
	mfclo_range = 20.	#sccm
	mfclo_sccm = data.mfcloR*(mfclo_range/5.)
	mfcmid_range = 100.	#sccm
	mfcmid_sccm = data.mfcmidR*(mfcmid_range/5.)

	dil_fac = mfclo_sccm/(mfclo_sccm+mfchi_sccm+mfcmid_sccm)
	isop_mr = pd.Series(dil_fac*isop_cyl,name='isop_mr')
	data = pd.concat([data,isop_mr],axis=1)

	Time_avg = '10S'

	mean_resampled = data.copy(deep=True)
	mean_resampled.RH1 = (((mean_resampled.RH1/mean_resampled.VS)-0.16)/0.0062)/(1.0546-0.00216*mean_resampled.Temp*100.)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=True)
	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')

	#filter out periods when isop changes rapidly (disopdt<0.1) and for 300 seconds afterwards
	nm_pts = 300./float(Time_avg[:-1])
	disopdt = pd.Series(np.absolute(mean_resampled.isop_mr.diff()),name='disopdt')
	disopdt_filt = pd.Series(0, index=disopdt.index,name='disopdt_filt')
	disop_ctr=0
	for dp in disopdt:
		if (dp>0.1):
			disopdt_filt[disop_ctr:int(disop_ctr+nm_pts)] = 1
		disop_ctr+=1

	mean_resampled = pd.concat([mean_resampled,disopdt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = pd.concat([mean_resampled,disopdt_filt],axis=1,join_axes=[mean_resampled.index])
	mean_resampled = mean_resampled[mean_resampled.disopdt_filt == 0]

# join files
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'

T3 = pd.datetime(2015,01,01,0)
# dt = pd.Series((data_concat.index - data_concat.index[0]),index=data_concat.index,name='dt')
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('timedelta64[s]')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])

# Correcting the data for the temperature (a1) and the long term drift (b1).
MOS1_cor = data_concat.MOS1-((a1[0]*data_concat.RH1)+(a1[1]*data_concat.dt)+b1)
MOS2_cor = data_concat.MOS2-((a2[0]*data_concat.RH1)+(a2[1]*data_concat.dt)+b2)

cor1fig = plt.figure("Comparing raw data with corrected")

cor1ax = cor1fig.add_subplot(2,1,1)
cor2ax = cor1fig.add_subplot(2,1,2)
cor3 = cor1ax.twinx()
cor4 = cor2ax.twinx()

cor1ax.plot(data_concat.dt,data_concat.MOS1,color='b',marker='o')
cor3.plot(data_concat.dt, data_concat.isop_mr, color='k')
cor2ax.plot(data_concat.dt, MOS1_cor,color='k',marker='o')
cor4.plot(data_concat.dt, data_concat.isop_mr, color='k')

cor1ax.set_ylabel("MOS1 (V)")
cor2ax.set_ylabel("MOS1 corrected (V)")


# MOS2 data.
cor2fig = plt.figure("comparing MOS2 raw data with the corrected data")
cor5ax = cor2fig.add_subplot(2,1,1)
cor7ax = cor2fig.add_subplot(2,1,2)
cor6 = cor5ax.twinx()
cor8 = cor7ax.twinx()

cor5ax.plot(data_concat.dt,data_concat.MOS2,color='r',marker='o')
cor6.plot(data_concat.dt, data_concat.isop_mr, color='k')
cor7ax.plot(data_concat.dt,MOS2_cor,color='k',marker='o')
cor8.plot(data_concat.dt, data_concat.isop_mr, color='k')

cor5ax.set_ylabel("MOS2 (V)")
cor6.set_ylabel("Isoprene /ppb")
cor8.set_ylabel("Isoprene / ppb")
cor7ax.set_ylabel("MOS2 corrected(V)")

### Need to plot up the isoprene sensitivity polts, with linear regression.
# Finding the isoprene sensitivity
# Bin the data into bins of 0.25ppb isoprene, get an average for this data and then plot this.

# Define a function to determine standard deviation
def stddev(dat):
	stanIS = np.std(dat)
	return stanIS
# Bin the data into 0.25 ppb of isoprene sections
bin1 = stats.binned_statistic(data_concat.isop_mr, MOS1_cor, statistic='mean', bins=60, range=(0,15))
bin2 = stats.binned_statistic(data_concat.isop_mr, MOS2_cor, statistic='mean', bins=60, range=(0,15))
bin3 = stats.binned_statistic(data_concat.isop_mr, data_concat.isop_mr, statistic='mean', bins=60, range=(0,15))
bin4 = stats.binned_statistic(data_concat.isop_mr, MOS1_cor, statistic=stddev, bins=60, range=(0,15))
bin5 = stats.binned_statistic(data_concat.isop_mr, MOS2_cor, statistic=stddev, bins=60, range=(0,15))
bin6 = stats.binned_statistic(data_concat.isop_mr, data_concat.isop_mr, statistic=stddev, bins=60, range=(0,15))
# Turn into pandas to get rid of NaNs.
MOS1_cor = pd.Series(bin1[0])
MOS2_cor = pd.Series(bin2[0])
isop = pd.Series(bin3[0])
st1 = pd.Series(bin4[0])
st2 = pd.Series(bin5[0])
stIs = pd.Series(bin6[0])
# get rid of NaNs for both the data and the standard deviation.
MOS1_cor = MOS1_cor.dropna()
MOS2_cor = MOS2_cor.dropna()
isop = isop.dropna()
st1 = st1.dropna()
st2 = st2.dropna()
stIs = stIs.dropna()

isoprene = plt.figure(" Isoprene sensitivity with the general background removed")
ax1 = isoprene.add_subplot(2,1,1)
ax2 = isoprene.add_subplot(2,1,2)
ax1.scatter(isop, MOS1_cor, color="g")
ax1.errorbar(isop, MOS1_cor, xerr=stIs, yerr=st1, lw=1, fmt='o', color="g")
ax2.scatter(isop, MOS2_cor, color="b")
ax2.errorbar(isop, MOS2_cor, xerr=stIs, yerr=st2, lw=1, fmt='o', color="b")
ax1.set_ylabel("MOS1 signal / V")
ax2.set_ylabel("MOS2 signal / v")
ax1.set_xlabel("Isoprene / ppb")
ax2.set_xlabel("Isoprene / ppb")
slope3, intercept3, R2value3, p_value3, st_err3 = stats.linregress(isop, MOS1_cor)
slope4, intercept4, R2value4, p_value4, st_err4 = stats.linregress(isop, MOS2_cor)
ax1.plot([np.min(isop), np.max(isop)], [(slope3*np.min(isop))+intercept3, (slope3*np.max(isop))+intercept3])
ax2.plot([np.min(isop), np.max(isop)], [(slope4*np.min(isop))+intercept4, (slope4*np.max(isop))+intercept4])
print ("Gradient of isop vs MOS1", slope3)
print ("Intercept of isop vsMOS1", intercept3)
print ("R2 of isop vs MOS1", R2value3)
print ("Gradient of isop vs MOS2", slope4)
print ("Intercept of isop vs MOS2", intercept4)
print ("R2 of isop vs MOS2", R2value4)
print ("Average RH", np.mean(data_concat.RH1))
print ("Average temp", np.mean(data_concat.Temp*100))

plt.show()

