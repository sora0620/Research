import networkx as nx
import random
import time

class RP:
    def __init__(self, s, k):
        self.sampled_graph = nx.DiGraph()
        self.ratio_of_seeds = s
        self.top_k_ratio = k
        
    def rank_pagerank_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()

        number_of_seeds = int(self.ratio_of_seeds * len(list(complete_graph))) # 最初の種の数
        if number_of_seeds == 0:
            number_of_seeds = 1
            
        pr_origin = nx.pagerank(complete_graph)
        
        seeds = []
        copy_graph = complete_graph.to_directed()
        
        while True: # ノード数が規定サンプル数に達したら終了
            new_seeds = [] # seeds 全て回し終わった後に次の種ノードとして利用
            remove_edges = []
            loop_flag = True
            end_flag = False
            no_deg_list = []
            
            if len(seeds) == 0: # 最初の種を選ぶ or 種を選び直す
                while len(seeds) != number_of_seeds: # 出次数が 0 のノードを排除した seeds を選ぶ
                    tmp_node = random.choice(list(copy_graph))
                    if tmp_node not in no_deg_list:
                        no_deg_list.append(tmp_node)
                    if len(list(copy_graph.successors(tmp_node))) != 0 and tmp_node not in seeds:
                        seeds.append(tmp_node)
                    if len(no_deg_list) == len(list(copy_graph)):
                        if len(seeds) == 0:
                            end_flag = True
                        break
                    
            if end_flag == True:
                random_nodes = random.sample(no_deg_list, nodes_to_sample - len(list(self.sampled_graph)))
                self.sampled_graph.add_nodes_from(random_nodes)
                break
            
            # 種ノードの内, 一つのノードに着目する
            for current_node in seeds:
                neighbor_pr = [] # 出隣接ノードの PR リスト
                selected_nodes = [] # サンプルグラフに追加するノードリスト
                
                # 現在ノードの出隣接ノード : neighbor_node の pr をリストに追加
                for neighbor_node in list(copy_graph.successors(current_node)):
                    neighbor_pr.append([neighbor_node, pr_origin[neighbor_node]])
                # neighbor_pr を降順に並べる
                pr_rank = sorted(neighbor_pr, key=lambda x:x[1], reverse=True)
                
                # top k 個の k の値を決定
                number_of_top_nodes = int(self.top_k_ratio * len(neighbor_pr))
                
                # k が 1 より小さくなったら 1 にする
                if number_of_top_nodes < 1:
                    number_of_top_nodes = 1
                
                if (number_of_top_nodes + len(list(self.sampled_graph))) < nodes_to_sample:
                    for i in range(number_of_top_nodes):
                        top_node = pr_rank[i][0]
                        edge = (current_node, top_node)
                        if edge not in list(self.sampled_graph.edges()):
                            self.sampled_graph.add_edge(current_node, top_node)
                            remove_edges.append(edge)
                else:
                    loop_flag = False
                    number_of_select_nodes = nodes_to_sample - len(list(self.sampled_graph))
                    if number_of_select_nodes == 0:
                        break
                    for i in range(number_of_top_nodes):
                        selected_nodes.append(pr_rank[i][0])
                    selected_nodes = random.sample(selected_nodes, number_of_select_nodes)
                    for i in selected_nodes:
                        if (current_node, i) not in list(self.sampled_graph.edges()):
                            self.sampled_graph.add_edge(current_node, i)
                    break
            
            if loop_flag == True:
                copy_graph.remove_edges_from(remove_edges)
                seeds = new_seeds
            else:
                break
            
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RP_Time  :", tim)
              
        return self.sampled_graph