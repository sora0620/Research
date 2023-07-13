import networkx as nx
import numpy as np
import time

class RPN:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def random_pagerank_node_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        pr = nx.pagerank(complete_graph)
        probability = []
        node_list = []
    
        for node, pr in pr.items():
            node_list.append(node)
            probability.append(pr)
        
        while self.sampled_graph.number_of_nodes() != nodes_to_sample: # ノード数が規定サンプル数に達したら終了
            selected_node = np.random.choice(node_list, p=probability)
            self.sampled_graph.add_node(selected_node)
        
        sampled_node_list = list(self.sampled_graph)
        for current_node in sampled_node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in sampled_node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
              
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RPN_Time :", tim)
        
        return self.sampled_graph