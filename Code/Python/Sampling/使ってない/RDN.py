import networkx as nx
import numpy as np
import time
import random

class RDN:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
    
    def random_degree_node_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()

        probability = []
        node_list = list(complete_graph)

        for node in node_list:
            probability.append(len(list(complete_graph.predecessors(node)))) # 各ノードの次数
            
        div = sum(probability)
        
        probability = [i / div for i in probability]
        
        not_zero_node_num = 0 # probability が 0 のノードもある場合を考慮する
        
        for i in probability:
            if i != 0:
                not_zero_node_num += 1
        
        while self.sampled_graph.number_of_nodes() != nodes_to_sample: # ノード数が規定サンプル数に達したら終了
            if len(list(self.sampled_graph)) >= not_zero_node_num:
                rand_node = random.choice(node_list)
                self.sampled_graph.add_node(rand_node)
            else:
                selected_node = np.random.choice(node_list, p=probability)
                self.sampled_graph.add_node(selected_node)
            
        sampled_node_list = list(self.sampled_graph)
        for current_node in sampled_node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in sampled_node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
                    
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RDN_Time :", tim)
        
        return self.sampled_graph