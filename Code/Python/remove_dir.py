import os
import shutil

# 選択ディレクトリ以下の情報を全て消去してしまうので注意！

REMOVE_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}" # 削除したいディレクトの 1 つ前までを指定

def remove_dir(div, partition, graph, num, remove):
    # remove には、消去したいファイル or ディレクトリ名を入力
    # 一回のremove_dir では, 1つのファイル or ディレクトリが削除される
    
    dir = REMOVE_FILE.format(div, partition, graph, num, size)
    dir_list = os.listdir(dir)
    
    if remove in dir_list:
        shutil.rmtree(dir+"/"+remove) # ディレクトリごと全て削除
        # os.remove(dir+"/"+remove)       # ファイルを削除
        

div_list = [2, 10]
partition_list = ["RN", "BFS", "BISECTION", "NXMETIS"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0, 1, 2] # NXMETIS の時だけ, [0] にする
# size_list = ["0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08", "0.09", "0.10",
#              "0.12", "0.14", "0.16", "0.18", "0.20", "0.22", "0.24", "0.26", "0.28", "0.30"]
size_list = ["free"]
sampling_list = ["FF", "RD", "RE", "RPN", "SRW", "TPN_re", "TP_rep"]

for div in div_list:
    for partition in partition_list:
        for graph in graph_list:
            if partition == "NXMETIS":
                tmp_list = [0]
            else:
                tmp_list = num_list
            for num in tmp_list:
                for size in size_list:
                        remove_dir(div, partition, graph, num, size)