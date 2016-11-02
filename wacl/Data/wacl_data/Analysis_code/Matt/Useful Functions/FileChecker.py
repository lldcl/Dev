import os
from time import strftime


####### Checks if the files exsist and returns a list of files that do exist
def FileChecker(path,month1, month2, day1,day2,number_of_files,file_size_limit):
    filesl=[]
    pfl = []
    month_now = strftime('%m')
    month_now = int(month_now)
    
    month2 = month2+1

    day2 = day2+1
    
    if month1 < 7:
        month1 = 7
    if month2 > 12:
        month2 = 12
    if month2 > month_now:
        month2 = month_now+1
    if day1 < 0:
        day1 = 0
    if day2 > 31:
        day2 = 31
    print path
    for month in range(month1, month2):
        if month < 10:
            month = '0'+str(month)
        path1 = path + '\\2015'+str(month)+'\\d2015'+str(month)
        for day in range (day1,day2):
            if day < 10:
                day = '0'+str(day)
            path2 = path1 + str(day)
            for filenumber in range(0,number_of_files):
                pfl.append(path2+'_0'+str(filenumber))
                
    filesl = []
    for i in pfl:
        if os.path.exists(i):
            if os.path.getsize(i) < file_size_limit: 
                filesl.append(i)
      

            
    return filesl
    
    
    
#### Example #####



filesla = FileChecker('C:\\Users\\mat_e_000\\Google Drive\\Bursary\\Data_Analysis\\RH_tests\Raw_Data\\201509\\Humidity Cals',9,9,10,17,8,25386763L)
# Checks for files 0-15 between 09/07 and 09/09