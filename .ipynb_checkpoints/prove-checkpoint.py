import AllPackage.Data.MakeData as MD
import AllPackage.Data.PreProcessing
import AllPackage.Models.MakePCA as PCA
import os
    
MD.build_S11x11_df()
print('Acquisito i dati...\n')
MD.process_transpose_all()
print('Trasposti e pre_processati MinMax e smootSavgol...\n')
PCA.make_PCA_all()
print('Effettuata pca')
