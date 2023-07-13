import time
import networkx as nx
import Calc
import Sampling as sp

EXCEL_NAME = "../../Excel/pr_calc_time.xlsx"
SHEET_NAME = "pr_calc_time"
ROW_SAMPLING_TIME = 3
ROW_SYNTHESIS_TIME = 4
ROW_PR_TIME = 5
DIV_NUM = 10
SAMPLING_RATE = 0.10
READ_DIV_FILE_SAMPLING = "../../Dataset/Partition/div_10/{}/{}/num_0/size_0.10/{}/ver_0/sampling/part_{}.adjlist"
READ_DIV_FILE_ORIGIN = "../../Dataset/Partition/div_10/{}/{}/num_0/origin/part_{}.adjlist"
READ_ORIGIN_FILE = "../../Dataset/Origin/Graph/{}.adjlist" # グラフ接続の際の参照用
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
partition_list = ["BFS", "BISECTION", "NXMETIS"]
sampling_list = ["TPN_re"] # SAMPLING_BOOL が False の時のみ使用
sampling_bool = [True, False] # True -> サンプリングしていない分割グラフに対して計算; False -> サンプリングした分割グラフに対して計算

# 各分散グラフは分散サーバ上にあると考える。
# 元グラフの方は接続、PR計算の2段階
# サンプリンググラフの方はサンプリング、接続、PR計算の3段階で計算する

def excel_value(sb, partition, graph):
    if graph == "p2p-Gnutella24":
        column = 2 + 2 * 0
    elif graph == "scale_free":
        column = 2 + 2 * 1
    elif graph == "wiki-Talk":
        column = 2 + 2 * 2
    elif graph == "web-Google":
        column = 2 + 2 * 3
    elif graph == "soc-Epinions1":
        column = 2 + 2 * 4
    elif graph == "amazon0601":
        column = 2 + 2 * 5
    
    if partition == "BFS":
        row_add = 6 * 0
    elif partition == "NXMETIS":
        row_add = 6 * 1
    elif partition == "BISECTION":
        row_add = 6 * 2
        
    if sb == True:
        column_add = 0
    elif sb == False:
        column_add = 1

    return column, column_add, row_add

def return_sampling_graph(subgraph_list, partition, graph, sampling_rate, sampling):
    sampled_subgraph_list = []
    sampling_time_list = []
    
    print()
    print(partition, graph, sampling, "RATE :", sampling_rate)
    
    sampling_rate = float(sampling_rate)
    
    for subgraph in subgraph_list:
        obj = sp.TPN_re()
        acc = nx.average_clustering(subgraph)
        pr_origin = nx.pagerank(subgraph)
        
        graph_size = int(len(list(subgraph)) * sampling_rate)
        
        if graph_size == 0:
            graph_size = 1
        
        sampling_time_start = time.perf_counter()

        sp_graph = obj.top_pagerank_sampling(subgraph, graph_size, acc, pr_origin)
        
        sampling_time_end = time.perf_counter()
        sampling_time_execute = sampling_time_end - sampling_time_start
        
        sampled_subgraph_list.append(sp_graph)
        sampling_time_list.append(sampling_time_execute)

    return sampled_subgraph_list, sum(sampling_time_list)

def calc_time_origin(partition, graph):
    print("ORIGIN :", partition, graph)
    subgraph_list = []
    origin_graph = nx.read_adjlist(READ_ORIGIN_FILE.format(graph), create_using=nx.DiGraph, nodetype=int)
    
    for i in range(DIV_NUM):
        subgraph = nx.read_adjlist(READ_DIV_FILE_ORIGIN.format(partition, graph, i), create_using=nx.DiGraph, nodetype=int)
        subgraph_list.append(subgraph)

    synthesis_graph, synthesis_time_execute = Calc.calc_synthesis_time(origin_graph, subgraph_list)
    
    pr_calc_time_start = time.perf_counter()

    pr_value = nx.pagerank(synthesis_graph)
    
    pr_calc_time_end = time.perf_counter()
    pr_calc_time_execute = pr_calc_time_end - pr_calc_time_start
    
    return synthesis_time_execute, pr_calc_time_execute

def calc_time_sampling(partition, graph, sampling):
    print("SAMPLING :", partition, graph, sampling)
    subgraph_list = []
    sampled_subgraph_list = []
    origin_graph = nx.read_adjlist(READ_ORIGIN_FILE.format(graph), create_using=nx.DiGraph, nodetype=int)
    
    for i in range(DIV_NUM):
        subgraph = nx.read_adjlist(READ_DIV_FILE_ORIGIN.format(partition, graph, i), create_using=nx.DiGraph, nodetype=int)
        subgraph_list.append(subgraph)
    
    sampled_subgraph_list, sampling_time_execute = return_sampling_graph(subgraph_list, partition, graph, SAMPLING_RATE, sampling)

    synthesis_graph, synthesis_time_execute = Calc.calc_synthesis_time(origin_graph, sampled_subgraph_list)
    
    pr_calc_time_start = time.perf_counter()

    pr_value = nx.pagerank(synthesis_graph)
    
    pr_calc_time_end = time.perf_counter()
    pr_calc_time_execute = pr_calc_time_end - pr_calc_time_start

    return sampling_time_execute, synthesis_time_execute, pr_calc_time_execute

for sb in sampling_bool:
    if sb == True:
        for partition in partition_list:
            for graph in graph_list:
                column, column_add, row_add = excel_value(sb, partition, graph)
                synthesis_time_execute, pr_calc_time_execute = calc_time_origin(partition, graph)
                Calc.write_excel(synthesis_time_execute, EXCEL_NAME, SHEET_NAME, column=column+column_add, row=ROW_SYNTHESIS_TIME+row_add)
                Calc.write_excel(pr_calc_time_execute, EXCEL_NAME, SHEET_NAME, column=column+column_add, row=ROW_PR_TIME+row_add)
    elif sb == False:
        for partition in partition_list:
            for graph in graph_list:
                for sampling in sampling_list:
                    column, column_add, row_add = excel_value(sb, partition, graph)
                    sampling_time_execute, synthesis_time_execute, pr_calc_time_execute = calc_time_sampling(partition, graph, sampling)
                    Calc.write_excel(sampling_time_execute, EXCEL_NAME, SHEET_NAME, column=column+column_add, row=ROW_SAMPLING_TIME+row_add)
                    Calc.write_excel(synthesis_time_execute, EXCEL_NAME, SHEET_NAME, column=column+column_add, row=ROW_SYNTHESIS_TIME+row_add)
                    Calc.write_excel(pr_calc_time_execute, EXCEL_NAME, SHEET_NAME, column=column+column_add, row=ROW_PR_TIME+row_add)