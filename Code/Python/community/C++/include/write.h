#ifndef GUARD_WRITE_H
#define GUARD_WRITE_H

#include <string>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <vector>
#include "../include/graph.h"

using namespace std;
class Graph;

void write_to_file(string file_path, Graph graph);

#endif // GUAD_WRITE_H