#ifndef GUARD_GRAPH_H
#define GUARD_GRAPH_H

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <algorithm>
#include <time.h>
#include <map>
#include <fstream>
#include <string>
#include <sstream>
#include <set>
#include <queue>
#include <ctime>
#include <cstdlib>
#include <tuple>
#include <cmath>
#include <cassert>
#include "../include/pair_hash.hpp"

using namespace std;

class Graph
{
    private: // グラフをコンストラクタを使用して作成したら, とりあえずこれらは作成するような関数にする
        unordered_set<int> node_list_set;
        unordered_map<int, vector<int> > adjacency_list; // ノードid -> 隣接ノードの set
        unordered_map<int, vector<int> > in_neighbor_list;
        unordered_map<int, int> degree;
        unordered_map<int, int> in_deg;
        int max_node_id = 0;
        int node_num;
        vector<vector<int>> adj_list_list; // map ではなく node_id で指定する用なので、vector で利用。id が 0 から順番に存在しない場合は使えないので注意。
        double r_max_func(int degree, double alpha, int walk_count, double r_max_coef) const {
            return (double)degree * r_max_coef / (alpha * (double)walk_count);
        }

    public:
        // デフォルトコンストラクタ
        Graph();

        // ファイル名を引数に取ると, そのファイルを読み込んだグラフを作成
        Graph(string file_path);

        // 全ノードが格納された vector を, ノードの昇順に並べて返す
        const vector<int> get_node_list_id_sort();

        // 全ノードが格納された set を返す
        const unordered_set<int> get_node_set() const;

        // ノードの vec を返す
        const vector<int> get_node_vec();

        // エッジの集合を取得
        const vector<pair<int, int> > get_edge_vec();

        // const 参照の隣接リストを返す
        const unordered_map<int, vector <int> > get_adjacency_list();

        // const 参照の入隣接リストを返す
        const unordered_map<int, vector <int> > get_in_adj_list();

        // 出次数の map を返す
        const unordered_map<int, int> get_out_deg();

        // 入次数の map を返す
        const unordered_map<int, int> get_in_deg();

        // ノード数を返す
        const int get_number_of_nodes();

        // エッジ数を返す
        const int get_number_of_edges() const;

        // ノードの追加
        void add_node(int node);

        // エッジの追加
        // 重複エッジが無いかをちゃんとチェックする
        void add_edge(int n1, int n2);

        // エッジの追加
        // 重複エッジが無いかをちゃんとチェックしなくて良い場合
        void add_edge_no_multi(int n1, int n2);

        void add_edges_from(unordered_set<pair <int, int> > edge_set);

        int getMaxNodeId();

        // 以下、tullys さんからもらった FORA 実装のための関数
        int get_random_adjacent(int node_id) const;
        vector<int> get_random_walk_end_nodes(int src_id, int walk_count, double alpha) const;

        // PPR 計算用関数２つ
        unordered_map<int, double> calc_ppr_by_fora(int src_id, int walk_count, double alpha=0.15, double r_max_coef=1.0) const;

        void calc_edge_ppr_by_fora(unordered_map<int, unordered_map <int, double> >& edge_ppr, int src_id, int walk_count, double alpha=0.15, double r_max_coef=1.0) const;

        // エッジ PPR 計算用関数２つ
        void calc_edge_ppr_by_fora_flow(unordered_map<pair<int, int>, double, pairhash>& edge_ppr, int src_id, int walk_count, int flow_rwer, double alpha=0.15, double r_max_coef=1.0) const;
        // unordered_map<pair <int, int>, double, pairhash> calc_edge_ppr_by_fora_flow(int src_id, int walk_count, int flow_rwer, double alpha=0.15, double r_max_coef=1.0) const;
        // unordered_map<int, unordered_map <int, double> > calc_edge_ppr_by_fora_flow(int src_id, int walk_count, int flow_rwer, double alpha=0.15, double r_max_coef=1.0) const;
        // unordered_map<int, double> calc_edge_ppr_by_fora_flow(int src_id, int walk_count, int flow_rwer, double alpha=0.15, double r_max_coef=1.0) const;

        int insert_edge(int src_id, int dst_id);

        int get_degree(int node_id) const {
            return adj_list_list[node_id].size();
        }
        vector<int> get_adj_list_list(int node_id) const {
            return adj_list_list[node_id];
        };
};

#endif // GURAD_GRAPH_H