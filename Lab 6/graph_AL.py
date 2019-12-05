#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:03:12 2019

@author: CarlosCardenas
"""

# Adjacency list representation of graphs
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import graph_AM as AM
import graph_EL as EL

class Edge:
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.al = [[] for i in range(vertices)]
        self.weighted = weighted
        self.directed = directed
    
    def insert_edge(self,source,dest,weight=1):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        if weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.al[source].append(Edge(dest,weight)) 
            if not self.directed:
                self.al[dest].append(Edge(source,weight))
                
    def delete_edge_(self,source,dest):
        i = 0
        for edge in self.al[source]:
            if edge.dest == dest:
                self.al[source].pop(i)
                return True
            i+=1    
        return False
    
    def delete_edge(self,source,dest):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        else:
            deleted = self.delete_edge_(source,dest)
            if not self.directed:
                deleted = self.delete_edge_(dest,source)
        if not deleted:        
            print('Error, edge to delete not found')  
            
    def display(self):
        print('[',end='')
        for i in range(len(self.al)):
            print('[',end='')
            for edge in self.al[i]:
                print('('+str(edge.dest)+','+str(edge.weight)+')',end='')
            print(']',end=' ')    
        print(']')   
    def draw(self):

        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(self.al)):
            for edge in self.al[i]:
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
        
        edgelist = EL.Graph(len(self.al),self.weighted, self.directed)
        
        for i in range(len(self.al)):
            for j in self.al[i]:
                edgelist.insert_edge(i, j.dest, j.weight)
        return edgelist
    
    def as_AM(self):
        
        matrix =  AM.Graph(len(self.al), self.weighted, self.directed)
        
        for i in range(len(self.al)):
            for j in self.al[i]:
                matrix.insert_edge(i, j.dest, j.weight)
                
        return matrix
    
    def as_AL(self):
        return self
    
    def BFS(self, s,end): 
  
        visited = [False] * (len(self.al)) 
  
        queue = [[s]] 
  
        while queue: 
  
            s = queue.pop(0)
            
            if s[-1]==end:
                print('From AL BFS')
                return s

  
            for i in self.al[s[-1]]: 
                if visited[i.dest] == False: 
                    queue.append(s + [i.dest]) 
                    visited[i.dest] = True
    
    def DFS(self, s, end):
        visited=[]
        
        print('From AL DFS')
        return self.DFS_(visited, s, end)
    
    def DFS_(self, visited, s, end):
        
        if s not in visited:
  
            if len(visited) > 0 and visited[-1]==end:
                return
            visited.append(s)
            
   
            for neighbour in self.al[s]:
                self.DFS_(visited, neighbour.dest, end)
        
        return visited

    def path_steps(self, func):
        if func == 'DFS':
            search_path = self.DFS(0,len(self.al)-1)
        if func == 'BFS':
            search_path = self.BFS(0,len(self.al)-1)
        
        for i in search_path:
            print (i, [int(x) for x in list('{0:04b}'.format(i))]) 