#include <iostream>
#include <string>
#include <fstream>
#include "../include/json.hpp"
#include "../include/graph.h"

using namespace std;
using json = nlohmann::json;

int default_flow = 1000;
int change_flow = 1000;

int main() {
    string path = "/Users/sora/Documents/Lab/Research/Dataset/Static/RW/practice/" + to_string(default_flow) + "_" + to_string(change_flow) + ".json";

    // 読み込み
    // ifstream ifs(path);
    // if (ifs.good())
    // {
    //     json m_json;

    //     ifs >> m_json;
    //     cout << m_json["1"] << endl;
    // }
    // else
    // {
    //     cout << "ファイルの読み込みに失敗しました" << endl;
    // }

    // 書き込み
    ofstream ofs(path);
    if (ofs.good()) {
        json m_json;

        m_json["1"] = {"a", "b"};

        ofs << m_json.dump(4);
    }

    return 0;
}