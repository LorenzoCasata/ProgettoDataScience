# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 18:06:33 2022

@author: Alessandro
"""

import pandas as pd
import os
import os.path
import matplotlib.pyplot as plt
import sklearn as skl
import numpy as np
import scipy 
from scipy.signal import find_peaks
from sklearn import preprocessing

#%%
# definisco la funzione che esegue il plot dello spettro di raman di ogni punto del campione 11x11,
# e lo salva in una cartella, la cui directory deve essere passata in input, 
# il titolo e il nome del plot viene stampato usando le etichette delle colonne in modo incrementale
# data = pandasdataframe contenente i dati nel formato 122 colonne
# clmns = etichette delle colonne 
# directory = percorso della cartella nella quale inserire i plot salvati in fromato pdf, esempio './Plot_S1/plot_S1_'
# silence =  True per spegnere l'output dei plot, False per visualizzare i plot direttamente

def plot_spettri_pdf(data, clmns , directory, silence = bool ):
    
    i = 1


    while i< len(clmns):
    
        fig = plt.figure();
    
        ax = fig.add_subplot(1, 1, 1);
    
        ax.plot(data[clmns[0]],  data[clmns[i]]);

        ax.grid(which='minor', linestyle=':', linewidth=0.5);
        ax.minorticks_on();
    
        ax.set_title(clmns[i]);
        ax.set_ylabel('Raman intensity')
        ax.set_xlabel('Raman shift (cm$^{-1}$)')
    
        fig.savefig(directory+clmns[i]+'.pdf');
        
        if silence:
            plt.close();
    
        i = i+1

#%%        
# definisco la funzione che normalizza gli spettri di Raman in area, lasciando l'asse dei numeri d'onda invariato
# data = dataframe da normalizzare, normalizzazione colonna per colonna
# return pandas dataframe riscalato

def norm_area(data, clmns):
    
    data_norm = data.copy()
    
    for colonna in clmns:
        
        int_psi_square = scipy.integrate.simps(data[colonna], data[clmns[0]])
        data_norm[colonna] = data[colonna]/int_psi_square
    
    data_norm[clmns[0]] = data[clmns[0]]
    
    return(data_norm)

#%%
# definisco la funzione che normalizza gli spettri di Raman in intenistà, settando il valore massimo a 1 e il minimo a 0
# data = dataframe da normalizzare
# clmns = etichette delle colonne
# return pandas dataframe riscalato

def norm_max_min(dataf, clmns):
    
    scaler =  skl.preprocessing.MinMaxScaler()

    data_normMm = pd.DataFrame( columns = clmns, data = scaler.fit_transform(dataf[clmns]))
    data_normMm['WaveNum'] = dataf[clmns[0]]
    
    return(data_normMm)



#%%
# funzione che trova i numeri d'onda corrispondenti ai picchi
# return:
# peaks_Wn = numeri d'onda corrispondenti ai picchi, è una list di array, ogni array sono le ascisse dei picchi per lo spettro...
# ... di un punto della griglia 11x11.
# peaks_Int = intensità del picco, è una list di array, ogni array sono le ordinate dei picchi per lo spettro...
# ... di un punto della griglia 11x11.
# NOTA BENE
# la funzione è molto sensibile al valore del picco, qui è ottimizzata per lavorare sui dati NON RINORMALIZZATI
# la normalizzazione non cambia la forma dello spettro quindi il conteggio dei picchi può essere fatto considerando 
# solo il campione non normalizzato

def trova_picchi(dataf, clmns):
      
    x,_ = find_peaks(dataf[clmns[1]],  prominence=11 )#width = 5, height = 0.05) #,
    
    j = 0
    numero_onda = np.empty(len(x))
    intensity = np.empty(len(x))
    while j<len(x):
            
            numero_onda[j] = dataf.iloc[x[j]].WaveNum
            intensity[j] = dataf.iloc[x[j]][clmns[1]]
            
            j = j+1
            
    peaks_Wn = [numero_onda]
    peaks_Int = [intensity]
    
    
    i = 2
    while i<len(clmns):
        
        x, _ = find_peaks(dataf[clmns[i]], prominence=11)
        
        
        j = 0
        numero_onda = np.empty(len(x))
        intensity = np.empty(len(x))
        while j<len(x):
            
            numero_onda[j] = dataf.iloc[x[j]].WaveNum
            intensity[j] = dataf.iloc[x[j]][clmns[i]]
            j = j+1
    
        peaks_Wn.append(numero_onda)
        peaks_Int.append(intensity)
        
        i = i+1
    
    return(peaks_Wn, peaks_Int)



#%%
# funzione che data una list di array contenente i numeri d'onda corrispondenti ai picchi degli spettri di Raman
# restituisce un array con il range di numeri d'onda nel quale si trovano i picchi

def range_picchi(wave_peak):
    
    wn_range_pic = np.empty( (len(wave_peak),2) )
    
    i = 0
    
    while i<len(wave_peak):
        
        x =  wave_peak[i]
        wn_range_pic[i] = [x[0],x[-1]]
        i = i+1
        
    return(wn_range_pic)     



#%%
# funzione che dato il dataframe contenente gli spettri di Raman calcola l'intensità integrale
# return numpy.array con l'intensità integrale di tutti gli spettri

def integral_intensity(dataf, clmns):
    
    intg = np.empty( len(clmns)-1 )
    
    i = 1
    
    while i < len(clmns):
        
        intg[i-1] = np.trapz(dataf[clmns[i]], x = dataf[clmns[0]])
        i = i+1
        
    return(intg)



#%%
# funzione che dato un pandas dataframe contenente gli spettri di Raman resitutisce un pd.dataframe contenente gli stessi
# spettri con applicato il filtro passabasso Savitzky-Golay

def smooth_filter_savgol(dataf, clmns):
    
    

    temp = np.empty( (  len(dataf[clmns[0]]) ,len(clmns) ) )
   
    i = 1
    while i<len(clmns):
        
        
        temp[:,i] = scipy.signal.savgol_filter(x = dataf[clmns[i]], window_length = 25, polyorder = 3)
        i = i+1
        
        
    data_smth = pd.DataFrame( columns = clmns, data = temp)
    data_smth['WaveNum'] = dataf[clmns[0]]
   
    return(data_smth)