import networkx as nx
import time
import numpy as np

# True だったノードの数を数えて, その分のノードを上位から取ってくる

class TPN_re_re_re:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def top_pagerank_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        pr_origin = nx.pagerank(complete_graph)
        pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        
        end_flag = 0
        
        for taple in pr_sorted:
            high_pr_node = taple[0]
            neighbor_node_pr = {}
            
            if len(list(self.sampled_graph)) != nodes_to_sample:
                self.sampled_graph.add_node(high_pr_node)
            else:
                end_flag = 1
            
            for neighbor_node in list(complete_graph.predecessors(high_pr_node)):
                neighbor_node_pr[neighbor_node] = pr_origin[neighbor_node]
                
            pr_sum = 0
            
            for v in neighbor_node_pr.values():
                pr_sum += v
                
            for k, v in neighbor_node_pr.items():
                neighbor_node_pr[k] = v / pr_sum
                
            if len(neighbor_node_pr) != 0:
                true_or_false = ["True", "False"]
                true_num = 0
                
                for k, v in neighbor_node_pr.items():
                    prob_list = [v, 1 - v]
                    selected_word = np.random.choice(true_or_false, p=prob_list)
                    if selected_word == "True":
                        true_num += 1
                        
                neighbor_node_pr = sorted(neighbor_node_pr.items(), key=lambda x:x[1], reverse=True)
                
                for i in range(true_num):
                    if len(list(self.sampled_graph)) == nodes_to_sample:
                        end_flag = 1
                        break
                    else:
                        self.sampled_graph.add_node(neighbor_node_pr[i][0])
                        
            if end_flag == 1:
                break
            
        node_list = list(self.sampled_graph)
        for current_node in node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TPN_re_re_re_Time  :", tim)
        
        return self.sampled_graph