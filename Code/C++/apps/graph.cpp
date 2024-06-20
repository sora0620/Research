#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <map>
#include <fstream>
#include <string>
#include <sstream>
#include <tuple>
#include "../include/graph.h"
#include "../include/pair_hash.hpp"

using namespace std;

// デフォルトコンストラクタ
Graph::Graph()
{

}

// グラフ名を引数に取ると, そのファイルを読み込んだグラフを作成
Graph::Graph(string graph_name)
{
    string graph_path = "../../../Dataset/Origin/" + graph_name + ".adjlist";
    ifstream file(graph_path);
    vector<string> lines;
    string line, s;

    auto start = chrono::system_clock::now();

    if(!file){
        cout << "Failed to open file" << endl;
        exit(-1);
    }

    cout << "グラフ読み込み Start!" << endl;

    // ノード数の読み込み
    while (getline(file, line)) {
        stringstream ss(line);
        string s;

        // あるソースノードと、それに対する隣接ノードを全て格納
        while (ss >> s) {
            this->node_list_set.insert(stoi(s));
        }
    }

    // 初期化
    this->node_num = node_list_set.size();
    this->adj_list_list = vector<vector<int>>(node_num, vector<int>());

    file.clear();
    file.seekg(0, ios::beg);

    while (getline(file, line)){
        vector<int> node_vec;
        stringstream ss(line);
        string s;

        while (ss >> s) {
            node_vec.push_back(stoi(s));
        }

        for (int i = 0; i < node_vec.size(); i++) {
            int src_id = node_vec[0];

            if (i != 0) {
                int dst_id = node_vec[i];
                if (src_id == dst_id) continue; // ignore self-loop
                int insert_count = insert_edge(src_id, dst_id);
                this->adjacency_list[src_id].push_back(dst_id);
                this->in_neighbor_list[dst_id].push_back(src_id);
            }
        }
    }

    for (int node_id : node_list_set) {
        max_node_id = max(max_node_id, node_id);
        this->degree[node_id] = this->adjacency_list[node_id].size();
        this->in_deg[node_id] = this->in_neighbor_list[node_id].size();
    }

    file.close();

    auto end = chrono::system_clock::now();       // 計測終了時刻を保存
    auto dur = end - start;        // 要した時間を計算
    auto sec = chrono::duration_cast<std::chrono::seconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    cout << "Graph Read Time: " << sec << " sec" << endl;
}

// const 参照のノードリストを返す vector でidが昇順
const vector<int> Graph::get_node_list_id_sort(){
    vector<int> node_list(this->node_list_set.begin(), this->node_list_set.end());
    sort(node_list.begin(), node_list.end());
    return node_list;
}

// ノードの set を返す
const unordered_set<int> Graph::get_node_set() const {
    return this->node_list_set;
}

// ノードの vec を返す
const vector<int> Graph::get_node_vec() {
    vector<int> node_vec;
    for (int node : this->node_list_set) {
        node_vec.push_back(node);
    }

    return node_vec;
}

// エッジの集合を取得
const vector<pair<int, int> > Graph::get_edge_vec()
{
    vector<pair <int, int> > edge_vec;

    for (int source_node : this->node_list_set) {
        vector<int> adj_vec = this->adjacency_list[source_node];
        if (adj_vec.size() != 0) {
            for (int target_node : adj_vec) {
                edge_vec.push_back(make_pair(source_node, target_node));
            }
        }
    }

    return edge_vec;
}

// const 参照の隣接リストを返す
const unordered_map<int, vector <int> > Graph::get_adjacency_list()
{
    return this->adjacency_list;
}

// const 参照の入隣接リストを返す
const unordered_map<int, vector <int> > Graph::get_in_adj_list()
{
    return this->in_neighbor_list;
}

const unordered_map<int, int> Graph::get_out_deg()
{
    for (int node : this->node_list_set) {
        this->degree[node] = this->adjacency_list[node].size();
    }
    
    return this->degree;
}

const unordered_map<int, int> Graph::get_in_deg()
{
    for (int node : this->node_list_set) {
        this->in_deg[node] = this->in_neighbor_list[node].size();
    }

    return this->in_deg;
}

// ノード数を返す
const int Graph::get_number_of_nodes(){
    return this->node_list_set.size();
}

// エッジ数を返す
const int Graph::get_number_of_edges() const {
    int number_of_edges = 0;

    // ノードが持つエッジ数を合計する
    for (int node : this->node_list_set) {
        number_of_edges += this->adjacency_list.at(node).size();
    }

    return number_of_edges;
}

// ノードの追加
void Graph::add_node(int node)
{
    this->node_list_set.insert(node);
    this->adjacency_list[node];
    this->in_neighbor_list[node];
}

// エッジの追加
// 重複エッジが無いかをちゃんとチェックする
void Graph::add_edge(int n1, int n2)
{
    // adjacency_list に n1 -> n2 を追加(有向のため)
    this->in_neighbor_list[n1];
    this->adjacency_list[n2];

    unordered_set<int> tmp_set;
    for (int node : this->adjacency_list[n1]) {
        tmp_set.insert(node);
    }
    if (tmp_set.find(n2) == tmp_set.end()) {
        this->adjacency_list[n1].push_back(n2);
    }

    unordered_set<int> tmp_set_2;
    for (int node : this->in_neighbor_list[n2]) {
        tmp_set_2.insert(node);
    }
    if (tmp_set_2.find(n1) == tmp_set_2.end()) {
        this->in_neighbor_list[n2].push_back(n1);
    }

    // 頂点リスト生成 (set)
    this->node_list_set.insert(n1);
    this->node_list_set.insert(n2);
}

// エッジの追加
// 重複エッジが無いかをちゃんとチェックしなくて良い場合
void Graph::add_edge_no_multi(int n1, int n2)
{
    // adjacency_list に n1 -> n2 を追加(有向のため)
    this->in_neighbor_list[n1];
    this->adjacency_list[n2];

    this->adjacency_list[n1].push_back(n2);
    this->in_neighbor_list[n2].push_back(n1);

    // 頂点リスト生成 (set)
    this->node_list_set.insert(n1);
    this->node_list_set.insert(n2);
}

void Graph::add_edges_from(unordered_set<pair <int, int> > edge_set)
{
    for (auto [source, target] : edge_set) {
        this->adjacency_list[source].push_back(target);
        this->in_neighbor_list[target].push_back(source);

        this->in_neighbor_list[source];
        this->adjacency_list[target];

        this->node_list_set.insert(source);
        this->node_list_set.insert(target);
    }
}

int Graph::getMaxNodeId() {
    return max_node_id;
}

// tullys さんの実装
// 出隣接ノードからノードを１つ選択
// ダングリングノードの場合、-1 を返す
int Graph::get_random_adjacent(int node_id) const {
    vector<int> adj_list = adj_list_list.at(node_id);
    int degree = adj_list.size();
    if (degree == 0) return -1;
    else return adj_list.at((int)(rand() % degree));
}

// path.back() == -1 は dangling node で強制終了した path を表現
// ある１ノードから開始した RWer が終了したノードを格納したリストを返す
// PPR はそのノードでの RWer 終了確率を表すので、それを表現していると思われる
vector<int> Graph::get_random_walk_end_nodes(int src_id, int walk_count, double alpha) const {
    // vector<int> end_node_id_list;
    vector<int> end_node_id_list(walk_count);
    for (int i = 0; i < walk_count; i++) {
        int current_node_id = src_id;
        while ((double)rand()/RAND_MAX > alpha) {
            if (current_node_id == -1) break;
            current_node_id = get_random_adjacent(current_node_id);
        }
        // end_node_id_list.push_back(current_node_id);
        end_node_id_list[i] = current_node_id;
    }
    return end_node_id_list;
}

// edge_ppr と ppr は独立に計算できて、計算時間を考えると無駄な操作は減らしたいので、PPR を計算する関数と edge_ppr を計算する関数は別々にしよう

// PPR 計算用関数
unordered_map<int, double> Graph::calc_ppr_by_fora(int src_id, int walk_count, double alpha, double r_max_coef) const {
    /**
    * FORA の前処理？
    * 
    * @param src_id RW の起点ノード
    * @param walk_count RW の開始回数
    * @param alpha 終了確率 = 0.15
    * @param r_max_coef リザーブ値のしきい値を決定する係数
    * @return ノードIDをキーとするPPRの結果のマップ
    * @return 各ノードのリザーブ値のマップ
    */

    // ForwardPush 部分
    unordered_map<int, double> ppr, residue;
    unordered_set<int> active_node_set;
    queue<int> active_node_queue;
    int src_degree = get_degree(src_id);
    unordered_set<int> node_list_set = get_node_set();
    active_node_set.insert(src_id);
    active_node_queue.push(src_id);
    residue.emplace(src_id, 1);
    while (active_node_queue.size() > 0) {
        int node_id = active_node_queue.front();
        int node_degree = get_degree(node_id);
        active_node_queue.pop();
        active_node_set.erase(node_id);
        // dangling node. スーパーノードはactive node 対象外
        if (node_degree == 0) {
            ppr[node_id] += alpha * residue.at(node_id);
        } else {
            vector<int> adj_list = get_adj_list_list(node_id);
            ppr[node_id] += alpha * residue.at(node_id);
            for (int i = 0; i < node_degree; i++) {
                int adj_id = adj_list[i];
                int adj_degree = get_degree(adj_id);
                residue[adj_id] += (1 - alpha) * residue.at(node_id) / node_degree;
                if ((residue.at(adj_id) > r_max_func(adj_degree, alpha, walk_count, r_max_coef)) && (active_node_set.count(adj_id) == 0)) {
                    active_node_set.insert(adj_id);
                    active_node_queue.push(adj_id);
                }
            }
        }
        residue[node_id] = 0;
    }

    // FORA 部分
    for (auto itr = residue.begin(); itr != residue.end(); itr++) {
        int node_id = itr->first;
        double r_val = itr->second;
        if (r_val == 0) continue;
        
        int walk_count_i = (int)ceil(r_val * walk_count);
        vector<int> end_node_id_list = get_random_walk_end_nodes(node_id, walk_count_i, alpha);
        for (int end_node_id : end_node_id_list) {
            if (ppr.count(end_node_id) == 0) ppr[end_node_id] = 0;
            ppr[end_node_id] += (double)r_val / walk_count_i;
        }
    }

    for (int node : node_list_set) {
        ppr[node];
    }

    return ppr;
}

// エッジ PPR 計算用関数
void Graph::calc_edge_ppr_by_fora(unordered_map<int, unordered_map <int, double> >& edge_ppr, int src_id, int walk_count, double alpha, double r_max_coef) const {
    /**
    * FORA の前処理？
    * 
    * @param src_id RW の起点ノード
    * @param walk_count RW の開始回数
    * @param alpha 終了確率 = 0.15
    * @param r_max_coef リザーブ値のしきい値を決定する係数
    * @return ノードIDをキーとするPPRの結果のマップ
    * @return 各ノードのリザーブ値のマップ
    */

    // ForwardPush 部分
    unordered_map<int, double> residue;
    unordered_set<int> active_node_set;
    queue<int> active_node_queue;
    int src_degree = get_degree(src_id);
    active_node_set.insert(src_id);
    active_node_queue.push(src_id);
    residue.emplace(src_id, 1);
    while (active_node_queue.size() > 0) {
        int node_id = active_node_queue.front();
        int node_degree = get_degree(node_id);
        active_node_queue.pop();
        active_node_set.erase(node_id);
        // 出次数が 0 の時はエッジ PPR は生じ得ないので無視
        if (node_degree != 0) {
            vector<int> adj_list = get_adj_list_list(node_id);
            for (int i = 0; i < node_degree; i++) {
                int adj_id = adj_list[i];
                int adj_degree = get_degree(adj_id);
                edge_ppr[node_id][adj_id] += ((alpha * residue[node_id]) / node_degree); // エッジ PPR 計算
                residue[adj_id] += (1 - alpha) * residue[node_id] / node_degree;
                if ((residue[adj_id] > r_max_func(adj_degree, alpha, walk_count, r_max_coef)) && (active_node_set.count(adj_id) == 0)) {
                    active_node_set.insert(adj_id);
                    active_node_queue.push(adj_id);
                }
            }
        }
        residue[node_id] = 0;
    }

    // FORA 部分
    for (auto itr = residue.begin(); itr != residue.end(); itr++) {
        int node_id = itr->first;
        double r_val = itr->second;
        if (r_val == 0) continue;
        
        int walk_count_i = (int)ceil(r_val * walk_count);

        vector<int> end_node_id_list = get_random_walk_end_nodes(node_id, walk_count_i, alpha);
        for (int end_node_id : end_node_id_list) {
            vector<int> adj_list = get_adj_list_list(end_node_id);
            for (int adj_node : adj_list) {
                int deg = get_degree(end_node_id);
                edge_ppr[end_node_id][adj_node] += (double)r_val / walk_count_i / deg;
            }
        }

        // for (int i = 0; i < walk_count_i; i++) {
        //     int current_node_id = node_id;
        //     int prev_node_id = current_node_id;
        //     while ((double)rand()/RAND_MAX > alpha) {
        //         if (current_node_id == -1) break;
        //         current_node_id = get_random_adjacent(current_node_id);
        //         if (current_node_id == -1) break;
        //         edge_ppr[prev_node_id][current_node_id] += 1 / walk_count_i;
        //     }
        // }

        // int walk_num = 0;
        // unordered_map<int, unordered_map <int, int> > tmp_map;
        // for (int i = 0; i < walk_count_i; i++) {
        //     int current_node_id = node_id;
        //     int prev_node_id = current_node_id;
        //     while ((double)rand()/RAND_MAX > alpha) {
        //         if (current_node_id == -1) break;
        //         current_node_id = get_random_adjacent(current_node_id);
        //         if (current_node_id == -1) break;
        //         walk_num++;
        //         tmp_map[prev_node_id][current_node_id] += 1;
        //     }
        // }
        // for (auto& [source_node, m] : tmp_map) {
        //     for (auto& [target_node, value] : m) {
        //         edge_ppr[source_node][target_node] += r_val * value / walk_num;
        //     }
        // }
    }

    return;
}

// エッジ PPR 計算用関数
// 流入 RWer も考えた場合
void Graph::calc_edge_ppr_by_fora_flow(unordered_map<pair<int, int>, double, pairhash>& edge_ppr, int src_id, int walk_count, int flow_rwer, double alpha, double r_max_coef) const {
// unordered_map<pair <int, int>, double, pairhash> Graph::calc_edge_ppr_by_fora_flow(int src_id, int walk_count, int flow_rwer, double alpha, double r_max_coef) const {
// unordered_map<int, unordered_map <int, double> > Graph::calc_edge_ppr_by_fora_flow(int src_id, int walk_count, int flow_rwer, double alpha, double r_max_coef) const {
// unordered_map<int, double> Graph::calc_edge_ppr_by_fora_flow(int src_id, int walk_count, int flow_rwer, double alpha, double r_max_coef) const {
    /**
    * FORA の前処理？
    * 
    * @param src_id RW の起点ノード
    * @param walk_count RW の開始回数
    * @param alpha 終了確率 = 0.15
    * @param r_max_coef リザーブ値のしきい値を決定する係数
    * @return ノードIDをキーとするPPRの結果のマップ
    * @return 各ノードのリザーブ値のマップ
    */

    // ForwardPush 部分
    unordered_map<int, double> residue;
    unordered_set<int> active_node_set;
    queue<int> active_node_queue;
    // unordered_map<int, unordered_map <int, double> > edge_ppr;
    // unordered_map<pair <int, int>, double, pairhash> edge_ppr;
    // unordered_map<int, double> edge_ppr;
    int src_degree = get_degree(src_id);
    active_node_set.insert(src_id);
    active_node_queue.push(src_id);
    residue.emplace(src_id, 1);
    while (active_node_queue.size() > 0) {
        int node_id = active_node_queue.front();
        int node_degree = get_degree(node_id);
        active_node_queue.pop();
        active_node_set.erase(node_id);
        // 出次数が 0 の時はエッジ PPR は生じ得ないので無視
        if (node_degree != 0) {
            vector<int> adj_list = get_adj_list_list(node_id);
            for (int i = 0; i < node_degree; i++) {
                int adj_id = adj_list[i];
                int adj_degree = get_degree(adj_id);
                edge_ppr[{node_id, adj_id}] += ((alpha * residue[node_id]) / node_degree) * flow_rwer; // エッジ PPR 計算
                // edge_ppr[node_id][adj_id] += ((alpha * residue[node_id]) / node_degree) * flow_rwer; // エッジ PPR 計算
                // edge_ppr[node_id] += ((alpha * residue[node_id]) / node_degree) * flow_rwer; // エッジ PPR 計算
                residue[adj_id] += (1 - alpha) * residue[node_id] / node_degree;
                if ((residue[adj_id] > r_max_func(adj_degree, alpha, walk_count, r_max_coef)) && (active_node_set.count(adj_id) == 0)) {
                    active_node_set.insert(adj_id);
                    active_node_queue.push(adj_id);
                }
            }
        }
        residue[node_id] = 0;
    }

    // FORA 部分
    for (auto itr = residue.begin(); itr != residue.end(); itr++) {
        int node_id = itr->first;
        double r_val = itr->second;
        if (r_val == 0) continue;
        
        int walk_count_i = (int)ceil(r_val * walk_count);

        for (int i = 0; i < walk_count_i; i++) {
            int current_node_id = node_id;
            int prev_node_id = current_node_id;
            while ((double)rand()/RAND_MAX > alpha) {
                if (current_node_id == -1) break;
                current_node_id = get_random_adjacent(current_node_id);
                if (current_node_id == -1) break;
                edge_ppr[{prev_node_id, current_node_id}] += 1 * flow_rwer;
                // edge_ppr[prev_node_id][current_node_id] += 1 * flow_rwer;
                // edge_ppr[prev_node_id] += 1 * flow_rwer;
            }
        }
    }

    // return edge_ppr;
    return;
}

// エッジを追加する関数
int Graph::insert_edge(int src_id, int dst_id) {
    this->adj_list_list.at(src_id).push_back(dst_id);
    
    return 1;
}