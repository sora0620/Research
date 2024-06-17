import networkx as nx
import time
import json

class EBC:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
    
    def edge_betweenness_centraliry_sampling(self, origin_graph, graph_name, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph

        path = "../../../Dataset/BC/{}_edge.json".format(graph_name)
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        edge_dict = {}
        
        with open(path, 'r') as f:
            edge_dict = json.load(f)
        
        edge_sorted = sorted(edge_dict.items(), key=lambda x: x[1], reverse=True)
        
        for i in range(sampling_edge_num):
            key = edge_sorted[i][0]
            source_node, target_node = map(int, key.split())
            self.sampled_graph.add_edge(source_node, target_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("EBC Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph