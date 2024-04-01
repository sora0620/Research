import networkx as nx
import random
import Calc
import matplotlib.pyplot as plt
from collections import defaultdict
import japanize_matplotlib
import matplotlib.ticker as ptick
import time
import datetime
import json

ALPHA = 0.85
RANDOM_WALK_NUM = 1000            # 通常の RW 回数
CHANGE_FLOW_NUM = RANDOM_WALK_NUM # 流量を変化させたい際の RW の値

# 関数
# 境界ノード (RW 流量を変えたいノード群) のリストと指定流量を引数にとる
# 個別に流量を変えられるようにしてもいいが, とりあえずは流量を変えたいノードの流量は全て統一とする
# それ以外のノードの流量は固定値 (RANDOM_WALK_NUM) で統一
def setting_random_walk_flow(change_node_list, change_flow, node_set):
    flow_dict = {}
    for node in (node_set - set(change_node_list)):
        flow_dict[node] = RANDOM_WALK_NUM
    for node in change_node_list:
        flow_dict[node] = change_flow
    
    return flow_dict

# 関数
# 任意の１ノードの PPR を RW で算出
# RW の回数は random_walk_num で指定. これが大きいほど値が収束しやすい
# 確率 ALPHA で始点ノードに戻り、１カウント

# 引数
#        adj_dict : グラフの入隣接辞書
#      start_node : 始点ノード
# random_walk_num : ランダムウォークを行う回数

# 返り値 : 各ノードの訪問回数を辞書型で返す
def visited_count_from_one_node(adj_dict, start_node, random_walk_num):
    rw_count_dict = defaultdict(int) # RW が訪れた回数を各ノードにおいて記録
    
    # 毎回 0 ~ 1 の乱数を発生させ, ALPHA を超えたらその RW は終了
    for _ in range(random_walk_num):
        current_node = start_node # RW の現在ノード
        rw_count_dict[current_node] += 1
        while True:
            next_node = random.choice(adj_dict[current_node]) # 遷移先ノードを選択
            rw_count_dict[next_node] += 1 # 訪問したノードをインクリメント
            current_node = next_node # 現在ノードを遷移先ノードに変更
            
            # 終了判定
            if random.random() > ALPHA:
                break
        
    return rw_count_dict

# 関数
# 全てのノードを始点として訪問回数を求める

# 引数
# グラフ

# 返り値
# key_1 : ノード, value_1 : {key_2 : ノード, value_2 : key_1 を始点とした RW の各ノードに対する訪問回数}
def visited_count_from_all_node(graph, change_node_list, change_flow):
    node_set = set(list(graph)) # 全ノード
    adj_dict = {} # 辞書型の隣接リスト
    
    # 隣接リスト作成
    for node in node_set:
        adj_dict[node] = list(graph.successors(node))
    
    # 出次数が 0 のノードからは全てのノードに対してエッジを張る
    for node, adj_list in adj_dict.items():
        if len(adj_list) == 0:
            for tmp_node in node_set:
                adj_dict[node].append(tmp_node)
        
    count_dict = {} # 全ノードに対する各ノードからの訪問回数を記録. 辞書の辞書の様な入れ子型
    flow_dict = setting_random_walk_flow(change_node_list, change_flow, node_set)
    
    for node in node_set:
        count_dict[node] = visited_count_from_one_node(adj_dict, node, flow_dict[node])
    
    return count_dict

# 関数
# 各ノードに RWer が訪れた回数を返す

# 返り値
# {key : ノード, value : RWer が通過した回数}
def return_rw_dict(graph, change_node_list, change_flow):
    time_start = time.perf_counter()
    print("RW Start Time : ", end="")
    print(datetime.datetime.now())
    tmp_dict = visited_count_from_all_node(graph, change_node_list, change_flow)
    return_dict = defaultdict(int)
    
    for node in list(graph):
        for key, value in tmp_dict[node].items():
            return_dict[key] += value
            
    time_end = time.perf_counter()
    tim = time_end - time_start
    print(f"RW に要した時間 : {tim}")
    
    return return_dict

# 関数
# 各ノードから見た PPR を返す関数

# 引数
# グラフ

# 返り値
# key_1 : ノード, value_1 : {key_2 : ノード, value_2 : key_1 を始点とした各ノードに対する PPR 値}
def return_ppr_dict(graph, change_node_list, change_flow):
    count_dict = visited_count_from_all_node(graph, change_node_list, change_flow)
    
    for node in list(graph):
        count_sum = sum(count_dict[node].values())
        for key, value in count_dict[node].items():
            count_dict[node][key] = value / count_sum
    
    return count_dict

# 関数
# PR は PPR の RW を各ノード個別にではなくすべてのノードに対して合計した値なので, 
# calc_ppr の各ノードに対する RW 回数を合計した値を全ての合計値で割って正規化した値が PR となる (はず)
# その様な実装を行う

# 引数
# グラフ

# 返り値
# key : ノード, value : PR 値 の辞書型
def calc_pr(graph, change_node_list, change_flow):
    time_start = time.perf_counter()
    print("PR Calc Start Time : ", end="")
    print(datetime.datetime.now())
    
    count_dict_pr = return_rw_dict(graph, change_node_list, change_flow) # PR 用のグローバルに訪問回数を格納した辞書
    
    count_sum = sum(count_dict_pr.values())
    for key, value in count_dict_pr.items():
        count_dict_pr[key] = value / count_sum  
    
    time_end = time.perf_counter()
    tim = time_end - time_start
    print(f"計算に要した時間 : {tim}")
    
    return count_dict_pr

# 関数
# 境界ノードを指定後, そこから開始する RW を変化させることでユーザの興味・関心グラフの変化によって生じた RW 流入量変化と仮定して実験
# 流入量変化前後 (変化前は RANDOM_WALK_NUM で固定) の各ノードの RW 流量変化を図で出力
# 横軸元の PR, 縦軸変化量

# 引数
# graph : グラフ
# change_node_list : 境界ノードのノードリスト
# change_flow : change_node_list で指定した各ノードを始点とした RW の試行回数
def disp_flow_change(graph_name, graph, change_node_list, change_flow):
    node_set = set(list(graph))
    pr_origin = nx.pagerank(graph)
    rw_dict_default = visited_count_from_all_node(graph, [], RANDOM_WALK_NUM) # 流量変化無しでの訪問回数
    print("Default RW Finished!")
    rw_dict_flow_changed = visited_count_from_all_node(graph, change_node_list, change_flow) # 流量変化をさせた際の訪問回数
    print("Flow_Changed RW Finished!")
    
    # default において, 各ノードの訪問回数を合計 (PR 的)
    tmp_dict = defaultdict(int) # PR 用のグローバルに訪問回数を格納した辞書
    
    for node in list(graph):
        for key, value in rw_dict_default[node].items():
            tmp_dict[key] += value
    rw_dict_default = tmp_dict
    
    # changed において, 各ノードの訪問回数を合計 (PR 的)
    tmp_dict = defaultdict(int) # PR 用のグローバルに訪問回数を格納した辞書
    
    for node in list(graph):
        for key, value in rw_dict_flow_changed[node].items():
            tmp_dict[key] += value
    rw_dict_flow_changed = tmp_dict
    
    x_list = []
    y_list = []
    
    for node in node_set:
        x_list.append(pr_origin[node])
        y_list.append(rw_dict_flow_changed[node] - rw_dict_default[node])
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_xlabel("PR")
    ax.set_ylabel("RW 訪問数の変化差分")
    fig.suptitle("RW 訪問数の変化差分")
    plt.rcParams["font.size"] = 18
    plt.ticklabel_format(style='plain')
    plt.tight_layout()
    ax.scatter(x_list, y_list, s=10)
    
    # 保存
    ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style="sci", axis="x", scilimits=(0,0))
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
    save_file = "../../Picture/RW訪問数の変化/{}.png"
    plt.savefig(save_file.format(graph_name))
    plt.close()

# 関数
# 実装が合っているかの値の確認用
# 実行には "practice.adjlist" を利用すると良い
def check_def(graph, change_node_list, change_flow):
    print(graph) # グラフのノード数、エッジ数出力
    print("-----------------------------------")
    
    node_list = list(graph)
    graph_size = len(node_list)
    disp_size = 5
    if disp_size > graph_size:
        disp_size = graph_size

    pr = nx.pagerank(graph, alpha=ALPHA)
    pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

    x_data = []
    for item in pr_sort:
        x_data.append(item[0])

    print("Networkx")
    for i in range(disp_size):
        print(f"Node ID : {x_data[i]} | PR value : {pr[x_data[i]]}")
    print("----------------------------")
    
    ppr_sum_dic = calc_pr(graph, change_node_list, change_flow)
    ppr_sum_dic_sort = sorted(ppr_sum_dic.items(), key=lambda x:x[1], reverse=True)
    y_data = []
    for item in ppr_sum_dic_sort:
        y_data.append(item[0])

    print("use PPR")
    for i in range(disp_size):
        print(f"Node ID : {y_data[i]} | PR value : {ppr_sum_dic[y_data[i]]}")
    print("----------------------------")

# 関数
# 毎回 RW をし直していると時間がかかる & 毎回多少の結果誤差が生じてしまうので, .json に保存していつでも取り出せる形にする
def write_rw(graph_name, rw_result):
    path = f"../../Dataset/Static/RW/{graph_name}/{RANDOM_WALK_NUM}_{CHANGE_FLOW_NUM}.json"
    with open(path, 'w') as f:
        json.dump(rw_result, f, indent=4, sort_keys=True)

def disp_nx_pr(graph):
    print(graph) # グラフのノード数、エッジ数出力
    print("-----------------------------------")
    
    node_list = list(graph)
    graph_size = len(node_list)
    disp_size = 5
    if disp_size > graph_size:
        disp_size = graph_size

    pr = nx.pagerank(graph, alpha=ALPHA)
    pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

    x_data = []
    for item in pr_sort:
        x_data.append(item[0])

    print("Networkx")
    for i in range(disp_size):
        print(f"Node ID : {x_data[i]} | PR value : {pr[x_data[i]]}")

# 関数
def main():
    # ハイパーパラメータ
    graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"]
    change_flow = CHANGE_FLOW_NUM
    
    for graph_name in graph_list:
        graph = Calc.read_origin_graph(graph_name)
        
        # ハイパーパラメータ
        # change_node_list = [random.choice(list(graph))]
        
        disp_flow_change(graph_name, graph, change_node_list, change_flow)

# 関数
# 実装が合っているかの値の確認用
# 実行には "practice.adjlist" を利用すると良い
def main_check():
    graph_name = "practice"
    change_node_list = []
    change_flow = RANDOM_WALK_NUM
    
    graph = Calc.read_origin_graph(graph_name)
    check_def(graph, change_node_list, change_flow)

# 関数
# RW 回数を .json ファイルに記載
def main_write():
    # ハイパーパラメータ
    graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"]
    change_flow = CHANGE_FLOW_NUM
    
    for graph_name in graph_list:
        graph = Calc.read_origin_graph(graph_name)
        
        # ハイパーパラメータ
        change_node_list = [random.choice(list(graph))]
        
        tmp_dict = return_rw_dict(graph, change_node_list, change_flow)
        write_rw(graph_name, tmp_dict)

def main_pr():
    graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"]
    
    for graph_name in graph_list:
        graph = Calc.read_origin_graph(graph_name)
        disp_nx_pr(graph)

if __name__ == "__main__":
    main_pr()