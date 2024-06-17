import networkx as nx
import random
import time

class RE:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
    
    def random_edge_sampling(self, complete_graph, nodes_to_sample):
        time_start = time.perf_counter()

        # .edges() はそのままだと型がリストではなくてrandom.choice が使えなさそうなので, 一回リスト型に入れ替える
        # ↑ は　list() を使えば解決しそうだが, while 文で毎回 list に変換する手間がかかるから(？)実行時間が 10 倍ほどになった
        # かなり違うので他の場面でも気をつけると良い
        
        edge_set = set(complete_graph.edges())
        node_list = list(complete_graph)

        # 計算を高速化するために, ある程度は一括で取ってきちゃう. 無くても良い部分.        
        if (len(list(edge_set)) >= int(nodes_to_sample / 2) - 1) and (int(nodes_to_sample / 2) - 1) > 0:
            tmp_list = random.sample(list(edge_set), int(nodes_to_sample / 2) - 1)
            self.sampled_graph.add_edges_from(tmp_list)
            edge_set = edge_set ^ set(tmp_list)
                
        if self.sampled_graph.number_of_nodes() > nodes_to_sample:
            print("Error_1!")
            exit(1)
        
        while self.sampled_graph.number_of_nodes() < nodes_to_sample: 
            # ノード数が規定サンプル数に達したら終了, 2個追加される場合は != では検知できないので注意!
            if len(edge_set) != 0:
                selected_edge = random.choice(list(edge_set))
                                
                if (nodes_to_sample - self.sampled_graph.number_of_nodes()) == 1:
                    if (selected_edge[0] not in list(self.sampled_graph)) and (selected_edge[1] not in list(self.sampled_graph)):
                        selected_node_list = [selected_edge[0], selected_edge[1]]
                        selected_node = random.choice(selected_node_list)
                        self.sampled_graph.add_node(selected_node)
                    else:
                        self.sampled_graph.add_edge(selected_edge[0], selected_edge[1])
                else:
                    self.sampled_graph.add_edge(selected_edge[0], selected_edge[1])
                
                edge_set.remove(selected_edge)
            else:
                print("ここまで来たよ")
                selected_node = random.choice(node_list)
                self.sampled_graph.add_node(selected_node)
                node_list.remove(selected_node)
        
        if self.sampled_graph.number_of_nodes() != nodes_to_sample:
            print("Error_2!")
            exit(1)
            
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RE_Time  :", tim)
                    
        return self.sampled_graph