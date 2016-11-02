# To analyse the MS files
from xml.dom import minidom
import base64
from struct import unpack as unpack
import pandas as pd
import matplotlib.pyplot as plt

def decode_element(myelement):
    try:
        mystring = myelement.childNodes[1].childNodes[0].nodeValue
        base64Data = mystring.encode("utf-8")
        decodedData = base64.b64decode(base64Data)

        
        myendian = myelement.childNodes[1].attributes["endian"].value
        myprecision =  myelement.childNodes[1].attributes["precision"].value
        mylength = myelement.childNodes[1].attributes["length"].value
        if myendian == "little":
            myendian = "<"
        else:
            myendian = ">"
        if myprecision == "32":
            myprecision = "f"
        else:
            myprecision = "d"
        
        fmt = "{endian}{arraylength}{floattype}".format( endian = myendian, arraylength = mylength , floattype = myprecision )
        unpackedData = list(unpack(fmt, decodedData))
    except:
        unpackedData = []
    return unpackedData

def get_time(myelement):
    if myelement.childNodes[5].attributes["name"].value == "TimeInMinutes":
        mytime = myelement.childNodes[5].attributes["value"].value
    return mytime

def get_int_value(val):
    return int(round(float(val),2))

def get_df(myfile,int_threshold):
    print("Decoding MZs")
    mz_list = decode_element_list(myfile.getElementsByTagName("mzArrayBinary"))
    print("Decoding intensities")
    int_list = decode_element_list(myfile.getElementsByTagName("intenArrayBinary"))
    times = []
    print("Decoding times")
    for mytime in myfile.getElementsByTagName("spectrumInstrument"):
        times.append(get_time(mytime))
    times = [round(float(i)*60,2) for i in times]
    ser_list = []
    print ("Creating pandas dataframe")
    for mzs,ints  in zip(mz_list,int_list):
        myser = pd.Series(data = ints,index = mzs).groupby(get_int_value).sum()
        ser_list.append(myser)
    ser_list = [i[i>int_threshold] for i in ser_list]
    overall_df = pd.concat(ser_list,axis = 1)
    print("Setting times")
    index_lists = []
    for sets in ser_list:
        if len(sets.index.values):
            index_lists.append(1)
        else:
            index_lists.append(0)
    time_cols = [i[0] for i in list(zip(times,index_lists)) if i[1] == 1]
    overall_df.columns = time_cols
    return overall_df

    
def decode_element_list(element_list):
    return_list = []
    list_length = len(element_list)
    if len(element_list) > 3000:
        updating = True
    
    for my_element in element_list:
        return_list.append(decode_element(my_element))
    return return_list

print("Reading file")
path = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/MS_files/'
# First mzData file from MS
filename = 'ms20160817_01.mzdata.xml'
myfile = minidom.parse(path+filename)
int_threshold = 10000
mydf = get_df(myfile,int_threshold)
mydf = mydf.transpose()

mydf['TIC'] = mydf.sum(axis=1)
# To get the start time from the original file, use the getElementsbyTag Name. Then the code searches for
# software ( the name in the file for time). It will then grab the value for completion time. 
# This needs to be converted into a pandas datetime object
Start_time = pd.to_datetime(myfile.getElementsByTagName("software")[0].attributes["completionTime"].value)
# Convert the seconds since file started into a datetime. 
mydf['STime'] = pd.to_timedelta(mydf.index,'s')
mydf['Date_and_time'] = Start_time + mydf.STime
# Get into excel to check the numbers
pd.DataFrame(data=mydf, index=mydf.index,).to_csv('MSfile.csv', index=True)

# Second mzData file
path3 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/MS_files/'
filename3 = 'ms20160817_02.mzdata.xml'
myfile3 = minidom.parse(path3+filename3)
int_threshold = 10000
mydf3 = get_df(myfile3,int_threshold)
mydf3 = mydf3.transpose()

mydf3['TIC'] = mydf3.sum(axis=1)
# To get the start time from the original file, use the getElementsbyTag Name. Then the code searches for
# software ( the name in the file for time). It will then grab the value for completion time. 
# This needs to be converted into a pandas datetime object
Start_time3 = pd.to_datetime(myfile3.getElementsByTagName("software")[0].attributes["completionTime"].value)
# Convert the seconds since file started into a datetime. 
mydf3['STime'] = pd.to_timedelta(mydf3.index,'s')
mydf3['Date_and_time'] = Start_time3 + mydf3.STime


# Third mzData file
path4 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/MS_files/'
filename4 = 'ms20160817_03.mzdata.xml'
myfile4 = minidom.parse(path4+filename4)
int_threshold = 10000
mydf4 = get_df(myfile4,int_threshold)
mydf4 = mydf4.transpose()
mydf4['TIC'] = mydf4.sum(axis=1)
# To get the start time from the original file, use the getElementsbyTag Name. Then the code searches for
# software ( the name in the file for time). It will then grab the value for completion time. 
# This needs to be converted into a pandas datetime object
Start_time4 = pd.to_datetime(myfile4.getElementsByTagName("software")[0].attributes["completionTime"].value)
# Convert the seconds since file started into a datetime. 
mydf4['STime'] = pd.to_timedelta(mydf4.index,'s')
mydf4['Date_and_time'] = Start_time4 + mydf4.STime

"""
# Fourth mzData file
path5 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/MS_files/'
filename5 = 'ms20160816_08.mzdata.xml'
myfile5 = minidom.parse(path5+filename5)
int_threshold = 10000
mydf5 = get_df(myfile5,int_threshold)
mydf5 = mydf5.transpose()
mydf5['TIC'] = mydf5.sum(axis=1)
# To get the start time from the original file, use the getElementsbyTag Name. Then the code searches for
# software ( the name in the file for time). It will then grab the value for completion time. 
# This needs to be converted into a pandas datetime object
Start_time5 = pd.to_datetime(myfile5.getElementsByTagName("software")[0].attributes["completionTime"].value)
# Convert the seconds since file started into a datetime. 
mydf5['STime'] = pd.to_timedelta(mydf5.index,'s')
mydf5['Date_and_time'] = Start_time5 + mydf5.STime



# Fifth MS mzData file
path6 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/MS_files/'
filename6 = 'ms20160818_04.mzdata.xml'
myfile6 = minidom.parse(path6+filename6)
int_threshold = 10000
mydf6 = get_df(myfile6,int_threshold)
mydf6 = mydf6.transpose()
mydf6['TIC'] = mydf6.sum(axis=1)
# To get the start time from the original file, use the getElementsbyTag Name. Then the code searches for
# software ( the name in the file for time). It will then grab the value for completion time. 
# This needs to be converted into a pandas datetime object
Start_time6 = pd.to_datetime(myfile6.getElementsByTagName("software")[0].attributes["completionTime"].value)
# Convert the seconds since file started into a datetime. 
mydf6['STime'] = pd.to_timedelta(mydf6.index,'s')
mydf6['Date_and_time'] = Start_time6 + mydf6.STime

# Sixth MS mzData file
path7 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/MS_files/'
filename7 = 'ms20160818_05.mzdata.xml'
myfile7 = minidom.parse(path7+filename7)
int_threshold = 10000
mydf7 = get_df(myfile7,int_threshold)
mydf7 = mydf7.transpose()
mydf7['TIC'] = mydf7.sum(axis=1)
# To get the start time from the original file, use the getElementsbyTag Name. Then the code searches for
# software ( the name in the file for time). It will then grab the value for completion time. 
# This needs to be converted into a pandas datetime object
Start_time7 = pd.to_datetime(myfile7.getElementsByTagName("software")[0].attributes["completionTime"].value)
# Convert the seconds since file started into a datetime. 
mydf7['STime'] = pd.to_timedelta(mydf7.index,'s')
mydf7['Date_and_time'] = Start_time7 + mydf7.STime

# plot up the total on chromatogram against time
TICplot = plt.figure()
ax1 = TICplot.add_subplot(111)
ax1.plot(mydf.Date_and_time, mydf.TIC, color= "navy")
ax1.plot(mydf3.Date_and_time, mydf3.TIC, color = "royalblue")
ax1.plot(mydf4.Date_and_time, mydf4.TIC, color = "cornflowerblue")
# ax1.plot(mydf5.Date_and_time, mydf5.TIC, color = "skyblue")
ax1.plot(mydf6.Date_and_time, mydf6.TIC, color = "teal")
ax1.plot(mydf7.Date_and_time, mydf7.TIC, color = "blue")
ax1.set_xlabel("Time since file started")
ax1.set_ylabel("Intensity")
TICplot.show()"""

###############################################################################################
import pandas as pd
import matplotlib.pyplot as plt

# Data file from sensors - DAQfactory txt file
path2 = '/Users/ks826/Google Drive/Data_Analysis/Raw_data_files/GC_MS/'

cal_file = ['mos_data_081716_01.txt']
# This bit of code works out which folder the file is in from the name of the file.
for i in cal_file:
# Pick out characters 18 to 21 to correspond to the filename.
	f = "".join(path2)+i
#for f in filenames:
	print f
	#read file into dataframe
	data = pd.read_csv(f)
	

# 	convert daqfac time into real time pd.datetime object - so it gives time as we would expect, not as a random number.
	data.TheTime = pd.to_datetime(data.TheTime,unit='D')

	T1 = pd.datetime(1970,01,01,0)
	T2 = pd.datetime(1970,01,01,0)
	offset=T1-T2
	data.TheTime+=offset
# Ten second averaging of the raw data
# 	Time_avg = '0S'
# Make a new copy of the data called mean_resampled 
	mean_resampled = data.copy(deep=True)
	mean_resampled.TheTime = pd.to_datetime(mean_resampled.TheTime,unit='L')
#Set the index to be the time column, when you do this it drops the index, even though it is set to False.
	mean_resampled = mean_resampled.set_index(mean_resampled.TheTime,drop=False)
# 	mean_resampled = mean_resampled.resample(Time_avg, how='mean',fill_method='pad')
# Re-add the time index so that it can be plotted later
	Time = pd.Series(mean_resampled.index,name='Time', index=mean_resampled.index)
	mean_resampled = pd.concat([mean_resampled,Time],axis=1)	
# If there are more than files the data_concat function will join tem together.
	print 'mean_resampled shape = ',mean_resampled.shape
	try:
		data_concat = data_concat.append(mean_resampled)
		print ' concatenating'
	except NameError:
		data_concat = mean_resampled.copy(deep=True)
		print ' making data_concat'
		
# Re-make and re-set the index to be the time column for the data_concat dataframe.
T3 = pd.datetime(2015,01,01,0)
dt = pd.Series((data_concat.index - T3),index=data_concat.index,name='dt')
dt = dt.astype('int')
data_concat = pd.concat([data_concat,dt],axis=1,join_axes=[data_concat.index])
stat = 'Y'

newindex = pd.Series(range(0,data_concat.shape[0]))
data_concat = data_concat.set_index(newindex)

print data_concat.TheTime[0]
#read file into dataframe

# Turn the time into a number:
new_time = pd.to_datetime(data_concat.Time)

#plot up the MOS voltages
MOSfig = plt.figure("MOS data")
ax1 = MOSfig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Sensor_ave,color="green",linewidth=3)
ax1.set_ylabel("MOS voltage (V)")
ax1.set_xlabel("Time")


# plot an overall chart
compare = plt.figure("MOS vs MS data")
ax1 = compare.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(data_concat.Time, data_concat.Sensor_ave, color="green", linewidth =3)
ax2.plot(mydf.Date_and_time, mydf.TIC, color="skyblue")
ax2.plot(mydf3.Date_and_time, mydf3.TIC, color = "skyblue")
ax2.plot(mydf4.Date_and_time, mydf4.TIC, color = "skyblue")
# ax2.plot(mydf5.Date_and_time, mydf5.TIC, color = "skyblue")
#ax2.plot(mydf6.Date_and_time, mydf6.TIC, color = "teal")
#ax2.plot(mydf6.Date_and_time, mydf6.TIC, color = "blue")
#ax2.plot(mydf7.Date_and_time, mydf7.TIC, color = "skyblue")
ax1.set_xlabel("Time", size=20)
ax1.set_ylabel("MOS voltage (V)", size=20)
ax2.set_ylabel("TIC MS intensity", size=20)
ax1.tick_params(labelsize=18)
#plt.title( filename2, size = 20)
# 
# compare.show()
plt.show()
