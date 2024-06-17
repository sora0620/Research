import random
import networkx as nx
import numpy as np
import time
from scipy.stats import binom

# この値は, Sampling for Large Graphs で最良とされていた結果を利用
forward_prob = 0.7 # 前方燃焼確率
back_prob = 0.2 # 後方燃焼確率

class FF:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    def forest_fire_sampling(self, complete_graph, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return complete_graph
        
        edge_list = list(complete_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate) # サンプリングエッジ数

        node_list = list(complete_graph)
        random_node = random.choice(node_list)
    
        que = []
        que.append(random_node)
    
        while len(list(self.sampled_graph.edges())) > sampling_edge_num:
            if len(que) > 0:
                initial_node = que.pop(0)
                if initial_node not in set(list(self.sampled_graph)):
                    # if len(list(self.sampled_graph)) == nodes_to_sample:
                    #     break
                    self.sampled_graph.add_node(initial_node)
                    out_neighbors = list(complete_graph.successors(initial_node)) # 出隣接ノード
                    in_neighbors = list(complete_graph.predecessors(initial_node)) # 入隣接ノード
                    
                    out_num = binom(len(out_neighbors), forward_prob) # 出隣接ノードの選択確率から導いた選択個数
                    in_num = binom(len(in_neighbors), back_prob) # 入隣接ノードの選択確率から導いた選択個数
                    
                    select_out_list = random.sample(out_neighbors, out_num)
                    select_in_list = random.sample(in_neighbors, in_num)
                    
                    for out_node in select_out_list:
                        # if len(list(self.sampled_graph)) == nodes_to_sample:
                        #     break
                        que.append(out_node)
                        self.sampled_graph.add_edge(initial_node, out_node)
                    for in_node in select_in_list:
                        # if len(list(self.sampled_graph)) == nodes_to_sample:
                        #     break
                        que.append(in_node)
                        self.sampled_graph.add_edge(in_node, initial_node)
                else:
                    continue
            else:
                random_node = random.choice(node_list)
                que.append(random_node)
        
        # if len(list(self.sampled_graph)) != nodes_to_sample:
        #     print("Error!")
        #     exit(1)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FF_Time  :", tim)
    
        return self.sampled_graph

# 修正前のやつ
'''
def forest_fire_sampling(self, complete_graph, nodes_to_sample):
    time_start = time.perf_counter()

    node_list = list(complete_graph)
    random_node = random.choice(node_list)

    q = set()
    q.add(random_node)
    self.sampled_graph.add_node(random_node)

    while (len(list(self.sampled_graph)) < nodes_to_sample):
        if (len(q) > 0):
            initial_node = q.pop()
            if (initial_node not in list(self.sampled_graph)):
                self.sampled_graph.add_node(initial_node)
                p_neighbors = list(complete_graph.successors(initial_node)) # 現在ノードから出ていくノード
                r_neighbors = list(complete_graph.predecessors(initial_node)) # 現在ノードに入ってくるノード
                len_neighbors = len(p_neighbors) + len(r_neighbors)
                if len_neighbors > 0:
                    x = np.random.binomial(len_neighbors, p, 1)
                    sum_neighbors = p_neighbors + r_neighbors
                    weights = [] # 選択の重み
                    pa = r / (r * len(p_neighbors) + len(r_neighbors)) # p_neighbors から選択する確率
                    pb = 1 / (r * len(p_neighbors) + len(r_neighbors)) # r_neighbors から選択する確率
                    for i in range(len(p_neighbors)):
                        weights.append(pa)
                    for i in range(len(r_neighbors)):
                        weights.append(pb)
                    select_nodes = np.random.choice(sum_neighbors, size=x, p=weights, replace=False)
                    for i in range(x[0]):
                        if (select_nodes[i] not in list(self.sampled_graph)):
                            q.add(select_nodes[i])
                            if (len(self.sampled_graph.nodes()) < nodes_to_sample):
                                if (select_nodes[i] in p_neighbors):
                                    self.sampled_graph.add_edge(initial_node, select_nodes[i])
                                else:
                                    self.sampled_graph.add_edge(select_nodes[i], initial_node)
                            else:
                                break
            else:
                continue
                
        else:
            random_node = random.choice(node_list)
            q.add(random_node)
    q.clear()
    
    time_end = time.perf_counter()
    tim = time_end - time_start
    print("FF_Time  :", tim)

    return self.sampled_graph
'''