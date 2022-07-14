# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 19:19:15 2022

@author: Alessandro
"""
import pandas as pd
import os
import os.path
import matplotlib.pyplot as plt
import sklearn as skl
import numpy as np
import scipy 

from matplotlib.colors import ListedColormap
from scipy.signal import find_peaks
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from AllPackage.PreProcessing import *

#%%
# funzione che esegue il plot della ricostruzione della grigli 11x11 dopo la clusterizzazione
# cluster = variabile contenente il risultato del cluster
# directory = direcoty dove salvare il pdf del plot in formato pdf, esempio './CartellaPlot/Plot_S1_ricostruito'
# name = nome del capione analizzato, esempio S1

def ricostruzion_grid_cluster(cluster, directory, name):
    
    cmap_custom = ListedColormap( [ 'tab:purple', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red' ] )
    x = np.arange(1, 12, 1)
    y = np.arange(1, 12, 1)

    Z = np.empty( (11,11) )

    i = 0
    j = 0
    while i<len(cluster):
        Z[j,:] = cluster [i:i+11]
        i = i+11
        j = j+1
        
        
    fig, ax = plt.subplots()



    pcm = ax.pcolormesh(x, y, Z, cmap =  cmap_custom)
    ax.set_title("Ricostruzione campione "+ name +" dal cluster")
    ax.set_xlabel('posizione x ($\mu$m)')
    ax.set_ylabel('posizione y ($\mu$m)')
    ax.set_yticks(y)
    ax.set_xticks(x)

    fig.colorbar(pcm, ax = ax, boundaries=[-1, 0 ,1 ,2, 3,4])
    plt.show()
    
    fig.savefig(directory+'.pdf');