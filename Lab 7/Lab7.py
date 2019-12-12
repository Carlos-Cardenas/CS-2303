# -*- coding: utf-8 -*-
"""
Created on Fri Dec 6 10:52:40 2019

@author: CarlosCardenas
"""

import numpy as np
import dsf
import graph_AL as AL
import graph_EL as EL
import random


def connected_components(g):
    vertices = len(g.al)
    components = vertices
    s = dsf.DSF(vertices)
    for v in range(vertices):
        for edge in g.al[v]:
            components -= s.union(v,edge.dest)
    return components


def in_degree(G, v):
	c = 0
	for i in range(len(G.al)):
		for j in G.al[i]:
			if j.dest == v:
				c = c + 1
	return c


def R_Hamiltonian(V, E):
    edge_list = V.as_EL()
    for i in range(E):
        Eh = random.sample(edge_list.el, len(V.al)) 
        # Creates an adjecenct list with the generated edges
        al = AL.Graph(len(V.al), weighted = V.weighted, directed = V.directed)
        for j in range(len(Eh)):
            al.insert_edge(Eh[j].source, Eh[j].dest)
        if connected_components(al) == 1:
            for i in range(len(al.al)):
                if in_degree(al, i) != 2:
                    return False
            return True
        
        
def test_RH(V,E):
    for i in range(100):
        if R_Hamiltonian(V,E) == True:
            return "graph is a Hamiltonian Cycle"
    return "graph is not a Hamiltonian Cycle"

# Recursive helper function
def Helper_BT(V, E):
	if len(V.el) == V.vertices:
		graphAL = V.as_AL()
        
		if connected_components(graphAL) == 1:
			for i in range(len(graphAL.al)):
				if in_degree(graphAL, i) != 2: 
					return None
			return graphAL
        
	if len(E) == 0:
		return
    
	else:
		V.el = V.el + [E[0]] 
		edges = Helper_BT(V,E[1:])
		if edges is not None:
			return edges
        
		V.el.remove(E[0])
		return Helper_BT(V, E[1:])


def BT(V):
    E = V.as_EL()
    el = EL.Graph(len(V.al), weighted=V.weighted, directed=V.directed)
    return Helper_BT(el,E.el)


def test_BT(V):
    h = BT(V)
    if isinstance(h, AL.Graph): #checks if object if of class
        h.display()
        return "is a Hamiltonian Cycle"
    else:
        return "is not a Hamiltonian Cycle"
    

#Original edit distance
def edit_distance(s1,s2):
    d = np.zeros((len(s1)+1,len(s2)+1),dtype=int)
    d[0,:] = np.arange(len(s2)+1)
    d[:,0] = np.arange(len(s1)+1)
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if s1[i-1] ==s2[j-1]:
                d[i,j] =d[i-1,j-1]
            else:
                n = [d[i,j-1],d[i-1,j-1],d[i-1,j]]
                d[i,j] = min(n)+1      
    return d[-1,-1]
        
#Modified edit distance
def Vowel_edit_distance(s1,s2):
    vowels = ['a','e','i','o','u'] #add a set with the vowels
    d = np.zeros((len(s1)+1,len(s2)+1),dtype=int)
    d[0,:] = np.arange(len(s2)+1)
    d[:,0] = np.arange(len(s1)+1)
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            
            if s1[i-1] == s2[j-1]:
                d[i,j] =d[i-1,j-1]    
                
            else:
                n = [d[i,j-1],d[i-1,j-1],d[i-1,j]] 
                if min(n) == d[i-1,j-1]: 
                    if (not s1[i-1] in vowels and s2[j-1] in vowels) or (s1[i-1] in vowels and not s2[j-1] in vowels):
                        n = [d[i,j-1],d[i-1,j]]
                d[i,j] = min(n)+1 
                
    return d[-1,-1] 
    


# Hamiltonian Cycle Graph
g1 = AL.Graph(5)
g1.insert_edge(0, 1)
g1.insert_edge(1, 3)
g1.insert_edge(1, 2)
g1.insert_edge(3, 4)
g1.insert_edge(2, 3)
g1.insert_edge(4, 0)
g1.draw()
# No Hamiltonian Cycle Graph
g2 = AL.Graph(5)
g2.insert_edge(0, 1)
g2.insert_edge(1, 3)
g2.insert_edge(1, 2)
g2.insert_edge(2, 3)
g2.insert_edge(4, 0)
g2.draw()

print("Graph 1", test_RH(g1, 100))
print("Graph 2", test_RH(g2, 100))
print()


# Hamiltonian Cycle Graph
g1 = AL.Graph(5)
g1.insert_edge(0, 1)
g1.insert_edge(1, 3)
g1.insert_edge(1, 2)
g1.insert_edge(3, 4)
g1.insert_edge(2, 3)
g1.insert_edge(4, 0)
g1.draw()
# No Hamiltonian Cycle Graph
g2 = AL.Graph(5)
g2.insert_edge(0, 1)
g2.insert_edge(1, 3)
g2.insert_edge(1, 2)
g2.insert_edge(2, 3)
g2.insert_edge(4, 0)
g2.draw()
    
print("Graph 1", test_BT(g1))
print("Graph 2", test_BT(g2))
print()

print("Original Edit Distance:")
print(edit_distance("sand","sound"))
print("Modified Edit Distance:")
print(Vowel_edit_distance("sand","sound"))
