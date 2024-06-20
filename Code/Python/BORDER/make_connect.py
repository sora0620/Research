import Calc

# connect_node_list を保存する用

def main():
    # ハイパーパラメータ
    graph_name = "slashdot"
    weight_node_num_list = [50, 100, 500]
    loop_num = 3
    border = "prefer"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    
    for weight_node_num in weight_node_num_list:
        for i in range(loop_num):
            connect_node_list = []
            if border == "random":
                connect_node_list = Calc.select_border_node(origin_graph, weight_node_num) # ランダム選択
            elif border == "prefer":
                connect_node_list = Calc.select_border_prefer(origin_graph, weight_node_num) # 優先付着
            path = "./connect_node/{}/{}/{}/ver_{}.txt".format(graph_name, border, weight_node_num, i)
            with open(path, 'w') as f:
                print(connect_node_list)
                for node in connect_node_list:
                    f.write(f"{node} ")

if __name__ == "__main__":
    main()