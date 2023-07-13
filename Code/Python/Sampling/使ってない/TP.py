import networkx as nx
import time

class TP:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def top_pagerank_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        pr_origin = nx.pagerank(complete_graph)
        pr_origin = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)

        for i in range(nodes_to_sample):
            selected_node = pr_origin[i][0]
            self.sampled_graph.add_node(selected_node)
        
        node_list = list(self.sampled_graph)
        for current_node in node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TP_Time  :", tim)
              
        return self.sampled_graph