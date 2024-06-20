import networkx as nx
import time
import random
import json

# この方法では、重み付けしたノードが必ずしも残るとは限らないので、そこだけ注意かな. 必ず残っている必要があるとも限らないけど

ALPHA = 0.15 # RW の終了確率

class FC:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
    
    # default_weight の設定を追加後
    # 今までの通常のやつ
    def flow_control_sampling(self, origin_graph, sampling_rate, connect_node_list, weight_dict):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        node_list = list(origin_graph)
        edge_list = list(origin_graph.edges())
        
        print("FC サンプリング, PPR 計算開始")
        
        # 任意の１ノードを起点とした PPR 辞書を取得
        def get_ppr(source_node):
            ppr_weight = {node: 0 for node in node_list}
            ppr_weight[source_node] = 1
            
            ppr_dict = nx.pagerank(origin_graph, personalization=ppr_weight)
            
            return ppr_dict
        
        # 境界ノードの PPR 取得
        ppr_dict = {} # 各ノードの PPR を, 辞書の辞書に格納
        
        for node in connect_node_list:
            ppr_dict[node] = get_ppr(node)
        
        print("PPR Calculated!")
        
        # 各エッジを流れる RW 流量を計算
        edge_weight = {}
        for edge in edge_list:
            edge_weight[edge] = 0
            for node in connect_node_list:
                edge_weight[edge] += ppr_dict[node][edge[0]] * ((1 - ALPHA) / ALPHA) / origin_graph.out_degree(edge[0]) * weight_dict[node]

        edge_weight_sorted = sorted(edge_weight.items(), key=lambda x: x[1], reverse=True)
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        sampling_edge_list = []
        
        for edge, weight in edge_weight_sorted[:sampling_edge_num]:
            sampling_edge_list.append(edge)
        
        self.sampled_graph.add_edges_from(sampling_edge_list)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FC_Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph

    # FC では PPR 計算を行わず, 既存の結果を利用することで計算 → 引数 : ppr_dict
    # ppr_dict は以下で定義
        '''
        # 任意の１ノードを起点とした PPR 辞書を取得
        def get_ppr(source_node):
            ppr_weight = {node: 0 for node in node_list}
            ppr_weight[source_node] = 1
            
            ppr_dict = nx.pagerank(origin_graph, personalization=ppr_weight)
            print(source_node)
            
            return ppr_dict
        
        # 境界ノードの PPR 取得
        ppr_dict = {} # 各ノードの PPR を, 辞書の辞書に格納
        
        for node in connect_node_list:
            ppr_dict[node] = get_ppr(node)
        '''
    
    # 後々 PPR 結果を再利用する形にする場合や, 様々なサンプリングサイズに対して実験を行いたい際に, 何度も同じ PPR 計算をしてしまっているのでその効率化
    def read_flow_control_sampling(self, origin_graph, sampling_rate, connect_node_list, weight_dict, ppr_dict):
        if sampling_rate == 1:
            return origin_graph
        time_start = time.perf_counter()
        
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        
        edge_weight = {}
        for edge in edge_list:
            edge_weight[edge] = 0
            for node in connect_node_list:
                edge_weight[edge] += ppr_dict[node][edge[0]] * ((1 - ALPHA) / ALPHA) / origin_graph.out_degree(edge[0]) * weight_dict[node]

        edge_weight_sorted = sorted(edge_weight.items(), key=lambda x: x[1], reverse=True)
        sampling_edge_list = []
        
        for edge, weight in edge_weight_sorted[:sampling_edge_num]:
            sampling_edge_list.append(edge)
        
        self.sampled_graph.add_edges_from(sampling_edge_list)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FC_Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph

    # 複数のサンプリングサイズに対してサンプリングする場合, 毎回計算を行う必要はない
    def read_rate_flow_control_sampling(self, origin_graph, sampling_rate_list, edge_weight_sorted):
        time_start = time.perf_counter()
        
        edge_list = list(origin_graph.edges())

        graph_list = []
        for rate in sampling_rate_list:
            if rate == 1:
                graph_list.append(origin_graph)
                continue
            tmp_graph = nx.DiGraph()
            sampling_edge_num = int(len(edge_list) * rate)
            sampling_edge_list = [edge for edge, weihgt in edge_weight_sorted[:sampling_edge_num]]
            tmp_graph.add_edges_from(sampling_edge_list)
            graph_list.append(tmp_graph)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FC_Time  :", tim)
        
        return graph_list
    
    # 境界ノードの優先付着がトップ (次数が高いノードを上から) のノードに対して FC を行う
    def fc_top_prefer_sampling(self, origin_graph, sampling_rate, weight_node_num, weight_dict):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph
        
        node_list = list(origin_graph)
        edge_list = list(origin_graph.edges())
        connect_node_list = []
        deg_dict = {}
        for node in node_list:
            deg_dict[node] = origin_graph.in_degree(node)
        deg_dict_sorted = sorted(deg_dict.items(), key=lambda x: x[1], reverse=True)
        
        for i in range(weight_node_num):
            connect_node_list.append(deg_dict_sorted[i][0])
        
        print("FC サンプリング, PPR 計算開始")
        
        # 任意の１ノードを起点とした PPR 辞書を取得
        def get_ppr(source_node):
            ppr_weight = {node: 0 for node in node_list}
            ppr_weight[source_node] = 1
            
            ppr_dict = nx.pagerank(origin_graph, personalization=ppr_weight)
            
            return ppr_dict
        
        # 境界ノードの PPR 取得
        ppr_dict = {} # 各ノードの PPR を, 辞書の辞書に格納
        
        for node in connect_node_list:
            ppr_dict[node] = get_ppr(node)
        
        print("PPR Calculated!")
        
        edge_weight = {}
        for edge in edge_list:
            edge_weight[edge] = 0
            for node in connect_node_list:
                edge_weight[edge] += ppr_dict[node][edge[0]] * ((1 - ALPHA) / ALPHA) / origin_graph.out_degree(edge[0]) * weight_dict[node]

        edge_weight_sorted = sorted(edge_weight.items(), key=lambda x: x[1], reverse=True)
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        sampling_edge_list = []
        
        for edge, weight in edge_weight_sorted[:sampling_edge_num]:
            sampling_edge_list.append(edge)
        
        self.sampled_graph.add_edges_from(sampling_edge_list)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FC_top_prefer Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph

    # 境界ノードをランダムにして, FC を複数回やった際に、出現した回数が多いエッジを上から順番に取得
    def fc_random_sampling(self, origin_graph, graph_name, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph

        path = "../../../Dataset/Sampling_Edge/{}_random.json".format(graph_name)
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        edge_dict = {}
        
        with open(path, 'r') as f:
            edge_dict = json.load(f)
        
        edge_sorted = sorted(edge_dict.items(), key=lambda x: x[1], reverse=True)
        
        for i in range(sampling_edge_num):
            key = edge_sorted[i][0]
            if key == "sampling_num":
                continue
            source_node, target_node = map(int, key.split())
            self.sampled_graph.add_edge(source_node, target_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FC_random Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph

    # 境界ノードを優先付着の確率にして, FC を複数回やった際に、出現した回数が多いエッジを上から順番に取得
    def fc_prefer_sampling(self, origin_graph, graph_name, sampling_rate):
        time_start = time.perf_counter()
        
        if sampling_rate == 1:
            return origin_graph

        path = "../../../Dataset/Sampling_Edge/{}_prefer.json".format(graph_name)
        edge_list = list(origin_graph.edges())
        sampling_edge_num = int(len(edge_list) * sampling_rate)
        edge_dict = {}
        
        with open(path, 'r') as f:
            edge_dict = json.load(f)
        
        edge_sorted = sorted(edge_dict.items(), key=lambda x: x[1], reverse=True)
        
        for i in range(sampling_edge_num):
            key = edge_sorted[i][0]
            if key == "sampling_num":
                continue
            source_node, target_node = map(int, key.split())
            self.sampled_graph.add_edge(source_node, target_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("FC_prefer Time  :", tim)
        print("Sampling_Graph: ", self.sampled_graph)
        
        return self.sampled_graph