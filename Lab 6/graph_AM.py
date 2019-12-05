#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:03:12 2019

@author: CarlosCardenas
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import graph_AL as AL
import graph_EL as EL

class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.am = np.zeros((vertices,vertices),dtype=int)-1
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AM'
    
    def insert_edge(self,source,dest,weight=1):
        
        if source >= len(self.am) or dest>=len(self.am) or source <0 or dest<0:
            print('Error, vertex number out of range')   
        elif weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            if not self.directed:
                self.am[source][dest]=weight
                self.am[dest][source]=weight
                
            else:
                self.am[source][dest]=weight
        return
    
    def delete_edge(self,source,dest):
        
        if source >= len(self.am) or dest>=len(self.am) or source <0 or dest<0:
            print('Error, vertex number out of range')
        else:
            if not self.directed:
                self.am[source][dest]=-1
                self.am[dest][source]=-1
            else:
                self.am[source][dest]=-1
        return 
    
    def display(self):
        print(self.am)
        print()
    

    def draw(self):
        
        adjlist = self.as_AL()
        
        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(adjlist.al)):
            for edge in adjlist.al[i]:
                d,w = edge.dest, edge.weight
                if self.directed or d>i:
                    x = np.linspace(i*scale,d*scale)
                    x0 = np.linspace(i*scale,d*scale,num=5)
                    diff = np.abs(d-i)
                    if diff == 1:
                        y0 = [0,0,0,0,0]
                    else:
                        y0 = [0,-6*diff,-8*diff,-6*diff,0]
                    f = interp1d(x0, y0, kind='cubic')
                    y = f(x)
                    s = np.sign(i-d)
                    ax.plot(x,s*y,linewidth=1,color='k')
                    if self.directed:
                        xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                        yd = [y0[2]-1,y0[2],y0[2]+1]
                        yd = [y*s for y in yd]
                        ax.plot(xd,yd,linewidth=1,color='k')
                    if self.weighted:
                        xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                        yd = [y0[2]-1,y0[2],y0[2]+1]
                        yd = [y*s for y in yd]
                        ax.text(xd[2]-s*2,yd[2]+3*s, str(w), size=12,ha="center", va="center")
            ax.plot([i*scale,i*scale],[0,0],linewidth=1,color='k')        
            ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
             bbox=dict(facecolor='w',boxstyle="circle"))
        ax.axis('off') 
        ax.set_aspect(1.0) 
    
    def as_EL(self):
        
        edgelist=EL.Graph(len(self.am), self.weighted, self.directed)
        
        for row in range(len(self.am)):
            for col in range(len(self.am[row])):
                if self.am[row][col]!=-1:
                    edgelist.insert_edge(row,col,self.am[row][col])
        return edgelist

    def as_AL(self):
        
        adjlist=AL.Graph(len(self.am), self.weighted, self.directed)
        
        for row in range(len(self.am)):
            for col in range(len(self.am[row])):
                if self.am[row][col]!=-1:
                    adjlist.insert_edge(row,col,self.am[row][col])
        return adjlist
    
    def as_AM(self):
        return self
    
    def BFS(self, s,end): 
  
        visited = [False] * (len(self.am)) 
  
        queue = [[s]]
        while queue: 
  
            s = queue.pop(0) 
            if s==end:
                return


            for i in range(len(self.am[s[-1]])): 
                if self.am[s[-1]][i] != -1 and visited[i]==False:
                    queue.append(s+[i]) 
                    visited[i] = True
        print('From AM BFS')
        return s
    
    def DFS(self, s, end):
        
        visited=[]
        
        print('From AM DFS')
        return self.DFS_(visited, s, end)
    
    def DFS_(self, visited, s, end):
        
        if s not in visited:
    
            if len(visited) > 0 and visited[-1]==end:
                return 'in AM DFS'
            
            visited.append(s)

            for i in range(len(self.am[s])):
                if self.am[s][i] != -1:
                    self.DFS_(visited, i, end)      
        return visited
    
  
    def path_steps(self, func):
        if func == 'DFS':
            search_path = self.DFS(0,len(self.am)-1)
        if func == 'BFS':
            search_path = self.BFS(0,len(self.am)-1)
        
        for i in search_path:
            print (i, [int(x) for x in list('{0:04b}'.format(i))])
