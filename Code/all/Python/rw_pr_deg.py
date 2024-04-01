import networkx as nx
import matplotlib.pyplot as plt
import Calc
import japanize_matplotlib
import matplotlib.ticker as ptick
import json

# RW 回数を変化させた際に, 入次数と PR 変化に多少相関があるのではないかという考え

DEFAULT_FLOW = 1000
CHANGE_FLOW = 1500

# JSON ファイルを読み込み, 結果を返す
# 返り値
# key : node, value : [PR 値, 入次数]
def load_json(path):
    return_dict = {}
    with open(path, 'r') as f:
        j = json.load(f)
        
        for node, pr_deg_list in j.items():
            return_dict[int(node)] = pr_deg_list
    
    return return_dict

# 実際に結果を取得する関数
def get_value(graph_name, default_flow, change_flow):
    default_path = f"../../Dataset/Static/RW/{graph_name}/{default_flow}_{default_flow}.json"
    change_path = f"../../Dataset/Static/RW/{graph_name}/{default_flow}_{change_flow}.json"
    
    default_dict = load_json(default_path)
    change_dict = load_json(change_path)
    
    return default_dict, change_dict

def disp(graph_name, default_flow, change_flow, node_list):
    default_result, change_result = get_value(graph_name, default_flow, change_flow) # 値の取得
    x_list = [] # PR 変化量
    y_list = [] # ノードの入次数
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    # PR 変化量と入次数の関係
    # for node in node_list:
    #     x_list.append(abs(default_result[node][0] - change_result[node][0]))
    #     y_list.append(default_result[node][1])
    # ax.set_xlabel("入次数")
    # save_file = f"../../Picture/RW変化に対するPRとDEG/{graph_name}/{default_flow}_{change_flow}.png"
    
    for node in node_list:
        x_list.append(default_result[node][0])
        y_list.append(default_result[node][0] - change_result[node][0])
    ax.set_xlabel("元のPR値")
    save_file = f"../../Picture/RW変化に対するPR変化量とPR/{graph_name}/{default_flow}_{change_flow}.png"
    
    ax.set_ylabel("PR 変化量")
    fig.suptitle(graph_name)
    plt.rcParams["font.size"] = 18
    plt.ticklabel_format(style='plain')
    plt.tight_layout()
    
    ax.scatter(x_list, y_list, s=10)
    
    # 保存
    ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style="sci", axis="x", scilimits=(0,0))
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
    plt.savefig(save_file)
    plt.close()

def main():
    graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"]
    
    for graph_name in graph_list:
        graph = Calc.read_origin_graph(graph_name)
        disp(graph_name, DEFAULT_FLOW, CHANGE_FLOW, list(graph))

if __name__ == "__main__":
    main()