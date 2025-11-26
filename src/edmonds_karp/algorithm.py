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
    
    