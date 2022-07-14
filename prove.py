import AllPackage.Data.MakeData as MD
import AllPackage.Data.PreProcessing
import AllPackage.Models.MakePCA as PCA
import os
    
[df1b, df1, df2b, df2]=MD.build_S11x11_df()
print('Acquisito i dati...\n')
[t1b, t1, t2b, t2]=MD.process_transpose_all()
print('Trasposti e pre_processati MinMax e smootSavgol...\n')
[a1b,a1,a2b,a2,pc1b, pc1, pc2b, pc2]=PCA.make_PCA_all(3)
print('Effettuata pca')
PCA.plot_var_PC_all()