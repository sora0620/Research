#include <string>
#include <vector>
#include <chrono>
#include <math.h>
#include <iostream>
#include <cmath>
#include <utility>
#include <limits>
#include "../include/graph.h"
#include "../include/calc.h"
#include "../include/sampling.h"
#include "../include/util.hpp"

using namespace std;

// g++ -std=c++17 ken_and_rmse.cpp graph.cpp calc.cpp sampling.cpp

// ランダム生成器
StdRandNumGenerator gen;

vector<pair <int, double> > return_sort_map(unordered_map<int, double>& multi_source_ppr_map)
{
    vector<pair <double, int> > tmp_vec;
    vector<pair <int, double> > result;

    for (auto iter = multi_source_ppr_map.begin(); iter != multi_source_ppr_map.end(); iter++) {
        tmp_vec.emplace_back(-iter->second, iter->first);
    }

    sort(tmp_vec.begin(), tmp_vec.end());

    for (auto [ppr, node] : tmp_vec) {
        result.push_back(make_pair(node, -ppr));
    }

    return result;
}

vector<int> return_weight(vector<int>& connect_node_vec, int weight_range, int default_weight)
{
    vector<int> weight_vec(connect_node_vec.size());

    for (int i = 0; i < connect_node_vec.size(); i++) {
        weight_vec.at(i) = gen.genRandHostId(default_weight+1, weight_range) - default_weight;
    }

    return weight_vec;
}

unordered_map<int, double> return_multi_source_ppr_map(Graph& graph, vector<int>& connect_node_vec, vector<int>& weight_vec, int random_walk_num)
{
    unordered_map<int, double> mulit_souce_ppr_map;
    unordered_map<int, vector<int> > adj_map = graph.get_adjacency_list();
    vector<int> node_vec = graph.get_node_vec();

    for (int node : node_vec) {
        mulit_souce_ppr_map[node] = 0;
    }

    double tmp_sum = 0;

    for (int i = 0; i < connect_node_vec.size(); i++) {
        int start_node = connect_node_vec[i];

        unordered_map<int, double> tmp_ppr_origin = personalized_pagerank(adj_map, node_vec, start_node, random_walk_num);

        for (int node : node_vec) {
            double add_value = tmp_ppr_origin[node] * weight_vec[i];
            mulit_souce_ppr_map[node] += add_value;
            tmp_sum += add_value;
        }
    }

    for (auto [node, ppr] : mulit_souce_ppr_map) {
        mulit_souce_ppr_map[node] /= tmp_sum;
    }

    return mulit_souce_ppr_map;
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

/*
double return_kendall(unordered_set<int>& node_set_sampling, unordered_map<int, double>& ppr_origin, unordered_map<int, double>& ppr_sampling)
{
    vector<pair <int, double> > ppr_origin_sorted = return_sort_map(ppr_origin);
    vector<pair <int, double> > ppr_sampling_sorted = return_sort_map(ppr_sampling);

    unordered_map<int, int> rank_origin, rank_sampling;

    int rank_o = 1;
    for (auto [node, ppr] : ppr_origin_sorted) {
        if (node_set_sampling.find(node) != node_set_sampling.end()) {
            rank_origin[node] = rank_o;
            rank_o++;
        }
    }

    int rank_s = 1;
    for (auto [node, ppr] : ppr_sampling_sorted) {
        rank_sampling[node] = rank_s;
        rank_s++;
    }

    vector<pair <int, int> > rank_vec; // (元グラフでの順位, 縮小グラフでの順位)

    for (int node: node_set_sampling) {
        rank_vec.push_back(make_pair(rank_origin[node], rank_sampling[node]));
    }

    // 以下は, ケンドールの操作
    long long plus_sum = 0, minus_sum = 0; // 順方向 & 逆方向のデータセットの個数を格納する変数
    int node_num = node_set_sampling.size();

    for (int i = 0; i < node_num; i++) {
        int standard_x = rank_vec[i].first, standard_y = rank_vec[i].second;
        for (int j = 0; j < node_num; j++) {
            if (i == j) {
                continue;
            }

            int compare_x = rank_vec[j].first, compare_y = rank_vec[j].second;

            // ここからが比較演算
            if ( (standard_x > compare_x) && (standard_y > compare_y) ) {
                plus_sum++;
            } else if ( (standard_x < compare_x) && (standard_y < compare_y) ) {
                plus_sum++;
            } else {
                minus_sum++;
            }
        }
    }

    double kendall = (double) ((long double) (plus_sum - minus_sum) / (node_num * (node_num - 1)));

    return kendall;
}
*/


// 以下２つはchatGPTが出力してくれたやつ
// ヘルパー関数：ペアの順序関係を決定
int pairwise_comparison(double a1, double b1, double a2, double b2) {
    if ((a1 - a2) * (b1 - b2) > 0) return 1;   // 一致
    if ((a1 - a2) * (b1 - b2) < 0) return -1;  // 不一致
    return 0;  // 同順位
}

// ケンドールの順位相関係数を計算
double kendalls_tau(const vector<double>& rank1, const vector<double>& rank2) {
    int n = rank1.size();
    if (n != rank2.size() || n == 0) {
        cerr << "Error: Vectors must be of the same size and non-empty." << endl;
        return numeric_limits<double>::quiet_NaN();
    }

    long long C = 0, D = 0, T = 0, U = 0;  // 一致ペア、不一致ペア、同順位ペアのカウント

    for (int i = 0; i < n - 1; ++i) {
        for (int j = i + 1; j < n; ++j) {
            int comparison = pairwise_comparison(rank1.at(i), rank2.at(i), rank1.at(j), rank2.at(j));
            if (comparison == 1) ++C;
            if (comparison == -1) ++D;
            if (comparison == 0) {
                if (rank1.at(i) == rank1.at(j)) ++T;
                if (rank2.at(i) == rank2.at(j)) ++U;
            }
        }
    }

    long double denominator = 0;

    if (C + D - T < 0 && C + D - U < 0) {
        denominator = (long double) (sqrt(-(C + D - T)) * sqrt(-(C + D - U)));
    } else if (C + D - T > 0 && C + D - U > 0) {
        denominator = (long double) (sqrt(C + D - T) * sqrt(C + D - U));
    } else {
        cerr << "Root Error!" << endl;
        return numeric_limits<double>::quiet_NaN();
    }

    cout << "C: " << C << ", D: " << D << ", T: " << T << ", U: " << U << endl;
    if (isnan(denominator)) {
        cerr << "Error1" << endl;
        return numeric_limits<double>::quiet_NaN();
    }
    if (denominator == 0.0) {
        cerr << "Error: Denominator is zero, cannot compute Kendall's Tau." << endl;
        return numeric_limits<double>::quiet_NaN();
    }

    return (double) ((C - D) / denominator);
}

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    // vector<string> sampling_vec = {"SRW", "RE", "FC"};
    vector<string> sampling_vec = {"RE"};
    int weight_node_num = 100;
    int weight_range = 100; // 境界ノードの重み幅
    int default_weight = 50; // 基本の重み
    double rate = 0.2; // サンプリングサイズ

    // 実装
    Graph origin_graph(graph_name);
    vector<int> node_vec = origin_graph.get_node_vec();
    vector<int> connect_node_vec;
    unordered_map<int, vector<int> > out_adj_map = origin_graph.get_adjacency_list();
    gen.gen_sample(node_vec, connect_node_vec, weight_node_num);
    vector<int> weight_vec = return_weight(connect_node_vec, weight_range, default_weight);

    // PPR は約 100 万回の RWer を走らせればよいが, 今回のような合計値を利用する場合は, 始点ノード数が多いほど, その分 RWer を減らして大丈夫. 例えば, PR では PPR ほどの RWer を走らせなくても正確な値を算出可能
    int random_walk_num = (int) (pow(10, 6) / weight_node_num); // pow 関数は引数と戻り値が double 型なので, 計算時にキャスト変換する必要無し
    unordered_map<int, double> multi_source_ppr_origin = return_multi_source_ppr_map(origin_graph, connect_node_vec, weight_vec, random_walk_num);
    for (string sampling : sampling_vec) {
        Graph sampling_graph = return_sampling_graph(origin_graph, connect_node_vec, rate, sampling, weight_vec, default_weight, random_walk_num);
        unordered_set<int> node_set_sampling = sampling_graph.get_node_set();
        unordered_map<int, double> multi_source_ppr_sampling = return_multi_source_ppr_map(sampling_graph, connect_node_vec, weight_vec, random_walk_num);
        // double kendall = return_kendall(node_set_sampling, multi_source_ppr_origin, multi_source_ppr_sampling);
        vector<double> origin_vec;
        vector<double> sampling_vec;
        for (int node : node_set_sampling) {
            origin_vec.push_back(multi_source_ppr_origin[node]);
            sampling_vec.push_back(multi_source_ppr_sampling[node]);
        }

        double kendall = kendalls_tau(origin_vec, sampling_vec);
        cout << sampling << " のケンドールの順位相関係数: " << kendall << endl;
    }
}