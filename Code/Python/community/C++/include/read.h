#ifndef GUARD_READ_H
#define GUARD_READ_H

#include <string>
#include <unordered_map>

using namespace std;
class Graph;

void read_ugraph_from_text_file(string file_path, Graph& graph);

void read_pr_from_text_file(string file_path, Graph& graph);

#endif // GUAD_READ_H