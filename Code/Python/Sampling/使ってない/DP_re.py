import networkx as nx
import time
import Calc
import random
import copy

# 上位 PR 群の総和 PR を最小にするようなエッジを一つずつ追加していく方法. 計算量が多すぎて無理だったやつ

class DP_re:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def divide_pagerank_sampling(self, complete_graph, nodes_to_sample, div_num):
        time_start_all = time.perf_counter()
        
        time_start_1 = time.perf_counter()
        
        pr_origin = nx.pagerank(complete_graph)
        pr_origin = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
        # PR 値の降順に並べたタプルのリストを, ノード番号のみのリストに変換
        for i in range(len(pr_origin)):
            pr_origin[i] = pr_origin[i][0]
        
    	# PR を上位から並べて, div_num 個のリストに分割
        pr_origin_div = Calc.list_div(pr_origin, div_num)
        copy_div = copy.copy(pr_origin_div) # ノードを削除するようのリスト, deep copy.
        number_list = [0] * div_num
        
        # 各割合ごとにサンプルするべきノード数. 若いインデックスのほうが PR 上位
        for i in range(nodes_to_sample):
            number_list[i % div_num] += 1
            
        time_end_1 = time.perf_counter()
        time_1 = time_end_1 - time_start_1
        print("Time_1 :", time_1)
            
        time_start_3 = time.perf_counter()
        
        # 以下, サンプリング
        for i in range(div_num):
            if i == 0: # PR 最上位のノードをランダムに取得
                
                time_start_2 = time.perf_counter()
                
                node_list = random.sample(pr_origin_div[i], number_list[i])
                self.sampled_graph.add_nodes_from(node_list)
                for current_node in list(self.sampled_graph.nodes()):
                    for adjacency_node in list(complete_graph.successors(current_node)):
                        if adjacency_node in list(self.sampled_graph.nodes()):
                            self.sampled_graph.add_edge(current_node, adjacency_node)
                
                time_end_2 = time.perf_counter()
                time_2 = time_end_2 - time_start_2
                print("Time_2 :", time_2)
                
            else: # 以降, エッジを一つずつ追加していく. 方法としては, 上位層の合計 PR 値を最も下げないようなノードを追加
                for j in range(number_list[i]):
                    
                    print(j + 1, "回目")
                    time_start_4 = time.perf_counter()
                    
                    pr_sampled_before = nx.pagerank(self.sampled_graph)
                    pr_sum_before = 0
                    pr_sum_list = []
                    for k, v in pr_sampled_before.items(): # 辞書型 PR のキーを取得
                        if k in pr_origin_div[i - 1]:
                            pr_sum_before += v
                    
                    print("a")
                            
                    for current_node in copy_div[i]:
                        pr_sum_after = 0
                        copy_graph = self.sampled_graph.to_directed()
                        copy_graph.add_node(current_node)
                        for adjacency_node in list(complete_graph.successors(current_node)):
                            if adjacency_node in list(copy_graph.nodes()):
                                copy_graph.add_edge(current_node, adjacency_node)
                        for adjacency_node in list(complete_graph.predecessors(current_node)):
                            if adjacency_node in list(copy_graph.nodes()):
                                copy_graph.add_edge(adjacency_node, current_node)
                                
                        pr_sampled_after = nx.pagerank(copy_graph)
                        for k, v in pr_sampled_after.items(): # 辞書型 PR のキーを取得
                            if k in pr_origin_div[i - 1]:
                                pr_sum_after += v
                        # 2 つ目の要素が小さい方が優秀
                        pr_sum_list.append([current_node, pr_sum_before - pr_sum_after])
                        
                    print("b")
                    
                    pr_sum_list = sorted(pr_sum_list, key=lambda x:x[1])
                    
                    determined_node = pr_sum_list[0][0]
                    self.sampled_graph.add_node(determined_node)
                    for adjacency_node in list(complete_graph.successors(determined_node)):
                        if adjacency_node in list(self.sampled_graph.nodes()):
                            self.sampled_graph.add_edge(determined_node, adjacency_node)
                    for adjacency_node in list(complete_graph.predecessors(determined_node)):
                        if adjacency_node in list(self.sampled_graph.nodes()):
                            self.sampled_graph.add_edge(adjacency_node, determined_node)
                    copy_div[i].remove(determined_node)
                    
                    time_end_4 = time.perf_counter()
                    time_4 = time_end_4 - time_start_4
                    print(j, "回目 :", time_4)
                    
        time_end_3 = time.perf_counter()
        time_3 = time_end_3 - time_start_3
        print("Time_3 :", time_3)                
    
        time_end_all = time.perf_counter()
        time_all = time_end_all - time_start_all
        print("DP_re_Time  :", time_all)
              
        return self.sampled_graph