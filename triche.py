# -*- coding: utf-8 -*-
"""
Ecrit par Clara j'espere que ca servira mdr


"""

"""
Bubble sort
"""

def bubbleSort(L):
    swap = True
    n = len(L)
    while swap:
        swap = False
        for i in range(n-1):
            if L[i] > L[i+1]:
                (L[i], L[i+1]) = (L[i+1], L[i])
                swap = True
        n -= 1
        
"""
Insertion sort
"""

def insert(x, L):
    '''
    insert(x, L) -> None -- insert x at its place in L sorted
    '''
    n = len(L)
    # search position
    i = 0
    while (i < n) and (x > L[i]):
        i += 1
    # shifts
    L.append(None)
    for j in range(n, i, -1):
        L[j] = L[j-1]
    # insertion
    L[i] = x

def insert2(x, L):
    '''
    search for place 
    and shifts at the same time
    '''
    i = len(L) - 1
    L.append(None)
    while (i >= 0) and (x < L[i]):
        L[i+1] = L[i]
        i -= 1
    L[i+1] = x

def insertSort(L):
    '''
    insertSort(L) -> new sorted list
    '''
    
    R = []
    for x in L:
        insert2(x, R)
    return R
    
'''
In place
'''

def __insert(x, L, n): 
    '''
    insert x at its position in L[0, n[ sorted (n < len(L))
    '''
    # search position
    i = 0
    while (i < n) and (x > L[i]):
        i += 1
    # shifts
    for j in range(n, i, -1):
        L[j] = L[j-1]
    # insertion
    L[i] = x

@timing.timing
def insertSort2(L):
    for i in range(1, len(L)):
        __insert(L[i], L, i)
    return L

# in one function: insert inlined
def insertSort3(L):
    for i in range(len(L)):
        x = L[i]
        j = i - 1
        while j >= 0 and x < L[j]:
            L[j + 1] = L[j]
            j -= 1
        L[j + 1] = x


"""
AVL

"""

from algopy import bintree

# BST -> list
def __bst2list(B, L):
    if B != None:
        __bst2list(B.left, L)
        L.append(B.key)
        __bst2list(B.right, L)
        

def bst2list(B):
    L = []
    __bst2list(B, L)
    return L


# list -> BST: warning, works only with **strictly** increasing lists!

def __list2bst(L, left, right):
    """
        build a balanced binary search trees with values in L [left, right[
    """    
    if left == right:
        return None
    else:
        mid = left +  (right - left) // 2
        B = bintree.BinTree(L[mid], None, None)
        B.left = __list2bst(L, left, mid)
        B.right = __list2bst(L, mid+1, right)
        return B
    
#or
def __list2bst2(L, left, right):
    if left == right:
        return None
    else:
        mid = left +  (right - left) // 2
        return bintree.BinTree(L[mid], 
                               __list2bst2(L, left, mid), 
                               __list2bst2(L, mid+1, right))

    
def list2bst(L):
    return __list2bst(L, 0, len(L))
    
    


# bonus: try to avoid the problem with not strictly increasing lists


###############################################################################

def nb_inter(B, a, b):
    """
    computes the number of values of the BST B in the interval [a, b[
    """
    if B == None:
        return 0
    elif B.key < a:
        return nb_inter(B.right, a, b)
    elif B.key >= b:
        return nb_inter(B.left, a, b)
    else:
        return 1 + nb_inter(B.left, a, b) + nb_inter(B.right, a, b)


##################################################################
#
#           CLASSICS

# Researches (dicho)

def minBST(B):
    """
    B != None
    """
    if B.left == None:
        return B.key
    else:
        return minBST(B.left)
    
def maxBST(B):
    """
    B != None
    """
    while B.right != None:
        B = B.right
    return B.key


def searchBST(B, x):
    if B == None or B.key == x:
        return B
    else:
        if x < B.key:
            return searchBST(B.left, x)
        else:
            return searchBST(B.right, x)

def searchBST_iter(B, x):
    while B != None and B.key != x:
        if x < B.key:
            B = B.left
        else:
            B = B.right
    return B

# insertions


def leaf_insert(B, x):
    if B == None:
        return bintree.BinTree(x, None, None)
    else:
        if x <= B.key:
            B.left = leaf_insert(B.left, x)
        else:
            B.right = leaf_insert(B.right, x)
        return B

def leaf_insert_iter(B, x):
    new = bintree.BinTree(x, None, None)
    P = None
    T = B
    while T != None:
        P = T
        if x <= T.key:
            T = T.left
        else:
            T = T.right
    
    if P == None:
        return new
    else:
        if x <= P.key:
            P.left = new
        else:
            P.right = new
        return B
    
"""
delete
"""



def del_bst(B, x):
    if B == None:
        return None
    else:
        if x == B.key:
            if B.left == None:
                return B.right
            elif B.right == None:
                return B.left
            else:
                B.key = maxBST(B.left)
                B.left = del_bst(B.left, B.key)
                return B
        else:
            if x < B.key:
                B.left = del_bst(B.left, x)
            else:
                B.right = del_bst(B.right, x)
            return B

# Optimization

def del_max_bst(B):
    """
    B != None
    """
    if B.right == None:
        return (B.left, B.key)
    else:
        (B.right, m) = del_max_bst(B.right)
        return (B, m)


def del_bst_opti(B, x):
    if B == None:
        return None
    else:
        if x == B.key:
            if B.left == None:
                return B.right
            elif B.right == None:
                return B.left
            else:
                (B.left, B.key) = del_max_bst(B.left)
                return B
        else:
            if x < B.key:
                B.left = del_bst_opti(B.left, x)
            else:
                B.right = del_bst_opti(B.right, x)
            return B


"""
root insertion
"""

def cut(B, x):
    if B == None:
        return (None, None)
    else:
        if B.key <= x:
            L = B
            (L.right , R) = cut(B.right, x)
        else:
            R = B
            (L, R.left) = cut(B.left, x)
        return (L, R)

def root_insertion(B, x):
    (L, R) = cut(B, x)
    return bintree.BinTree(x, L, R)
    

#dictionnaire

a = {} # ou a = dict()
a["nom"] = "Wayne"
a["prenom"] = "Bruce"
a
{'nom': 'Wayne', 'prenom': 'Bruce'}

#recup 
>>> data = {"name": "Wayne", "age": 45}
>>> data.get("name")
'Wayne'
>>> data.get("adresse", "Adresse inconnue")
'Adresse inconnue'

#si une clé est presente
>>> a.has_key("nom")
True
 
#sup
>>> del a["nom"]
>>> a
{'prenom': 'Bruce'}

>>> fiche = {"nom":"Wayne","prenom":"Bruce"}
>>> for cle,valeur in fiche.items():
...     print cle, valeur
... 
nom Wayne
prenom Bruce
