#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 23:05:13 2021

@author: cameronleong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 16:30:10 2021

@author: cameronleong
"""
import random
import numpy as np
import sys
import math as m

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
#print(dataset.target)
N = len(dataset.data)

# M is the number of attributes each sample has
M = len(dataset.data[0])

global c1,c2,c3                         #centers
c1 = c2 = c3 = np.zeros(M)
num = N                               #len(dataset.data)
global clusters
clusters = np.zeros(num)
prev_clusters = [-1 for a in range(num)]
best = np.zeros(num)
end_clusters = 3    #desired number of final clusters


def print_clusters(array):
    for i in range(end_clusters):
        txt = "Cluster #{cluster_num:}:"
        print(txt.format(cluster_num = i+1))
        for j in range(num):
            if array[j] == i+1:
                print(j)
def dist(a,center):         #calculates square of the distance between a point and the center
    temp = 0
    for i in range(M):
        temp += pow((dataset.data[a][i]-center[i]),2)
        return temp


def rand_centers():          #generates random points as centers and saves their attributes in c1,c2,c3
    global c1,c2,c3
    print("CENTER INDICES:")
    c1_idx,c2_idx,c3_idx = random.sample(range(0,num),3)
    print(c1_idx,c2_idx,c3_idx)
    c1 = dataset.data[c1_idx]
    c2 = dataset.data[c2_idx]
    c3 = dataset.data[c3_idx]
    print("CENTERS")
    print(c1)
    print(c2)
    print(c3)
    global c1_,c2_,c3_
    c1_,c2_,c3_ = c1,c2,c3
    return c1,c2,c3

def find_closest_center(a):
    global c1,c2,c3
    min = dist(a,c1)
    c = 1
    if dist(a,c2) < min:
        min = dist(a,c2)
        c = 2
    if dist(a,c3) < min:
        min = dist(a,c3)
        c = 3
    return c

def link_centers(): #join two closest points or clusters
    for i in range(num):
        c = find_closest_center(i)
        clusters[i] = c
    return

def recalculate_centers():
    global c1,c2,c3
    global clusters
    c1_sums = np.zeros(M)                       #to store the sums of the attributes for each cluster
    c2_sums = np.zeros(M)
    c3_sums = np.zeros(M)
    c1_size = c2_size = c3_size = 0
    for i in range(num):                        #sum the attributes in each cluster
        if clusters[i] == 1:                    #if in cluster 1, sum attributes of that point in c1_sums
            for j in range(M):
                c1_sums[j]+= dataset.data[i][j]
            c1_size += 1
        elif clusters[i] == 2:                  #if in cluster 2, sum attributes of that point in c2_sums
            for j in range(M):
                c2_sums[j]+= dataset.data[i][j]
            c2_size += 1
        else:                                   #if in cluster 3, sum attributes of that point in c3_sums
            for j in range(M):
                c3_sums[j]+= dataset.data[i][j]
            c3_size += 1
    for i in range(M):
        if c1_size !=0:                 #makes sure no divisions by 0
            c1_sums[i]/=c1_size         #gets averages for each attribute
        else:
            c1_sums[i] = 0
        if c2_size !=0:    
            c2_sums[i]/=c2_size
        else:
            c2_sums[i] = 0
        if c3_size !=0:
            c3_sums[i]/=c3_size
        else:
            c2_sums[i]=0
    for i in range(M):
        c1[i] = c1_sums[i]             #new centers
        c2[i] = c2_sums[i]
        c3[i] = c3_sums[i]
    return
        
def save_clusters():
    for i in range(len(clusters)):
        prev_clusters[i] = clusters[i]
    return

def is_change():
    for i in range(len(clusters)):
        if prev_clusters[i] != clusters[i]:
            return True
    return False


def kmeans():
    sum = 0
    for i in range(num):
        if clusters[i]== 1:
            sum += dist(i,c1)
        elif  clusters[i]==2:
            sum += dist(i,c2)
        else:
            sum += dist(i,c3)
    return sum

def save_best():
    global clusters
    global best
    for i in range(len(clusters)):
        best[i] = clusters[i]
    return

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


min_k = sys.maxsize
#main
for i in range(100):          #repeat the whole clustering process 100 times to find the best
    print("\nIteration:")
    print(i)
    c1,c2,c3 = rand_centers()   #create initial centers
    link_centers()              #cluster each point to its closest center
    prev_clusters[0]=-1         #change the previous clusters array so that it runs at least once
    while is_change() == True:  #keep clustering until no change between iterations
        print("recalculating centers...")
        recalculate_centers()   #calculate centers
        print("linking centers...")
        link_centers()          #cluster points to closest center
        print("saving clusters...")
        save_clusters()         #save clustering to check for change
    temp = kmeans()
    if temp < min_k:            #if the kmeans is better than the previous minimum, save the new data
        min_k = temp            #k will store the lowest kmeans cost
        save_best()
    

print("Best Clustering:")
print("Best Clustering:")
print_clusters(best)    #print best clusetering
print(best)
print("Best kmeans cost:")
print(min_k)     
print("Hamming distance:")
print(hamming(best,dataset.target))
    
