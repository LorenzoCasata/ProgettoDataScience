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

def process_transpose(df):
    
    df_smooth = smooth_filter_savgol(df,df.columns)
    df_smooth = norm_max_min(df_smooth,df_smooth.columns)
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

def process_transpose_all(initial_path = './Data/Initial/S_11x11' , final_path = './Data/PreProcessed/S_11x11'):
    
    data_S1_bkg = pd.read_csv(initial_path+'/data_S1_bkg.csv', index_col = 0)
    data_S1 = pd.read_csv(initial_path+'/data_S1.csv', index_col = 0)
    data_S2_bkg = pd.read_csv(initial_path+'/data_S2_bkg.csv', index_col = 0)
    data_S2 = pd.read_csv(initial_path+'/data_S2.csv', index_col = 0)
    
    
    data_S1_bkg_smooth = smooth_filter_savgol(data_S1_bkg,data_S1_bkg.columns)
    data_S1_bkg_smooth = norm_max_min(data_S1_bkg_smooth,data_S1_bkg_smooth.columns)
    data_S1_bkg_transp = transpose_df(data_S1_bkg_smooth)
    
    data_S2_bkg_smooth = smooth_filter_savgol(data_S2_bkg,data_S2_bkg.columns)
    data_S2_bkg_smooth = norm_max_min(data_S2_bkg_smooth,data_S2_bkg_smooth.columns)
    data_S2_bkg_transp = transpose_df(data_S2_bkg_smooth)
    
    data_S1_smooth = smooth_filter_savgol(data_S1,data_S1.columns)
    data_S1_smooth = norm_max_min(data_S1_smooth,data_S1_smooth.columns)
    data_S1_transp = transpose_df(data_S1_smooth)
    
    data_S2_smooth = smooth_filter_savgol(data_S2,data_S2.columns)
    data_S2_smooth = norm_max_min(data_S2_smooth,data_S2_smooth.columns)
    data_S2_transp = transpose_df(data_S1_bkg_smooth)
    
    data_S1_bkg_transp.to_csv(final_path+'/data_S1_bkg_transp.csv',index = False)
    data_S1_transp.to_csv(final_path+'/data_S1_transp.csv',index = False)
    data_S2_transp.to_csv(final_path+'/data_S2_transp.csv',index = False)
    data_S2_bkg_transp.to_csv(final_path+'/data_S2_bkg_transp.csv',index = False)
    
    
    return(data_S1_transp, data_S1_bkg_transp, data_S2_transp, data_S2_bkg_transp)