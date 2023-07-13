import networkx as nx
import time

# 複製情報を加味した上で, 入次数の高い順にノードを取得していく手法

class TP_rep:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    def top_in_edge_sampling(self, complete_graph, rep_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        node_list = list(self.sampled_graph)
        comp_node_list = list(complete_graph)
        
        tmp_graph = nx.DiGraph()
        tmp_graph = nx.compose(complete_graph, rep_graph)
        in_edge_num_dic = {}
        
        for node in comp_node_list:
            in_edge_num_dic[node] = len(list(tmp_graph.predecessors(node)))
        
        in_edge_num_sorted = sorted(in_edge_num_dic.items(), key=lambda x:x[1], reverse=True)
                
        edge_rank = 0
        
        # 以下では, 隣接を取得した際にそれが PR 上位の場合重複するが, Graph() に直接追加するとノードの重複は無視される性質を利用しているので, 
        # ノード数の操作に若干注意が必要. (add_node をしても既にノードが存在して追加されない場合がある)
        
        while len(node_list) != nodes_to_sample:
            high_edge_node = in_edge_num_sorted[edge_rank][0]
            self.sampled_graph.add_node(high_edge_node)
            
            neighbors_num = 0
            neighbor_dict = {}
            
            neighbor_list = list(complete_graph.predecessors(high_edge_node))
            
            for adj_node in neighbor_list:
                neighbor_dict[adj_node] = in_edge_num_dic[adj_node]
                neighbors_num += 1
                
            neighbor_dict = sorted(neighbor_dict.items(), key=lambda x:x[1], reverse=True)
            
            for i in range(neighbors_num):
                # r最後だけ入次数上位から取ってくるような設計になってることに注意
                node_list = list(self.sampled_graph)
                if len(node_list) == nodes_to_sample:
                    break
                self.sampled_graph.add_node(neighbor_dict[i][0])
            
            edge_rank += 1
            node_list = list(self.sampled_graph)
        
        node_set = set(node_list)
        
        for current_node in node_set:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_set:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TP_rep_Time  :", tim)

        return self.sampled_graph