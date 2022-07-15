#%%
#Pacchetto con le funzioni necessarie per creare tutti i dati necessari da quelli raw

import pandas as pd
import os
import os.path
import matplotlib.pyplot as plt

import numpy as np

import scipy 
from scipy.signal import find_peaks

import sklearn as skl
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans

from AllPackage.Data.PreProcessing import *


#%%
# funzione che dai dati raw crea i pandas dataframe per i campioni S11x11
# initial_path = percorsi dei dati raw in csv
# final_path = percorsi dei dati in csv dei nuovi DF
# i percorsi di default sono quelli della cartella del progetto
# return i 4 dataframe, nell'  ordine S1, S1_bkg; S2, S2_bkg

def build_S11x11_df(initial_path='./Data/Raw/S_11x11', final_path='./Data/Initial/S_11x11'):
    
    namefiles = [f for f in os.listdir(initial_path) if os.path.isfile(os.path.join(initial_path, f))]
    namefiles = ['S1_bkg_mapA_11x11.txt', 'S1_mapA_11x11.txt', 'S2_bkg_mapA_11x11.txt', 'S2_mapA_11x11.txt']
    columns = ['WaveNum']+[f'row{k}_point{i}' for k in range(1,12) for i in range(1,12)]
    
    data_S1_bkg = pd.read_csv(initial_path+'/'+namefiles[0], delim_whitespace=True,names = columns)
    data_S1 = pd.read_csv(initial_path+'/'+namefiles[1], delim_whitespace=True,names = columns)
    data_S2_bkg = pd.read_csv(initial_path+'/'+namefiles[2], delim_whitespace=True,names = columns)
    data_S2 = pd.read_csv(initial_path+'/'+namefiles[3], delim_whitespace=True,names = columns)
        
    data_S1_bkg.to_csv(final_path+'/data_S1_bkg.csv',index = False)
    data_S1.to_csv(final_path+'/data_S1.csv',index = False)
    data_S2.to_csv(final_path+'/data_S2.csv',index = False)
    data_S2_bkg.to_csv(final_path+'/data_S2_bkg.csv',index = False)
    
    return(data_S1, data_S1_bkg, data_S2, data_S2_bkg)



#%%
# funzione che normalizza il dataframe secondo normalizzazione Min-Max, lo passa sotto lo smooth filter sav-gol, e traspone
# df = il dataframe iniziale dai dati raw
# return il dataframe risultante

def process_transpose(df, smooth = 'savgol', norm = 'max_min'):
    
    if(smooth == 'savgol'):
        
        df_smooth = smooth_filter_savgol(df,df.columns)
    
    elif(smooth == 'none'):#aggiungere casi se si aggiungono smoothing o altri filtri
    
        df_smooth = df
    
    if(norm == 'max_min'):
       
        df_smooth = norm_max_min(df_smooth,df_smooth.columns)
       
    elif(norm == 'area'):
        
        df_smooth = norm_area(df_smooth,df_smooth.columns)
        
    elif(norm == 'none'):
        
        df_smooth=df_smooth
        
    #aggiungere step di preprocessing se necessario   
              
    df_transp = transpose_df(df_smooth) 
    
    return(df_transp)
           
           

#%%
#%%
# funzione che normalizza i dataframe secondo normalizzazione Min-Max, li passa sotto lo smooth filter sav-gol, e traspone
# lo fa in automatico per i 4 dataset S_11x11
# initial_path = percorsi dei dati raw in csv
# final_path = percorsi dei dati in csv dei nuovi DF
# i percorsi di default sono quelli della cartella del progetto
# return i 4 dataframe, nell'  ordine S1, S1_bkg; S2, S2_bkg  

def process_transpose_all(smooth = 'savgol', norm = 'max_min', initial_path = './Data/Initial/S_11x11' , final_path = './Data/PreProcessed/S_11x11'):

    #prende i dati
    data_S1_bkg = pd.read_csv(initial_path+'/data_S1_bkg.csv')
    data_S1 = pd.read_csv(initial_path+'/data_S1.csv')
    data_S2_bkg = pd.read_csv(initial_path+'/data_S2_bkg.csv')
    data_S2 = pd.read_csv(initial_path+'/data_S2.csv')
    
    #preprocessa
    data_S1_bkg_transp = process_transpose(data_S1_bkg, smooth, norm)
    data_S1_transp = process_transpose(data_S1, smooth, norm)
    data_S2_bkg_transp = process_transpose(data_S2_bkg, smooth, norm)
    data_S2_transp = process_transpose(data_S2, smooth, norm)
    
    #salva i dati
    data_S1_bkg_transp.to_csv(final_path+'/data_S1_bkg_transp.csv',index = False)
    data_S1_transp.to_csv(final_path+'/data_S1_transp.csv',index = False)
    data_S2_bkg_transp.to_csv(final_path+'/data_S2_bkg_transp.csv',index = False)       
    data_S2_transp.to_csv(final_path+'/data_S2_transp.csv',index = False)    
    
    return(data_S1_bkg_transp, data_S1_transp, data_S2_bkg_transp, data_S2_transp)