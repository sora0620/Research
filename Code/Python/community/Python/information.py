import networkx as nx
import os
import copy
import re
import time
import Calc

DIR_ORIGIN = "../../../Dataset/Origin"

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def information_origin(root_dir):
    dir_list = os.listdir(root_dir)

    if "information.txt" in dir_list:
        dir_list.remove("information.txt")
    if "notice.txt" in dir_list:
        dir_list.remove("notice.txt")
    if ".DS_Store" in dir_list:
        dir_list.remove(".DS_Store")
    
    graph_list = copy.deepcopy(dir_list)
    
    max_len = 0
    for dir in dir_list:
        if max_len < len(dir):
            max_len = len(dir)
    
    for i, graph in enumerate(graph_list):
        graph_list[i] = root_dir + f"/{graph}"

    f = open(root_dir + "/information.txt", "w")

    for i, graph in enumerate(graph_list):
        if os.path.isdir(graph):
            information_origin(graph)
            continue
            
        print(graph)
                
        G = nx.read_adjlist(graph, nodetype=int, create_using=nx.DiGraph)
        f.write("{}, node : {:,}, edge : {:,}\n".format(dir_list[i].rjust(max_len), len(list(G)), len(list(G.edges()))))
        
    f.close()

def main():
    information_origin(DIR_ORIGIN)

if __name__ == "__main__":
    main()