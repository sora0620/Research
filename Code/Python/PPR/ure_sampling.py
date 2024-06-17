import networkx as nx
import Calc
import Sampling as sp
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

READ_FILE = "../../Dataset/Origin/{}.adjlist"

def make_plt(origin_list, sampled_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
    """
    １つのグラフを表示するための関数

    Parameters:
        figsize (taple): グラフ全体のサイズ
        graph_label (string): グラフの凡例 (名前表示)
        x_label (string): 横軸の名前
        y_label (string): 縦軸の名前
        title (string): グラフのタイトル
        axis (string): 軸の表記を設定. "plain" はそのまま, "sci" を指定すると指数表記になる. なお, [x 軸, y 軸] で指定
        save_path (string): .pngとして保存したい場合, パスを指定
    """
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # 元グラフ用
    ax.plot(origin_list[0], origin_list[1], c="red", label="縮小前")
    
    # 縮小グラフ用
    ax.scatter(sampled_list[0], sampled_list[1], c="blue", marker="x", label="縮小後")
    
    # ax の設定
    if title != None:
        ax.set_title(title)
    if x_label != None:
        ax.set_xlabel(x_label)
    if y_label != None:
        ax.set_ylabel(y_label)
    ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style=axis[0], axis="x", scilimits=(0,0))
    ax.ticklabel_format(style=axis[1], axis="y", scilimits=(0,0))
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.show()
    plt.legend()
    plt.close()

def return_sampling_graph(origin_graph, sampling_rate):
    obj = sp.RE()
    sampling_graph = obj.random_edge_sampling(origin_graph, sampling_rate)
    
    return sampling_graph

def return_list(origin_graph, sampling_rate, top_N, k_div):
    sampling_graph = return_sampling_graph(origin_graph, sampling_rate)
    node_set_sampled = set(list(sampling_graph))
    
    pr_origin = nx.pagerank(origin_graph)
    pr_sampled = nx.pagerank(sampling_graph)
    pr_origin_sorted = sorted(pr_origin.items(), key=lambda x: x[1], reverse=True)
    
    top_node_list = []
    for i in range(k_div):
        top_node_list.append(pr_origin_sorted[i][0])
        
    tmp_sum = 0
    for node in top_node_list:
        if node in node_set_sampled:
            tmp_sum += 1
    
    print("NDCG: {:.3}".format(Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_origin, k_div)))
    print(f"PR 上位 {k_div} ノードが縮小グラフに含まれる割合: {tmp_sum / k_div:.2}")
    
    x_list_before = []
    y_list_before = []
    x_list_after = []
    y_list_after = []
    
    for i in range(top_N):
        tmp_node = pr_origin_sorted[i][0] # 元グラフ PR 上位 i + 1 番目のノード
        x_list_before.append(i+1)
        y_list_before.append(pr_origin_sorted[i][1])
        
        if tmp_node in node_set_sampled:
            x_list_after.append(i+1)
            y_list_after.append(pr_sampled[tmp_node])
    
    origin_list = [x_list_before, y_list_before]
    sampled_list = [x_list_after, y_list_after]
    
    return origin_list, sampled_list

def main():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_rate = 0.2
    top_N = 100 # PR 何ノードを描画するか
    k_div = 100 # NDCG の評価範囲
    
    # 描画用パラメータ
    x_label = "順位"
    y_label = "PR 値"
    title = f"上位{top_N}ノードのPR分布"
    
    path = READ_FILE.format(graph_name)
    graph = Calc.read_graph(path)
    origin_list, sampled_list = return_list(graph, sampling_rate, top_N, k_div)
    make_plt(origin_list, sampled_list, x_label=x_label, y_label=y_label, title=title)

if __name__ == "__main__":
    main()