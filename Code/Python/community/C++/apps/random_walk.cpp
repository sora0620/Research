#include <unordered_map>
#include <unordered_set>
#include <random>
#include <string>
#include <omp.h>
#include <chrono>
#include <atomic>
#include <algorithm>
#include "../include/graph.h"
#include "../include/json.hpp"
#include "../include/util.hpp"

// g++ -std=c++2a random_walk.cpp graph.cpp -fopenmp
// _1 が最古、数字が大きいほうが新しく、random_walk.cpp が最新って形にしよう

using namespace std;
using json = nlohmann::json;

double ALPHA = 0.15; // 終了確率
int RANDOM_WALK_NUM = 500;
int CHANGE_FLOW = 500;
int THREAD_NUM = 20;

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

unordered_map<int, double> setting_random_walk_flow(vector<int>& change_node_set, int change_flow, unordered_set<int>& node_set)
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

            if (gen.gen_float(1.0) < ALPHA) break;

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

void visited_count_from_all_node(vector<unordered_map<int, int>>& count_dict, Graph& graph, vector<int>& change_node_set, int change_flow)
{
    unordered_set<int> node_set = graph.get_node_set();
    unordered_map<int, vector <int> > adj_map = graph.get_adjacency_list();
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

    #pragma omp parallel for num_threads(THREAD_NUM)
    for (int i = 0; i < parallel_vec.size(); i++) {
        int node = parallel_vec.at(i);
        count_dict[node] = visited_count_from_one_node(adj_map, parallel_vec, node, flow_map[node]);
    }
}

vector<pair <int, double> > calc_pr(Graph& graph, vector<int>& change_node_set, double change_flow)
{
    int max_node_id = graph.getMaxNodeId();
    vector<unordered_map <int, int> > count_dict(max_node_id+1);

    // RW 実行
    auto start = chrono::system_clock::now();

    visited_count_from_all_node(count_dict, graph, change_node_set, change_flow);

    auto end = chrono::system_clock::now();       // 計測終了時刻を保存
    auto dur = end - start;        // 要した時間を計算
    auto sec = chrono::duration_cast<std::chrono::seconds>(dur).count();

    cout << "RW Time: " << sec << " sec" << endl;

    // PR 計算
    auto start_pr = chrono::system_clock::now();

    // unordered_map<int, double> count_dict_pr;
    vector<atomic <double> > count_dict_pr(max_node_id+1);
    unordered_set<int> node_set = graph.get_node_set();
    // atomic<int> count_sum = 0;
    int count_sum = 0;

    vector<int> parallel_vec;

    for (int node : node_set) {
        parallel_vec.push_back(node);
    }

    #pragma omp parallel for num_threads(THREAD_NUM)
    for (int i = 0; i < parallel_vec.size(); i++) {
        int node = parallel_vec.at(i);
        for (auto iter = count_dict[node].begin(); iter != count_dict[node].end(); iter++) {
            count_dict_pr[iter->first] = count_dict_pr[iter->first] + iter->second;
            // count_sum = count_sum + iter->second;
        }
    }

    for (int node : node_set) {
        count_sum += count_dict_pr[node];
    }

    // cout << count_sum << endl;

    // for (auto iter = count_dict_pr.begin(); iter != count_dict_pr.end(); iter++) {
    //     count_sum = count_sum + iter->second;
    // }

    vector<pair<double, int>> vec; // (pr の値*(-1), node_id)

    for (int node : node_set) {
        count_dict_pr[node] = count_dict_pr[node] / count_sum;
        vec.emplace_back(-count_dict_pr[node], node);
    }

    sort(vec.begin(), vec.end());

    vector<pair<int, double>> result; // (node_id, pr の値)
    for (auto [pr, node] : vec) {
        result.emplace_back(node, -pr);
    }

    // for (auto iter = count_dict_pr.begin(); iter != count_dict_pr.end(); iter++) {
    //     count_dict_pr[iter->first] = iter->second / count_sum;
    // }

    // return count_dict_pr;

    auto end_pr = chrono::system_clock::now();       // 計測終了時刻を保存
    auto dur_pr = end_pr - start_pr;        // 要した時間を計算
    auto sec_pr = chrono::duration_cast<std::chrono::seconds>(dur_pr).count();

    cout << "PR_calc Time: " << sec_pr << " sec\n" << endl;

    return result;
}

void check_def(Graph& graph, vector<int>& change_node_set, int change_flow)
{
    unordered_set<int> node_set = graph.get_node_set();
    int graph_size = node_set.size();
    int top_num = 5;
    if (top_num > graph_size) {
        top_num = graph_size;
    }
    unordered_map<int, double> pr = graph.pagerank();
    vector<pair <int, double> > pr_sorted = sort_second(pr, true);

    cout << "NetworkX" << endl;
    for (int i = 0; i < top_num; i++) {
        cout << "Node ID : " << pr_sorted[i].first << " | PR value : " << pr_sorted[i].second << endl;
    }
    cout << "----------------------------" << endl;

    vector<pair <int, double> > ppr_sum_map_sort = calc_pr(graph, change_node_set, change_flow);
    // vector<pair <int, double> > ppr_sum_map_sort = sort_second(ppr_sum_map, true);

    cout << "user PR" << endl;
    for (int i = 0; i < top_num; i++) {
        cout << "Node ID : " << ppr_sum_map_sort[i].first << " | PR value : " << ppr_sum_map_sort[i].second << endl;
    }
    cout << "----------------------------" << endl;
}

void write_json(string graph_name, Graph& graph, vector<int>& change_node_set, int change_flow)
{
    string path = "../../../Dataset/Static/RW/" + graph_name + "/" + to_string(RANDOM_WALK_NUM) + "_" + to_string(change_flow) + ".json";

    ofstream ofs(path);
    if (ofs.good())
    {
        json m_json;
        vector<pair <int, double> > ppr_sum_map_sort = calc_pr(graph, change_node_set, change_flow);
        unordered_map<int, int> in_deg_map = graph.get_in_deg();

        for (pair p : ppr_sum_map_sort) {
            // m_json[to_string(p.first)] = p.second;
            m_json[to_string(p.first)] = {p.second, in_deg_map[p.first]};
        }

        ofs << m_json.dump(4);
    }
    else
    {
        cout << "ファイルの読み込みに失敗しました" << endl;
    }
}

// チェック用関数
int main(int argc, char* argv[])
{
    // vector<string> graph_list = {"practice"};
    // vector<string> graph_list = {"p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"};
    // vector<string> graph_list = {"p2p-Gnutella24", "wiki-Talk"};
    vector<string> graph_list = {"amazon0601"};
    vector<int> change_node_set;
    int change_flow = RANDOM_WALK_NUM;

    for (string graph_name : graph_list) {
        Graph graph(graph_name);
        cout << graph_name << endl;
        check_def(graph, change_node_set, change_flow);
    }
}

/*
int main()
{
    // ハイパーパラメータ
    // vector<string> graph_list = {"p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"};
    vector<string> graph_list = {"wiki-Talk"};
    int change_flow = CHANGE_FLOW;

    for (string graph_name : graph_list) {
        Graph graph(graph_name);
        vector<int> change_node_set; // 境界ノードを格納する変数
        unordered_set<int> node_set = graph.get_node_set();
        int graph_size = node_set.size(); // グラフサイズ
        double reduction_value = 0.001; // 境界ノード数を グラフサイズ * この変数 で設定. とりあえずノード数の 0.1 % で設定
        int get_size = graph_size * reduction_value;
        sample(node_set.begin(), 
            node_set.end(), 
            back_inserter(change_node_set), 
            get_size, 
            engine);

        cout << graph_name << endl;
        write_json(graph_name, graph, change_node_set, change_flow);
    }
}
*/