from collections import deque
class Graph_Trav:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
    def iterative_dfs(self, start):
        path = []
        stack = [start]
        while stack:
            v = stack.pop()
            if v not in self.visited:
                path.append(v)
                self.visited.add(v)
                stack.extend([node for node in self.graph[v] if node not in self.visited])
        return path
    def bfs(self, start_node):
        visited = []
        queue = deque([start_node])
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.append(vertex)
                queue.extend(set(self.graph[vertex]) - set(visited))
        return visited
class Incidence_Matrix:
    def __init__(self, vertex_list, adjacency_matrix):
        self.vertex_list = vertex_list
        self.adjacency_matrix = adjacency_matrix
        self.incidence_matrix = self.create_incidence_matrix()
    def create_incidence_matrix(self):
        incidence_matrix = []
        for i in range(len(self.vertex_list)):
            row = []
            for j in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] != 0:
                    row.append(1)
                else:
                    row.append(0)
            incidence_matrix.append(row)
        return incidence_matrix
    def print_incidence_matrix(self):
        print("incidence matrix :")
        for row in self.incidence_matrix:
            print(row)
class Adjacency_list:
    def __init__(self, vertex_list, adjacency_matrix):
        self.vertex_list = vertex_list
        self.adjacency_matrix = adjacency_matrix
        self.adjacency_list = self.create_adjacency_list()
    def create_adjacency_list(self):
        adjacency_list = {}
        for i in range(len(self.vertex_list)):
            vertex = self.vertex_list[i]
            adjacency_list[vertex] = []
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] != 0:
                    adjacency_list[vertex].append(self.vertex_list[j])
        return adjacency_list
    def print_adjacency_list(self):
        print("incidence list :")
        for vertex, neighbors in self.adjacency_list.items():
            print(f"{vertex}: {neighbors}")
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
    def find_parent(self, parent, i):
        if parent[i] == i:
            return i
        return self.find_parent(parent, parent[i])
    def union(self, parent, rank, x, y):
        x_root = self.find_parent(parent, x)
        y_root = self.find_parent(parent, y)
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1
    def Krusk(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        return result
def read_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            line = line.replace('\n', '')
            line = line.replace(' ', '')
            matrix.append(list(map(int, line)))
        return matrix
def read_vertices_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        vertices = lines[0].split()
        return vertices    
def in_sort(list):
    for i in range(1, len(list)):
        temp = list[i]
        j = i - 1
        while (j >= 0 and temp < list[j]):
            list[j + 1] = list[j]
            j = j - 1
        list[j + 1] = temp
def main():
    filename = 'file.txt'
    with open(filename, 'r') as file:
        data = file.readlines()
        matrix = [list(map(int, line.split())) for line in data[1:]]
        edges = data[0].split()
        num_vertices = len(edges)
        incidence_matrix = Incidence_Matrix(read_vertices_matrix(filename), read_matrix(filename))
        incidence_matrix.print_incidence_matrix()
        adjacency_list = Adjacency_list(read_vertices_matrix(filename), read_matrix(filename))
        adjacency_list.print_adjacency_list()
        graph_traversal_obj = Graph_Trav(adjacency_list.create_adjacency_list())
        print("Width traversal :")
        print(graph_traversal_obj.iterative_dfs('A'))
        print("Depth traversal :")
        print(graph_traversal_obj.bfs('A'))
        print('Adjacency matrix :')
        m = read_matrix(filename)
        for i in range(len(m)):
            for x in m:
                print(x[i], end=' ')
            print()
        print("Unsorted list of edges :")
        for row in matrix:
            print(row)
        for i in range(len(matrix)):
            in_sort(matrix[i])
        print("Sorted list of edges :")
        for row in matrix:
            print(row)
        g = Graph(num_vertices)
        for i in range(1, num_vertices + 1):
            weights = list(map(int, data[i].split()))
            for j in range(num_vertices):
                if weights[j] != 0:
                    g.add_edge(i - 1, j, weights[j])
        result = g.Krusk()
        print('Kruskal algorithm :')
        for u, v, weight in result:
            print(f"{edges[u]} {edges[v]}")
        weights_sum = 0
        for u, v, weight in result:
            weights_sum += weight
        print(weights_sum)       
if __name__ == "__main__":
    main()
