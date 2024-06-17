#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <filesystem>
#include <utility>
#include <algorithm>
#include <chrono>
#include <map>
#include <queue>
#include <iterator>
#include <random>
#include <algorithm>
#include <numeric>
#include "../include/graph.h"

using namespace std;

// BFS の実装. ランダムなノードを開始点として, 選択サイズ分辿った時点で終了.
// 最後まで BFS をしてもノードが足りない (開始ノードの問題や接続の問題) 場合に対しての処理は行っていないので注意
Graph bfs(Graph origin_graph, int size)
{
    random_device seed_gen;
    mt19937 engine {seed_gen()};

    int node_num = origin_graph.get_number_of_nodes(); // ノード数
    unordered_set<int> node_set = origin_graph.get_node_set(); // ノードリスト
    unordered_map<int, unordered_set <int> > adj_list = origin_graph.get_adjacency_list();
    map<int, int> dist;
    queue<int> que;
    unordered_set<int> get_node_set; // BFS をして取得したノードセット
    const int random_num = 1; // 初期ノードの選択個数
    vector<int> vec; // ランダム用
    vector<int> seed; // 初期ノード用

    // 全頂点を「未訪問」に初期化
    for (int node : node_set) {
        dist[node] = -1;
    }

    // 選択取得サイズがグラフサイズを超えてしまった場合, エラーを出力
    // 取得サイズはグラフサイズを基準に決めるため, このエラーが出たらグラフサイズを決めている側のコードがおかしいはず

    if (size > node_num) {
        cerr << "Error!" << endl;
        exit(1);
    }

    for (int node : node_set) {
        vec.push_back(node);
    }

    sample(vec.begin(),
           vec.end(),
           back_inserter(seed),
           random_num,
           engine);

    dist[seed[0]] = 0; // 初期条件 (頂点 seed を初期ノードとする)
    que.push(seed[0]); // seed を橙色頂点にする

    while (get_node_set.size() != size) {
        if (get_node_set.size() > size) {
            cerr << "Error!" << endl;
            exit(1);
        }
        while ((!que.empty()) && (get_node_set.size() != size)) {
            int v = que.front(); // キューから先頭頂点を取り出す
            get_node_set.insert(v);
            cout << get_node_set.size() << endl; // 確認用
            que.pop();
            node_set.erase(v);

            // v から辿れる頂点をすべて調べる
            if (adj_list[v].size() == 0) {
                continue;
            }

            for (int node : adj_list[v]) {
                if (dist[node] != -1) {
                    continue;
                }
                dist[node] = dist[v] + 1;
                que.push(node);
            }
        }

        vec.clear();
        seed.clear();

        for (int node : node_set) {
            vec.push_back(node);
        }

        sample(vec.begin(),
               vec.end(),
               back_inserter(seed),
               random_num,
               engine);

        dist[seed[0]] = 0; // 初期条件 (頂点 seed を初期ノードとする)
        que.push(seed[0]); // seed を橙色頂点にする
    }

    Graph new_graph = Graph(get_node_set, origin_graph);

    return new_graph;
}

vector<Graph> cut_edge_graph(Graph origin_graph, vector<Graph> subgraph_vec)
{
    vector<Graph> cut_graph_vec;
    unordered_map<int, unordered_set <int> > origin_graph_adj = origin_graph.get_adjacency_list();
    unordered_map<int, unordered_set <int> > origin_graph_in_adj = origin_graph.get_in_adj_list();

    for (auto iter = subgraph_vec.begin(); iter != subgraph_vec.end(); iter++) {
        Graph cut_graph = Graph();
        Graph subgraph = *iter;
        unordered_set<int> node_set = subgraph.get_node_set();

        for (auto node = node_set.begin(); node != node_set.end(); node++) {
            // 出隣接ノードの場合
            unordered_set<int> out_node_adj = origin_graph_adj[*node];
            for (auto out_node = out_node_adj.begin(); out_node != out_node_adj.end(); out_node++) {
                if (node_set.find(*out_node) == node_set.end()) {
                    cut_graph.add_edge(*node, *out_node);
                }
            }

            // 入隣接ノードの場合
            unordered_set<int> in_node_adj = origin_graph_in_adj[*node];
            for (auto in_node = in_node_adj.begin(); in_node != in_node_adj.end(); in_node++) {
                if (node_set.find(*in_node) == node_set.end()) {
                    cut_graph.add_edge(*in_node, *node);
                }
            }
        }

        cut_graph_vec.push_back(cut_graph);
    }

    return cut_graph_vec;
}

vector<int> random_num_out(int subgraph_num, int graph_size, float size_range) {
    int level = 0;

    int kijun = graph_size / subgraph_num;
    vector<int> tmp_list;
    int int_size_range = static_cast<int>(kijun * size_range);
    int upper = kijun + int_size_range;
    int lower = kijun - int_size_range;

    random_device rd;
    mt19937 gen(rd());

    for (int i = 0; i < subgraph_num; ++i) {
        int ran;
        if (i != subgraph_num - 1) {
            int sub = abs(level) + int_size_range - (subgraph_num - i - 1) * int_size_range;
            if (sub > 0) {
                if (level < 0) {
                    uniform_int_distribution<> dist(lower + sub, upper);
                    ran = dist(gen);
                } else if (level > 0) {
                    uniform_int_distribution<> dist(lower, upper - sub);
                    ran = dist(gen);
                }
            } else {
                uniform_int_distribution<> dist(lower, upper);
                ran = dist(gen);
            }
        } else if (i == subgraph_num - 1) {
            ran = graph_size - accumulate(tmp_list.begin(), tmp_list.end(), 0);
        }
        tmp_list.push_back(ran);
        level += ran - kijun;
    }

    if (accumulate(tmp_list.begin(), tmp_list.end(), 0) != graph_size) {
        cout << "Error!" << endl;
        exit(1);
    }

    cout << "サブグラフサイズ : ";
    for (int i : tmp_list) {
        cout << i << " ";
    }
    cout << endl;
    
    cout << "抜けの確認 : 元グラフサイズ -> " << graph_size << ", サブグラフの合計 -> " << accumulate(tmp_list.begin(), tmp_list.end(), 0) << endl;

    return tmp_list;
}

int main(int argc, char* argv[])
{
    int DIV_SIZE = 10;
    float RANGE = 0.2;
    string graph_path = "../../../Dataset/Origin/Graph/amazon0601.adjlist";
    vector<int> size_vec;
    Graph origin_graph = Graph(graph_path);
    Graph update_graph = origin_graph;
    vector<Graph> subgraph_vec; // 作成した部分グラフを格納
    int check_graph_size = 0;

    size_vec = random_num_out(DIV_SIZE, origin_graph.get_number_of_nodes(), RANGE);

    for (int i = 0; i < DIV_SIZE; i++) {
        cout << "BFS 開始" << endl;
        Graph sub_graph = bfs(update_graph, size_vec.at(i));
        cout << "BFS 終了" << endl;
        unordered_set<int> node_set = sub_graph.get_node_set();
        subgraph_vec.push_back(sub_graph);
        check_graph_size += sub_graph.get_number_of_nodes();

        for (int node : node_set) {
            update_graph.remove_node(node);
        }

        cout << "グラフサイズ : " << sub_graph.get_number_of_nodes() << endl;
    }

    cout << "元グラフサイズ: " << origin_graph.get_number_of_nodes() << "サブグラフサイズ: " << check_graph_size << endl;

    return 0;
}