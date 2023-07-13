import os

def make_dir(dir):
    if dir == "partition":
        file_name = "../../Dataset/Partition/div_{}/{}"
        for div in div_list:
            for partition in partition_list:
                dir_path = file_name.format(div, partition)
                os.mkdir(dir_path)
    elif dir == "graph":
        file_name = "../../Dataset/Partition/div_{}/{}/{}"
        for div in div_list:
            for partition in partition_list:
                for graph in graph_list:
                    dir_path = file_name.format(div, partition, graph)
                    os.mkdir(dir_path)
    elif dir == "num":
        file_name = "../../Dataset/Partition/div_{}/{}/{}/num_{}"
        for div in div_list:
            for partition in partition_list:
                for graph in graph_list:
                    if partition == "NXMETIS":
                        tmp_num = [0]
                    else:
                        tmp_num = num_list
                    for num in tmp_num:
                        dir_path = file_name.format(div, partition, graph, num)
                        os.mkdir(dir_path)
    elif dir == "size":
        file_name = "../../Dataset/Partition/div_{}/{}/{}/num_{}"
        for div in div_list:
            for partition in partition_list:
                for graph in graph_list:
                    if partition == "NXMETIS":
                        tmp_num = [0]
                    else:
                        tmp_num = num_list
                    for num in tmp_num:
                        dir_path = file_name.format(div, partition, graph, num)
                        os.mkdir(dir_path+"/origin")
                        os.mkdir(dir_path+"/detail")
                        for size in size_list:
                            os.mkdir(dir_path+f"/size_{size}")
    elif dir == "sampling":
        file_name = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}"
        for div in div_list:
            for partition in partition_list:
                for graph in graph_list:
                    if partition == "NXMETIS":
                        tmp_num = [0]
                    else:
                        tmp_num = num_list
                    for num in tmp_num:
                        for size in size_list:
                            for sampling in sampling_list:
                                dir_path = file_name.format(div, partition, graph, num, size, sampling)
                                os.mkdir(dir_path)
    elif dir == "ver":
        file_name = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}"
        for div in div_list:
            for partition in partition_list:
                for graph in graph_list:
                    if partition == "NXMETIS":
                        tmp_num = [0]
                    else:
                        tmp_num = num_list
                    for num in tmp_num:
                        for size in size_list:
                            for sampling in sampling_list:
                                for ver in ver_list:
                                    dir_path = file_name.format(div, partition, graph, num, size, sampling, ver)
                                    os.mkdir(dir_path)
                                    os.mkdir(dir_path+"/sampling")
                                    # os.mkdir(dir_path+"/detail")
    elif dir == "cent":
        file_name = "../../Dataset/Origin/Centrality/{}"
        for graph in graph_list:
            dir_path = file_name.format(graph)
            os.mkdir(dir_path)

div_list = [2, 10]
partition_list = ["RN", "BFS", "BISECTION", "NXMETIS"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0, 1, 2] # NXMETIS の時はちゃんと [0] になるようになってるので変えなくて OK
# size_list = ["0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08", "0.09", "0.10",
#              "0.12", "0.14", "0.16", "0.18", "0.20", "0.22", "0.24", "0.26", "0.28", "0.30"]
size_list = ["free"] # 内部エッジの本数によって縮小率を決定
sampling_list = ["FF", "RD", "RE", "RPN", "SRW", "TPN_re", "TP_rep"]
ver_list = [0, 1, 2]

# dir_list = ["partition"]
# dir_list = ["graph"]
# dir_list = ["num"]
# dir_list = ["size"]
# dir_list = ["sampling"]
dir_list = ["ver"]

for dir in dir_list:
    make_dir(dir)