import random
import networkx as nx
import time

class SRW:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    def simple_random_walk_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()

        growth_size = 2
        T = 100    # number of iterations
        iteration = 1
        edges_before_t_iter = 0
        
        current_node = random.choice(list(complete_graph)) # サンプリングの最初のノード番号
        self.sampled_graph.add_node(current_node)
        
        while self.sampled_graph.number_of_nodes() < nodes_to_sample: # ノード数が規定サンプル数に達したら終了            
            if len(list(self.sampled_graph)) == nodes_to_sample:
                break
            
            edges = list(complete_graph.successors(current_node)) # 現在ノードの隣接ノードのノード番号リスト
            if len(edges) != 0:
                chosen_node = random.choice(edges) # ノードの選択
                self.sampled_graph.add_edge(current_node, chosen_node) # エッジ追加
                current_node = chosen_node # ノード番号を変更
            
            iteration += 1
            
            if iteration % T == 0:
                if ((self.sampled_graph.number_of_edges() - edges_before_t_iter) < growth_size):
                    current_node = random.choice(list(complete_graph))
                    self.sampled_graph.add_node(current_node)
                edges_before_t_iter = self.sampled_graph.number_of_edges()
        
        if len(list(self.sampled_graph)) != nodes_to_sample:
            print("Over Node Error!")
            exit(1)
            
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("SRW_Time :", tim)
                
        return self.sampled_graph