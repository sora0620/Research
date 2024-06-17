#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <map>
#include <sstream>
#include <random>
#include "../include/graph.h"
#include "../include/util.hpp"

#define ALPHA 0.15 // RWer の終了確率

using namespace std;

// pagerank 演算
unordered_map<int, double> pagerank(Graph& graph)
{
    #define MAX_ITER 100

    int node_num = graph.get_number_of_nodes(); // グラフのノード数
    const double error = node_num * pow(10, -6); // 誤差範囲のしきい値. 値は NetworkX と同様の値を利用

    unordered_map<int, double> score;
    unordered_map<int, double> init_score;
    unordered_set<int> node_set = graph.get_node_set();
    unordered_map<int, vector <int> > out_neighbor_map = graph.get_adjacency_list(); // キーにノード, 値に出隣接ノードのリストの辞書

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

        for (auto [prev_node, adj_vec] : out_neighbor_map) {
            int out_deg = adj_vec.size();
            if (out_deg == 0) {
                dangling_score += (1 - ALPHA) * prev_score[prev_node] / node_num;
            } else {
                for (int out_node : adj_vec) {
                    score[out_node] += (1 - ALPHA) * prev_score[prev_node] / out_deg;
                }
            }
        }

        for(int node : node_set){
            score[node] += dangling_score;
            score[node] += ALPHA / node_num;
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

// １ノードを始点とした RWer を走らせた際の各ノードにおける RWer 訪問回数
unordered_map<int, double> personalized_pagerank(unordered_map<int, vector<int>>& adj_map, vector<int>& node_vec, int start_node, int random_walk_num)
{
    unordered_map<int, int> rw_count_map;
    int node_num = node_vec.size(); // ノード数
    int current_node; // 現在ノード
    int next_node; // RW で選択する次のノード
    int rwer_num = 0;

    // ランダム生成器
    StdRandNumGenerator gen;

    for (int i = 0; i < random_walk_num; i++) {
        current_node = start_node;
        
        while (true) {
            int degree = adj_map[current_node].size();
            rw_count_map[current_node]++;
            rwer_num++;

            if (gen.gen_float(1.0) < ALPHA) break;

            if (degree == 0) {
                next_node = node_vec[gen.gen(node_num)];
            } else {
                next_node = adj_map[current_node][gen.gen(degree)];
            }

            current_node = next_node;
        }
    }

    unordered_map<int, double> result;

    for (int node : node_vec) {
        result[node] = rw_count_map[node] / (double) rwer_num;
    }

    return result;
}