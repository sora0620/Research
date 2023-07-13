#ifndef USEFUL_H
#define USEFUL_H

#include "header.h"

void print(int);

void print(double);

void print(std::map<int, int>);

void print(std::map<int, double>);

void print(std::map<int, std::vector <int> >);

void print(std::vector<int>);

void tokenize(std::string const &str, const char delim, std::vector<std::string> &out);

#endif