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
        
        edge_list = list(complete_graph.edges())
        node_list = list(complete_graph)
        
        while self.sampled_graph.number_of_nodes() != nodes_to_sample: 
            # ノード数が規定サンプル数に達したら終了, 2個追加される場合は != では検知できないので注意!
            if len(edge_list) != 0:
                selected_edge = random.choice(edge_list)
                
                if (nodes_to_sample - self.sampled_graph.number_of_nodes()) == 1:
                    if (selected_edge[0] not in list(self.sampled_graph)) and (selected_edge[1] not in list(self.sampled_graph)):
                        selected_node_list = [selected_edge[0], selected_edge[1]]
                        selected_node = random.choice(selected_node_list)
                        self.sampled_graph.add_node(selected_node)
                    else:
                        self.sampled_graph.add_edge(selected_edge[0], selected_edge[1])
                else:
                    self.sampled_graph.add_edge(selected_edge[0], selected_edge[1])
                
                edge_list.remove(selected_edge)
            else:
                selected_node = random.choice(node_list)
                self.sampled_graph.add_node(selected_node)
                node_list.remove(selected_node)
                
            # 辺を追加した際, その頂点が存在しない場合勝手に頂点も追加されるらしいので, 下のコードは無駄な気がするのでとりあえずコメントアウト
            '''
            if selected_edge[0] not in list(sampled_graph.nodes()):
                sampled_graph.add_node(selected_edge[0])
            if selected_edge[1] not in list(sampled_graph.nodes()):
                sampled_graph.add_node(selected_edge[1])
            '''
            
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("RE_Time  :", tim)
                    
        return self.sampled_graph