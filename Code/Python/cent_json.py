import json
import networkx as nx
import time
import pickle

READ_FILE = "./data/partition_data/origin_graph/{}.adjlist"

graph_list = ["scale_free_2"]
cent_list = ["pr"]

load_time_start = time.perf_counter()

read_list = []
for graph in graph_list:
    read_list.append(nx.read_adjlist(READ_FILE.format(graph), nodetype=int, create_using=nx.DiGraph))

load_time_end = time.perf_counter()
load_tim = load_time_end - load_time_start
print("Graph Loading Time :", load_tim)

if "pr" in cent_list:
    origin_pr_time_start = time.perf_counter()
    
    file = "./data/partition_data/graph_cent/{}/pr.json"
    for i, graph in enumerate(graph_list):
        pr = nx.pagerank(read_list[i])
        with open(file.format(graph), "w") as f:
            json.dump(pr, f, indent=4, sort_keys=True)

    origin_pr_time_end = time.perf_counter()
    origin_pr_tim = origin_pr_time_end - origin_pr_time_start
    print("Origin PR Time :", origin_pr_tim)
if "deg" in cent_list:
    origin_deg_time_start = time.perf_counter()
    
    file = "./data/partition_data/graph_cent/{}/deg.json"
    for i, graph in enumerate(graph_list):
        deg = nx.degree_centrality(read_list[i])
        with open(file.format(graph), "w") as f:
            json.dump(deg, f, indent=4, sort_keys=True)
    
    origin_deg_time_end = time.perf_counter()
    origin_deg_tim = origin_deg_time_end - origin_deg_time_start
    print("Origin Deg Time :", origin_deg_tim)
if "eigen" in cent_list:
    origin_eigen_time_start = time.perf_counter()
    
    file = "./data/partition_data/graph_cent/{}/eigen.json"
    for i, graph in enumerate(graph_list):
        eigen = nx.eigenvector_centrality(read_list[i])
        with open(file.format(graph), "w") as f:
            json.dump(eigen, f, indent=4, sort_keys=True)
    
    origin_eigen_time_end = time.perf_counter()
    origin_eigen_tim = origin_eigen_time_end - origin_eigen_time_start
    print("Origin Eigen Time :", origin_eigen_tim)
if "closeness" in cent_list:
    origin_closeness_time_start = time.perf_counter()
    
    file = "./data/partition_data/graph_cent/{}/closeness.json"
    for i, graph in enumerate(graph_list):
        closeness = nx.closeness_centrality(read_list[i])
        with open(file.format(graph), "w") as f:
            json.dump(closeness, f, indent=4, sort_keys=True)
    
    origin_closeness_time_end = time.perf_counter()
    origin_closeness_tim = origin_closeness_time_end - origin_closeness_time_start
    print("Origin Closeness Time :", origin_closeness_tim)
if "between" in cent_list:
    origin_between_time_start = time.perf_counter()
    
    file = "./data/partition_data/graph_cent/{}/between.json"
    for i, graph in enumerate(graph_list):
        between = nx.betweenness_centrality(read_list[i])
        with open(file.format(graph), "w") as f:
            json.dump(between, f, indent=4, sort_keys=True)
    
    origin_between_time_end = time.perf_counter()
    origin_between_tim = origin_between_time_end - origin_between_time_start
    print("Origin Between Time :", origin_between_tim)