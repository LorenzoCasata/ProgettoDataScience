# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 17:28:16 2022

@author: Alessandro
"""

import pandas as pd
import os
import os.path
import matplotlib.pyplot as plt
import sklearn as skl
import numpy as np
import scipy 
import AllPackage.PreProcessing as pp # pachetto con le funzioni per eseguire il preprocessing 

from scipy.signal import find_peaks
from sklearn import preprocessing
#%%
# leggo i file contunuti nella cartella Campioni_S_11x11 e acquisisco i nomi dei file

namefiles = [f for f in os.listdir('./Campioni _S_11x11') if os.path.isfile(os.path.join('./Campioni _S_11x11', f))]


# creo la variabile contenente i nomi delle colonne del pandas dataframe

columns = ['WaveNum']+[f'row{k}_point{i}' for k in range(1,12) for i in range(1,12)]

# creo i pandas dataframe dai file contenuti nella cartella Campioni_S_11x11

#for name in namefiles:
#    globals()['dataset_%s' % name[:-4]] = pd.read_csv('./Campioni _S_11x11/'+namefiles[0], delim_whitespace=True,names = columns)
    
data_S1_bkg = pd.read_csv('./Campioni _S_11x11/'+namefiles[0], delim_whitespace=True,names = columns)
data_S1 = pd.read_csv('./Campioni _S_11x11/'+namefiles[1], delim_whitespace=True,names = columns)
data_S2_bkg = pd.read_csv('./Campioni _S_11x11/'+namefiles[2], delim_whitespace=True,names = columns)
data_S2 = pd.read_csv('./Campioni _S_11x11/'+namefiles[3], delim_whitespace=True,names = columns)

#%%