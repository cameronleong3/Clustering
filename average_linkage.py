#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 14:22:10 2021

@author: cameronleong
"""
import numpy as np
import sys
import math as m


#allow user to choose which dataset to use
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


# N is number of data samples
# M is the number of attributes each sample has
print(dataset.target)
N,M = np.shape(dataset.data)
print("# of data samples:")
print(N)
print("# of attributes:")
print(M)

          
num = N                             #amount of data samples being tested 
num_clusters = num
end_clusters = 3
#the value in each index is the cluster which the point at that index belongs to
clusters = [a for a in range(num)]  #every element starts in its own cluster 
distances = [[0 for a in range(num)] for b in range(num)]
min = 0
from math import sqrt

def dist(a,b):      #euclidean distance calculation
    temp = 0
    for i in range(M):
        temp += (dataset.data[a][i]-dataset.data[b][i])**2
        return sqrt(temp)

def avg_dist(clust_a,clust_b):  #finds avg distance between two clusters, where clust_a and clust_b
    global clusters             #are indices of the clusters array
    sum = 0
    size = 0
    if clusters[clust_a] == clusters[clust_b]:          #in case points are from the same cluster
        return -1
    for i in range(len(clusters)):              
        if clusters[i]==clusters[clust_a]:              #finds all points in cluster a
            for j in range(len(clusters)):
                if clusters[j] == clusters[clust_b]:    #finds all points in cluster b
                    sum += distances[i][j]              #averages all distances between points in clusters a and b
                    size += 1
    avg = sum/size
    return avg
  
def find_closest(): #finds closest two clusters
    global clusters
    min = sys.maxsize
    used_1idx = 0
    used_1 = [-1 for i in range(num_clusters)]
    for i in range(len(clusters)):
        if clusters[i] not in used_1:                  #if distances for cluster not calculated yet
            used_1[used_1idx] = clusters[i]
            used_1idx += 1
            used_2 = [-1 for i in range(num_clusters)] #to save which distances have been calculated
            used_2idx =  0
            for j in range(i+1,len(clusters)):
                if (clusters[j] != clusters[i]) & (clusters[j] not in used_2):
                    used_2[used_2idx] = clusters[j]    #keep track of clusters already calculated
                    temp = avg_dist(i,j)
                    if (temp<min) & (temp > 0):        #if the clusters are the closest so far
                        min = temp
                        a = i
                        b = j
    return(a,b)#returns indices of two points whose clusters are the closest

def link(): #join two closest points or clusters
    a,b = find_closest()                #finds closest clusters
    global clusters
    global num_clusters
    new_cluster = clusters[a]           #all points will be joined to a's cluster
    b_cluster = clusters[b]
    for i in range(num):
        if clusters[i] == b_cluster:    #finds all elements in b's cluster
            clusters[i] = new_cluster   #assigns them to a's cluster 
    num_clusters -= 1
    print("number of clusters:")
    print(num_clusters)
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
    return (a+b)/m.comb(num,2)
    
 #Main

for i in range(num):
    for j in range(num):
        distances[i][j] = dist(i,j)     #calculate all distances once
    
while num_clusters > end_clusters:      #continue joining clusters until only 3
    link()
print(clusters)
print_clusters()
print("hamming distance:")
print(hamming(clusters, dataset.target))
print("done")

        