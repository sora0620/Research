import networkx as nx
import time
import json

class EPR:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
    
    def edge_pagerank_sampling(self, origin_graph, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        
        pr_dict = nx.pagerank(origin_graph)
        edge_pr_dict = {}
        
        for node in list(origin_graph.nodes()):
            for adj_node in list(origin_graph.successors(node)):
                edge_pr_dict[(node, adj_node)] = pr_dict[node] / origin_graph.out_degree(node)
        
        edge_sorted = sorted(edge_pr_dict.items(), key=lambda x: x[1], reverse=True)
        
        for i in range(sampling_edge_num):
            source_node = edge_sorted[i][0][0]
            target_node = edge_sorted[i][0][1]
            self.sampled_graph.add_edge(source_node, target_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("EPR_Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph