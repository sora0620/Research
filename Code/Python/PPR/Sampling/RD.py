import networkx as nx
import random
import time

# 色々試した結果目標取得ノード数と大きいときで 200 ノード程ズレていたので, 多分変なコードになってます修正しましょう

class RD:
    def __init__(self, s, k):
        self.sampled_graph = nx.DiGraph()
        self.ratio_of_seeds = s
        self.top_k_ratio = k
    
    def rank_degree_sampling(self, complete_graph, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return complete_graph

        edge_list = list(complete_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate) # サンプリングエッジ数

        number_of_seeds = int(self.ratio_of_seeds * len(list(complete_graph))) # 最初の種の数
        if number_of_seeds == 0:
            # number_of_seeds = 1
            print("Seed_Error!")
            exit(1)
        
        seed_set = set()
        copy_graph = complete_graph.to_directed()
        
        # 出エッジを持つノードを確認
        deg_node_list = []
        
        for node in list(copy_graph):
            if len(list(copy_graph.successors(node))) != 0:
                deg_node_list.append(node)
        
        # 取得シード数よりも出次数を持つノードが少ない場合, それらのみを選択
        # これによって, 確実に出次数が存在するノードをシードにする
        if len(deg_node_list) == 0: # 出次数を持つノードが存在しない場合は, 全グラフからノードを適当に取得
            self.sampled_graph.add_nodes_from(random.sample(list(complete_graph), nodes_to_sample))
        else:
            if len(deg_node_list) < number_of_seeds:
                seed_set = set(deg_node_list)
            else:
                seed_set = random.sample(deg_node_list, number_of_seeds)
            self.sampled_graph.add_nodes_from(list(seed_set))
        
            # 以下, エッジ追加プログラム
            flag = 0
            
            while True:
                new_seed_set = set()
                add_edge_set = set()
                
                # 種ノードの内, 一つのノードに着目する
                # 追加するエッジ, 新たなシードの候補探し
                for current_node in seed_set:
                    neighbor_deg = [] # 出隣接ノードの次数リスト
                    
                    # 現在ノードの出隣接ノード : neighbor_node を key に, リストに各ノードの次数を追加
                    for neighbor_node in list(copy_graph.successors(current_node)):
                        neighbor_deg.append([neighbor_node, len(list(copy_graph.successors(neighbor_node)))])
                    # neighbor_deg を降順に並べる
                    deg_rank = sorted(neighbor_deg, key=lambda x:x[1], reverse=True)
                    
                    # top k 個の k の値を決定
                    number_of_top_nodes = int(self.top_k_ratio * len(neighbor_deg))
                    
                    # k が 0 になったら 1 にして, 確実に隣接ノードを取得する
                    if number_of_top_nodes == 0:
                        number_of_top_nodes = 1
                    
                    # 取得するノードセット
                    tmp_list = []
                    for i in range(number_of_top_nodes):
                        tmp_list.append(deg_rank[i][0])
                    
                    new_seed_set.update(set(tmp_list))
                    
                    # 追加するエッジを格納
                    for neighbor_node in tmp_list:
                        add_edge_set.add((current_node, neighbor_node))
                
                # 実際にエッジを追加する部分
                for edge in add_edge_set:
                    self.sampled_graph.add_edge(edge[0], edge[1])
                    copy_graph.remove_edge(edge[0], edge[1])
                    if len(list(self.sampled_graph)) == nodes_to_sample:
                        flag = 1
                        break
                    elif len(list(self.sampled_graph)) > nodes_to_sample:
                        self.sampled_graph.remove_node(edge[1])
                        flag = 1
                        break
                
                if flag == 1:
                    break
                
                # 新たなシード選択部分
                # シードノードに出次数を有するノードが無い場合, 検討が必要. ある場合はそのまま続けてOK
                tmp_set = set() # 出次数を持つノードだけ格納
                
                for seed in new_seed_set:
                    if len(list(copy_graph.successors(seed))) != 0:
                        tmp_set.add(seed)
                
                if len(tmp_set) != 0: # 出次数を持つシードが存在する場合
                    seed_set = tmp_set
                else: # 新たにシードを探す必要がある
                    # 出次数がある全ノードを取得
                    deg_node_list = []
                    
                    for node in list(copy_graph):
                        if len(list(copy_graph.successors(node))) != 0:
                            deg_node_list.append(node)
                    
                    # 取得シード数よりも出次数を持つノードが少ない場合, それらのみを選択
                    # これによって, 確実に出次数が存在するノードをシードにする
                    if len(deg_node_list) == 0: # 出次数を持つノードが存在しない場合は, 全グラフからノードを適当に取得
                        while len(list(self.sampled_graph)) != nodes_to_sample:
                            random_node = random.choice(list(copy_graph))
                            self.sampled_graph.add_node(random_node)
                        flag = 1
                    else:
                        if len(deg_node_list) < number_of_seeds:
                            seed_set = set(deg_node_list)
                        else:
                            seed_set = random.sample(deg_node_list, number_of_seeds)
                        
                        # 追加するとノード数が取得数を超えてしまう場合
                        if (len(list(self.sampled_graph)) + len(seed_set)) >= nodes_to_sample:
                            add_node_list = random.sample(list(seed_set), nodes_to_sample - len(list(self.sampled_graph)))
                            self.sampled_graph.add_nodes_from(add_node_list)
                            flag = 1
                        else:
                            self.sampled_graph.add_nodes_from(list(seed_set))
                    
                if flag == 1:
                    break          
        
        # if len(list(self.sampled_graph)) != nodes_to_sample:
        #     print("Error!")
        #     print("Node Sub : {}".format(len(list(self.sampled_graph)) - nodes_to_sample))
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RD_Time  :", tim)
              
        return self.sampled_graph