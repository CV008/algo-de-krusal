import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, u, v, w):
        # Ajoute une arête avec poids w entre les sommets u et v
        self.edges.append((u, v, w))

    def find_parent(self, parent, i):
        # Trouve le représentant (parent) de l'ensemble auquel i appartient
        if parent[i] == i:
            return i
        return self.find_parent(parent, parent[i])

    def union(self, parent, rank, x, y):
        # Effectue l'union de deux ensembles en utilisant l'heuristique du rang
        root_x = self.find_parent(parent, x)
        root_y = self.find_parent(parent, y)

        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_x] = root_y
            rank[root_y] += 1

    def kruskal(self):
        result = []  # Stocke les arêtes de l'arbre couvrant minimal
        self.edges = sorted(self.edges, key=lambda item: item[2])  # Trie par poids croissant

        parent = [i for i in range(self.vertices)]
        rank = [0] * self.vertices

        i = 0  # Indice de l'arête triée
        e = 0  # Indice de l'arête ajoutée à l'arbre couvrant minimal

        while e < self.vertices - 1:
            u, v, w = self.edges[i]
            i += 1
            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)

            if x != y:
                e += 1
                result.append((u, v, w))
                self.union(parent, rank, x, y)

        return result

# Sommet graphe
g = Graph(7)
g.add_edge(0, 1, 9)
g.add_edge(0, 2, 5)
g.add_edge(0, 3, 3)
g.add_edge(1, 3, 14)
g.add_edge(2, 4, 6)
g.add_edge(3, 5, 2)
g.add_edge(4, 6, 10)
g.add_edge(2, 6, 8)
g.add_edge(1, 5, 7)
g.add_edge(3, 6, 5)
# g.add_edge(1, 4, 11)

# Visualisation du graphe initial
G = nx.Graph()
for edge in g.edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Graphe initial")
plt.show()

# Application de l'algorithme de Kruskal
minimum_spanning_tree = g.kruskal()

# Visualisation de l'arbre couvrant minimal
MST = nx.Graph()
for edge in minimum_spanning_tree:
    MST.add_edge(edge[0], edge[1], weight=edge[2])

pos_MST = nx.spring_layout(MST)
nx.draw(MST, pos_MST, with_labels=True, font_weight='bold', node_size=700, edge_color='r')
edge_labels_MST = nx.get_edge_attributes(MST, 'weight')
nx.draw_networkx_edge_labels(MST, pos_MST, edge_labels=edge_labels_MST)
plt.title("Arbre couvrant minimal (Kruskal)")
plt.show()