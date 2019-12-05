#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:03:12 2019

@author: CarlosCardenas
"""

# Adjacency matrix representation of graphs
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
    
    # Insert edge function that adds an edge given its source, destination and weight    
    def insert_edge(self,source,dest,weight=1):
        
        # check parameters are valid
        if source >= len(self.am) or dest>=len(self.am) or source <0 or dest<0:
            print('Error, vertex number out of range')   
        elif weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            # check if not directed
            if not self.directed:
                # insert weight to both valid positons for undirected
                self.am[source][dest]=weight
                self.am[dest][source]=weight
                
                # otherwise, graph is directed and must only be inserted one way
            else:
                self.am[source][dest]=weight
        return
    
    # Delete edge function that deletes an edge given its source and destination
    def delete_edge(self,source,dest):
        
        # check if parameters are valid
        if source >= len(self.am) or dest>=len(self.am) or source <0 or dest<0:
            print('Error, vertex number out of range')
        else:
            # check if directed or undirected
            if not self.directed:
                # if undirected, delete or subsitute to -1 both positions
                self.am[source][dest]=-1
                self.am[dest][source]=-1
                # otherwise for directed, only one position is deleted
            else:
                self.am[source][dest]=-1
        return 
    
    # Display function to print the entire adjacency matrix edges       
    def display(self):
        print(self.am)
        print()
    
    # Draw function that converts the current graph to an adjacency list then draws
    # the graph (as per lab instructions)
    def draw(self):
        
        # converts current graph to an adjacency list to be used for the function
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
    
    # as_EL converts current adjacency matrix graph to an edge list
    def as_EL(self):
        
        # create an empty graph with the same length as current graph
        edgelist=EL.Graph(len(self.am), self.weighted, self.directed)
        
        # insert edges using a nested loop
        for row in range(len(self.am)):
            for col in range(len(self.am[row])):
                if self.am[row][col]!=-1:
                    edgelist.insert_edge(row,col,self.am[row][col])
        return edgelist

    # as_AL converts current adjacency matrix graph to an adjacency list
    def as_AL(self):
        
        # create an empty graph with the same length as current graph
        adjlist=AL.Graph(len(self.am), self.weighted, self.directed)
        
        # insert edges using a nested loop
        for row in range(len(self.am)):
            for col in range(len(self.am[row])):
                if self.am[row][col]!=-1:
                    adjlist.insert_edge(row,col,self.am[row][col])
        return adjlist
    
    def as_AM(self):
        return self
    
    # Breadth first search function used to return path
    def BFS(self, s,end): 
  
        # Mark all the vertices as not visited 
        visited = [False] * (len(self.am)) 
  
        # Create a queue for BFS 
        queue = [[s]]
        while queue: 
  
            # pop element from queue and assign it to s
            s = queue.pop(0) 
            # if end is found, return
            if s==end:
                return

  
            # Get all adjacent vertices of the 
            # popped vertex s. If a adjacent 
            # has not been visited, then mark it 
            # visited and append it 
            for i in range(len(self.am[s[-1]])): 
                if self.am[s[-1]][i] != -1 and visited[i]==False:
                    queue.append(s+[i]) 
                    visited[i] = True
        print('From AM BFS')
        return s
    
    # Depth first search function used to return path 
    def DFS(self, s, end):
        
        # start an empty list of visited elements
        visited=[]
        
        # call DFS helper function
        print('From AM DFS')
        return self.DFS_(visited, s, end)
    
    # Depth first search helper function used to return path
    def DFS_(self, visited, s, end):
        
        # check if s is in the visited list
        if s not in visited:
            
            # check if visited is not empty and if the last element of
            # visited is the end element
            if len(visited) > 0 and visited[-1]==end:
                return 'in AM DFS'
            
            # append s to visited list
            visited.append(s)

            # call function recursively with the starting element as the
            # destination of the neighbours of s
            for i in range(len(self.am[s])):
                if self.am[s][i] != -1:
                    self.DFS_(visited, i, end)      
        return visited
    
    # Function to print the path in the correct format as shown in the lab
    # instructions [b0,b1,b2,b3]
    def path_steps(self, func):
        if func == 'DFS':
            search_path = self.DFS(0,len(self.am)-1)
        if func == 'BFS':
            search_path = self.BFS(0,len(self.am)-1)
        
        for i in search_path:
            print (i, [int(x) for x in list('{0:04b}'.format(i))])