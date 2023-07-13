import networkx as nx
import time
import Calc
import random

# PR を降順に並べ, 分割数に合わせてその範囲の PR 値からランダムにサンプルを取得する方法

class DP:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def divide_pagerank_sampling(self, complete_graph, nodes_to_sample, div_num):
        time_start = time.perf_counter()
        
        pr_origin = nx.pagerank(complete_graph)
        pr_origin = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        
        # PR 値の降順に並べたタプルのリストを, ノード番号のみのリストに変換
        for i in range(len(list(complete_graph))):
            pr_origin[i] = pr_origin[i][0]
        
    	# PR を上位から並べて, div_num 個のリストに分割
        pr_origin_div = Calc.list_div(pr_origin, div_num)
        number_list = [0] * div_num
        
        # 各割合ごとにサンプルするべきノード数. 若いインデックスのほうが PR 上位
        for i in range(nodes_to_sample):
            number_list[i % div_num] += 1
            
        # 以下, サンプリング
        for i in range(div_num):
            for j in range(number_list[i]):
                selected_node = random.choice(pr_origin_div[i])
                self.sampled_graph.add_node(selected_node)
                pr_origin_div[i].remove(selected_node)
        
        sampled_node_list = list(self.sampled_graph)
        for current_node in sampled_node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in sampled_node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("DP_Time  :", tim)
              
        return self.sampled_graph