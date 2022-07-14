import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



#%%
# funzione che fa la PCA di un set di dati
# df = dataframe, con colonne numeri d' onda, su cui eseguire la PCA
# n_components = la percentuale di varianza che si vuole tenere o il numero di PC, se <1, >0 è la varianza si usa il 
# n_components minimo per ottenere una varianza superiore
# # return data_PCA  = array dei dati trasformati nelle coordinate dei PC
#        PCA = l'oggetto PCA da PCA.fit(df)

def make_PCA(df, n_components=0):
    
    scaler = StandardScaler()
    df = scaler.fit_transform(df)
    
    temp = PCA(n_components)
    pca = temp.fit(df)
    
    return(pca.transform(df),pca)


#%%
# funzione che fa la PCA di tutti i dati a disposizione
# initial_path = path contentente i dataframe  dei dati con colonne numeri d' onda, su cui eseguire la PCA
# final_path = path dove salvare i dati relativi alla pca
# n_components= la percentuale di varianza che si vuole tenere o il numero di PC, se <1, >0 è la varianza si usa il 
# n_components minimo per ottenere una varianza superiore
# # return pca_...  = arrays dei dati trasformati nelle coordinate dei PC
#          PCA = l'oggetto PCA da PCA.fit(df)



def make_PCA_all(n_components=0, initial_path = './Data/PreProcessed/S_11x11', final_path = './Data/PCA/S_11x11'):
    
    data_S1_bkg_transp = pd.read_csv(initial_path+'/data_S1_bkg_transp.csv', index_col = 0)
    data_S1_transp = pd.read_csv(initial_path+'/data_S1_transp.csv', index_col = 0)
    data_S2_bkg_transp = pd.read_csv(initial_path+'/data_S2_bkg_transp.csv', index_col = 0)
    data_S2_transp = pd.read_csv(initial_path+'/data_S2_transp.csv', index_col = 0)
    
    scaler = StandardScaler()
    scaled_S1_bkg = scaler.fit_transform(data_S1_bkg_transp)
    scaled_S1 = scaler.fit_transform(data_S1_transp)
    scaled_S2_bkg = scaler.fit_transform(data_S2_bkg_transp)
    scaled_S2 = scaler.fit_transform(data_S2_transp)
    
    temp = PCA(n_components)
    
    pca_S1_bkg = temp.fit_transform(scaled_S1_bkg)
    pca_S1 = temp.fit_transform(scaled_S1)
    pca_S2_bkg = temp.fit_transform(scaled_S2_bkg)
    pca_S2 = temp.fit_transform(scaled_S2)
    
    columns = ['PC'+str(x) for x in range(0,temp.n_components)]
    index = data_S1_bkg_transp.index
    
    pca_S1_bkg_df = pd.DataFrame(pca_S1_bkg, columns = columns, index = index)
    pca_S1_df = pd.DataFrame(pca_S1, columns = columns, index = index)
    pca_S2_bkg_df = pd.DataFrame(pca_S2_bkg, columns = columns, index = index)
    pca_S2_df = pd.DataFrame(pca_S2, columns = columns, index = index)
    
    pca_S1_bkg_df.to_csv(final_path+'/pca_S1_bkg.csv', index = False)
    pca_S1_df.to_csv(final_path+'/pca_S1.csv', index = False)
    pca_S2_bkg_df.to_csv(final_path+'/pca_S2_bkg.csv', index = False)
    pca_S2_df.to_csv(final_path+'/pca_S2.csv', index = False)
    
    return(pca_S1_bkg, pca_S1, pca_S2_bkg, pca_S2, temp.fit(scaled_S1_bkg), temp.fit(scaled_S1), temp.fit(scaled_S2_bkg), temp.fit(scaled_S2))



#%%
# funzione che plotta la varianza totale ottenuta in funzione del numero di componenti principali
# initial_path = path contentente i dataframe  dei dati trasformati con PCA
# final_path = path dove salvare i dati relativi alla pca
# n_components= la percentuale di varianza che si vuole tenere o il numero di PC, se <1, >0 è la varianza si usa il 
# n_components minimo per ottenere una varianza superiore
# # return data_PCA  = arrays dei dati trasformati nelle coordinate dei PC

def plot_var_PC(pca, direcotry, nome):
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    PCs = [x for x in range(1,10)]
    ax.bar(PCs,total_var)
    plt.axhline(y=0.85 ,color='r')
    plt.show()
    
    return()