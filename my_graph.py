from __future__ import annotations

class MyGraphNode(dict):
    
    def __init__(self, id):
        self.id = id
        self._adj = []
    
    def add_edge(self, v: MyGraphNode):
        self._adj.append(v)
    
    def add_weighted_edge(self, v: MyGraphNode, w: float):
        self._adj.append((v, w))
        v.add_edge(self, w)

    def add_property(self, k: str, v: object):
        self[k] = v

    def __eq__(self, other):
        ids_match = self.id == other.id
        adj_match = self._adj == other._adj
        properties_match = self.items() == other.items()
        return ids_match and adj_match and properties_match
    
    def copy(self) -> MyGraphNode:
        copy = MyGraphNode(self.id)
        copy._adj = self._adj.copy()
        copy._adj = self._adj.copy()
        return copy

class MyGraph:
    
    def __init__(self, E: list[tuple[int,int]] = [], num_vertices: int = None):
        
        self.num_vertices = num_vertices
        if num_vertices is None:
            self.num_vertices = max([max(e) for e in E]) + 1 if len(E) > 0 else 0
        
        self._adj = [MyGraphNode(i) for i in range(self.num_vertices)]
        
        for e in E:
            self._adj[e[0]].add_edge(self._adj[e[1]])
            self._adj[e[1]].add_edge(self._adj[e[0]])

    def set_weights(self, u: int, v: int, w: float):
        self._adj[u].add_weighted_edge(self._adj[v], w)
    
    def copy(self):
        copy = MyGraph()
        copy._adj = [v.copy() for v in self._adj]
        copy.num_vertices = self.num_vertices
        return copy
    
    def add_node_properties(self, node_properties: dict[int, tuple[str, object]]):
        for k, v in node_properties.items():
            self._adj[k].add_property(v[0],v[1])
    
    def __eq__(self, other):
        adj_match = all([u == v for u, v in zip(self._adj, other._adj)])
        return adj_match and self.num_vertices == other.num_vertices
    
    def get_bst(self, v: int) -> MyGraph:
        spanning_tree = self.copy()
        
        # initialize spanning tree properties
        parents = {v: ('parent', None) for v in range(self.num_vertices)}
        distances = {v: ('distance', None) for v in range(self.num_vertices)}
        colors = {v: ('color', 'white') for v in range(self.num_vertices)}
        spanning_tree.add_node_properties(parents)
        spanning_tree.add_node_properties(distances)
        spanning_tree.add_node_properties(colors)
        
        # initialize root
        v_node = spanning_tree._adj[v]
        v_node["color"] = 'gray'
        v_node["distance"] = 0
        queue = [v_node]
        while queue:
            u = queue.pop(0)
            
            if u['color'] == 'black':
                continue
            
            for v in u._adj:
                if v['color'] == 'white':
                    v['color'] = 'gray'
                    v['distance'] = u['distance'] + 1
                    v['parent'] = u
                    queue.append(v)
            u['color'] = 'black'
        
        return spanning_tree
        

if __name__ == '__main__':
    pass
        