# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 20:28:38 2020

@author: Gabri
"""

import pandas as pd

def build_input_file(table,isoforms):
    d = table[table["Unnamed: 0"].isin(isoforms)]
    d = d.transpose()
    d.to_csv("../Files/pcalg_input.csv",header=False,index=False)
        

if __name__ == "__main__":
    path = "../Data/hgnc_filtered_mat.csv"
    table = pd.read_csv(path)
    
    with open("../Files/isoforms_in_common.csv","r") as iso_file:
        isoforms = []
        for line in iso_file.readlines():
            line = line.replace("\n","")
            isoforms.append(line)
    build_input_file(table,isoforms)