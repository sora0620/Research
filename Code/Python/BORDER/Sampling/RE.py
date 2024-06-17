import networkx as nx
import random
import time

class RE:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
    
    def random_edge_sampling(self, origin_graph, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        # サンプリングサイズはエッジ数で規定
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate) # サンプリングエッジ数
        sampling_edge_list = random.sample(edge_list, sampling_edge_num)
        
        self.sampled_graph.add_edges_from(sampling_edge_list)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RE_Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph