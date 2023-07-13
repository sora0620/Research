import random
import networkx as nx
import numpy as np
import time

p = 0.7 # 前方燃焼確率 p = 0.7 が最も代表的なサンプルを取れる値らしい
r = 0.3 # 後方燃焼確率

class FF:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    def forest_fire_sampling(self, complete_graph, size):
        time_start = time.perf_counter()

        node_list = list(complete_graph)
        random_node = random.choice(node_list)
    
        q = set()
        q.add(random_node)
        self.sampled_graph.add_node(random_node)
    
        while (len(list(self.sampled_graph)) < size):
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
                                if (len(self.sampled_graph.nodes()) < size):
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