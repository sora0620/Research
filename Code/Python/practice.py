import random

graph_size = 26518
subgraph_num = 2
size_range = 0.2

# 8 ~ 12 の範囲で値を10分割する

level = 0

kijun = graph_size // subgraph_num
tmp_list = []
size_range = int(kijun * size_range)
upper = kijun + size_range
lower = kijun - size_range

for i in range(subgraph_num):
    if i != subgraph_num - 1:
        sub = abs(level) + size_range - (subgraph_num - i - 1) * size_range
        print(f"{i+1} level, sub: {level}, {sub}")
        if sub > 0:
            if level < 0:
                ran = random.randint(lower + sub, upper)
            elif level > 0:
                ran = random.randint(lower, upper - sub)
        else:
            ran = random.randint(lower, upper)
    elif i == subgraph_num - 1:
        ran = graph_size - sum(tmp_list)
    tmp_list.append(ran)
    level += ran - kijun

if sum(tmp_list) != graph_size:
    print("Error!")
    exit(1)

print(tmp_list)
print(sum(tmp_list))