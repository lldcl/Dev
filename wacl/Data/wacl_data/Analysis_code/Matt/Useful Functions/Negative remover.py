import numpy as np

### Removes negative first indexes from 2 lists (I use it for the selection indexes (mfc_setS and mfc_setF)) if they have negative indicies (off the graph)


def negative_remover(list1,list2):

    if list1[0] < 0:
        negative_removerS = [i for i in xrange(0,len(list1)) if list1[i]<0]
        negative_removerF = [i for i in xrange(0,len(list2)) if list2[i]<0]

        if negative_removerF < negative_removerS:
            negative_removerF = max(negative_removerS)
            negative_removerS = max(negative_removerS)+1         
        
            A = [0] + list1[negative_removerS:]
            B = list2[negative_removerF:]
        else:
            A = list1[max(negative_removerS)+1:]
            B = list2[max(negative_removerF)+1:]
        
        if len(A)<len(list1):
            A = list(np.zeros(len(list1)-len(A)))+A
        if len(B)<len(list2):
            B = list(np.zeros(len(list2)-len(B)))+B
        return A,B
        
        
    else:
        return list1,list2
        
        
 
Frank = [200,1700,3700,5199,7199,8699,10698,12197,14196,15696,17696,19195,21195,22695,24694,26194,28194,29693,30693,32192,34192,90637]

Sam = [i-300 for i in Frank]



x = negative_remover([1,2,3,4],[3,4,5,6])
y = negative_remover(Sam,Frank)
z = negative_remover([-4,-3,-2,9,10],[-1,0,1,12,13])

print '\n\n\n[1,2,3,4]\n[3,4,5,6]\n\nNo numbers have been removed here as they are all positive:\n\n',x[0],'\n',x[1]

print '\n\n\n\n\n',Sam,'\n\n',Frank
print '\n\nHere the first values in Sam and Frank have been removed as Sam has a negative first index, even though Frank doesn\'t:\n\n',y[0],'\n\n',y[1],'\n\n'


print '\n\n\n[-4,-3,-2,9,10]\n[-1,0,1,12,13]\n\nHere there is a bigger difference than one in the index for the negative number, in this case the last negative number in list1 becomes zero:\n\n',z[0],'\n',z[1]