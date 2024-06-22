#include <unordered_map>
#include <vector>
#include <fstream>
#include <filesystem>
#include <utility>
#include <unordered_set>
#include <iostream>
#include <string>
#include <iterator>
#include <random>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <math.h>
#include <chrono>
#include "../include/graph.h"
#include "../include/util.hpp"
#include "../include/pair_hash.hpp"

using namespace std;

// 最初のエッジ PPR 用の変数を作ったことで PPR 計算が少し遅くなったけどエッジの追加が少し高速なやつ

Graph Simple_Random_Walk(Graph& origin_graph, double rate)
{
    auto start = chrono::system_clock::now();

    // ランダム生成器
    StdRandNumGenerator gen;

    int growth_size = 2;
    int T = 100;    // number of iterations
    int iteration = 1;
    int edges_before_t_iter = 0;
    Graph sampling_graph;
    vector<pair <int, int> > edge_vec = origin_graph.get_edge_vec();
    int sampling_edge_num = (int) (edge_vec.size() * rate);

    vector<int> node_vec = origin_graph.get_node_vec();
    int node_num = node_vec.size();

    unordered_map<int, vector <int> > out_adj_map = origin_graph.get_adjacency_list();
    
    int current_node = node_vec[gen.gen(node_num)];
    sampling_graph.add_node(current_node);

    while (sampling_graph.get_number_of_edges() < sampling_edge_num) {
        cout << sampling_graph.get_number_of_edges() << endl;
        vector<int> edges = out_adj_map[current_node];
        if (edges.size() != 0) {
            int chosen_node = edges[gen.gen(edges.size())];
            sampling_graph.add_edge(current_node, chosen_node);
            current_node = chosen_node;
        }
        iteration++;

        if (iteration % T == 0) {
            if (sampling_graph.get_number_of_edges() - edges_before_t_iter < growth_size) {
                current_node = node_vec[gen.gen(node_num)];
                sampling_graph.add_node(current_node);
            }
            edges_before_t_iter = sampling_graph.get_number_of_edges();
        }
    }

    if (sampling_graph.get_number_of_edges() > sampling_edge_num) {
        cerr << "Over Edge Error!" << endl;
        exit(1);
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<chrono::milliseconds>(dur).count();
    cout << "SRW_Time: " << msec / pow(10, 3) << "sec\n";
    cout << "Node: " << sampling_graph.get_number_of_nodes() << ", Edge: " << sampling_graph.get_number_of_edges() << endl;
    
    return sampling_graph;
}

// こいつの実装かなり微妙な気がするので, 使わない方が良いかも
Graph Forest_Fire(Graph& origin_graph, int nodes_to_sample)
{
    auto start = chrono::system_clock::now();

    // 乱数生成
    std::random_device seed_gen;
    std::mt19937 engine {seed_gen()};

    // ランダム生成器
    StdRandNumGenerator gen;

    double forward_prob = 0.7, back_prob = 0.2; // 前方燃焼確率と後方燃焼確率
    queue<int> que; // キュー
    int initial_node; // FF の開始ノード
    int random_node;
    Graph sampling_graph; // サンプリンググラフ
    unordered_map<int, int> flag; // 一度取得したノードは 2 度操作はしない. 2 度してしまうと, 2 回隣接取得を行うことになり FF の意味がない
    unordered_set<int> node_set = origin_graph.get_node_set(); // 元グラフのノードリスト
    unordered_map<int, vector <int> > out_adj_list = origin_graph.get_adjacency_list(); // 出隣接ノード
    unordered_map<int, vector <int> > in_adj_list = origin_graph.get_in_adj_list(); // 入隣接ノード

    vector<int> node_vec;
    int node_num = node_vec.size();
    for (int node : node_set) {
        node_vec.push_back(node);
    }

    // ノード取得の有無を初期化
    for (int node : node_set) {
        flag[node] = 0;
    }

    random_node = node_vec[gen.gen(node_num)]; // シードノードを取得
    
    que.push(random_node); // シードノードをプッシュ
    sampling_graph.add_node(random_node); // 隣接が存在しない場合もあるため, シードノードをサンプリンググラフに追加
    node_set.erase(random_node);

    while (sampling_graph.get_number_of_nodes() != nodes_to_sample) {
        // キューにノードが存在する場合
        if (que.size() > 0) {
            initial_node = que.front(); // 開始ノードを取得
            node_set.erase(initial_node);
            que.pop(); // キューから削除

            // 開始ノードがまだ隣接取得を行ったことがない場合
            if (flag[initial_node] == 0) {
                if (sampling_graph.get_number_of_nodes() == nodes_to_sample) {
                    break;
                }
                // sampling_graph.add_node(initial_node);
                vector<int> out_neighbors = out_adj_list[initial_node];
                vector<int> in_neighbors = in_adj_list[initial_node];

                  // 成功確率0.7の事象をsize回試行する
                binomial_distribution<> out_dist(out_neighbors.size(), forward_prob);
                // 成功した回数を取得(0以上out_neighbors.size()以下の値が返される)
                int out_num = out_dist(engine);

                  // 成功確率0.2の事象をsize回試行する
                binomial_distribution<> in_dist(in_neighbors.size(), back_prob);
                // 成功した回数を取得(0以上in_neighbors.size()以下の値が返される)
                int in_num = in_dist(engine);

                vector<int> select_out_list;
                vector<int> select_in_list;

                sample(out_neighbors.begin(),
                    out_neighbors.end(),
                    back_inserter(select_out_list),
                    out_num,
                    engine);
                sample(in_neighbors.begin(),
                    in_neighbors.end(),
                    back_inserter(select_in_list),
                    in_num,
                    engine);
                
                for (int out_node : select_out_list) {
                    if (sampling_graph.get_number_of_nodes() == nodes_to_sample) {
                        break;
                    }
                    que.push(out_node);
                    sampling_graph.add_edge(initial_node, out_node);
                }

                for (int in_node : select_in_list) {
                    if (sampling_graph.get_number_of_nodes() == nodes_to_sample) {
                        break;
                    }
                    que.push(in_node);
                    sampling_graph.add_edge(in_node, initial_node);
                }
                flag[initial_node] = 1; // initial_node を隣接取得済みにする
            }

        // キューにノードが存在しない場合
        } else {
            random_node = node_vec[gen.gen(node_num)]; // シードノードを選択し直す
            que.push(random_node); // シードノードをプッシュ
            sampling_graph.add_node(random_node); // 隣接が存在しない場合もあるため, シードノードをサンプリンググラフに追加
            node_set.erase(random_node);
        }

        if (node_set.size() == 0) {
            cerr << "Error!" << endl;
            exit(1);
        }
    }

    if (sampling_graph.get_number_of_nodes() > nodes_to_sample) {
        cerr << "Over Node Error!" << endl;
        exit(1);
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    cout << "FF_Time: " << msec / pow(10, 3) << "sec\n";
    
    return sampling_graph;
}

// 演算時間高速なやつ, 精度は低いです多分
Graph Flow_Control(Graph& origin_graph, double rate, vector<int> connect_node_vec, vector<int> rwer_flow_vec, int default_weight, int random_walk_num)
{
    vector<pair <int, int> > edge_vec = origin_graph.get_edge_vec();
    unordered_map<int, int> out_deg_map = origin_graph.get_out_deg();
    int sampling_edge_num = (int) (edge_vec.size() * rate);
    double alpha = 0.15;
    unordered_map<pair<int, int>, double, pairhash> edge_ppr;
    vector<pair <double, pair<int, int> > > tmp_vec;

    Graph sampling_graph;

    // map のキーとして pair を使うことは難しいらしいので, エッジを指定するようなベクトルを作って, そのベクトルを使用したい時に呼び出す形にしよう

    auto start = chrono::system_clock::now();

    double sum = 0;

    for (int i = 0; i < connect_node_vec.size(); i++) {
        int node = connect_node_vec[i];
        int flow_rwer = rwer_flow_vec[i];

        auto start_ppr_calc_2 = chrono::system_clock::now();

        origin_graph.calc_edge_ppr_by_fora_flow_time(edge_ppr, node, random_walk_num, flow_rwer);
        
        auto end_ppr_calc_2 = chrono::system_clock::now();
        auto dur_ppr_calc_2 = end_ppr_calc_2 - start_ppr_calc_2;
        auto microsec_ppr_calc_2 = chrono::duration_cast<chrono::microseconds>(dur_ppr_calc_2).count();

        sum += microsec_ppr_calc_2 / pow(10, 6);
    }

    cout << "PPR Time: " << sum << endl;

    auto start_before_sort = chrono::system_clock::now();

    for (auto& [edge, value] : edge_ppr) {
        tmp_vec.push_back(make_pair(-value, edge));
    }
    auto end_before_sort = chrono::system_clock::now();
    auto dur_before_sort = end_before_sort - start_before_sort;
    auto microsec_before_sort = chrono::duration_cast<chrono::microseconds>(dur_before_sort).count();
    cout << "ソートの事前処理に要した時間: " << microsec_before_sort / pow(10, 6) << "sec\n";

    auto start_sort = chrono::system_clock::now();

    sort(tmp_vec.begin(), tmp_vec.end());

    auto end_sort = chrono::system_clock::now();
    auto dur_sort = end_sort - start_sort;
    auto microsec_sort = chrono::duration_cast<chrono::microseconds>(dur_sort).count();
    cout << "ソートに要した時間: " << microsec_sort / pow(10, 6) << "sec\n";

    auto start_add = chrono::system_clock::now();

    for (int i = 0; i < sampling_edge_num; i++) {
        sampling_graph.add_edge_no_multi(tmp_vec[i].second.first, tmp_vec[i].second.second);
    }

    auto end_add = chrono::system_clock::now();
    auto dur_add = end_add - start_add;
    auto microsec_add = chrono::duration_cast<chrono::microseconds>(dur_add).count();
    cout << "エッジ追加に要した時間: " << microsec_add / pow(10, 6) << "sec\n";

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    cout << "FC_Time: " << msec / pow(10, 3) << "sec\n";
    cout << "Node: " << sampling_graph.get_number_of_nodes() << ", Edge: " << sampling_graph.get_number_of_edges() << endl;

    return sampling_graph;
}

Graph Random_Edge(Graph& origin_graph, double rate)
{
    auto start = chrono::system_clock::now();

    // ランダム生成器
    StdRandNumGenerator gen;

    // StdRandNumGenerator gen = origin_graph.return_random_param();
    Graph sampling_graph;
    vector<pair <int, int> > edge_vec = origin_graph.get_edge_vec();
    int sampling_edge_num = (int) (edge_vec.size() * rate);
    vector<pair <int, int> > sampling_edge_vec;

    gen.gen_sample_pair(edge_vec, sampling_edge_vec, sampling_edge_num);

    for (auto [source_node, target_node] : sampling_edge_vec) {
        sampling_graph.add_edge(source_node, target_node);
    }

    if (sampling_graph.get_number_of_edges() != sampling_edge_num) {
        cerr << "Edge Size Error!" << endl;
        exit(1);
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<chrono::milliseconds>(dur).count();
    cout << "RE_Time: " << msec / pow(10, 3) << "sec\n";
    cout << "Node: " << sampling_graph.get_number_of_nodes() << ", Edge: " << sampling_graph.get_number_of_edges() << endl;
    
    return sampling_graph;
}