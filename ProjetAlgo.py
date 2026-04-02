# ==============================
# Génération de polygone de test
# ==============================

import math
import random

def generer_polygone(n, rayon_min=50, rayon_max=150, seed=42):
    """
    Génère un polygone convexe irrégulier à n sommets.
    Méthode :
    - On génère des angles aléatoires dans [0, 2π]
    - On les trie pour garantir un ordre circulaire → convexité
    - On associe un rayon aléatoire à chaque angle pour obtenir une forme irrégulière
    Paramètres :
    - n : nombre de sommets
    - rayon_min, rayon_max : bornes du rayon
    - seed : pour reproductibilité
    Retour :
    - liste de points (x, y)
    """
    random.seed(seed)
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)], reverse=True)
    sommets = []
    for angle in angles:
        rayon = random.uniform(rayon_min, rayon_max)
        x = rayon * math.cos(angle)
        y = rayon * math.sin(angle)
        sommets.append((x, y))
    return sommets


def distance(p1, p2):
    """
    Calcule la distance euclidienne entre deux points.
    """
    return math.dist(p1, p2)

def generer_vecteur_C(sommets):
    """
    Génère l'ensemble des cordes possibles du polygone.
    Une corde est un segment reliant deux sommets non consécutifs.
    Retour :
    - liste de tuples (i, j, longueur)
    """
    n = len(sommets)
    cordes = []
    for i in range(n):
        for j in range(i + 2, n):
            # Exclusion de l’arête extérieure (0, n-1)
            if i == 0 and j == n - 1:
                continue
            longueur = distance(sommets[i], sommets[j])
            cordes.append((i, j, longueur))
    return cordes


# ==============================
# Initialisation
# ==============================

n = 13
sommets = generer_polygone(n)
cordes = generer_vecteur_C(sommets)
# Matrice booléenne des cordes
T = [[False] * n for _ in range(n)]


# ==============================
# Fonction validecorde
# ==============================

def validecorde(i, j):
    """
    Vérifie si la corde (i, j) peut être ajoutée sans créer d'intersection.
    Conditions :
    - i != j
    - pas une arête du polygone
    - la corde n'existe pas déjà
    - ne croise aucune corde existante dans T
    Retour :
    - True si valide, False sinon
    """
    # On force i < j pour simplifier les comparaisons
    if i > j:
        i, j = j, i
    # Cas interdits
    if i == j:
        return False
    if abs(i - j) == 1 or abs(i - j) == n - 1:
        return False  # sommets consécutifs
    if T[i][j]:
        return False  # corde déjà présente
    # Vérification des croisements
    for k in range(n):
        for l in range(k + 1, n):
            if T[k][l]:
                if k > l:
                    k, l = l, k
                # Ignorer si partage un sommet
                if k in (i, j) or l in (i, j):
                    continue
                # Cas de croisement
                if i < k < j and j < l:
                    return False
                if k < i < l and l < j:
                    return False
    return True


# ==============================
# Backtracking (essais successifs)
# ==============================

def triangulation_minimale(cordes, n):
    """
    Algorithme par essais successifs (backtracking).
    Principe :
    - Explorer toutes les combinaisons de cordes
    - Garder celles formant une triangulation valide
    - Minimiser la somme des longueurs
    Complexité :
    - O(n² * 2^(n²)) (exponentielle)
    """
    meilleur_poids = float("inf")
    meilleure_solution = []
    def backtracking(i, solution, poids_courant):
        nonlocal meilleur_poids, meilleure_solution
        # Condition d'arrêt : triangulation complète
        if len(solution) == n - 3:
            if poids_courant < meilleur_poids:
                meilleur_poids = poids_courant
                meilleure_solution = solution.copy()
            return
        # Fin des cordes
        if i == len(cordes):
            return
        # Cas 1 : ne pas prendre la corde
        backtracking(i + 1, solution, poids_courant)
        # Cas 2 : prendre la corde si valide
        (a, b, longueur) = cordes[i]
        if validecorde(a, b):
            T[a][b] = True
            T[b][a] = True
            solution.append(cordes[i])
            backtracking(i + 1, solution, poids_courant + longueur)
            # Backtrack
            solution.pop()
            T[a][b] = False
            T[b][a] = False
    backtracking(0, [], 0)
    return meilleure_solution, meilleur_poids

# ==============================
# Version optimisée (élagage)
# ==============================

def triangulation_minimale_opt(cordes, n):
    """
    Version optimisée avec élagage (branch and bound).
    Idée :
    - Si poids_courant >= meilleur_poids → on coupe la branche
    Gain :
    - accélère en pratique
    - mais complexité pire cas inchangée
    """
    meilleur_poids = float("inf")
    meilleure_solution = []
    def backtracking(i, solution, poids_courant):
        nonlocal meilleur_poids, meilleure_solution
        if len(solution) == n - 3:
            if poids_courant < meilleur_poids:
                meilleur_poids = poids_courant
                meilleure_solution = solution.copy()
            return
        if i == len(cordes):
            return
        # Élagage
        if poids_courant >= meilleur_poids:
            return
        backtracking(i + 1, solution, poids_courant)
        (a, b, longueur) = cordes[i]
        if validecorde(a, b):
            T[a][b] = True
            T[b][a] = True
            solution.append(cordes[i])
            backtracking(i + 1, solution, poids_courant + longueur)
            solution.pop()
            T[a][b] = False
            T[b][a] = False
    backtracking(0, [], 0)
    return meilleure_solution, meilleur_poids


# ==============================
# Programmation dynamique
# ==============================

def progDynamique(points):
    """
    Algorithme de triangulation minimale par programmation dynamique.
    Principe :
    - Décomposition en sous-polygones
    - Réutilisation des solutions intermédiaires
    Complexité :
    - Temps : O(n³)
    - Espace : O(n²)
    """
    n = len(points)
    T = [[0] * n for _ in range(n)]
    for longueur in range(3, n + 1):
        for i in range(n - longueur + 1):
            j = i + longueur - 1
            T[i][j] = float("inf")
            for k in range(i + 1, j):
                cout = 0
                if k != i + 1:
                    cout += distance(points[i], points[k])
                if k != j - 1:
                    cout += distance(points[k], points[j])
                T[i][j] = min(T[i][j], T[i][k] + T[k][j] + cout)
    return T[0][n - 1]


# ==============================
# Algorithme glouton
# ==============================

def algoGlouton(sommets):
    """
    Algorithme glouton pour la triangulation.
    Principe :
    - Ajouter à chaque étape la plus petite corde valide
    Limite :
    - Ne garantit PAS une solution optimale
    Complexité :
    - Temps : O(n⁴)
    - Espace : O(n²)
    """
    solution = []
    n = len(sommets)
    c = 0
    # Matrice des distances
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = distance(sommets[i], sommets[j])
    while c < n - 3:
        m = float("inf")
        meilleur = (-1, -1, -1)
        for i in range(n):
            for j in range(n):
                # Ignorer arêtes
                if i not in [(j - 1) % n, j, (j + 1) % n]:
                    # Pas déjà choisie
                    if ((i, j, C[i][j]) not in solution and
                        (j, i, C[j][i]) not in solution):
                        if C[i][j] < m and validecorde(i, j):
                            m = C[i][j]
                            meilleur = (i, j, m)
        a, b, _ = meilleur
        T[a][b] = True
        T[b][a] = True
        solution.append(meilleur)
        c += 1
    return solution