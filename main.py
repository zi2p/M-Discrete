# M-Discrete
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import approximation

G = nx.Graph()  # создание нового графа
g = nx.Graph()  # граф-максимальная компонента связности
g_w = nx.Graph()   # взвешенный граф
with open('vertices.txt', encoding='windows-1251') as f:  # считывание вершин
    s = f.readlines()
    country = {}  # список вершин (список стран)
    for i in s:
        raw = i.split(',')
        country[raw[0]] = raw[1]

with open('edges.txt', encoding='windows-1251') as f:  # считывание ребер
    s = f.readlines()
    country_list = {}  # словарь (список смежности)
    for i in s:
        raw = i.split(',')
        a, b = raw[0], raw[1]
        if country_list.get(a) == None:
            country_list[a] = []
        country_list[a].append(b)
        if country_list.get(b) == None:
            country_list[b] = []
        country_list[b].append(a)

with open('v_for_g.txt', encoding='utf-8') as f:  # считывание вершин
    s = f.readlines()
    country_maxcomp = {}  # список вершин (список стран)
    for i in s:
        raw = i.split(',')
        country_maxcomp[raw[0]] = raw[1]

with open('edge_for_g.txt', encoding='windows-1251') as f:  # считывание ребер
    s = f.readlines()
    country_list_maxcomp = {}  # словарь (список смежности)
    for i in s:
        raw = i.split(',')
        a, b = raw[0], raw[1]
        if country_list_maxcomp.get(a) == None:
            country_list_maxcomp[a] = []
        country_list_maxcomp[a].append(b)
        if country_list_maxcomp.get(b) == None:
            country_list_maxcomp[b] = []
        country_list_maxcomp[b].append(a)

for i in country_list_maxcomp:  # добавление ребер в граф
    for j in country_list_maxcomp[i]:
        a, b = i, j
        g.add_edge(country_maxcomp[a], country_maxcomp[b])
        g.add_edge(country_maxcomp[b], country_maxcomp[a])

for i in range(len(country_maxcomp)):
    if country_list_maxcomp.get(str(i)) == None:
        g.add_node(country_maxcomp[str(i)])

print("радиус =", nx.radius(g))

for i in country_list:  # добавление ребер в граф
    for j in country_list[i]:
        a, b = i, j
        G.add_edge(country[a], country[b])
        G.add_edge(country[b], country[a])

for i in range(len(country)):
    if country_list.get(str(i)) == None:
        G.add_node(country[str(i)])

maxcomp = sorted([i for i in nx.connected_components(G)], key=lambda x: -len(x))[0]  # максимальная компонента графа

reverse_country = {country[i]: i for i in country}  # менять местами ключ и его значение

plt.plot()
nx.draw_networkx(G, with_labels = True, font_size = 8)
plt.show()

print("минимальная степень вершин =", min([len(country_list[str(i)]) for i in country_list if
                                           i in [reverse_country[j] for j in maxcomp]]))  # минимальная степень вершин

print("максимальная степень вершин =", max([len(country_list[str(i)]) for i in country_list if
                                            i in [reverse_country[j] for j in maxcomp]]))  # максимальная степень вершин

print("размер клики =", nx.graph_clique_number(g))
print("ВСЕ КЛИКИ ->", nx.cliques_containing_node(g))
print("|matching| =", len(nx.max_weight_matching(g)), "\nвот они(ребра) =", nx.max_weight_matching(g))
print("stable set (вероятно\невероятно)", len(nx.maximal_independent_set(g)), nx.maximal_independent_set(g))
print("stable set ", len(nx.algorithms.approximation.maximum_independent_set(g)))
print("вершинное покрытие ", len(nx.algorithms.approximation.min_weighted_vertex_cover(g)), nx.algorithms.approximation.min_weighted_vertex_cover(g))

with open('weight.txt', encoding='windows-1251') as f:  # считывание ребер
    s = f.readlines()
    for i in s:
        r = i.split(',')
        fr, to, w = r[0], r[1], int(r[2])
        g_w.add_edge(fr, to, weight=int(w))
        g_w.add_edge(to, fr, weight=int(w))

plt.plot()
t = nx.Graph    # оставное дерево
t = nx.algorithms.tree.mst.minimum_spanning_tree(g_w)
nx.draw_networkx(t, with_labels = True, font_size = 8)
plt.show()
