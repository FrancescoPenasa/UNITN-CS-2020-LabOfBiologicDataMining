# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:44:18 2020

@author: Gabri
"""

import subprocess as sub
import pandas as pd

file_names = pd.read_csv("../Data/expansion_files.csv",header=None)
file_names = list(file_names[0])

for file in file_names:
    command = 'rclone copy "gDrive unitn":experiments_results/'+file+" /dest/"
    print(sub.run(command,shell=True))
    if file == file_names[0]:
        break
    
