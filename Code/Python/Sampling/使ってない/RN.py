import networkx as nx
import numpy as np
import time

class RN:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def random_node_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        node_list = list(complete_graph)
        
        while self.sampled_graph.number_of_nodes() != nodes_to_sample: # ノード数が規定サンプル数に達したら終了
            selected_node = np.random.choice(node_list)
            self.sampled_graph.add_node(selected_node)
            node_list.remove(selected_node)
        
        sampled_node_list = list(self.sampled_graph)
        for current_node in sampled_node_list:
            for adjacency_node in list(complete_graph.successors(current_node)):
                if adjacency_node in sampled_node_list:
                    self.sampled_graph.add_edge(current_node, adjacency_node)

        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RN_Time  :", tim)
              
        return self.sampled_graph