# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:45:06 2020

@author: Gabri
"""

import pandas as pd
import numpy as np

def genes_to_isoforms(table,genes):
    isoforms = []
    for gene in genes:
        d = table[table["symbol"] == gene]
        isoforms += list(d["Unnamed: 0"])
    return isoforms
    
def isoforms_to_genes(table,isoforms):
    genes = []
    for iso in isoforms:
        d = table[table["Unnamed: 0"] == iso]
        genes += list(d["symbol"])
    return np.unique(np.array(genes)).tolist()
    
if __name__ == "__main__":
    anno_table = pd.read_csv("../Data/hgnc_filtered_anno.csv")
    with open("../Files/genes_in_common.csv","r") as file:
        genes = []
        for line in file.readlines():
            line = line.replace("\n","")
            genes.append(line)
    iso = genes_to_isoforms(anno_table,genes)
    g = isoforms_to_genes(anno_table,iso)
    
    """
    with open("isoforms_in_common.csv","w") as out:
        for i in iso:
            out.write(i+"\n")"""