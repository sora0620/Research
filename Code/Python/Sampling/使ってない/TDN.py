import networkx as nx
import time

class TDN:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def top_pagerank_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        deg_dict = {}
        
        for node in list(complete_graph):
            deg_dict[node] = len(list(complete_graph.predecessors(node)))
        
        deg_dict = sorted(deg_dict.items(), key=lambda x:x[1], reverse=True)

        pr_rank = 0
        
        while len(list(self.sampled_graph)) != nodes_to_sample:
            high_deg_node = deg_dict[pr_rank][0]
            self.sampled_graph.add_node(high_deg_node)
            
            for adj_node in list(complete_graph.predecessors(high_deg_node)):
                if len(list(self.sampled_graph)) == nodes_to_sample:
                    break
                self.sampled_graph.add_node(adj_node)
            
            pr_rank += 1
        
        node_list = list(self.sampled_graph)
        for current_node in node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TDN_Time  :", tim)
        
        return self.sampled_graph