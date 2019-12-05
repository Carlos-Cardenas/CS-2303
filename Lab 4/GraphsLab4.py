#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:35:32 2019

@author: CarlosCardenas
"""

import numpy as np 
import time  


# B Tree

class BTree(object):
    # Constructor
    def __init__(self,data,child=[],isLeaf=True,max_data=5):  
        self.data = data
        self.child = child 
        self.isLeaf = isLeaf
        if max_data <3: #max_data must be odd and greater or equal to 3
            max_data = 3
        if max_data%2 == 0: #max_data must be odd and greater or equal to 3
            max_data +=1
        self.max_data = max_data
    
def FindChild(T,k):
    
    for i in range(len(T.data)):
        
        if k.word < T.data[i].word:
            return i
    return len(T.data)

def Split(T):
    mid = T.max_data//2
    if T.isLeaf:
        leftChild = BTree(T.data[:mid],max_data=T.max_data) 
        rightChild = BTree(T.data[mid+1:],max_data=T.max_data) 
    else:
        leftChild = BTree(T.data[:mid],T.child[:mid+1],T.isLeaf,max_data=T.max_data) 
        rightChild = BTree(T.data[mid+1:],T.child[mid+1:],T.isLeaf,max_data=T.max_data) 
    return T.data[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    
    T.data.append(i) 
    
    T.data.sort(key = lambda x: x.word) 

def IsFull(T):
    return len(T.data) >= T.max_data

def InsertInternal(T,word_object):
    if T.isLeaf:
        InsertLeaf(T,word_object)
    else:
        k = FindChild(T,word_object)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.data.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,word_object)  
        InsertInternal(T.child[k],word_object)   
 
def Insert(T,i):
     
    if not IsFull(T):
        InsertInternal(T,i)

    else:
        m, l, r = Split(T)
        T.data =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i) 

def PrintD(T,space):
    if T.isLeaf:
        for i in range(len(T.data)-1,-1,-1):
            print(space,T.data[i].word)
           
    else:
        PrintD(T.child[len(T.data)],space+'   ')  
        for i in range(len(T.data)-1,-1,-1):
            print(space,T.data[i].word)
            PrintD(T.child[i],space+'   ')
            
def NumItems(T):
    
    sum = len(T.data)
    for i in T.child:
        sum+=NumItems(i)
        
    return sum 

def Search(T,k): 
    
    for i in range(len(T.data)):
        
        if k.word == T.data[i].word:
           
            return T.data[i]
    if T.isLeaf: 
        return None
    
    return Search(T.child[FindChild(T,k)],k) 
            
def Height(T):
    if T.isLeaf:
        return 0
    return 1 + Height(T.child[0])    


#   Binary Search Tree
    
class BST(object):
    def __init__(self, data, left=None, right=None):  
        self.data = data
        self.left = left 
        self.right = right  

def InsertBinary(T,newItem):
   
    if T == None:
        
        T =  BST(newItem)
    elif T.data.word > newItem.word: 
        
        T.left = InsertBinary(T.left,newItem)
    else:
        T.right = InsertBinary(T.right,newItem)
    return T

def height(T): 
    
    if T == None:
        return -1
    l = height(T.left)
    r = height(T.right)
    
    return 1 + max([l,r])

def items(T):
    
    if T == None:
        return 0 
     
    leftNum = items(T.left)
    rightNum = items(T.right) 
    
    return 1 + sum([leftNum,rightNum])

def SearchBST(T,k): 
        
    if T == None or T.data.word == k: 
        return T 
    elif k < T.data.word:
        return SearchBST(T.left,k)    
    else: 
        return SearchBST(T.right,k)
       

class WordEmbedding(object): 
    def __init__(self,word,embedding=[]): 
        # word must be a string, embedding can be a list or and array of ints or floats 
        self.word = word 
        self.emb = np.array(embedding, dtype=np.float32) 
        # For Lab 4, len(embedding=50)

if __name__ == "__main__":    

    menu = 0
 
    
    while menu <= 2: 
        
           
        print("1. Binary Search Tree")
        print("2. B-Tree")
        print("3. Exit")
        
        menu = int(input("Choose table implementation\n"))
        print()
        
        # B Tree
        
        if menu == 1:
            
            
            print("Building Binary Search Tree")
            
            BinaryST = None 
            
            with open("glove.6B.50d.txt", 'r', encoding='utf-8') as file: 
            
                start = time.time()
                
                for line in file: 
                    binary_list = line.split(" ")
                    
                    word_object = WordEmbedding(binary_list[0],binary_list[1:])
                    
                    BinaryST = InsertBinary(BinaryST,word_object)
                    
            end = time.time()
            
            print("Binary Search Tree stats:")
            print("Number of nodes",items(BinaryST),"\n")
            print("Height:", height(BinaryST))
            print("Running time for Binary Search Tree construction:", end-start)
            
            print("Reading word file to determine similarities")
            
            
            
            with open("wordpairs.txt","r") as file2: 
                start2 = time.time()
                print("Word similarities found:")

                for line2 in file2: 
                    #splits lines
                    listBST = line2.split(" ") 
                    
                    #removes extra space from words
                    listBST[1]=listBST[1].strip()
                    
                
                     
                    word1 = SearchBST(BinaryST,listBST[0])  
                    word2 = SearchBST(BinaryST,listBST[1])
                    
                    
                    #cosine distance calculation
                    cosine_distance = np.dot(word1.data.emb,word2.data.emb)/(abs(np.linalg.norm(word1.data.emb))*abs(np.linalg.norm(word2.data.emb))) 
                    
                    print("Similarity [", word1.data.word,",", word2.data.word, "] =",'%.4f'%cosine_distance)
         
                    
            end2 = time.time()
            print("\nTime taken to compute similarities", end2-start2,"\n") 

        # Binary Search Tree
                    
        if menu == 2:
            

     
            user_max_keys = int(input("Enter max keys in B Tree:\n "))
            
            
            print()
            print("Building B-Tree")

            
            
            T = BTree([], max_data = user_max_keys)
            
            with open("glove.6B.50d.txt", 'r', encoding='utf-8') as file: 
             
                start = time.time()
                    
                for line in file: 
                    list1 = line.split(" ")
                        
                    word_object = WordEmbedding(list1[0],list1[1:])
                    
                    Insert(T,word_object)
                    
            end = time.time()
            print("Running time for B-Tree construction (with max_items = ",user_max_keys, ") = " , end-start)
            print("Height:", Height(T))
            print("Number of Items",NumItems(T),"\n") 
           
            
            with open("wordpairs.txt","r") as file2:
                
                start2 = time.time()
                print("Word similarities found:")

                for line in file2: 
                    
                    line = line.strip().split(" ")
        
                    firstW = WordEmbedding(line[0])
                    secondW = WordEmbedding(line[1])  
                    
                    word1 = Search(T,firstW) 
                    word2 = Search(T,secondW) 
                    
                    
                    cosine_distance = np.dot(word1.emb,word2.emb)/(abs(np.linalg.norm(word1.emb))*abs(np.linalg.norm(word2.emb))) 
                    
                    print("Similarity [",word1.word,",",word2.word, "] =",'%.4f'%cosine_distance)
    
            end2 = time.time()
            print("\nTime taken to compute similarities", end2-start2,"\n") 
            
            
        if menu > 2:
            print("Bye!")
            
            