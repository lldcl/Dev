# This Function will find where the difference between the setter indexes (S and F, they used to be called mfc_setS and mfc_setF) is extremely long.
# It then takes a specified number of extra cals from those lines.

#I don't use this function in the cal code.



# Cal Adder, this takes a specified extra amount of cals along the long flat sections.
S = [1000,5000,9000,14000,19000,26000]
F = [3000,7000,17000,21000,25000,35000]

def cal_adder(number_of_additions,S,F,tolerance_length,cal_length,cal_spacing):
    long_ones = [i for i in range(0,len(S)) if S[i] - S[i-1] > tolerance_length]
    
    for pt in range(0,(number_of_additions-1)):
        F = F + [F[i] for i in long_ones]
        S = S + [S[i] for i in long_ones]
        
    F.sort()
    S.sort()
    
    S_indexes = [i for i in range(0,len(S)) if S[i] == S[i-(number_of_additions-1)]]
    F_indexes = [i for i in range(0,len(F)) if F[i] == F[i-(number_of_additions-1)]]
    
    for i in F_indexes:
        for pt in range(0,number_of_additions):
            if pt >= 1:
                F[i-pt] = F[i-pt] - (pt*(cal_spacing) + (pt-1)*cal_length)
    
    for i in S_indexes:
        for pt in range(0,number_of_additions):
            if pt >= 1:
                S[i-pt] = S[i-pt] - (pt*(cal_spacing) + (pt-1)*cal_length)
    
        
    return S,F
    
    
print '\n\nExample:\n\n'    
    
SF = cal_adder(2,S,F,6999,200,150)

print S,'\n',F
print '\nHere I have chosen the long length at the end to add more cal points to (it has a length of more than 6999), it just took a cal with a specified length and spacing'
print '\n',SF[0],'\n',SF[1]