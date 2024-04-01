import networkx as nx
import time

class TPN_re:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()

    def top_pagerank_sampling(self, complete_graph, nodes_to_sample, pr_origin):
        neighbor_dict = {node: list(complete_graph.predecessors(node)) for node in list(complete_graph)}
                
        time_start = time.perf_counter()
        
        pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        node_set = set()
        
        # if acc > 0.1:
        #     rate = 0
        # elif acc <= 0.1:
        #     rate = 1
        
        rate = 1
        pr_rank = 0
        
        # 以下では, 隣接を取得した際にそれが PR 上位の場合重複するが, Graph() に直接追加するとノードの重複は無視される性質を利用しているので, 
        # ノード数の操作に若干注意が必要. (add_node をしても既にノードが存在して追加されない場合がある)
        
        while len(node_set) != nodes_to_sample:
            high_pr_node = pr_sorted[pr_rank][0]
            node_set.add(high_pr_node)
            
            neighbors_num = len(neighbor_dict[high_pr_node])
            neighbor_pr = {}
            
            for adj_node in neighbor_dict[high_pr_node]:
                neighbor_pr[adj_node] = pr_origin[adj_node]
                
            neighbor_pr = sorted(neighbor_pr.items(), key=lambda x:x[1], reverse=True)
            neighbors_num *= rate

            if len(node_set) + neighbors_num <= nodes_to_sample:
                for i in range(neighbors_num):
                    node_set.add(neighbor_pr[i][0])
            else:
                for i in range(neighbors_num):
                    # rate = 1 のとき, 最後だけ PR 上位から取ってくるような設計になってることに注意
                    if len(node_set) == nodes_to_sample:
                        break
                    node_set.add(neighbor_pr[i][0])
            
            pr_rank += 1
        
        self.sampled_graph.add_nodes_from(list(node_set))
        
        for current_node in node_set:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_set:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TPN_re_Time  :", tim)
              
        return self.sampled_graph

    def top_pagerank_sampling_time(self, complete_graph, nodes_to_sample, pr_origin):
        neighbor_dict = {node: list(complete_graph.predecessors(node)) for node in list(complete_graph)}
                
        time_start = time.perf_counter()
        
        pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        node_set = set()
        
        # if acc > 0.1:
        #     rate = 0
        # elif acc <= 0.1:
        #     rate = 1
        
        rate = 1
        pr_rank = 0
        
        # 以下では, 隣接を取得した際にそれが PR 上位の場合重複するが, Graph() に直接追加するとノードの重複は無視される性質を利用しているので, 
        # ノード数の操作に若干注意が必要. (add_node をしても既にノードが存在して追加されない場合がある)
        
        while len(node_set) != nodes_to_sample:
            high_pr_node = pr_sorted[pr_rank][0]
            node_set.add(high_pr_node)
            
            neighbors_num = len(neighbor_dict[high_pr_node])
            neighbor_pr = {}
            
            for adj_node in neighbor_dict[high_pr_node]:
                neighbor_pr[adj_node] = pr_origin[adj_node]
                
            neighbor_sorted = sorted(neighbor_pr.items(), key=lambda x:x[1], reverse=True)
            neighbors_num *= rate

            if len(node_set) + neighbors_num <= nodes_to_sample:
                for i in range(neighbors_num):
                    node_set.add(neighbor_sorted[i][0])
            else:
                for i in range(neighbors_num):
                    # rate = 1 のとき, 最後だけ PR 上位から取ってくるような設計になってることに注意
                    if len(node_set) == nodes_to_sample:
                        break
                    node_set.add(neighbor_sorted[i][0])
            
            pr_rank += 1
        
        self.sampled_graph.add_nodes_from(list(node_set))
        
        for current_node in node_set:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_set:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TPN_re_Time  :", tim)
              
        return self.sampled_graph, tim 