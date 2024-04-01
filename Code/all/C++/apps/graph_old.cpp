#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <algorithm>
#include <time.h>
#include <chrono>
#include <cmath>
#include <map>
#include <fstream>
#include <string>
#include <sstream>
#include "../include/graph.h"

using namespace std;

// デフォルトコンストラクタ
Graph::Graph()
{

}

// グラフ名を引数に取ると, そのファイルを読み込んだグラフを作成
Graph::Graph(string graph_name)
{
    string graph_path = "../../../Dataset/Static/Origin/" + graph_name + ".adjlist";
    ifstream ifs(graph_path);
    vector<string> lines;
    // unordered_map<int, unordered_set <int> > node_map;
    string line, s;

    auto start = chrono::system_clock::now();

    if(!ifs){
        cout << "Failed to open file" << endl;
        exit(-1);
    } else {
        cout << "グラフ読み込み Start!" << endl;

        while (getline(ifs, line)){
            vector<int> node_vec;
            stringstream ss(line);
            string s;

            while (ss >> s) {
                node_vec.push_back(stoi(s));
            }

            for (int i = 0; i < node_vec.size(); i++) {
                // if (i == 0) {
                //     node_map[node_vec[0]];
                // } else {
                //     node_map[node_vec[0]].insert(node_vec[i]);
                // }

                node_list_set.insert(node_vec[i]);

                if (i != 0) {
                    adjacency_list[node_vec[0]].push_back(node_vec[i]);
                }
            }
        }
        // add_adj_edge(node_map);
    }

    for (int node_id : node_list_set) {
        degree[node_id] = adjacency_list[node_id].size();
    }

    auto end = chrono::system_clock::now();       // 計測終了時刻を保存
    auto dur = end - start;        // 要した時間を計算
    auto sec = chrono::duration_cast<std::chrono::seconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    cout << "Graph Read Time: " << sec << " sec\n" << endl;
}

// サンプリング等で取得したノードセットが存在し, 元グラフのエッジ関係を利用してグラフを作成したい場合
// Graph::Graph(unordered_set<int> node_set, Graph origin_graph)
// {
//     unordered_map<int, unordered_set <int> > origin_adj_list = origin_graph.get_adjacency_list(); // 元グラフの隣接リスト
//     unordered_map<int, unordered_set <int> > new_adj_list; // 新たなグラフの隣接リスト

//     for (auto current_node = node_set.begin(); current_node != node_set.end(); current_node++) {
//         new_adj_list[*current_node];
//         unordered_set<int> origin_adj = origin_adj_list[*current_node];
//         for (auto adjacency_node = origin_adj.begin(); adjacency_node != origin_adj.end(); adjacency_node++) {
//             if (node_set.find(*adjacency_node) != node_set.end()) {
//                 new_adj_list[*current_node].insert(*adjacency_node);
//             }
//         }
//     }

//     add_adj_edge(new_adj_list);
// }

// const 参照のノードリストを返す vector でidが昇順
const vector<int> Graph::get_node_list_id_sort(){
    vector<int> node_list(this->node_list_set.begin(), this->node_list_set.end());
    sort(node_list.begin(), node_list.end());
    return node_list;
}

// ノードの set を返す
const unordered_set<int> Graph::get_node_set() {
    return this->node_list_set;
}

// const 参照の隣接リストを返す
const unordered_map<int, vector <int> > Graph::get_adjacency_list()
{
    return this->adjacency_list;
}

// const 参照の入隣接リストを返す
const unordered_map<int, unordered_set <int> > Graph::get_in_adj_list()
{
    return this->in_neighbor_list;
}

// ノード数を返す
const int Graph::get_number_of_nodes(){
    return this->node_list_set.size();
}

// エッジ数を返す
const int Graph::get_number_of_edges(){
    int number_of_edges = 0;

    // ノードが持つエッジ数を合計する
    for (auto iter = this->adjacency_list.begin(); iter != this->adjacency_list.end(); iter++) {
        number_of_edges += iter->second.size();
    }

    return number_of_edges;
}


/* グラフの操作 */

// ノードの追加
void Graph::add_node(int node)
{
    this->node_list_set.insert(node);
    this->adjacency_list[node];
    this->in_neighbor_list[node];
}

// エッジ生成 有向グラフ
// void Graph::add_edge(int n1, int n2)
// {
//     // adjacency_list に n1 -> n2 を追加(有向のため)
//     this->adjacency_list[n1].insert(n2);
//     this->adjacency_list[n2];

//     this->in_neighbor_list[n2].insert(n1);
//     this->in_neighbor_list[n1];

//     // 頂点リスト生成 (set)
//     this->node_list_set.insert(n1);
//     this->node_list_set.insert(n2);
// }

// エッジ生成 隣接リスト用 (実質的には, グラフ作成用)
void Graph::add_adj_edge(unordered_map<int, unordered_set <int> > node_map)
{
    // // 出隣接リストを作成
    // this->adjacency_list = node_map;
    // for (auto iter = node_map.begin(); iter != node_map.end(); iter++) {
    //     for (int node : iter->second) {
    //         this->adjacency_list[node];
    //     }
    // }

    // // 頂点リスト生成 (set)
    // for (auto iter = adjacency_list.begin(); iter != adjacency_list.end(); iter++) {
    //     int source_node = iter->first;
    //     this->node_list_set.insert(source_node);
    //     this->in_neighbor_list[source_node];

    //     for (auto node = iter->second.begin(); node != iter->second.end(); node++) {
    //         this->node_list_set.insert(*node);
    //     }
    // }

    // // 入隣接リスト作成
    // // 存在する全ノードに対して初期化
    // for (auto iter = this->adjacency_list.begin(); iter != this->adjacency_list.end(); iter++) {
    //     if (iter->second.size() != 0) {
    //         for (auto node = iter->second.begin(); node != iter->second.end(); node++) {
    //             this->in_neighbor_list[*node].insert(iter->first);
    //         }
    //     }
    // }
}

// エッジ生成 無向グラフ
// void Graph::u_add_edge(int n3, int n4)
// {
//     // adjacency_list に n1 -> n2 を追加(有向のため)
//     this->adjacency_list[n3].insert(n4);
//     this->adjacency_list[n4].insert(n3);

//     // 頂点リスト生成 (set)
//     this->node_list_set.insert(n3);
//     this->node_list_set.insert(n4);
// }

// ノード削除
// void Graph::remove_node(int node)
// {
//     unordered_set<int> node_adj = this->adjacency_list[node];

//     for (int out_node : node_adj) {
//         in_neighbor_list[out_node].erase(node);
//     }

//     this->node_list_set.erase(node);
//     this->adjacency_list.erase(node);
// }

// n1 -> n2 のエッジ削除
// void Graph::remove_edge(int n1, int n2)
// {
//     this->adjacency_list[n1].erase(n2);
//     this->in_neighbor_list[n2].erase(n1);
// }

// pagerank 演算
unordered_map<int, double> Graph::pagerank()
{
    #define ALPHA 0.85
    #define MAX_ITER 100

    int node_num = get_number_of_nodes(); // グラフのノード数
    const double error = node_num * pow(10, -6); // 誤差範囲のしきい値. 値は NetworkX と同様の値を利用

    unordered_map<int, double> score;
    unordered_map<int, double> init_score;
    unordered_set<int> node_set = get_node_set();
    unordered_map<int, vector <int> > out_neighbor_map = get_adjacency_list(); // キーにノード, 値に出隣接ノードのリストの辞書
    // unordered_map<int, unordered_set <int> > in_neighbor_map = get_in_adj_list();  // キーにノード, 値に入隣接ノードのリストの辞書

    // 各ノード初期 PR 値
    for (int node : node_set) {
        score[node] = 1 / (double) node_num;
        init_score[node] = 0;
    }

    for (int i = 0; i < MAX_ITER; i++) {
        // 「prev_score : 今のスコア」, 「score : 次の iteration のスコア」, という状態にする
        unordered_map<int, double> prev_score = init_score;
        swap(score, prev_score);
        double dangling_score = 0;

        for (auto iter = out_neighbor_map.begin(); iter != out_neighbor_map.end(); iter++) {
            int out_deg = iter->second.size();
            if (out_deg == 0) {
                dangling_score += ALPHA * prev_score[iter->first] / node_num;
            } else {
                for (int out_node : iter->second) {
                    score[out_node] += ALPHA * prev_score[iter->first] / out_deg;
                }
            }
        }

        for(int node : node_set){
            score[node] += dangling_score;
            score[node] += (1.0 - ALPHA) / node_num;
        }

        double error_sum = 0;

        for (int node : node_set) {
            error_sum += abs(score[node] - prev_score[node]);
        }

        if (error_sum < error) {
            break;
        }
    }
    
    return score;
}