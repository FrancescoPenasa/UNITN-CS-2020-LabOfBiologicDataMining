# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 14:37:24 2020

@author: Gabri
"""

import os 
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network

def getGenes(path):
    gene_file_dict = {}

    for file in os.listdir(path):
        if "," in file:
            continue
        geneName = ((file.split("@"))[1].split("."))[0]
        if geneName not in gene_file_dict:
            gene_file_dict[geneName] = [file]
        else:
            gene_file_dict[geneName] += [file]

    return gene_file_dict

def mergeExpansionListsExclusive(gene,path,fileList):
    merged = []
    first = True
    for file in fileList:          
        df = pd.read_csv(path+file,header=1)
        df = df[(df["Frel"] > 0.95) & df["gene_name"]]
        neighbors = list(df["gene_name"])                 
        
        if first:
            merged += list(neighbors)
            merged =(np.unique(np.array(merged))).tolist()
        
            if gene in merged:
                merged.remove(gene)
            first = False
        else:
            new_merged = []
            for gene in neighbors:
                if gene in merged:
                    new_merged.append(gene)
            merged = new_merged.copy()
                
    return merged

def mergeExpansionLists(gene,path,fileList):
    merged = []
    
    for file in fileList:
        df = pd.read_csv(path+file,header=1)
        df = df[(df["Frel"] > 0.95) & df["gene_name"]]

        merged += list(df["gene_name"])
        merged =(np.unique(np.array(merged))).tolist()
        
        if gene in merged:
            merged.remove(gene)
    return merged  

def mergeExpansionListsSemiExclusive(gene,path,fileList):
    merged = {}
    N = len(fileList)
    
    for file in fileList: 
        df = pd.read_csv(path+file,header=1)
        df = df[(df["Frel"] > 0.95) & df["gene_name"]]
        
        gene_list_tmp = list(df["gene_name"])
        gene_list_tmp =(np.unique(np.array(gene_list_tmp))).tolist()
        
        if gene in gene_list_tmp:
            gene_list_tmp.remove(gene)

        for g in gene_list_tmp:
            if g not in merged.keys():
                merged[g] = 1
            else:
                merged[g] += 1                  
        
    return [x for x in merged.keys() if merged[x]/N >= 0.5]             

def mergeAll(gf_dict,path):
    final = {}
    i = 1
    for gene in list(gf_dict):
        final[gene] = mergeExpansionListsSemiExclusive(gene,path,gf_dict[gene])
        print(i,"/",len(gf_dict.keys()))
        i += 1
    return final

def getAllGenes(gf_dict):
    total_genes = list(gf_dict)
    for gene in f.keys():
        total_genes += list(f[gene])
        
    total_genes = (np.unique(np.array(total_genes))).tolist()
    return total_genes

def buildGraph(gf_dict):
    G = nx.Graph()
    keys = list(gf_dict)
    total_genes = getAllGenes(gf_dict)
    
    print("Building the nodes...")
    index = 1
    for geneName in total_genes:        
        if geneName in keys:
            G.add_node(geneName,id = index,color="red")
        else:
            G.add_node(geneName,id = index,color="blue")
        index += 1
    print("Building the edges...")
    for centerGene in gf_dict:
        neighours = gf_dict[centerGene]
        
        for n in neighours:
            G.add_edge(centerGene,n,color = "black")
    print(len(G.edges),"edges buit")
    return G

def createNetworkFiles(G,structure_file,label_file):
    # Create the file containing the connections between the nodes
    with open(structure_file,"w") as sf:
        sf.write("Source,Target\n")
        for edge in list(G.edges):
            sf.write(str(G.nodes[edge[0]]["id"])+","+str(G.nodes[edge[1]]["id"])+"\n")
    # Create the file containing the labels of the nodes
    with open(label_file,"w") as lf:
        lf.write("id,label\n")
        for node in list(G.nodes):
            lf.write(str(G.nodes[node]["id"])+","+node+"\n")

def recursiveCut(G,degree):
    to_remove = []
    for node in G.nodes:
        l = [x for x in G.neighbors(node)]
        if len(l) <= degree:
            to_remove += [node]
    if len(to_remove) > 0:
        G.remove_nodes_from(to_remove)
        return recursiveCut(G,degree)
    else:
        return G.copy()

path = "all.results/"
gf_dict = getGenes(path)
print(len(gf_dict.keys()))

f = mergeAll(gf_dict,path)

total_genes = list(gf_dict)
for gene in f.keys():
    total_genes += list(f[gene])
    
total_genes = (np.unique(np.array(total_genes))).tolist()
print(len(total_genes))


G = buildGraph(f)
createNetworkFiles(G,"net.csv","labels.csv")

# Visualize Total network
"""
nt = Network("600px","1000px")
print("Building the network from the graph...")
nt.from_nx(G)
print("Finished!")
nt.show("prova1.html")


G2 = G.copy()
print("Number of nodes:",len(G2.nodes))
print("Number of edges:",len(G2.edges))
to_remove = []
for node in G2.nodes:
    l = [x for x in G2.neighbors(node)]
    if len(l) < 6:
        to_remove += [node]
G2.remove_nodes_from(to_remove)
print("- Number of nodes:",len(G2.nodes))
print("- Number of edges:",len(G2.edges))


nt = Network("600px","1000px")
print("Building the network from the graph...")
nt.from_nx(G2)
print("Finished!")
nt.show("prova2.html")


components = nx.connected_components(G2)
subgraphs = []
for c in components:
    subgraphs.append(G.subgraph(c))


nt = Network("600px","1000px")
print("Building the network from the graph...")
nt.from_nx(subgraphs[0])
print("Finished!")
nt.show("prova3.html")


h1n1 = pd.read_table("genes_h1n1.txt",header=None)
h1n1 = list(h1n1[0])

covid1 = list(G.nodes)
covid2 = list(G2.nodes)
covid3 = list(subgraphs[0].nodes)

both1 = [x for x in h1n1 if x in covid1]
both2 = [x for x in h1n1 if x in covid2]
both3 = [x for x in h1n1 if x in covid3]

print("\nGenes in common between h1n1 and the full network: ",len(both1))
print(both1)
print("\nGenes in common between h1n1 and trimmed network: ",len(both2))
print(both2)
print("\nGenes in common between h1n1 and trimmed connected network: ",len(both2))
print(both2)


both_plus = both.copy()
for node in both:
    both_plus += list(G.neighbors(node))

G4 = G.subgraph(both_plus)

nt = Network("600px","1000px")
print("Building the network from the graph...")
nt.from_nx(G4)
print("Finished!")
nt.show("h1n1.html")
"""