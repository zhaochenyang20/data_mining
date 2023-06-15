import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class PageRank:
    def __init__(self, beta=0.85):
        self.beta = beta
        self.node_to_num = {}
        self.N = 0

    def create_node_mapping(self, edges):
        nodes = []
        for edge in edges:
            if edge[0] not in nodes:
                nodes.append(edge[0])
            if edge[1] not in nodes:
                nodes.append(edge[1])

        self.N = len(nodes)

        # 将节点映射到整数值
        i = 0
        for node in nodes:
            self.node_to_num[node] = i
            i += 1
        for edge in edges:
            edge[0] = self.node_to_num[edge[0]]
            edge[1] = self.node_to_num[edge[1]]

    def create_adjacency_matrix(self, edges):
        # 初始化 S 矩阵
        S = np.zeros([self.N, self.N])
        for edge in edges:
            S[edge[1], edge[0]] = 1

        # 列归一化
        for j in range(self.N):
            sum_of_col = sum(S[:, j])
            for i in range(self.N):
                S[i, j] /= sum_of_col

        return S

    def calculate_pagerank(self, S):
        A = self.beta * S + (1 - self.beta) / self.N * np.ones([self.N, self.N])

        P_n = np.ones(self.N) / self.N
        P_n1 = np.zeros(self.N)

        e = 100000

        while e > 1e-3:  # 迭代
            P_n1 = np.dot(A, P_n)
            e = P_n1 - P_n
            e = max(map(abs, e))
            P_n = P_n1

        return P_n

    def get_pagerank(self, edges):
        self.create_node_mapping(edges)
        S = self.create_adjacency_matrix(edges)
        P_n = self.calculate_pagerank(S)

        result = {}
        for node, num in self.node_to_num.items():
            result[node] = P_n[num]

        return result


if __name__ == "__main__":
    edges = [
        ["1", "2"],
        ["1", "3"],
        ["1", "4"],
        ["2", "1"],
        ["2", "4"],
        ["3", "1"],
        ["4", "2"],
        ["4", "3"],
        ["5", "2"],
        ["5", "3"],
        ["5", "1"],
        ["6", "2"],
        ["6", "3"],
        ["6", "5"],
        ["7", "3"],
        ["7", "6"],
    ]

    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    pagerank = PageRank()
    P_n = pagerank.get_pagerank(edges)
    print("PageRank (Custom Implementation):", P_n)

    pagerank_list = nx.pagerank(G, alpha=0.85)
    print("PageRank (NetworkX):", pagerank_list)


    plt.figure(figsize=(5, 4))
    nx.draw(G, with_labels=True)
    plt.show()