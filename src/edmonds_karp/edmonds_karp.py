from collections import deque

class EdmondsKarpGraph:
    def __init__(self, size: int) -> None:
        """
        Initialize an Edmonds-Karp graph with the specified number of vertices.
        
        :param size: The number of vertices in the graph
        """
        self.size = size
        self.adj_matrix = [[0] * size for _ in range(size)] # Adjacency matrix for capacities
        self.vertex_labels = [''] * size

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        """
        Add a directed edge from vertex u to vertex v with given capacity.
        
        :param u: Source vertex index
        :param v: Destination vertex index
        :param capacity: Edge capacity (must be positive)
        """
        if u != v:
            self.adj_matrix[u][v] = capacity

    def set_vertex_label(self, vertex: int, label: str) -> None:
        """
        Set a label for a vertex (e.g., 'S', 'T', 'U').
        
        :param vertex: The vertex index
        :param label: The label for the vertex
        """
        if 0 <= vertex < self.size:
            self.vertex_labels[vertex] = label

    def bfs(self, s: int, t: int, parent: list[int]) -> bool:
        """
        Find an augmenting path from source s to sink t using BFS.
        Updates the parent array to track the path found.
        
        :param s: Source vertex index
        :param t: Sink/target vertex index
        :param parent: List to store the parent of each vertex in the path
        :return: True if a path exists, False otherwise
        """
        visited = [False] * self.size
        queue = deque([s]) # Initialize queue with source vertex s
        visited[s] = True

        while queue:
            u = queue.popleft()

            for v in range(self.size):
                # If not visited and there's remaining capacity on the edge from u to v
                if not visited[v] and self.adj_matrix[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

                    if v == t:
                        return True
        return False
    
    def edmonds_karp(self, source: int, sink: int) -> int:
        """
        Compute the maximum flow from source to sink using the Edmonds-Karp algorithm.
        
        :param source: Source vertex index
        :param sink: Sink/target vertex index
        :return: The value of the maximum flow
        """
        parent = [-1] * self.size # parent array stores the path
        max_flow = 0

        
        while self.bfs(source, sink, parent):

            # Find the bottle neck capacity of the found path, the minimum residual capacity    
            # use a large integer sentinel to keep path_flow an int (avoids float assignment to matrix)
            path_flow = 10**18
            s = sink

            while s != source:
                path_flow = min(path_flow, self.adj_matrix[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                # Decrease the capacity of the forward edge by path_flow
                self.adj_matrix[u][v] -= int(path_flow)
                # Increase the capacity of the backward edge by path_flow
                self.adj_matrix[v][u] += int(path_flow)

                v = parent[v]

            path: list[int] = []
            v = sink
            while v != source:
                path.append(v)
                v = parent[v]
            path.append(source)
            path.reverse()

            path_names = [self.vertex_labels[i] for i in path]
            print(f"Augmenting path found: {' -> '.join(path_names)} with flow {path_flow}")
        
        return max_flow  

