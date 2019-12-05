#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 19:03:12 2019

@author: CarlosCardenas
"""

import matplotlib.pyplot as plt
import graph_AL as AL_test
import graph_AM as AM_test # Replace line 3 by this one to demonstrate adjacy maxtrix implementation
import graph_EL as EL_test # Replace line 3 by this one to demonstrate edge list implementation

def tests(choice):  
    
    plt.close("all")   
    
    if choice == 1:
        impl=AL_test
        print('\nYou selected Adjacency List\n')
    if choice == 2:
        impl=AM_test
        print('\nYou selected Adjacency Matrix\n')
    if choice == 3:
        impl=EL_test
        print('\nYou selected Edge List\n')
        
    g = impl.Graph(6)
    g.insert_edge(0,1)
    g.insert_edge(0,2)
    g.insert_edge(1,2)
    g.insert_edge(2,3)
    g.insert_edge(3,4)
    g.insert_edge(4,1)
    print("Graph 1")
    g.display()
    g.delete_edge(1,2)
    print("After deletion:")
    g.display()
    g.draw()
    
    
    g = impl.Graph(6,directed = True)
    g.insert_edge(0,1)
    g.insert_edge(0,2)
    g.insert_edge(1,2)
    g.insert_edge(2,3)
    g.insert_edge(3,4)
    g.insert_edge(4,1)
    print("Graph 2")
    g.display()
    g.draw()
    g.delete_edge(1,2)
    print("After deletion:")
    g.display()
    g.draw()
    
    g = impl.Graph(6,weighted=True)
    g.insert_edge(0,1,4)
    g.insert_edge(0,2,3)
    g.insert_edge(1,2,2)
    g.insert_edge(2,3,1)
    g.insert_edge(3,4,5)
    g.insert_edge(4,1,4)
    print("Graph 3")
    g.display()
    g.draw()
    g.delete_edge(1,2)
    print("After deletion:")
    g.display()
    g.draw()
    
    g = impl.Graph(6,weighted=True,directed = True)
    g.insert_edge(0,1,4)
    g.insert_edge(0,2,3)
    g.insert_edge(1,2,2)
    g.insert_edge(2,3,1)
    g.insert_edge(3,4,5)
    g.insert_edge(4,1,4)
    print("Graph 4")
    g.display()
    g.draw()
    g.delete_edge(1,2)
    print("After deletion:")
    g.display()
    g.draw()
    
    print('\nas_AL')
    g1=g.as_AL()
    g1.draw()
    g1.display()
    
    print('\nas_AM')
    g2=g.as_AM()
    g2.draw()
    g2.display()
    
    print('\nas_EL')
    g3=g.as_EL()
    g3.draw()
    g3.display()
    