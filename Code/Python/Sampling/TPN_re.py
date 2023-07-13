import networkx as nx
import time

class TPN_re:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    def top_pagerank_sampling(self, complete_graph, nodes_to_sample, acc, pr_origin):
        time_start = time.perf_counter()
        
        pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        
        if acc > 0.1:
            rate = 0
        elif acc <= 0.1:
            rate = 1

        pr_rank = 0
        node_list = list(self.sampled_graph)
        
        # 以下では, 隣接を取得した際にそれが PR 上位の場合重複するが, Graph() に直接追加するとノードの重複は無視される性質を利用しているので, 
        # ノード数の操作に若干注意が必要. (add_node をしても既にノードが存在して追加されない場合がある)
        
        while len(node_list) != nodes_to_sample:
            high_pr_node = pr_sorted[pr_rank][0]
            self.sampled_graph.add_node(high_pr_node)
            
            neighbors_num = 0
            neighbor_dict = {}
            
            neighbor_list = list(complete_graph.predecessors(high_pr_node))
            
            for adj_node in neighbor_list:
                neighbor_dict[adj_node] = pr_origin[adj_node]
                neighbors_num += 1
                
            neighbor_dict = sorted(neighbor_dict.items(), key=lambda x:x[1], reverse=True)
            neighbors_num *= rate
            
            for i in range(neighbors_num):
                # rate = 1 のとき, 最後だけ PR 上位から取ってくるような設計になってることに注意
                node_list = list(self.sampled_graph)
                if len(node_list) == nodes_to_sample:
                    break
                self.sampled_graph.add_node(neighbor_dict[i][0])
            
            pr_rank += 1
            node_list = list(self.sampled_graph)
        
        node_set = set(node_list)
        
        for current_node in node_set:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_set:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TPN_re_Time  :", tim)
              
        return self.sampled_graph