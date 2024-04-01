#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <map>
#include <sstream>
#include "../include/graph.h"


using namespace std;

// 指定したファイルの読み込み　無向グラフ
void read_ugraph_from_text_file(string file_path, Graph& graph){
    ifstream ifs(file_path);
    if(!ifs){
        cout << "Failed to open file" << endl;
        exit(-1);
    } else {
        for(int n3, n4; ifs >> n3 >> n4;){
            graph.u_add_edge(n3, n4);
        }
    }
}

// PR 値読み込み
void read_pr_from_text_file(string file_path, Graph& graph){
    ifstream ifs(file_path);
    if(!ifs){
        cout << "Failed to open file" << endl;
        exit(-1);
    } else{
        string str;
        int i;
        double d;
        while(getline(ifs, str)){
            stringstream ss(str);
            ss >> i >> d;
            graph.pr_list[i] = d;
        }
    }
}