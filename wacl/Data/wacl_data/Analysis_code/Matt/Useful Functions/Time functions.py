import pandas as pd
import datetime as dt



############### Converts a timestamp to a list in the form, [year, month, week, day, hour, minute, second, millisecond] ############


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

##################### Converts a list of timestamps to a list of lists in the form given above ##################
def timelist_convert(data):    
    time_listA = []
    time_listL = []
    try:
        for i in data.Time:
            b = timestamp_convert(i)[3:6]
            time_listA.append(b)
        return time_listA
    
    except AttributeError:
            for i in data['TheTime']:
                b = timestamp_convert(i)[3:6]
                time_listL.append(b)
            return time_listL
      

    
    

print 'The year, month, day, hour, minute, second and where possible millisecond have been converted into list form, this is useful for comparing timestamps:\n', timestamp_convert(pd.Timestamp('2015-09-07 11:43:18.624000'))
print "\n\nThe different components of the timestamp can now easily be compared, e.g: The following 2 timestamps are out by 1 hour which can be found in the 4th index of the outputted list\n\nint(timestamp_convert(pd.Timestamp('2015-09-07 11:43:18.624000'))[3]) - int(timestamp_convert(pd.Timestamp('2015-09-07 12:43:18.624000'))[3]) = ", int(timestamp_convert(pd.Timestamp('2015-09-07 11:43:18.624000'))[3]) - int(timestamp_convert(pd.Timestamp('2015-09-07 12:43:18.624000'))[3])
print '\n\nThe timelist_convert does the same thing however this is for a whole list'