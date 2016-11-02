#################### Takes splices of a list at given indicies ######################

### E.G. list_multisplicer(range(0,100),range(0,100)[0:100:10],range(0,100)[5:100:10]) returns [0-5,10-15,20-25,30-35,etc...]

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








Examplel = list_multisplicer_listsout(range(0,100),[-10,30,40,50,60,80,100],[-5,35,45,47,55,65,85,105])
Example = list_multisplicer(range(0,100),range(0,100)[0:100:10],range(0,100)[5:100:10])

print '\nlist_multisplicer_listout = ', Examplel
print '\nlist_multisplicer = ',Example
print '\n\nThe listout multisplicer outputs the sections in lists inside one big list\n\nThe non listout one has all the values in one list'