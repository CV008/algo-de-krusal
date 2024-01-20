#include <stdio.h>
#include <stdlib.h>

struct Edge {
    char u, v;    // Vertices connected by the edge
    float poids;  // Weight of the edge
};

struct DisjointSet {
    int *parent, *rank;
    int n;
};

struct DisjointSet *createSet(int n) {
    struct DisjointSet *set = (struct DisjointSet *)malloc(sizeof(struct DisjointSet));
    set->n = n;
    set->parent = (int *)malloc(n * sizeof(int));
    set->rank = (int *)malloc(n * sizeof(int));

    for (int i = 0; i < n; ++i) {
        set->parent[i] = i;
        set->rank[i] = 0;
    }

    return set;
}

int findSet(struct DisjointSet *set, int i) {
    if (i != set->parent[i]) {
        set->parent[i] = findSet(set, set->parent[i]); // Path compression
    }
    return set->parent[i];
}

void unionSets(struct DisjointSet *set, int x, int y) {
    int rootX = findSet(set, x);
    int rootY = findSet(set, y);

    if (set->rank[rootX] < set->rank[rootY]) {
        set->parent[rootX] = rootY;
    } else if (set->rank[rootX] > set->rank[rootY]) {
        set->parent[rootY] = rootX;
    } else {
        set->parent[rootY] = rootX;
        set->rank[rootX]++;
    }
}

int compareEdges(const void *a, const void *b) {
    return ((struct Edge *)a)->poids - ((struct Edge *)b)->poids;
}

void kruskal(struct Edge *edges, int nbEdges, int nbVertices) {
    qsort(edges, nbEdges, sizeof(struct Edge), compareEdges);

    struct DisjointSet *set = createSet(nbVertices);

    printf("Minimum Spanning Tree (Kruskal's Algorithm):\n");
    for (int i = 0; i < nbEdges; ++i) {
        char u = edges[i].u;
        char v = edges[i].v;

        int setU = findSet(set, u - 'A');
        int setV = findSet(set, v - 'A');

        if (setU != setV) {
            printf("%c -- %.2f -- %c\n", u, edges[i].poids, v);
            unionSets(set, setU, setV);
        }
    }

    free(set->parent);
    free(set->rank);
    free(set);
}

int main() {
    int nbVertices, nbEdges;

    printf("Enter the number of vertices in the graph: ");
    scanf("%d", &nbVertices);
    nbEdges = nbVertices * (nbVertices - 1) / 2;

    struct Edge edges[nbEdges];

    printf("Enter the weights of the edges in the graph:\n");
    for (int i = 0; i < nbEdges; ++i) {
        printf("Enter the weight for edge %d (u v poids): ", i + 1);
        scanf(" %c %c %f", &edges[i].u, &edges[i].v, &edges[i].poids);
    }

    kruskal(edges, nbEdges, nbVertices);

    return 0;
}
