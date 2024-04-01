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
        
        selected_node_list = np.random.choice(node_list, size=nodes_to_sample, replace=False, p=probability)
        self.sampled_graph.add_nodes_from(selected_node_list.tolist())
        
        if len(list(self.sampled_graph)) != nodes_to_sample:
            print("Error!")
            exit(1)
        
        sampled_node_set = set(self.sampled_graph)
        for current_node in sampled_node_set:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in sampled_node_set:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        if len(list(self.sampled_graph)) != nodes_to_sample:
            print("Error!")
            exit(1)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RPN_Time :", tim)
        
        return self.sampled_graph