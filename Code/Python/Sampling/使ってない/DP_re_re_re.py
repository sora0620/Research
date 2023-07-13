import networkx as nx
import time
import Calc
import random

# 今回は次数を考慮して, 高い PR 精度を保ちながら, 次数分布も保つために, より密なグラフにする
# 特に, 前回の方法では最下層群が孤立ノードを選べば解決してしまうようになっていたので, そこに手を加える
# とりあえずは, 合計エッジ数でやってみる
# ↑ .txt には孤立ノードは存在しないので, 上記は間違い. しかし, 結果的に孤立ノードになってしまうことは大いにあるので, エッジ数を考えるのは大切

class DP_re_re_re:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def divide_pagerank_sampling(self, complete_graph, nodes_to_sample, div_num, random_num):
        time_start_all = time.perf_counter()
        
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
            if i == 0: # PR 最上位のノードをランダムに取得
                node_list = random.sample(pr_origin_div[i], number_list[i])
                self.sampled_graph.add_nodes_from(node_list)
                
                loop_node_list = list(self.sampled_graph)
                for current_node in loop_node_list:
                    for adjacency_node in list(complete_graph.successors(current_node)):
                        if adjacency_node in loop_node_list:
                            self.sampled_graph.add_edge(current_node, adjacency_node)
            else:
                pr_sum_before = 0
                pr_sum_list = []
                edge_sum_list = []
                
                pr_sampled_before = nx.pagerank(self.sampled_graph)
                for k, v in pr_sampled_before.items(): # 辞書型 PR のキーを取得
                    if k in pr_origin_div[i - 1]:
                        pr_sum_before += v
                
                for j in range(random_num):
                    pr_sum_after = 0
                    copy_graph = self.sampled_graph.to_directed()
                    # 第 i 層に追加するノード群を, 必要分ランダムに取得
                    add_node_list_random = random.sample(pr_origin_div[i], number_list[i])
                    copy_graph.add_nodes_from(add_node_list_random)
                    
                    loop_node_list = list(copy_graph)
                    for current_node in add_node_list_random:
                        for adjacency_node in list(complete_graph.successors(current_node)):
                            if adjacency_node in loop_node_list:
                                copy_graph.add_edge(current_node, adjacency_node)
                        for adjacency_node in list(complete_graph.predecessors(current_node)):
                            if adjacency_node in loop_node_list:
                                copy_graph.add_edge(adjacency_node, current_node)
                                
                    pr_sampled_after = nx.pagerank(copy_graph)
                    for k, v in pr_sampled_after.items(): # 辞書型 PR のキーを取得
                        if k in pr_origin_div[i - 1]:
                            pr_sum_after += v
                    
                    pr_sum_list.append([add_node_list_random, pr_sum_before - pr_sum_after])
                    edge_sum_list.append(len(list(copy_graph.edges())))
                
                for i in range(random_num):
                    if edge_sum_list[i] == 0:
                        edge_sum_list[i] = 1 # エッジが存在しない場合は影響を与えないように 1 とする
                    pr_sum_list[i][1] *= 1 / edge_sum_list[i]
                
                pr_sum_list = sorted(pr_sum_list, key=lambda x:x[1])
                selected_node_list = pr_sum_list[0][0]
                self.sampled_graph.add_nodes_from(selected_node_list)
                
                loop_node_list = list(self.sampled_graph)
                for selected_node in selected_node_list:
                    for adjacency_node in list(complete_graph.successors(selected_node)):
                        if adjacency_node in loop_node_list:
                            self.sampled_graph.add_edge(selected_node, adjacency_node)
                    for adjacency_node in list(complete_graph.predecessors(selected_node)):
                        if adjacency_node in loop_node_list:
                            self.sampled_graph.add_edge(adjacency_node, selected_node)
    
        time_end_all = time.perf_counter()
        time_all = time_end_all - time_start_all
        print("DP_re_re_re_Time  :", time_all)
        
        return self.sampled_graph