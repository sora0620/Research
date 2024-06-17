import random
import networkx as nx
import time

class SRW:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    # エッジ数を基準としたサンプリングとしている
    def simple_random_walk_sampling(self, complete_graph, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return complete_graph

        growth_size = 2
        T = 100    # number of iterations
        iteration = 1
        edges_before_t_iter = 0
        sampling_edge_num = int(complete_graph.number_of_edges() * sampling_rate) # サンプリングエッジ数
        
        node_list = list(complete_graph)
        current_node = random.choice(node_list) # サンプリングの最初のノード番号
        self.sampled_graph.add_node(current_node)
        adj_dict = {}
        for node in node_list:
            adj_dict[node] = list(complete_graph.successors(node))
        
        while self.sampled_graph.number_of_edges() < sampling_edge_num: # ノード数が規定サンプル数に達したら終了
            edges = adj_dict[current_node] # 現在ノードの隣接ノードのノード番号リスト
            if len(edges) != 0:
                chosen_node = random.choice(edges) # ノードの選択
                self.sampled_graph.add_edge(current_node, chosen_node) # エッジ追加
                current_node = chosen_node # ノード番号を変更
            
            iteration += 1
            
            if iteration % T == 0:
                if ((self.sampled_graph.number_of_edges() - edges_before_t_iter) < growth_size):
                    current_node = random.choice(node_list)
                    self.sampled_graph.add_node(current_node)
                edges_before_t_iter = self.sampled_graph.number_of_edges()
            print(self.sampled_graph.number_of_edges())
        
        if self.sampled_graph.number_of_edges() != sampling_edge_num:
            print("Over Edge Error!")
            exit(1)
            
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("SRW_Time :", tim)
        
        return self.sampled_graph