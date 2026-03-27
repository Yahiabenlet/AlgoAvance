#Génération de polygone de test
import math

def generer_polygone(n, rayon=10):
    """
    Génère un polygone convexe à n sommets,
    placés régulièrement sur un cercle.
    """
    sommets = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = rayon * math.cos(angle)
        y = rayon * math.sin(angle)
        sommets.append((x, y))
    return sommets



def distance(p1, p2):
    return math.dist(p1, p2)

def generer_vecteur_C(sommets):
    """
    Génère le vecteur C :
    toutes les cordes possibles du polygone.
    Chaque corde est (i, j, longueur).
    """
    n = len(sommets)
    cordes = []

    for i in range(n):
        for j in range(i + 2, n):
            # Exclure l'arête (0, n-1)
            if i == 0 and j == n - 1:
                continue
            longueur = distance(sommets[i], sommets[j])
            cordes.append((i, j, longueur))

    return cordes




n = 12
sommets = generer_polygone(n)
cordes = generer_vecteur_C(sommets)
T = [[False]*n for _ in range(n)]

def validecorde(i, j):
    if i > j:
        i, j = j, i
    if i == j:
        return False
    if abs(i - j) == 1 or abs(i - j) == n-1:
        return False
    if T[i][j]:
        return False
    for k in range(n):
        for l in range(k+1, n):
            if T[k][l]:
                if k > l:
                    k, l = l, k
                if k in (i,j) or l in (i,j):
                    continue
                if i < k < j and j < l:
                    return False
                if k < i < l and l < j:
                    return False

    return True

def triangulation_minimale(cordes, n):
    meilleur_poids = float("inf")
    meilleure_solution = []
    def backtracking(i, solution, poids_courant):
        nonlocal meilleur_poids, meilleure_solution
        if len(solution) == n - 3:
            meilleur_poids = poids_courant
            meilleure_solution = solution.copy()
            return
        if i == len(cordes):
            return
        backtracking(i+1, solution, poids_courant)
        (a, b, longueur) = cordes[i]
        if validecorde(a, b):
            T[a][b] = True
            T[b][a] = True
            solution.append(cordes[i])
            backtracking(i+1,solution,poids_courant + longueur)
            solution.pop()
            T[a][b] = False
            T[b][a] = False
    backtracking(0, [], 0)
    return meilleure_solution, meilleur_poids

#O(2^n2⋅X n^2)


#Version élagage
def triangulation_minimale_opt(cordes, n):
    meilleur_poids = float("inf")
    meilleure_solution = []
    def backtracking(i, solution, poids_courant):
        nonlocal meilleur_poids, meilleure_solution
        if len(solution) == n - 3:
            meilleur_poids = poids_courant
            meilleure_solution = solution.copy()
            return
        if i == len(cordes):
            return
        if poids_courant >= meilleur_poids:
            return
        backtracking(i+1, solution, poids_courant)
        (a, b, longueur) = cordes[i]
        if validecorde(a, b):
            T[a][b] = True
            T[b][a] = True
            solution.append(cordes[i])
            backtracking(i+1,solution,poids_courant + longueur)
            solution.pop()
            T[a][b] = False
            T[b][a] = False
    backtracking(0, [], 0)
    return meilleure_solution, meilleur_poids

print(triangulation_minimale_opt(cordes,n))

#O(2^n2⋅X n^2)



def triangulation_minimale(points):
    n = len(points)
    T = [[0]*n for _ in range(n)]

    for longueur in range(3, n):
        for i in range(n - longueur):
            j = i + longueur - 1
            T[i][j] = int("inf")

            for k in range(i+1, j):
                cout = 0
                if k != i+1:
                    cout += distance(points[i], points[k])
                if k != j-1:
                    cout += distance(points[k], points[j])

                T[i][j] = min(T[i][j], T[i][k] + T[k][j] + cout)

    return T[0][n-1]


#O(n^3)





def algoGlouton(sommets):
    solution = []
    n = len(sommets)
    m = int("inf")
    c =0
    while c < n-3:
        for i in range(n):
            for j in range(n):
                if ((i==(j+2)%2)or(i==(j-2)%2)) and ((i,j,T[i][j]) not in solution):
                    m = min(m,T[i][j])
            solution.append((i,j,m))
            c+=1
    return solution

#O(n^4)
                    