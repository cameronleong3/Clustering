#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 14:22:10 2021

@author: cameronleong
"""


import numpy as np
import math as m

#user selects which dataset to use
done = False
while done == False:
    choice = input("Which dataset: Iris (I) or Wine(W)?")
    if (choice == "I"):
        from sklearn.datasets import load_iris
        dataset = load_iris()
        done = True
    if (choice == "W"):
        from sklearn.datasets import load_wine
        dataset = load_wine()
        done = True
    print("Try again")

# N is number of data samples
print(dataset.target)
N,M = np.shape(dataset.data)
print("# of data samples:")
print(N)
print("# of attributes:")
print(M)

from math import sqrt
import sys           
num = N             #amount of data samples being tested 
num_clusters = num
end_clusters = 3
#the value in each index is the cluster which the point at that index belongs to
clusters = [a for a in range(num)] #every element starts in its own cluster
distances = [[0 for a in range(num)] for b in range(num)]
min = 0

#function to calculate distance between points
def dist(a,b):      #euclidean distance calculation
    temp = 0
    for i in range(M):
        temp += (dataset.data[a][i]-dataset.data[b][i])**2
        return sqrt(temp)


def find_closest(): #function to find the closest pair
    global clusters
    min = sys.maxsize
    for i in range(num):
        for j in range(i+1,num):
            temp = distances[i][j]
            if (temp < min) & (clusters[i]!=clusters[j]):   #distance between i and j is smaller than min and they aren't in the same cluster
                min = temp
                a = i
                b = j
    return(a,b)

def link(): #join two closest points or clusters
    a,b = find_closest()
    global clusters
    new = clusters[a]
    old = clusters[b]
    for i in range(num):
        if clusters[i] == old:
            clusters[i] = new
    txt = "joining points {a:} and {b:}..."
    print(txt.format(a=a,b=b))
    global num_clusters
    num_clusters -= 1
    return

def print_clusters():
    used = [-1 for a in range(end_clusters)]    #keep track of points already printed
    j = 0
    for i in range(end_clusters):
        txt = "Cluster #{cluster_num:}:"
        print(txt.format(cluster_num = i+1))
        clust_idx = clusters[0]
        while clusters[j] in used:              #finds next cluster not yet printed
            j+=1
        clust_idx = clusters[j]
        used[i] = clusters[j]
        for k in range(len(clusters)):
            if clusters[k]==clust_idx:
                print(k)
    
def hamming(array1,array2):
    a = 0
    b = 0
    for i in range(num):
        for j in range(i+1,num):
            if array1[i] == array1[j]:      #edge in array1
                if array2[i] != array2[j]:  #not an edge in array2
                    a+=1
            if array2[i] == array2[j]:      #edge in array2
                if array1[i] != array1[j]:  #not an edge in array1
                    b+=1
    return (a+b)/m.comb(len(array1),2)      #calculate (a+b)/(# of edges)
  
#Main
print("STARTING")
for i in range(num):
    for j in range(num):
        distances[i][j] = dist(i,j)         #calculate all distances
        
while num_clusters > end_clusters:          #repeatedly link until only 3 clusters
    link()
print_clusters()
#print(clusters)
print("hamming distance:")
print(hamming(clusters, dataset.target))
print("done")
        