import networkx as nx
import numpy as np
import time
import random

class RPN:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def random_pagerank_node_sampling(self, origin_graph, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate) # サンプリングエッジ数
        
        pr_dict = nx.pagerank(origin_graph)
        probability = []
        node_list = []
        for node, pr in pr_dict.items():
            node_list.append(node)
            probability.append(pr)

        sampling_edge_set = set()
        tmp_adj_list = []
        tmp_node = 0
        while len(sampling_edge_set) < sampling_edge_num:
            selecte_node_list = np.random.choice(node_list, size=10, replace=False, p=probability)
            for select_node in selecte_node_list:
                tmp_node = select_node
                tmp_adj_list = list(origin_graph.successors(select_node))
                for adj_node in tmp_adj_list:
                    sampling_edge_set.add((select_node, adj_node))
                if len(sampling_edge_set) > sampling_edge_num:
                    break

        if len(sampling_edge_set) > sampling_edge_num:
            delete_num = len(sampling_edge_set) - sampling_edge_num
            delete_adj_list = random.sample(tmp_adj_list, delete_num)
            
            for adj_node in delete_adj_list:
                sampling_edge_set.remove((tmp_node, adj_node))
        
        self.sampled_graph.add_edges_from(list(sampling_edge_set))

        if len(list(self.sampled_graph.edges())) != sampling_edge_num:
            print("Error!")
            exit(1)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RPN_Time :", tim)
        
        return self.sampled_graph