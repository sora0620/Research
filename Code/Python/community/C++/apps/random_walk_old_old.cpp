#include <unordered_map>
#include <unordered_set>
#include <random>
#include <string>
#include <omp.h>
#include <chrono>
#include "../include/graph.h"
#include "../include/util.hpp"

// g++ -std=c++20 random_walk.cpp graph.cpp

using namespace std;

double ALPHA = 0.85; // 終了確率
int RANDOM_WALK_NUM = 1000;
int THREAD_NUM = 4;

// 乱数生成
std::random_device seed_gen;
std::mt19937 engine {seed_gen()};

// unordered_map 型の変数を value にてソートするための関数
// reverse が true だと降順, false だと昇順でソート
template<typename T,typename U>
vector<pair <T, U> > sort_second(unordered_map<T, U>& origin_map, bool reverse)
{
    vector<pair <T, U> > sorted_vec;
    vector<pair <U, T> > tmp_vec;

    for (auto iter = origin_map.begin(); iter != origin_map.end(); iter++) {
        pair<U, T> tmp_pair = make_pair(iter->second, iter->first);
        tmp_vec.push_back(tmp_pair);
    }
    if (reverse == true) {
        sort(tmp_vec.rbegin(), tmp_vec.rend());
    } else if (reverse == false) {
        sort(tmp_vec.begin(), tmp_vec.end());
    }

    for (pair<U, T> p : tmp_vec) {
        pair<T, U> tmp_pair = make_pair(p.second, p.first);
        sorted_vec.push_back(tmp_pair);
    }

    return sorted_vec;
}

unordered_map<int, double> setting_random_walk_flow(unordered_set<int>& change_node_set, int change_flow, unordered_set<int>& node_set)
{
    unordered_map<int, double> flow_map;

    for (int node : node_set) {
        flow_map[node] = RANDOM_WALK_NUM;
    }

    for (int node : change_node_set) {
        flow_map[node] = change_flow;
    }

    return flow_map;
}

unordered_map<int, int> visited_count_from_one_node(unordered_map<int, vector<int>>& adj_map, vector<int>& node_vec, int start_node, int random_walk_num)
{
    unordered_map<int, int> rw_count_map;
    int node_num = node_vec.size(); // 頂点数
    // vector<int> next_node_vec(1); // ランダム値保存用に 1 つだけ領域を確保

    // ランダム生成器
    StdRandNumGenerator gen;
    
    int current_node;
    int next_node;

    for (int i = 0; i < random_walk_num; i++) {
        current_node = start_node;

        while (true) {

            rw_count_map[current_node]++;

            if (gen.gen_float(1.0) > ALPHA) break;

            int degree = adj_map[current_node].size();

            if (degree == 0) {
                next_node = node_vec[gen.gen(node_num)];
            } else {
                next_node = adj_map[current_node][gen.gen(degree)];
            }

            current_node = next_node;


            // sample(adj_map[current_node].begin(),
            //     adj_map[current_node].end(),
            //     next_node_vec.begin(),
            //     1,
            //     engine);
            // next_node = next_node_vec.at(0);
            // rw_count_map[next_node]++;
            // current_node = next_node;

            // if (((double)rand() / RAND_MAX) > ALPHA) {
            //     break;
            // }
        }
    }

    return rw_count_map;
}

unordered_map<int, unordered_map <int, int> > visited_count_from_all_node(Graph& graph, unordered_set<int>& change_node_set, int change_flow)
{
    unordered_set<int> node_set = graph.get_node_set();
    unordered_map<int, vector <int> > adj_map = graph.get_adjacency_list();
    unordered_map<int, unordered_map <int, int> > count_map;
    unordered_map<int, double> flow_map = setting_random_walk_flow(change_node_set, change_flow, node_set);
    vector<int> parallel_vec; // OpenMP を利用するためには、数字指定で for 文を回す必要があるっぽい

    for (int node : node_set) {
        parallel_vec.push_back(node);
    }

    // for (auto iter = adj_map.begin(); iter != adj_map.end(); iter++) {
    //     if (iter->second.size() == 0) {
    //         for (int tmp_node : node_set) {
    //             adj_map[iter->first].insert(tmp_node);
    //         }
    //     }
    // }

    cout << "エッジ追加終了" << endl;

    // #pragma omp parallel for num_threads(THREAD_NUM)
    // count_map 競合しない？
    for (int i = 0; i < parallel_vec.size(); i++) {
        int node = parallel_vec.at(i);
        count_map[node] = visited_count_from_one_node(adj_map, parallel_vec, node, flow_map[node]);
        // cout << node << endl;
    }

    return count_map;
}

unordered_map<int, double> calc_pr(Graph& graph, unordered_set<int>& change_node_set, double change_flow)
{
    auto start = chrono::system_clock::now();

    unordered_map<int, unordered_map <int, int> > count_dict = visited_count_from_all_node(graph, change_node_set, change_flow);
    unordered_map<int, double> count_dict_pr;
    unordered_set<int> node_set = graph.get_node_set();
    int count_sum = 0;

    for (int node : node_set) {
        for (auto iter = count_dict[node].begin(); iter != count_dict[node].end(); iter++) {
            count_dict_pr[iter->first] += iter->second;
        }
    }

    for (auto iter = count_dict_pr.begin(); iter != count_dict_pr.end(); iter++) {
        count_sum += iter->second;
    }

    for (auto iter = count_dict_pr.begin(); iter != count_dict_pr.end(); iter++) {
        count_dict_pr[iter->first] = iter->second / count_sum;
    }

    auto end = chrono::system_clock::now();       // 計測終了時刻を保存
    auto dur = end - start;        // 要した時間を計算
    auto sec = chrono::duration_cast<std::chrono::seconds>(dur).count();

    cout << "Calc PR Time: " << sec << " sec\n" << endl;

    return count_dict_pr;
}

void check_def(Graph& graph, unordered_set<int>& change_node_set, int change_flow)
{
    unordered_set<int> node_set = graph.get_node_set();
    int graph_size = node_set.size();
    int top_num = 5;
    if (top_num > graph_size) {
        top_num = graph_size;
    }
    unordered_map<int, double> pr = graph.pagerank();
    vector<pair <int, double> > pr_sorted = sort_second(pr, true);
    vector<int> x_data;
    vector<int> y_data;

    for (pair<int, double> p : pr_sorted) {
        x_data.push_back(p.first);
    }

    cout << "Networkx" << endl;
    for (int i = 0; i < top_num; i++) {
        cout << "Node ID : " << x_data[i] << " | PR value : " << pr[x_data[i]] << endl;
    }
    cout << "----------------------------" << endl;

    unordered_map<int, double> ppr_sum_map = calc_pr(graph, change_node_set, change_flow);
    vector<pair <int, double> > ppr_sum_map_sort = sort_second(ppr_sum_map, true);

    for (pair<int, double> p : ppr_sum_map_sort) {
        y_data.push_back(p.first);
    }

    cout << "use PPR" << endl;
    for (int i = 0; i < top_num; i++) {
        cout << "Node ID : " << y_data[i] << " | PR value : " << ppr_sum_map[y_data[i]] << endl;
    }
    cout << "----------------------------" << endl;
}

// チェック用関数
/*
int main(int argc, char* argv[])
{
    string graph_name = "practice";
    unordered_set<int> change_node_set;
    int change_flow = RANDOM_WALK_NUM;

    Graph graph(graph_name);
    check_def(graph, change_node_set, change_flow);
}
*/

// これが main の関数なんだけど結果の表示をどうするかが問題
int main()
{
    // ハイパーパラメータ
    // vector<string> graph_list = {"p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"};
    vector<string> graph_list = {"scale_free"};
    unordered_set<int> change_node_set;
    int change_flow = RANDOM_WALK_NUM;

    for (string graph_name : graph_list) {
        cout << graph_name << endl;
        Graph graph(graph_name);
        check_def(graph, change_node_set, change_flow);
    }
}