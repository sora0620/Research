import networkx as nx
import time
import json
import random

class CC:
    def __init__(self):
        self.sampling_graph = nx.DiGraph()

    # 近接中心性の高い順にノードの周辺エッジ (入エッジ, 出エッジ両方) を取得していく
    def closeness_centrality_in_out_sampling(self, origin_graph, graph_name, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)

        path = "../../../Dataset/Centrality/CC/{}.json".format(graph_name)
        cc_dict = {}
        
        with open(path, 'r') as f:
            cc_dict = json.load(f)
        
        cc_sorted = sorted(cc_dict.items(), key=lambda x:x[1], reverse=True)
        cc_sorted_node_list = [node for node, cc in cc_sorted]
        sampling_edge_set = set()
        
        while len(sampling_edge_set) < sampling_edge_num:
            current_node = int(cc_sorted_node_list.pop(0)) # 現存ノードの中で最も CC が高いノードを取得 & リストから削除
            
            out_edge_set  = {(current_node, out_node) for out_node in list(origin_graph.successors(current_node))}
            in_edge_set = {(in_node, current_node) for in_node in list(origin_graph.predecessors(current_node))}
            
            if len(sampling_edge_set | out_edge_set | in_edge_set) > sampling_edge_num:
                diff = sampling_edge_num - len(sampling_edge_set)
                tmp_list = list((out_edge_set | in_edge_set) - sampling_edge_set)
                sampling_edge_set.update(set(random.sample(tmp_list, diff)))
                break
            else:
                sampling_edge_set.update(out_edge_set, in_edge_set)
        
        self.sampling_graph.add_edges_from(list(sampling_edge_set))
        if self.sampling_graph.number_of_edges() != sampling_edge_num:
            print("Size Error!")
            exit(1)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("CC_in_out_Time  :", tim)
              
        return self.sampling_graph
    
    # 入次数を取得
    def closeness_centrality_in_sampling(self, origin_graph, graph_name, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)

        path = "../../../Dataset/Centrality/CC/{}.json".format(graph_name)
        cc_dict = {}
        
        with open(path, 'r') as f:
            cc_dict = json.load(f)
        
        cc_sorted = sorted(cc_dict.items(), key=lambda x:x[1], reverse=True)
        cc_sorted_node_list = [node for node, cc in cc_sorted]
        sampling_edge_set = set()
        
        while len(sampling_edge_set) < sampling_edge_num:
            current_node = int(cc_sorted_node_list.pop(0)) # 現存ノードの中で最も CC が高いノードを取得 & リストから削除
            in_edge_set = {(in_node, current_node) for in_node in list(origin_graph.predecessors(current_node))}
            
            if len(sampling_edge_set | in_edge_set) > sampling_edge_num:
                diff = sampling_edge_num - len(sampling_edge_set)
                tmp_list = list(in_edge_set - sampling_edge_set)
                sampling_edge_set.update(set(random.sample(tmp_list, diff)))
                break
            else:
                sampling_edge_set.update(in_edge_set)
        
        self.sampling_graph.add_edges_from(list(sampling_edge_set))
        if self.sampling_graph.number_of_edges() != sampling_edge_num:
            print("Size Error!")
            exit(1)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("CC_in_Time  :", tim)
              
        return self.sampling_graph
    
    # 出次数を取得
    def closeness_centrality_out_sampling(self, origin_graph, graph_name, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)

        path = "../../../Dataset/Centrality/CC/{}.json".format(graph_name)
        cc_dict = {}
        
        with open(path, 'r') as f:
            cc_dict = json.load(f)
        
        cc_sorted = sorted(cc_dict.items(), key=lambda x:x[1], reverse=True)
        cc_sorted_node_list = [node for node, cc in cc_sorted]
        sampling_edge_set = set()
        
        while len(sampling_edge_set) < sampling_edge_num:
            current_node = int(cc_sorted_node_list.pop(0)) # 現存ノードの中で最も CC が高いノードを取得 & リストから削除
            out_edge_set  = {(current_node, out_node) for out_node in list(origin_graph.successors(current_node))}
            
            if len(sampling_edge_set | out_edge_set) > sampling_edge_num:
                diff = sampling_edge_num - len(sampling_edge_set)
                tmp_list = list(out_edge_set - sampling_edge_set)
                sampling_edge_set.update(set(random.sample(tmp_list, diff)))
                break
            else:
                sampling_edge_set.update(out_edge_set)
        
        self.sampling_graph.add_edges_from(list(sampling_edge_set))
        if self.sampling_graph.number_of_edges() != sampling_edge_num:
            print("Size Error!")
            exit(1)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("CC_out_Time  :", tim)
              
        return self.sampling_graph