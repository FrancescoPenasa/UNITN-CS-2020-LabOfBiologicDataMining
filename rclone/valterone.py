# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:29:38 2020

@author: Gabri
"""

import pandas as pd

h1n1 = pd.read_csv("../Data/h1n1.csv",header = None)
al = pd.read_csv("../Data/genehome_history.csv")

h1n1 = list(h1n1.iloc[:,0])
al = al[["id","lgn"]]

done = al[al["lgn"].isin(h1n1)]

file_names = [str(id)+"_Hs.interactions\n" for id in list(done["id"])]

with open("../Data/expansion_files.csv","w") as out:
    out.writelines(file_names)

#done = [x+"\n" for x in h1n1 if x in al]

#with open("done.csv","w") as out:
#    out.writelines(done)