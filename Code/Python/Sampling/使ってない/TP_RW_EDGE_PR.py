import random
import networkx as nx
import time
import numpy as np

class TP_RW_EDGE_PR:
    def __init__(self, sr):
        self.sampled_graph = nx.DiGraph()
        self.seed_rate = sr

    def top_pagerank_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        pr_origin = nx.pagerank(complete_graph)
        pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        
        seed_list = []
        seed_index = 0
        
        seed_num = int(self.seed_rate * nodes_to_sample)
        if seed_num == 0:
            seed_num = 1
            
        for i in range(seed_num):
            seed_list.append(pr_sorted[i][0])

        growth_size = 2
        T = 100   # number of iterations
        iteration = 0
        edges_before_t_iter = 0
        end_flag = 0
        
        while len(list(self.sampled_graph)) != nodes_to_sample: # ノード数が規定サンプル数に達したら終了
            for node in seed_list:
                if len(list(self.sampled_graph)) != nodes_to_sample:
                    self.sampled_graph.add_node(node)
                else:
                    end_flag = 1
                    break
            
            if end_flag == 1:
                break
            
            # ノード数上限にも達さず, 上手く抜け出せてないっぽい
            while True:
                iteration += 1
                for i in range(seed_num):
                    current_node = seed_list[i]
                    edge_list = list(complete_graph.predecessors(current_node))
                    
                    if len(edge_list) != 0:
                        if len(list(self.sampled_graph)) != nodes_to_sample:
                            edge_pr_dist = {}
                            for node in edge_list:
                                edge_pr_dist[node] = pr_origin[node]
                            pr_sum = 0
                            for k, v in edge_pr_dist.items():
                                edge_pr_dist[k] = v / len(list(complete_graph.successors(k)))
                                pr_sum += edge_pr_dist[k]
                            for k, v in edge_pr_dist.items():
                                edge_pr_dist[k] = v / pr_sum
                                
                            prob_list = []
                            prob_node_list = []
                            
                            for k, v in edge_pr_dist.items():
                                prob_node_list.append(k)
                                prob_list.append(v)
                            chosen_node = np.random.choice(prob_node_list, p=prob_list)
                            self.sampled_graph.add_edge(chosen_node, current_node)
                            seed_list[i] = chosen_node
                        else:
                            end_flag = 1
                            break
                                
                if end_flag == 1:
                    break
                    
                if iteration % T == 0:
                    if ((len(list(self.sampled_graph.edges())) - edges_before_t_iter) < growth_size):
                        break
                    edges_before_t_iter = len(list(self.sampled_graph.edges()))
                    
            seed_list = []
            seed_index += seed_num
            
            for i in range(seed_num):
                seed_list.append(pr_sorted[i + seed_index][0])
                
            seed_index += seed_num
                
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TP_RW_EDGE_PR_Time :", tim)
        
        return self.sampled_graph