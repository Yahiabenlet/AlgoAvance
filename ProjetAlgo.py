

def validecorde(i,j):
    if (i==j+1) or (i==j-1) or (i==j):
        return False
    elif( T[i][j]==True):
        return False
    for l in range(i,j):
        for k in range(j+1,len(T[0])):
            if T[l][k]:
                return False
        for p in range(0,i):
            if T[l][p]:
                return False
    return True


