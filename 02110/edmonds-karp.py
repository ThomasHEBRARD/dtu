from collections import deque


class EdgeInfo:
    def __init__(self, v, u, edge_id, forward):
        self.v = v
        self.u = u
        self.edge_id = edge_id
        self.forward = forward


class FlowGraph:
    def __init__(self, number_of_nodes):
        # not agency matrix cause we wont be able tu run bfs
        self.number_of_nodes = number_of_nodes
        self.adjency_list = [[] for _ in range(number_of_nodes)]
        self.flow = []
        self.capacity = []

    def add_edge(self, v, u, c):
        self.adjency_list[v].append(EdgeInfo(v, u, len(self.flow), True))
        self.adjency_list[u].append(EdgeInfo(u, v, len(self.flow), False))
        self.flow.append(0)
        self.capacity.append(c)

    def left_over_capacity(self, edge):
        if edge.forward:
            return self.capacity[edge.edge_id] - self.flow[edge.edge_id]
        else:
            return self.flow[edge.edge_id]

    def traversable(self, edge):
        return self.left_over_capacity(edge) > 0

    def add_flow(self, edge, flow):
        if edge.forward:
            self.flow[edge.edge_id] += flow
        else:
            self.flow[edge.edge_id] -= flow


def BFS(graph, s, t):
    marked = [False for _ in range(graph.number_of_nodes)]
    edge_taken = [None for _ in range(graph.number_of_nodes)]
    marked[s] = True
    q = deque()
    q.append(s)

    while q:
        v = q.popleft()
        if v == t:
            break
        for edge in graph.adjency_list[v]:
            if graph.traversable(edge) and not marked[edge.u]:
                marked[edge.u] = True
                edge_taken[edge.u] = edge
                q.append(edge.u)

    if edge_taken[t]:
        v = t
        path = []
        while edge_taken[v]:
            path.append(edge_taken[v])
            v = edge_taken[v].v
        return path
    return None


def edmonds(graph, s, t):
    while True:
        path = BFS(graph, s, t)
        if not path:
            break
        flow = graph.left_over_capacity(path[0])
        for edge in path:
            flow = min(flow, graph.left_over_capacity(edge))
        for edge in path:
            graph.add_flow(edge, flow)

    total_flow = 0

    for edge in graph.adjency_list[s]:
        if edge.forward:
            total_flow += graph.flow[edge.edge_id]

    return total_flow


n = int(input())
m = int(input())

flow_graph = FlowGraph(n)

for _ in range(m):
    v, u, c = tuple(map(int, input().split()))
    flow_graph.add_edge(v, u, c)

print(edmonds(flow_graph, 0, 1))
