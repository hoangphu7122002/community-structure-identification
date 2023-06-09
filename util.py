import numpy as np
import pandas as pd
import networkx as nx
from typing import Callable
from itertools import product, combinations
from collections import deque

np.random.seed(4)

def get_data(k):
        # np.random.seed(10)
    data = np.zeros((k,k))
    for i in range(len(data)):
        for j in range(len(data)):
            data[i,j] = np.random.choice([0,1], p=[0.6, 0.4])
    data = data + np.multiply(data.T, data.T > data) - np.multiply(data, data.T > data)
    for i in range(len(data)):
        data[i, i] = 0
        # data[i,k] = 0
        # data[k,i] = 0
    return data

def intercommunity_matrix(adj_matrix, communities, aggr: Callable = sum):
    num_nodes = len(communities)
    intercomm_adj_matrix = np.zeros((num_nodes, num_nodes))
    for i, src_comm in enumerate(communities):
        for j, targ_comm in enumerate(communities):
            if j > i:
                break
            edge_weights = []
        for u, v in product(src_comm, targ_comm):
            edge_weights.append(adj_matrix[u, v])
        edge_weight = aggr(edge_weights)
        intercomm_adj_matrix[i, j] = edge_weight
        intercomm_adj_matrix[j, i] = edge_weight
    
    return intercommunity_matrix()
        
def laplacian_matrix(adj_matrix : np.ndarray):
    diagonal = adj_matrix.sum(axis=1)
    D = np.diag(diagonal)
    L = D - adj_matrix

    return L

def modularity_matrix(adj_matrix : np.ndarray):
    k_i = np.expand_dims(adj_matrix.sum(axis=1), axis=1)
    # print(k_i)
    k_j = k_i.T
    norm = 1 / k_i.sum()
    K = norm * np.matmul(k_i, k_j)

    return (adj_matrix - K)

def modularity(mod_matrix : np.ndarray, communities : list):
    C = np.zeros_like(mod_matrix)
    for community in communities:
        for i, j in combinations(community, 2):
            C[i, j] = 1.0
            C[j, i] = 1.0
    # print(C)
    return np.tril(np.multiply(mod_matrix, C), 0).sum()

def getAdjMatrix(input_file, m = 10000):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Determine the number of nodes from the maximum node ID
    max_node_id = max([int(line.strip().split()[1]) for line in lines])
    num_nodes = max_node_id

    
    if m < max_node_id:
        num_nodes = m


    # Initialize adjacency matrix
    adj_matrix = np.zeros((num_nodes, num_nodes))
    # print(adj_matrix.shape)


    count = 0
    # Iterate over edges and update adjacency matrix
    for line in lines:
        if count >= m:
            break
        else: 
            count += 1
        a, b = map(int, line.strip().split())
        if a > m or b > m:
            count -=1
            continue
        # print(a,b)
        # Resize adjacency matrix if necessary
        if max(a, b) > num_nodes:
            adj_matrix = np.pad(adj_matrix, ((0, max(a, b)-num_nodes), (0, max(a, b)-num_nodes)), mode='constant')
            num_nodes = max(a, b)
        adj_matrix[a-1][b-1] = 1
        adj_matrix[b-1][a-1] = 1

    return adj_matrix


G = nx.karate_club_graph()
    
def getComponent(G):
    # Get list of edges

    # Initialize visited set and components list
    visited = set()
    components = []
    for u in range(G.number_of_nodes()):
        if u not in visited:
            component = []
            queue = deque([u])
            visited.add(u)
            while queue:
                node = queue.popleft()
                component.append(node)
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        queue.append(neighbor)
                        visited.add(neighbor)
            components.append(component)
    # Iterate over edges and perform BFS
    # for u, v in edges:
    #     if u not in visited:
    #         # Start a new component
    #         component = []
    #         queue = deque([u])
    #         visited.add(u)
    #         while queue:
    #             node = queue.popleft()
    #             component.append(node)
    #             for neighbor in G.neighbors(node):
    #                 if neighbor not in visited and (node, neighbor) in edges:
    #                     queue.append(neighbor)
    #                     visited.add(neighbor)
    #         components.append(component)

    return components
    
def getComponentAdjMatrix(adjMatrix, max = 0):
    # Initialize visited set and components list
    visited = set()
    components = []
    if max == 0 or max > adjMatrix.shape[0]:
        max = adjMatrix.shape[0]

    # Iterate over nodes and perform BFS
    for node in range(max):
        if node not in visited:
            # Start a new component
            component = []
            queue = deque([node])
            visited.add(node)
            while queue:
                node = queue.popleft()
                component.append(node)
                neighbors = np.nonzero(adjMatrix[node])[0]
                for neighbor in neighbors:
                    if neighbor not in visited and adjMatrix[node][neighbor] == 1:
                        queue.append(neighbor)
                        visited.add(neighbor)
            components.append(component)

    return components

import csv


def generate_adjacency_matrix_from_multigraph(input_file):
    # Read the input file
    with open(input_file, "r") as file:
        input_data = [line.strip().split()[:2] for line in file.readlines()]

    with open('input.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(input_data)

    # Extract the unique nodes from the input data
    nodes = set()
    for edge in input_data:
        nodes.add(int(edge[0]))
        nodes.add(int(edge[1]))

    # Create an empty adjacency matrix
    num_nodes = len(nodes)
    adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    # Populate the adjacency matrix
    for edge in input_data:
        node_a, node_b = int(edge[0]), int(edge[1])
        adj_matrix[node_a - 1][node_b - 1] += 1
        adj_matrix[node_b - 1][node_a - 1] += 1  # Consider the reverse direction as well


    return adj_matrix

  
if __name__ == "__main__":
    data = get_data(4)
    # print(data)
    # print(modularity_matrix(data))
    # print(betweennes_matrix(data))
    # lap_matrix = laplacian_matrix(data)
    # print(lap_matrix)

    # eigenvalues, eigenvectors = np.linalg.eig(lap_matrix)
    # print(eigenvalues)


# adj_matrix_multi = generate_adjacency_matrix_from_multigraph("multigraph.txt")
# print(adj_matrix_multi)
# adj_matrix = getAdjMatrix("dataset/edge.txt",40)
# print(adj_matrix)
# print(adj_matrix.shape)
# # print(getComponent(G))
# print(getComponentAdjMatrix(adj_matrix,400))