

def validecorde(i,j):
    if (i==j+1) or (i==j-1) or (i==j): #a verifier
        return False
    elif( T[i][j]==True):
        return False
    for l in range(i,j):
        for k in range(j+1,len(T[0])):  #on regarde les sommets entre j et la fin du tableau
            if T[l][k]:
                return False
        for p in range(0,i):    #on regarde les sommets entre le début du tableau et i
            if T[l][p]:
                return False
    return True

def Question3(n):
    E=[]
    T=[][]
    Triangul(T,n,E)
    return E



def Triangul(Te,n,E):
    T=Te
    if n<3:  #cas de base
        return T
    for l in range(n):     #triangulation de la question2
        for k in range(l+2,n):
            if validecorde(l,k):
                T[l][k]=True
                T[k][l]=True
        E.append(T)
        T=[][]




        #triangulation de la question3

    for i in range(n/2):
        for j in range(i):
            T[l][k]=False
    Triangul(T,i,E)









