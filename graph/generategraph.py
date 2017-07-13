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

    files = listdir('../bon_4_2_run/smoothed/')
    unit_spikes = []

    ax1.set_xlim([0,10000])
    ax1.set_ylim([0,0.1*len(files)])
    ax1.yaxis.set_visible(False)

    file_pos = 0
    for f in files :
        placecell1 = loadSpikes('../bon_4_2_run/smoothed/' + f)
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
    G = nx.DiGraph()

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


    bad = [(u,v) for (u,v,w) in G.edges(data='weight') if w <= 1]

    #G.remove_edges_from(bad)

    more_bad = []

    for (u, v) in G.edges():
        if not G.has_edge(v, u):
            more_bad.append((u, v))

    G.remove_edges_from(more_bad)

    outdeg = G.out_degree()
    indeg = G.in_degree()
    to_remove = [n for n in G.nodes() if outdeg[n] == 0 and indeg[n] == 0]
    G.remove_nodes_from(to_remove)

    labels = nx.get_edge_attributes(G,'weight')
    pos=nx.circular_layout(G)
    nx.draw(G,pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,  label_pos=0.8)
    nx.draw_networkx_labels(G, pos)
    plt.show()

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
    G = nx.DiGraph()

    for x in labels :
        node_x = Node(x)
        if not G.has_node(node_x):
            G.add_node(node_x)
        for t in range(0, len(overlaps) - 1):
            if x in overlaps[t] and x not in overlaps[t+1]:
                for y in overlaps[t+1]:
                    if y not in overlaps[t]:
                        node_y = Node(y)
                        if not G.has_node(node_y):
                            G.add_node(node_y)
                        if not G.has_edge(node_x, node_y):
                            G.add_edge(node_x, node_y, weight=1.0)
                        else:
                            G[node_x][node_y]['weight'] = G[node_x][node_y]['weight'] + 1.0

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

def generateAdjacencyRCC(overlaps, labels) :
    PO = nx.Graph()
    PP = nx.Graph()

    for x in labels:
        node_x = Node(x)
        if not PO.has_node(node_x):
            PO.add_node(node_x)

    for x in labels:
        node_x = Node(x)
        if not PP.has_node(node_x):
            PP.add_node(node_x)

    for bin in overlaps:
        nodes = [Node(x) for x in bin]
        for i in range(0,len(nodes)):
            for j in range(i,len(nodes)):
                if not PO.has_edge(nodes[i], nodes[j]):
                    PO.add_edge(nodes[i], nodes[j], weight=1.0)
                else:
                    PO[nodes[i]][nodes[j]]['weight'] = PO[nodes[i]][nodes[j]]['weight'] + 1.0

    # remove proper part nodes

    pp_nodes = []
    for node in PP.nodes() :
        node_fire_count = 0
        for bin in overlaps:
            nodes = [Node(x) for x in bin]
            if node in nodes:
                node_fire_count += 1
                for other in nodes:
                    if other == node:
                        continue
                    if not PP.has_edge(node, other):
                        PP.add_edge(node, other, weight=1.0)
                    else:
                        PP[node][other]['weight'] = PP[node][other]['weight'] + 1.0
        for (u,v,w) in PP.edges(data='weight') :
            if u == node and w/node_fire_count > 0.7 :
                print('{} part of {}'.format(u,v))
                if u not in pp_nodes:
                    pp_nodes.append(u)

        PP.clear()
        for x in labels:
            node_x = Node(x)
            if not PP.has_node(node_x):
                PP.add_node(node_x)
    #PO.remove_nodes_from(pp_nodes)

    # cutoff 25 for W, 140 for figure8
    bad = [(u, v) for (u, v, w) in PO.edges(data='weight') if w <= 25 or u == v]
    PO.remove_edges_from(bad)

    outdeg = PO.degree()
    to_remove = [n for n in PO.nodes() if outdeg[n] == 0]
    PO.remove_nodes_from(to_remove)

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
    # for cutoff in range(100,250) :
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
    #print([nodes, graph.nodes()])

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
        count += getNumComponents(s, graph.subgraph([n for n in graph.nodes() if n not in nodes]))
    if count == 0:
        return 1
    return count


overlaps = showBoxPlot()
generateAdjacencyRCC(overlaps, labels)
#generateAdjacencyCount(overlaps, labels)
#generateAdjacency(overlaps)
#generateAdjacencyNonIntersect(overlaps,labels)
