import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=100)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family='sans-serif')
    grafo_labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph,pos, edge_labels = grafo_labels)

    plt.axis('off')
    plt.show()


def plot_fitness(vect):
    plt.plot(vect)
    plt.show()
