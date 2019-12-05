#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:03:12 2019

@author: CarlosCardenas
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import graph_AM as AM
import graph_AL as AL

class Edge:
    def __init__(self, source, dest, weight=1):
        self.source = source
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.el = []
        self.vertices = vertices
        self.weighted = weighted
        self.directed = directed
        self.representation = 'EL'
    
    def insert_edge(self,source,dest,weight=1):

        if weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.el.append(Edge(source,dest,weight)) 

    def delete_edge(self,source,dest):
        
        for i in self.el:
            if i.source==source and i.dest==dest:
                self.el.remove(i)
    
    def display(self):
        print('[',end='')
        for i in self.el:
            print('('+str(i.source)+','+str(i.dest)+','+str(i.weight)+')',end='')
        print(']',end=' ')
        print('')
    
   
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
        return self
    
    def as_AM(self):
        
        matrix =  AM.Graph(self.vertices, self.weighted, self.directed)
        
        for i in self.el:
            matrix.insert_edge(i.source, i.dest, i.weight)
        return matrix
    
    def as_AL(self):
        
        adjlist =  AL.Graph(self.vertices, self.weighted, self.directed)

        for i in self.el:
            adjlist.insert_edge(i.source, i.dest, i.weight)
        return adjlist
    
    def BFS(self, s,end): 
  
        visited = [False] * (self.vertices)
        visited[s]=True
        queue = [[s]] 
        path=[s]
  
        while queue: 
  
            s = queue.pop(0)
            if s==end:
                return

  
           
            for i in self.el: 
                if visited[i.dest] == False: 
                    queue.append(i.dest)
                    visited[i.dest] = True
                    path.append(i.dest)
            print('From EL BFS')      
            return path
    
    def DFS(self, s, end):
        
        visited=[]
        
        print('From EL DFS')
        return self.DFS_(visited, s, end)
    
    def DFS_(self, visited, s, end):
        
        if s not in visited:
            
            if len(visited) > 0 and visited[-1]==end:
                return
            
            visited.append(s)

            for neighbour in self.el:
                self.DFS_(visited, neighbour.dest, end)
          
        return visited
    
    def path_steps(self, func):
        if func == 'DFS':
            search_path = self.DFS(0,self.vertices-1)
        if func == 'BFS':
            search_path = self.BFS(0,self.vertices-1)
        
        for i in search_path:
            print (i, [int(x) for x in list('{0:04b}'.format(i))]) 
