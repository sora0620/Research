import networkx as nx
import Calc
import json
import concurrent.futures

READ_FILE = "../../Dataset/Origin/{}.adjlist"
WRITE_FILE = "../../Dataset/PPR/{}_p.json"

# 任意のグラフにおいて、各ノードに対する PPR を計算するプログラム
# PPR のデータ保存用に作ったけどめちゃめちゃ時間がかかるので放置

# ハイパーパラメータ
graph_name = "p2p-Gnutella24"

path = READ_FILE.format(graph_name)
save_path = WRITE_FILE.format(graph_name)
graph = Calc.read_graph(path)
node_list = list(graph)

def calc_ppr_single(node):
    weight_dict = {tmp_node: 0 for tmp_node in node_list}
    weight_dict[node] = 1
    print(node)
    
    return node, nx.pagerank(graph, personalization=weight_dict)

def calc_ppr():
    ppr_dict = {} # 起点とするノードをkey, その key に対する全てのノードの PPR 辞書を value とする. 要するに, 辞書の辞書.
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(calc_ppr_single, node_list)
        
        for node, result in results:
            ppr_dict[node] = result
    
    return ppr_dict

def write_json(ppr_dict, save_path):
    with open(save_path, "w") as f:
        json.dump(ppr_dict, f, indent=4, sort_keys=True)

def main():
    ppr_dict = calc_ppr()
    write_json(ppr_dict, save_path)

if __name__ == "__main__":
    main()
    

# # 並列化なしの場合
# # 色々実験してみた結果、並列化は上手くできているっぽいので、基本的には上記のやつを使っちゃって大丈夫
# import networkx as nx
# import Calc
# import json

# READ_FILE = "../../Dataset/Origin/{}.adjlist"
# WRITE_FILE = "../../Dataset/PPR/{}.json"

# def calc_ppr(graph):
#     ppr_dict = {}
#     node_list = list(graph)
    
#     for i, node in enumerate(node_list):
#         weight_dict = {}
#         for tmp_node in node_list:
#             weight_dict[tmp_node] = 0
#         weight_dict[node] = 1
        
#         ppr_dict[node] = nx.pagerank(graph, personalization=weight_dict)
#         print(i)
    
#     return ppr_dict

# def write_json(ppr_dict, save_path):
#     with open(save_path, "w") as f:
#         json.dump(ppr_dict, f, indent=4, sort_keys=True)

# def main():
#     # ハイパーパラメータ
#     graph_name = "com"
    
#     path = READ_FILE.format(graph_name)
#     save_path = WRITE_FILE.format(graph_name)
#     graph = Calc.read_graph(path)
    
#     ppr_dict = calc_ppr(graph)
#     write_json(ppr_dict, save_path)

# if __name__ == "__main__":
#     main()