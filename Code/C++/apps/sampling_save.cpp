#include <string>
#include <vector>
#include <chrono>
#include <math.h>
#include <fstream>
#include <sstream>
#include <filesystem>
#include "../include/graph.h"
#include "../include/calc.h"
#include "../include/sampling.h"
#include "../include/util.hpp"

using namespace std;
namespace fs = filesystem;

// g++ -std=c++17 sampling_save.cpp graph.cpp calc.cpp sampling.cpp

// ランダム生成器
StdRandNumGenerator gen;

vector<int> return_weight(vector<int>& connect_node_vec, int weight_range, int default_weight)
{
    vector<int> weight_vec(connect_node_vec.size());

    for (int i = 0; i < connect_node_vec.size(); i++) {
        weight_vec.at(i) = gen.genRandHostId(default_weight+1, weight_range) - default_weight;
    }

    return weight_vec;
}

unordered_map<int, unordered_map<int, double> > return_ppr_map(vector<int>& node_vec, unordered_map<int, vector <int> >& adj_map, vector<int>& connect_node_vec, int random_walk_num)
{
    cout << "FC の PPR 計算開始" << endl;

    unordered_map<int, unordered_map<int, double> > ppr_map;

    // int check_num = 1;
    for (int node : connect_node_vec) {
        ppr_map[node] = personalized_pagerank(adj_map, node_vec, node, (int) ( (double) random_walk_num / connect_node_vec.size()));
        // cout << check_num << endl;
        // check_num++;
    }

    cout << "PPR Calculated!" << endl;

    return ppr_map;
}

Graph return_sampling_graph(Graph& origin_graph, vector<int>& connect_node_vec, double rate, string sampling_method, vector<int>& weight_vec, int default_weight, int random_walk_num)
{
    Graph sampling_graph;

    if (sampling_method == "FC") {
        sampling_graph = Flow_Control(origin_graph, rate, connect_node_vec, weight_vec, default_weight, random_walk_num);
    } else if (sampling_method == "SRW") {
        sampling_graph = Simple_Random_Walk(origin_graph, rate);
    } else if (sampling_method == "RE") {
        sampling_graph = Random_Edge(origin_graph, rate);
    } else {
        cout << "Sampling Error!" << endl;
        exit(1);
    }

    unordered_map<int, vector <int> > out_adj_origin = origin_graph.get_adjacency_list();
    unordered_map<int, vector <int> > out_adj_sampling = sampling_graph.get_adjacency_list();
    for (int node : connect_node_vec) {
        unordered_set<int> tmp_set = sampling_graph.get_node_set();
        if (tmp_set.find(node) == tmp_set.end()) {
            sampling_graph.add_node(node);
        }
        vector<int> out_edge_vec_origin = out_adj_origin[node];
        vector<int> out_edge_vec_sampling = out_adj_sampling[node];

        if (out_edge_vec_sampling.size() == 0 && out_edge_vec_origin.size() != 0) {
            int get_out_num = (int) (out_edge_vec_origin.size() * rate);
            if (get_out_num == 0) {
                get_out_num = 1;
            }

            vector<int> tmp_vec;
            gen.gen_sample(out_edge_vec_origin, tmp_vec, get_out_num);
            for (int out_node : tmp_vec) {
                sampling_graph.add_edge(node, out_node);
            }
        }
    }

    return sampling_graph;
}

void write_adjlist(Graph& sampling_graph, vector<int>& connect_node_vec, string save_folder, int ver)
{
    if (!fs::exists(save_folder)) { // フォルダが存在しない場合
        if (fs::create_directories(save_folder)) {
            cout << "Folder created successfully: " << save_folder << endl;
        }
    }

    string save_file = save_folder + "/ver_" + to_string(ver+1) + ".adjlist";
    ofstream writing_file;
    writing_file.open(save_file, ios::out);

    unordered_set<int> node_set = sampling_graph.get_node_set();
    unordered_map<int, vector<int>> adj_map = sampling_graph.get_adjacency_list();

    for (int node : connect_node_vec) {
        writing_file << node << " ";
    }
    writing_file << endl;

    for (int node : node_set) {
        writing_file << node << " ";
        for (auto iter = adj_map[node].begin(); iter != adj_map[node].end(); iter++) {
            writing_file << *iter << " ";
        }

        writing_file << endl;
    }

    return;
}

vector<int> return_connect_node_vec(string graph_name, string type, int weight_node_num, int ver)
{
    string path = "../../../Dataset/connect_node/" + graph_name + "/" + type + "/" + to_string(weight_node_num) + "/ver_" + to_string(ver) + ".txt";
    ifstream file(path);
    vector<int> return_vec;
    string line, s;

    if(!file){
        cout << "Failed to open file" << endl;
        exit(-1);
    }

    while (getline(file, line)) {
        stringstream ss(line);
        string s;

        while (ss >> s) {
            return_vec.push_back(stoi(s));
        }
    }

    return return_vec;
}

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    string sampling = "FC";
    string border_type = "prefer";
    vector<string> rate_vec = {"0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"};
    // vector<string> rate_vec = {"0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08", "0.09"};
    int weight_node_num = 50; // 境界ノード数
    int weight_range = 100; // 境界ノードの重み幅
    int default_weight = 50; // 基本の重み
    int sampling_num = 5; // 何回分保存するか

    // 実装
    Graph origin_graph(graph_name);
    vector<int> node_vec = origin_graph.get_node_vec();

    // PPR は約 100 万回の RWer を走らせればよいが, 今回のような合計値を利用する場合は, 始点ノード数が多いほど, その分 RWer を減らして大丈夫. 例えば, PR では PPR ほどの RWer を走らせなくても正確な値を算出可能
    int random_walk_num = (int) pow(10, 6) / weight_node_num;
    
    for (int i = 0; i < sampling_num; i++) {
        vector<int> connect_node_vec = return_connect_node_vec(graph_name, border_type, weight_node_num, i);
        vector<int> weight_vec = return_weight(connect_node_vec, weight_range, default_weight);
        for (string rate_str : rate_vec) {
            string save_folder = "../../../Dataset/FC/" + graph_name + "/境界ノード_" + to_string(weight_node_num) + "/" + rate_str;
            double rate = stod(rate_str);
            Graph sampling_graph = return_sampling_graph(origin_graph, connect_node_vec, rate, sampling, weight_vec, default_weight, random_walk_num);
            write_adjlist(sampling_graph, connect_node_vec, save_folder, i);
        }
    }
}