# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 09:11:07 2020

@author: Gabri
"""

import pandas as pd
import networkx as nx
import stringdb as sdb

def build_network_from_files(nodes_file,edges_file):
    nodes_table = pd.read_csv(nodes_file)
    edges_table = pd.read_csv(edges_file)
    nodes_table = nodes_table[["Id","Label"]]
    edges_table = edges_table[["Source","Target"]]
    
    nodes_dict = {}
    for index, row in nodes_table.iterrows():
        nodes_dict[row[0]] = row[1]

    net = nx.Graph()
    net.add_nodes_from(list(nodes_dict.values()))
    
    for index,row in edges_table.iterrows():
        source = nodes_dict[row[0]]
        target = nodes_dict[row[1]]       
        net.add_edge(source,target)
        
    return net

def build_network_from_string(gene_list):
    net_table = sdb.get_network(gene_list)
    
    net = nx.Graph()
    net.add_nodes_from(gene_list)
    
    for index,row in net_table.iterrows():
        net.add_edge(row[2],row[3])
        
    remove_not_connected_nodes(net)

    return net

def remove_not_connected_nodes(G):
    for node in list(G.nodes):
        if len(list(G.neighbors(node))) == 0:
            G.remove_node(node)

def build_network_from_string_table(string_table_file):
    string_table = pd.read_csv(string_table_file)
    
    net = nx.Graph()
    for index,row in string_table.iterrows():
        net.add_edge(row[0],row[1])
    
    return net

def net_in_common(net1,net2):
    common_net = nx.Graph()
    
    edges1 = list(net1.edges)
    edges2 = list(net2.edges)
    
    common_edges = []
    
    for edge in edges1:
        if edge in edges2 or edge[::-1] in edges2:
            common_edges.append(edge)
    common_net.add_edges_from(common_edges) 
    
    """
    for node in net1.nodes():
        if len(list(net1.neighbors(node))) == 0 and len(list(net2.neighbors(node))) == 0:
            common_net.add_node(node)
    """
    return common_net

def write_network_files(net,nodes_file,edges_file):
    with open(edges_file,"w") as sf:
        sf.write("Source,Target\n") 
        for edge in list(net.edges):
            sf.write(edge[0]+","+edge[1]+"\n")
    with open(nodes_file,"w") as lf:
        lf.write("id,label\n")
        for node in list(net.nodes):
            lf.write(node+","+node+"\n")
    
if __name__ == "__main__":
    nodes_file = "../Files/filtered_network10connections.csv"
    edges_file = "../Files/filtered_network10connections_edges.csv"
    string_file = "../Files/string_interactions.csv"
    
    our_net = build_network_from_files(nodes_file,edges_file)    
    string_net = build_network_from_string(our_net.nodes)
    string_net_control = build_network_from_string_table(string_file)
    
    print("--- NODES ----")
    print("our: ",len(our_net.nodes),"\tstringdb:",len(string_net.nodes),"\tstring_control:",len(string_net_control.nodes))
    
    print("--- EDGES ----")
    print("our: ",len(our_net.edges),"\tstringdb:",len(string_net.edges),"\tstring_control:",len(string_net_control.edges))
        
    common_net = net_in_common(our_net,string_net)
    common_net_control = net_in_common(our_net,string_net_control)
    print("common:",len(common_net.nodes),"\t",len(common_net.edges))
    print("control:",len(common_net_control.nodes),"\t",len(common_net_control.edges))
    
    write_network_files(common_net,"../Files/common_labels.csv","../Files/common_net.csv")
    write_network_files(string_net,"../Files/string_labels.csv","../Files/string_net.csv")


    
    
    