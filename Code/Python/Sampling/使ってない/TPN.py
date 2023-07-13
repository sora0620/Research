import networkx as nx
import time

# TP だと、web-Google のような PR 値の小さな多数のノード群から支持されているような場合に、 上位ノードしか取得しないために途端に支持が弱まってしまう。
# そこで、上位ノード + そのノードの全隣接ノードを取ってくるような手法を試してみる。こうすることで、PR が小さにノードからの支持もうけつつ、PR 上位のノードも残せる。

class TPN:
    def __init__(self):
        self.sampled_graph = nx.DiGraph()
        
    def top_pagerank_sampling(self, complete_graph, nodes_to_sample, rate):
        # rate : 隣接ノードから何割持ってくるか. PR の高い順から持ってくるようにする
        
        time_start = time.perf_counter()
        
        pr_origin = nx.pagerank(complete_graph)
        pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)

        pr_rank = 0
        
        while len(list(self.sampled_graph)) != nodes_to_sample:
            high_pr_node = pr_sorted[pr_rank][0]
            self.sampled_graph.add_node(high_pr_node)
            
            neighbors_num = 0
            neighbor_dict = {}
            
            for adj_node in list(complete_graph.predecessors(high_pr_node)):
                neighbor_dict[adj_node] = pr_origin[adj_node]
                neighbors_num += 1
                
            neighbor_dict = sorted(neighbor_dict.items(), key=lambda x:x[1], reverse=True)
            neighbors_num = int(neighbors_num * rate)
            
            for i in range(neighbors_num):
                # rate = 1 のとき, 最後だけ PR 上位から取ってくるような設計になってることに注意
                if len(list(self.sampled_graph)) == nodes_to_sample:
                    break
                self.sampled_graph.add_node(neighbor_dict[i][0])
            
            pr_rank += 1
        
        node_list = list(self.sampled_graph)
        for current_node in node_list:
            for adjancency_node in list(complete_graph.successors(current_node)):
                if adjancency_node in node_list:
                    self.sampled_graph.add_edge(current_node, adjancency_node)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("TPN_Time  :", tim)
              
        return self.sampled_graph