import csv
import math
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as pch
from os import listdir
import networkx as nx

labels = []

def loadSpikes(filename) :
    spikes = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            spikes.append(float(row[0]))
    return spikes

def smoothUnitSpikes(spikes, sd_threshold) :
    var = np.var([s for s in spikes if s != 0.0])
    sd = np.square(var)
    return [1 if s > sd*sd_threshold else 0 for s in spikes]

def compareUnitSpikes(spikes, labels) :
    series = range(0,len(spikes))
    times = range(0,len(spikes[0]))
    ordering = [[s for s in series if spikes[s][t] == 1] for t in times ]
    ordering = [x for x in ordering if len(x) > 0]
    return [[labels[l] for l in x[0]] for x in groupby(ordering)]

def showBoxPlot() :
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    files = listdir('../bon_4_6_run/smoothed/')
    unit_spikes = []

    ax1.set_xlim([0,10000])
    ax1.set_ylim([0,0.1*len(files)])
    ax1.yaxis.set_visible(False)

    file_pos = 0
    for f in files :
        placecell1 = loadSpikes('../bon_4_6_run/smoothed/' + f)
        #pc_var = np.var(placecell1)
        #print(pc_var)

        labels.append(f[5:-4])

        ax1.text(-1.0, file_pos + 0.01, f[5:-4],
            verticalalignment='bottom', horizontalalignment='right',
            #transform=ax1.transAxes,
            color='black', fontsize=10)

        unit_spikes1 = smoothUnitSpikes(placecell1, 0)
        unit_spikes.append(unit_spikes1)
        #print(unit_spikes1)

        for s in range(1,len(unit_spikes1)) :
            if unit_spikes1[s] == 1 :
                ax1.add_patch(
                    pch.Rectangle(
                        (s, file_pos),   # (x,y)
                        1,          # width
                        0.1,          # height
                    facecolor="blue")
                )
        file_pos += 0.1

    plt.show()

    overlaps = compareUnitSpikes(unit_spikes, labels)
    return overlaps

class Node :
    def __init__(self, cells) :
        self.cells = cells

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.cells == other.cells

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True

        return self.cells != other.cells

    def __hash__(self):
        return hash(tuple(sorted([hash(c) for c in self.cells])))

    def __repr__(self):
        return '{}'.format(self.cells)

    def __str__(self):
        return '{}'.format(self.cells)


def generateAdjacency(overlaps) :
    G = nx.Graph()

    for bin in range(0,len(overlaps)-1) :
        X = overlaps[bin]
        Y = overlaps[bin+1]
        node_x = Node(X)
        node_y = Node(Y)
        if not G.has_node(node_x) :
            G.add_node(node_x)
        if not G.has_node(node_y) :
            G.add_node(node_y)
        if not G.has_edge(node_x, node_y):
            G.add_edge(node_x, node_y, weight=1.0)
        else :
            G[node_x][node_y]['weight'] = G[node_x][node_y]['weight'] + 1.0


    bad = [(u,v) for (u,v,w) in G.edges(data='weight') if w <= 3 or (len(u.cells) == 1 and len(v.cells) == 1)]

    G.remove_edges_from(bad)

    more_bad = []

    for (u, v) in G.edges():
        if not G.has_edge(v, u):
            more_bad.append((u, v))

    G.remove_edges_from(more_bad)

    outdeg = G.degree()
    to_remove = [n for n in G.nodes() if outdeg[n] == 0]
    G.remove_nodes_from(to_remove)

    labels = nx.get_edge_attributes(G,'weight')
    pos=nx.circular_layout(G)
    nx.draw(G,pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,  label_pos=0.5)
    nx.draw_networkx_labels(G, pos)
    plt.show()

    return G

def generateAdjacencyNonIntersect(overlaps, labels) :
    G = nx.DiGraph()

    for x in labels :
        for t in range(0, len(overlaps) - 1):
            if x in overlaps[t] and x not in overlaps[t+1]:
                for nextbin in range(t+1, len(overlaps)-1):
                    if x not in overlaps[nextbin]:
                        ys = [y for y in overlaps[nextbin] if y not in overlaps[t]]
                        if ys :
                            node_x = Node(x)
                            if not G.has_node(node_x):
                                G.add_node(node_x)

                            node_y = Node(ys[0])
                            weights = [G[node_x][Node(y)]['weight'] for y in ys if G.has_node(Node(y)) and G.has_edge(node_x,Node(y))]
                            if weights:
                                y_index = np.argmax(np.array(weights))
                                node_y = Node(ys[y_index])

                            if not G.has_node(node_y):
                                G.add_node(node_y)

                            if not G.has_edge(node_x, node_y):
                                G.add_edge(node_x, node_y, weight=1.0)
                            else :
                                G[node_x][node_y]['weight'] = G[node_x][node_y]['weight'] + 1.0

                            break

    bad = [(u, v) for (u, v, w) in G.edges(data='weight') if w <= 1]

    G.remove_edges_from(bad)

    more_bad = []

    for (u, v) in G.edges():
        if not G.has_edge(v,u) :
            more_bad.append((u,v))

    G.remove_edges_from(more_bad)

    outdeg = G.out_degree()
    indeg = G.in_degree()
    to_remove = [n for n in G.nodes() if outdeg[n] == 0 and indeg[n] == 0]
    G.remove_nodes_from(to_remove)

    labels = nx.get_edge_attributes(G, 'weight')
    pos = nx.circular_layout(G)
    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.8)
    nx.draw_networkx_labels(G, pos)
    plt.show()

def generateAdjacencyCount(overlaps, labels) :
    G = nx.Graph()

    for x in labels :
        node_x = Node(x)
        if not G.has_node(node_x):
            G.add_node(node_x)
        for t in range(0, len(overlaps) - 1):
            if x in overlaps[t] and x not in overlaps[t+1]:
                for y in overlaps[t+1]:
                    node_y = Node(y)
                    if not G.has_node(node_y):
                        G.add_node(node_y)
                    if not G.has_edge(node_x, node_y):
                        G.add_edge(node_x, node_y, weight=1.0)
                    else:
                        G[node_x][node_y]['weight'] = G[node_x][node_y]['weight'] + 1.0

    # outdeg = G.degree()
    # for (u,v,w) in G.edges(data='weight'):
    #     G[u][v]['weight'] = G[u][v]['weight'] / outdeg[u]

    bad = [(u, v) for (u, v, w) in G.edges(data='weight') if w <= 20]

    G.remove_edges_from(bad)

    more_bad = []

    for (u, v) in G.edges():
        if not G.has_edge(v,u) :
            more_bad.append((u,v))

    G.remove_edges_from(more_bad)

    outdeg = G.degree()
    to_remove = [n for n in G.nodes() if outdeg[n] == 0]
    G.remove_nodes_from(to_remove)

    labels = nx.get_edge_attributes(G, 'weight')
    pos = nx.circular_layout(G)
    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.8)
    nx.draw_networkx_labels(G, pos)
    plt.show()
    return G

def generateAdjacencyRCC(overlaps, labels) :
    PO = nx.Graph()

    for x in labels:
        node_x = Node([x])
        if not PO.has_node(node_x):
            PO.add_node(node_x)

    firing_counts = {}
    for l in labels:
        firing_counts[l] = 0

    for bin in overlaps:
        nodes = [Node([x]) for x in bin]
        for x in bin:
            firing_counts[x] += 1
        for i in range(0,len(nodes)):
            for j in range(i,len(nodes)):
                if not PO.has_edge(nodes[i], nodes[j]):
                    PO.add_edge(nodes[i], nodes[j], weight=1.0)
                else:
                    PO[nodes[i]][nodes[j]]['weight'] = PO[nodes[i]][nodes[j]]['weight'] + 1.0

    # remove proper part nodes


    # averages = {}
    # for node in PO.nodes():
    #     weights = [w for (u,v,w) in PO.edges(node, data='weight')]
    #     averages[node] = np.mean(weights)
    #
    # for (u,v,w) in PO.edges(data='weight'):
    #     forward = PO[u][v]['weight'] / averages[u]
    #     backward = PO[v][u]['weight'] / averages[v]
    #     PO[u][v]['weight'] = max([forward, backward])

    mix = generateAdjacency(overlaps)
    PO = nx.compose(PO, mix)

    # pp_nodes = []
    # PP = nx.Graph()
    # for node in PO.nodes() :
    #     node_fire_count = 0
    #     if not PP.has_node(node):
    #         PP.add_node(node)
    #     for bin in overlaps:
    #         if node not in bin:
    #             continue
    #         node_fire_count += 1
    #         for other in PO.nodes():
    #             if other in bin:
    #                 if not PP.has_node(other):
    #                     PP.add_node(other)
    #                 if not PP.has_edge(node, other):
    #                     PP.add_edge(node, other, weight=1.0)
    #                 else:
    #                     G[node][other]['weight'] = G[node][other]['weight'] + 1.0
    #     for (u,v,w) in PP.edges(data='weight') :
    #         if u == node and w/node_fire_count > 0.7 :
    #             print('{} part of {}'.format(u,v))
    #             if u not in pp_nodes:
    #                 pp_nodes.append(u)
    #
    # PO.remove_nodes_from(pp_nodes)


    # cutoff 25 for W, 140 for figure8
    bad = [(u, v) for (u, v, w) in PO.edges(data='weight') if w <= 6 or u == v]
    PO.remove_edges_from(bad)

    outdeg = PO.degree()
    to_remove = [n for n in PO.nodes() if outdeg[n] == 0]
    PO.remove_nodes_from(to_remove)

    edges = []
    for node in PO.nodes():
        if len(node.cells) > 1:
            for (u,v) in PO.edges(node):
                for (u2, v2) in PO.edges(node):
                    if not v.cells == v2.cells:
                        if PO.has_edge(v, v2):
                            if all(i in node.cells for i in v.cells) and all(i in node.cells for i in v2.cells):
                                if PO[u][v]['weight'] < (PO[v][v2]['weight'] * (3.0/4.0)) and PO[u][v2]['weight'] < (PO[v][v2]['weight'] * 3.0 / 4.0):
                                    edges.append((v,v2))
    print(edges)

    PO.remove_edges_from(edges)

    # for (u,v,w) in PO.edges(data='weight'):
    #     forward = PO[u][v]['weight'] / firing_counts[str(u)]
    #     backward = PO[v][u]['weight'] / firing_counts[str(v)]
    #     PO[u][v]['weight'] = max([forward, backward])

    # adjGraph = generateAdjacencyCount(overlaps, labels)
    #
    # for t in range(1,len(overlaps)-1):
    #     nodes_nm1 = [Node(n) for n in overlaps[t-1]]
    #     nodes_n = [Node(n) for n in overlaps[t]]
    #     nodes_np1 = [Node(n) for n in overlaps[t+1]]
    #     for n in nodes_n:
    #         for nm1 in nodes_nm1:
    #             if PO.has_edge(nm1, n):
    #                 for np1 in nodes_np1:
    #                     if PO.has_edge(n, np1):
    #                         if (not adjGraph.has_edge(n, np1)) :
    #                             PO[nm1][n]['weight'] = PO[nm1][n]['weight'] - 1
    #                         else :
    #                             PO[nm1][n]['weight'] = PO[nm1][n]['weight'] + 1
    #
    # for (u,v,w) in PO.edges(data='weight'):
    #     forward = PO[u][v]['weight']
    #     backward = PO[v][u]['weight']
    #     PO[u][v]['weight'] = max([forward, backward])
    #
    # bad = [(u, v) for (u, v, w) in PO.edges(data='weight') if w <= 0 or u == v]
    # PO.remove_edges_from(bad)
    #
    # outdeg = PO.degree()
    # to_remove = [n for n in PO.nodes() if outdeg[n] == 0]
    # PO.remove_nodes_from(to_remove)

    for node in PO.nodes():
        print([node, getNumComponents([node], PO)])

    labels = nx.get_edge_attributes(PO, 'weight')
    pos = nx.circular_layout(PO)
    nx.draw(PO, pos)
    nx.draw_networkx_edge_labels(PO, pos, edge_labels=labels, label_pos=0.5)
    nx.draw_networkx_labels(PO, pos)
    plt.show()

    #weight cutoff plot
    # totals = []
    # means = []
    # for cutoff in range(1,100) :
    #     graph = nx.Graph(PO)
    #     bad = [(u, v) for (u, v, w) in graph.edges(data='weight') if w <= cutoff or u == v]
    #     graph.remove_edges_from(bad)
    #
    #     outdeg = graph.degree()
    #     to_remove = [n for n in graph.nodes() if outdeg[n] == 0]
    #     graph.remove_nodes_from(to_remove)
    #
    #     estimates = []
    #     for node in graph.nodes():
    #         estimates.append(getNumComponents([node], graph))
    #     totals.append(sum(estimates))
    #     means.append(np.median(estimates))
    #
    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(111)
    # ax1.plot(totals)
    # ax1.plot(means)
    # plt.show()

def getNumComponents(nodes, graph) :

    adjacent_nodes = []
    for (u,v) in graph.edges(nodes):
        adjacent_nodes.append(v)
    adjacent_nodes = list(set(adjacent_nodes) - set(nodes))

    if not adjacent_nodes:
        if len(nodes) > 1:
            return 1
        return 0

    subgraph = graph.subgraph([n for n in graph.nodes() if n in adjacent_nodes])

    separates = nx.connected_components(subgraph)
    count = 0
    for s in separates:
        #print([nodes, s])
        count += getNumComponents(s, graph.subgraph([n for n in graph.nodes() if n not in nodes]))
    if count == 0:
        return 1
    return count


overlaps = showBoxPlot()
generateAdjacencyRCC(overlaps, labels)
#generateAdjacencyCount(overlaps, labels)
#generateAdjacency(overlaps)
#generateAdjacencyNonIntersect(overlaps,labels)
