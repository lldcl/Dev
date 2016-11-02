# The Cal Ammender creates a dictionary of standard deviations of the same cal point translated left and right.
# It then finds the minimum of these standard deviations and uses that as the cal point.
# In this way it finds the 'flatest' part of the graph to take a data point from, as this will have the smallest stddev.
# It also uses the negative_remover function, that should be in the Useful Functions file with this.



from operator import itemgetter
import numpy as np



### Finds the cal points with the lowest standard deviations by shifting the points left and right slightly and checking the standard deviation
def cal_point_ammender(data_set,shifter,bad_cal_length,S,F):
    for i in xrange(0,len(S)):
        orig_std = np.nanstd(data_set[S[i]:F[i]])
        
        if orig_std > 0.5:
            S[i] = F[i] - bad_cal_length
        
        
        
        
        left_shift_stds = {}
        for k in xrange(1,20):
                x_shiftL = k*shifter
                left_shift_stds[k] = np.nanstd(data_set[S[i]-x_shiftL:F[i]-x_shiftL])
    
        dogel = [q for q in left_shift_stds if np.isnan(left_shift_stds[q])]
        for t in dogel:
                del(left_shift_stds[t])

                    
        minPairL = min(left_shift_stds.iteritems(), key=itemgetter(1))
        
        right_shift_stds = {}
        for k in xrange(1,20):
            x_shiftR = k*shifter
            right_shift_stds[k] = np.nanstd(data_set[S[i]+x_shiftR:F[i]+x_shiftR])
            
        dogeR = [q for q in right_shift_stds if np.isnan(right_shift_stds[q])]
        for t in dogeR:
            del(right_shift_stds[t])
            
        minPairR = min(right_shift_stds.iteritems(), key=itemgetter(1))
    
        if minPairL[1] < orig_std and minPairL[1] < minPairR[1]:
                list(S)[i] = S[i]-minPairL[0]*shifter
                list(F)[i] = F[i]-minPairL[0]*shifter
        elif minPairR[1] < orig_std and minPairR[1] < minPairL[1]:
            list(S)[i] = S[i]+minPairR[0]*shifter
            list(F)[i] = F[i]+minPairR[0]*shifter
    if S[0] < 0:
        SF = negative_remover(S,F)
        S = SF[0]
        F = SF[1]
        
    return S,F