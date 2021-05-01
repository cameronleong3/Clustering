import numpy as np
import sys
import math as m
import random
from math import sqrt

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
N,M = np.shape(dataset.data)
print("# of data samples:")
print(N)
print("# of attributes:")
print(M)
global c1,c2,c3
c1 = [0 for i in range(M)]
c2 = [0 for i in range(M)]
c3 = [0 for i in range(M)]
k = 3          
num = 150                           #amount of data samples being tested 
num_clusters = num
end_clusters = 3
#the value in each index is the cluster which the point at that index belongs to
clusters = [a for a in range(num)]  #every element starts in its own cluster 
prev_clusters = [-1 for a in range(num)]
distances = [[0 for a in range(num)] for b in range(num)]
global centers
centers = [-1 for a in range(k)]
min = 0

size = 3 #number of clusters


def dist(a,b):      #euclidean distance calculation
    temp = 0
    for i in range(M):
        temp += (dataset.data[a][i]-dataset.data[b][i])**2
        return sqrt(temp)
  
def dist2(a,c):         #calculates the distance between a point and the center
   temp = 0
   for i in range(M):
       temp += pow((dataset.data[a][i]-c[i]),2)
       return sqrt(temp)
def closest_center2(a):     #returns cluster # of closest center
    min = dist2(a,c1)
    c = 1
    temp = dist2(a,c2)
    if temp < min:
        min = temp 
        c = 2
    temp = dist2(a,c3)
    if temp < min:
        min = temp
        c = 3
    return c

def link_centers():
    for i in range(num):
        c = closest_center2(i)
        clusters[i] = c #clusters each point with closest center

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

def is_change():
    for i in range(len(clusters)):
        if prev_clusters[i] != clusters[i]:
            return True
    return False

def save_clusters():
    for i in range(len(clusters)):
        prev_clusters[i] = clusters[i]
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

def print_clusters(array):
    for i in range(end_clusters):
        txt = "Cluster #{cluster_num:}:"
        print(txt.format(cluster_num = i+1))
        for j in range(num):
            if array[j] == i+1:
                print(j)

def kmeans():
    sum = 0
    for i in range(num):
        if prev_clusters[i]== 1:
            sum += (dist2(i,c1))**2
        elif  prev_clusters[i]==2:
            sum += (dist2(i,c2))**2
        else:
            sum += (dist2(i,c3))**2
    return sum





#choose random initial center
c_idx = random.randint(0,N)     #random first center, index of point in dataset
centers[0] = c_idx           #add c to list of centers
counter = 1
data_points = [a for a in range(num)]
for j in range(size-1):        #since we need to find size-1 more centers
    weights = []
    for i in range(num):
        c_idx = closest_center2(i)
        temp = dist(i,c_idx)
        weights.append(temp)
    new_center = random.choices(data_points,weights)    #weighted choice for new center
    centers[counter] = new_center[0]                        #appends new point to centers array
    counter += 1

for i in range(M):
    c1[i] = dataset.data[centers[0]][i] #saves centers chosen previously
    c2[i] = dataset.data[centers[1]][i]
    c3[i] = dataset.data[centers[2]][i]
print("\n\nCenters:")
print(c1,c2,c3)
link_centers()
prev_clusters[0]=-5         #change the previous clusters array so that it runs at least once
print("\n\nBeginning Kmeans...")
while is_change() == True:  #keep clustering until no change between iterations
    print("recalculating centers...")
    recalculate_centers()   #calculate centers
    print("linking centers...")
    link_centers()          #cluster points to closest center
    print("saving clusters...")
    save_clusters()         #save clustering to check for change
print("Clustering:")
print_clusters(clusters)    #print best clusetering
print("kmeans cost:")
print(kmeans())     
print("Hamming distance:")
print(hamming(clusters,dataset.target))
print(clusters)
        

    
        
    
    