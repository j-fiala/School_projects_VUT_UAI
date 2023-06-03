from random import randint
import networkx as nx
import matplotlib.pyplot as plt
import sys
from timeit import default_timer

#made by Jan Fiala 
#program  for visual represenation of minimal spanning tree of matematical graph using Boruvkas and Jarniks alg.
#comments language: Czech

#funkce hledani kostry grafu pomoci Boruvkova alg.
def boruvka(G):
    # Kopie zakladniho grafu a vrcholu
    T = nx.Graph()
    T.add_nodes_from(G.nodes)
    #separace 
    components = {node: [node] for node in G.nodes}

    # Opakuj dokud zustane jeden 
    while True:
        # Pocatecni hodnoty
        cheapest = sys.maxsize
        component_a = None
        component_b = None
        edge = None

        # Hledani nejlevnejsi hrany
        for u, v, w in G.edges(data='weight'):
            if w is not None and (u in components) and (v in components):
                if w < cheapest:
                    cheapest = w
                    component_a = components[u] if u in components else components[v]
                    component_b = components[v] if u in components else components[u]
                    edge = (u, v)

        # pridani hrany do kostry grafu
        if edge is not None:
            T.add_edge(*edge)

        # Sjednoceni komponent
        if component_a is not None and component_b is not None:
            component_a.extend(component_b)
            del components[component_b[0]]
            root_node = min(component_a, key=lambda x: x)
            components[root_node] = component_a
        
        # Break out kdyz zustane posledni komponent
        if len(components) == 1:
            break

    return T

#funkce na zjisteni minimalni hrany
def minDistance(dist, mstSet, V):
    min = sys.maxsize 
    for v in range(V):
        if mstSet[v] == False and dist[v] < min:
            min = dist[v]
            min_index = v
    return min_index

#funkce hledani kostry grafu pomoci Jarnika
def jar(G):
    # Kopie zakladniho grafu a vrcholu
    T = nx.Graph()
    T.add_nodes_from(G.nodes)
    V = len(G.nodes()) 

    dist = [] 
    parent = [None]*V 
    mstSet = []
    
    #Pocatecni podminky
    for i in range(V):
        dist.append(sys.maxsize)
        mstSet.append(False)
        dist[0] = 0
    # pocatecni hodnota, bez souseda
    parent[0]= -1 
    
    for count in range(V-1):
        u = minDistance(dist, mstSet, V) #nalezeni min hrany
        mstSet[u] = True
        
        #update vrcholu 
        for v in range(V):
            if (u, v) in G.edges():
                if mstSet[v] == False and G[u][v]['weight'] < dist[v]:
                    dist[v] = G[u][v]['weight']
                    parent[v] = u
    
    for X in range(V):
        if parent[X] != -1: 
            if (parent[X], X) in G.edges():
                T.add_edge(parent[X], X)

    
    return T

if __name__ == "__main__":

    # Vytvoreni random grafu, pocet vrcholu a hran
    G = nx.gnm_random_graph(8, 30)

    # Nahodne generovana váha hran
    edges = [(u, v, randint(0, 20)) for u, v in G.edges()]
    G.add_weighted_edges_from(edges)
    
    start = default_timer()
    B = boruvka(G)
    timevalueB = default_timer()-start
    J = jar(G)
    timevalueJ = default_timer()-start-timevalueB

    # Vykresleni grafu
    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(10,10))
    fig.suptitle('Pocet vrcholu: 8, pocet hran: 30')
    plt.subplot(221)
    nx.draw(G, pos=pos, with_labels=True)
    plt.title("Původní graf")
    plt.subplot(222)
    nx.draw(J, pos=pos, with_labels=True, node_color = 'r', edge_color = 'r')
    plt.title("Jarnikova minimalní kostra")
    plt.text(-0.8,-1.1,'Doba hledání: {} s'.format(timevalueJ), color='Black')
    plt.subplot(223)
    nx.draw(G, pos=pos, with_labels=True)
    plt.title("Původní graf")
    plt.subplot(224)
    nx.draw(B, pos=pos, with_labels=True, node_color = 'r', edge_color = 'r')
    plt.text(-0.8,-1.1,'Doba hledání: {} s'.format(timevalueB), color='Black')
    plt.title("Borůvkova minimalní kostra")
    plt.show()
