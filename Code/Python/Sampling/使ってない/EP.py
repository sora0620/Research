import networkx as nx
import time

class EP:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def edge_pagerank_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()
        
        # num = 0 # デバッグ用
        edge_weight = {}
        pr_origin = nx.pagerank(complete_graph) # 元グラフの PR 辞書
        pr_origin_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True) # (ノード番号, PR 値) の PR 値で降順にしたリスト
        
        for node, pr_value in pr_origin.items():
            # 外向きのエッジがない場合はエッジの PR は 0 とする
            edge_num = len(list(complete_graph.successors(node)))
            if edge_num != 0:
                edge_pr = pr_value / edge_num
            else:
                edge_pr = 0
            edge_weight[node] = edge_pr # ノードリスト
        
        list_index = 0
        initial_node = pr_origin_sorted[list_index][0] # 最も PR 値の高いノード
        current_node = initial_node
        end_node = 0
            
        while len(list(self.sampled_graph)) != nodes_to_sample:
            self.sampled_graph.add_node(current_node)
            next_node = pr_origin_sorted[list_index + 1][0] # 次に PR 値の高いノード
            
            if len(list(self.sampled_graph)) == nodes_to_sample:
                break
            
            # 現在ノードと次のノードにエッジがない場合、次のノードとその次のノードに移行
            # ここはもう少し考えたほうが良さそう。とりあえずの処置
            
            if nx.has_path(complete_graph, source=next_node, target=current_node):
                # num += 1
                # print(num, "回目, ノード数 :", len(list(self.sampled_graph)))
                # ノード u から v への全てのパスのリストを入れる、リストのリスト
                path_list = list(nx.all_simple_paths(complete_graph, source=next_node, target=current_node, cutoff=3))
                
                if len(path_list) != 0: # has_path で経路が存在するのは確認しているが, 経路長を限定しているのでもう一度確認
                    path_pr_sum = [0] * len(path_list) # パス毎のエッジの PR 合計値を格納、パスの番号 (path_list の index) も格納する。[パス番号, 合計値] のリスト
                    for path_index, path in enumerate(path_list):
                        for node in path:
                            path_pr_sum[path_index] += edge_weight[node]
                            end_node = node
                        path_pr_sum[path_index] -= edge_weight[end_node]
                    
                    max_pr_path_index = path_pr_sum.index(max(path_pr_sum)) # 経路の PR 合計値が最大の経路リストのインデックスを取得

                    # PR 合計値が最小の経路のエッジを追加
                    self.sampled_graph.add_node(next_node)
                    for i in range(len(path_list[max_pr_path_index]) - 1):
                        if len(list(self.sampled_graph)) == nodes_to_sample:
                            break
                        self.sampled_graph.add_edge(path_list[max_pr_path_index][i], path_list[max_pr_path_index][i + 1])
            
            list_index += 1
            current_node = next_node # 次に PR 値の高いノード
            
        node_list = list(self.sampled_graph)
        for current_node in node_list:
            for adjacency_node in list(complete_graph.successors(current_node)):
                if adjacency_node in node_list:
                    self.sampled_graph.add_edge(current_node, adjacency_node)

        time_end = time.perf_counter()
        tim = time_end - time_start
        print("EP_Time  :", tim)
        
        return self.sampled_graph