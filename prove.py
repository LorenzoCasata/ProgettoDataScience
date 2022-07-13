import AllPackage.Data.MakeData as MD
import AllPackage.Data.PreProcessing
import AllPackage.Models.MakePCA as PCA
import os
    
MD.build_S11x11_df()
print(os.getcwd())
MD.process_transpose_all()

PCA.make_PCA_all()
