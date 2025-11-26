from collections import deque

class EdmondsKarpGraph:
    """
    Docstring for EdmondsKarpGraph
    """
    def __init__(self, size):
        self.size = size
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.vertex_data = [''] * size

    def add_edge(self, u, v, capacity):
        if u != v:
            self.adj_matrix[u][v] = capacity
    
    def set_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
    
    def bfs(self, s, t, parent):
        visited = [False] * self.size
        queue = deque([s])
        visited[s] = True

        while queue:
            u = queue.popleft()

            for v in range(self.size):
                if not visited[v] and self.adj_matrix[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

                    if v == t:
                        return True
        return False