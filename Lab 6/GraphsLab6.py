#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:03:12 2019

@author: CarlosCardenas
"""

import graph_AL as AL
import graph_AM as AM
import graph_EL as EL
import test_graphs as test
import time

print('1. Adjacency List')
print('2. Adjacency Matrix')
print('3. Edge List')

choice=int(input('Select Graph Representation: '))


print('\n1. Test Graphs')
print('2. Puzzle')

choice2=int(input('Select choice: '))

if choice2==1:
    
    test.tests(choice)
    
if choice2==2:
    
    if choice==1:
        g=AL.Graph(16)
    if choice==2:
        g=AM.Graph(16)
    if choice==3:
        g=EL.Graph(16)
    
    g.insert_edge(0,5)
    g.insert_edge(5,4)
    g.insert_edge(4,7)
    g.insert_edge(4,13)
    g.insert_edge(2,13)
    g.insert_edge(7,11)
    g.insert_edge(10,11)
    g.insert_edge(10,15)
    
    timer=0    
    
    print('\n1. Breadth First Search')
    print('2. Depth First Search')
    
    choice3=int(input('Select search function: '))
    
    if choice3==1:
        start = time.perf_counter()
        print(g.BFS(0,15))
        end = time.perf_counter()
        print('')
        g.path_steps('BFS')
        
    if choice3==2:
        start = time.perf_counter()
        print(g.DFS(0,15))
        end = time.perf_counter()
        print('')
        g.path_steps('DFS')
        
    timer += end - start
    print('\nSearch running time:', str(round(timer,6)), 'seconds')
    print('\n1. Drawing graph')
    g.draw()