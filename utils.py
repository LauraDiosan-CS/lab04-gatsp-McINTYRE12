import networkx as nx
import matplotlib.pyplot as plt

def read_input(path):
    graph = nx.Graph()
    
    file = open(path, "r")
    
    number_of_cities = int(file.readline())
    
    for i in range(0, number_of_cities):
        dists = file.readline()
        dists = dists.split(',')
        
        crt = 0
        for x in dists:
            graph.add_edge(str(i), str(crt), weight = x, distance = x)
            crt = crt + 1
            
    start_city = int(file.readline())
    dest_city = int(file.readline())