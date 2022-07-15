# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 19:19:15 2022

@author: Alessandro
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np 
import pandas as pd
import os
import os.path
import sklearn as skl
import scipy 
import matplotlib.ticker as ticker
import seaborn as sns

from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans


#%%
# funzione che esegue il plot della ricostruzione della grigli 11x11 dopo la clusterizzazione
# cluster = variabile contenente il risultato del cluster
# directory = direcoty dove salvare il pdf del plot in formato pdf, esempio './CartellaPlot/Plot_S1_ricostruito'
# name = nome del capione analizzato, esempio S1
# color = colori da usare
# bounds = labels dei vari cluster esempio (-1 , 0 , 1 , 2 ,3), list di numeri

def ricostruzion_grid_cluster(cluster, directory, name, color, bounds):
    
    x = np.arange(1, 12, 1)
    y = np.arange(1, 12, 1)

    Z = np.empty( (11,11) )

    i = 0
    j = 0
    
    while i<len(cluster):
        Z[j,:] = cluster [i:i+11]
        i = i+11
        j = j+1
        
       
    
    cmap = ListedColormap( color )
    
    
    fig, ax = plt.subplots()

    ax.pcolormesh(x, y, Z, cmap =  cmap)
    
    ax.set_title("Ricostruzione campione "+ name +" dal cluster")
    ax.set_xlabel('posizione x ($\mu$m)')
    ax.set_ylabel('posizione y ($\mu$m)')
    ax.set_yticks(y)
    ax.set_xticks(x)
    ax.grid(which='minor', linestyle='-', linewidth=0.7, color = 'k')
    
    
    ncolors = len(color)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(bounds)

    
    
    plt.show()
    
    fig.savefig(directory+'.pdf');
    
#%%
# data = dati sui quali fare il cluster. Un pandas dataframe al quale è stata fatta una PCA
# directory =  directory nella quale salvare il plot del cluster e della mappa 11x11 ricostruita
# settings = parametri con cui eseguire il cluster DBSCAN, array 2D contenente [eps, min_samples] s.f.r documentazione DBSCAN
# nome = nome del dataset usato
# pca_plot = 'boolean' se True fa il plot 3D del claster nelle 3 Componenti Principali della PCA

def clustering(data, directory, settings, nome, pca_plot ):
    

    cluster = DBSCAN(eps= settings[0], min_samples = settings[1]).fit_predict(data)
    
    lista_cluster = sorted(set(cluster))
    lista_cluster.sort()
    num_cluster = len(lista_cluster)
    
    if num_cluster > 10:
        palette = sns.color_palette("tab20", num_cluster)
    else:
        palette = sns.color_palette("tab10", num_cluster)
            
            

    palette[0] = 'white'
    color = []


    for x in cluster:
        i = 0
        for k in lista_cluster:
            if (x == k):
                color.append(palette[i])
            i = i+1

    if pca_plot:
        
        fig = plt.figure();

        X = data[:,0]
        Y = data[:,1]
        Z = data[:,2]
    
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(X, Y, Z, c=color, marker='*')
        ax.grid(which='minor', linestyle=':', linewidth=0.5)
        ax.set_title("Cluster del dataset "+nome+" per 3 componenti principali")
        ax.minorticks_on()
        ax.set_ylabel('PC1')
        ax.set_xlabel('PC0')
        ax.set_zlabel('PC2')

        plt.show()



    ricostruzion_grid_cluster(cluster, directory, nome, palette, lista_cluster)
    
    
    
#%%
# Elbow method per valutare numero ottimale di cluster
# data = dati sui cui eseguire il plot
def plot_elbow_kmeans(data, name):
    
    distorsions = []
    for k in range(2, 20):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)
        distorsions.append(kmeans.inertia_)

    fig = plt.figure(figsize=(5, 5))
    plt.plot(range(2, 20), distorsions)
    plt.grid(True)
    plt.title('Elbow curve per '+'name')
    plt.set_xlabel('Numero di cluster')
    plt.set_ylabel('Sum within cluster distance')