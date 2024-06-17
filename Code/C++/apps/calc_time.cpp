#include <string>
#include <vector>
#include <chrono>
#include <math.h>
#include "../include/graph.h"
#include "../include/calc.h"
#include "../include/sampling.h"
#include "../include/util.hpp"

using namespace std;

// g++ -std=c++17 calc_time.cpp graph.cpp calc.cpp sampling.cpp

// ランダム生成器
StdRandNumGenerator gen;

vector<int> return_weight(vector<int>& node_vec, vector<int>& connect_node_vec, int weight_range, int default_weight)
{
    vector<int> flow_vec;

    for (int node : connect_node_vec) {
        flow_vec.push_back(gen.genRandHostId(default_weight+1, weight_range) - default_weight);
    }

    return flow_vec;
}

pair<Graph, double> return_sampling_graph(Graph& origin_graph, vector<int>& connect_node_vec, double rate, string sampling_method, vector<int>& weight_map, int default_weight, int random_walk_num)
{
    Graph sampling_graph;
    double time = 0;

    if (sampling_method == "FC") {
        auto start = chrono::system_clock::now();

        sampling_graph = Flow_Control(origin_graph, rate, connect_node_vec, weight_map, default_weight, random_walk_num);

        auto end = chrono::system_clock::now();
        auto dur = end - start;
        double microsec = chrono::duration_cast<chrono::microseconds>(dur).count();
        time = microsec / pow(10, 6); // マイクロ秒を秒に変換
    } else if (sampling_method == "SRW") {
        auto start = chrono::system_clock::now();

        sampling_graph = Simple_Random_Walk(origin_graph, rate);

        auto end = chrono::system_clock::now();
        auto dur = end - start;
        double microsec = chrono::duration_cast<chrono::microseconds>(dur).count();
        time = microsec / pow(10, 6); // マイクロ秒を秒に変換
    } else if (sampling_method == "RE") {
        auto start = chrono::system_clock::now();

        sampling_graph = Random_Edge(origin_graph, rate);

        auto end = chrono::system_clock::now();
        auto dur = end - start;
        double microsec = chrono::duration_cast<chrono::microseconds>(dur).count();
        time = microsec / pow(10, 6); // マイクロ秒を秒に変換
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

    return make_pair(sampling_graph, time);
}

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    // vector<string> sampling_vec = {"RE", "SRW", "FC"};
    vector<string> sampling_vec = {"FC"};
    int weight_node_num = 100;
    int weight_range = 100; // 境界ノードの重み幅
    int default_weight = 50; // 基本の重み
    double rate = 0.2; // サンプリングサイズ

    // 実装
    vector<double> time_vec;
    vector<string> name_vec;
    Graph origin_graph(graph_name);
    vector<int> node_vec = origin_graph.get_node_vec();
    vector<int> connect_node_vec;
    unordered_map<int, vector<int> > out_adj_map = origin_graph.get_adjacency_list();
    gen.gen_sample(node_vec, connect_node_vec, weight_node_num);
    vector<int> flow_vec = return_weight(node_vec, connect_node_vec, weight_range, default_weight);

    // PPR は約 100 万回の RWer を走らせればよいが, 今回のような合計値を利用する場合は, 始点ノード数が多いほど, その分 RWer を減らして大丈夫. 例えば, PR では PPR ほどの RWer を走らせなくても正確な値を算出可能
    int random_walk_num = (int) (pow(10, 6) / weight_node_num); // pow 関数は引数と戻り値が double 型なので, 計算時にキャスト変換する必要無し
    
    for (string sampling : sampling_vec) {
        pair<Graph, double> sampling_pair = return_sampling_graph(origin_graph, connect_node_vec, rate, sampling, flow_vec, default_weight, random_walk_num);
        Graph sampling_graph = sampling_pair.first;
        double time = sampling_pair.second;

        name_vec.push_back(sampling);
        time_vec.push_back(time);
        cout << sampling << endl;
        cout << "Time: " << time << endl;
    }
}