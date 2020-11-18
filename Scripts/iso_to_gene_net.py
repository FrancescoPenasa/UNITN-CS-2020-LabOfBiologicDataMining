# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 23:32:51 2020

@author: Gabri
"""

import pandas as pd
import numpy as np

def get_genes_iso_dict(table,isoforms):
    res_dict = {}
    
    for i in isoforms:
        d = table[table["Unnamed: 0"] == i]
        res_dict[i] = list(d["symbol"])[0]
        
    return res_dict

def create_gene_edges(edges,iso_gene_dict):
    gene_edges = pd.DataFrame(columns=["Source","Target"])
    
    for index,row in edges.iterrows():
        source = iso_gene_dict[row["Source"]]
        target = iso_gene_dict[row["Target"]]
        if source == target:
            continue
        gene_edges = gene_edges.append({"Source":source,"Target":target},ignore_index=True)
    return gene_edges.drop_duplicates()

if __name__ == "__main__":
    edges = pd.read_csv("../Files/net_pc.csv")
    nodes = pd.read_csv("../Files/labels_pc.csv")
    nodes = list(nodes["Label"])
    
    table = pd.read_csv("../Data/hgnc_filtered_anno.csv")
    
    d = get_genes_iso_dict(table,nodes)
    
    net = create_gene_edges(edges,d)
    
    net.to_csv("../Files/net_genes.csv",index=False)
    
    gene_nodes = np.unique(np.array(list(d.values()))).tolist()
    lables = pd.DataFrame(list(zip(gene_nodes,gene_nodes)),columns=["Id","Label"])
    
    lables.to_csv("../Files/lables_genes.csv",index=False)