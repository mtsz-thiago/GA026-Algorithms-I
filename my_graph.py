from __future__ import annotations

class MyNode(dict):
    
    def __init__(self, id) -> None:
        self._id = id
    
    def add_property(self, key, value):
        self[key] = value
    
    def __hash__(self):
        return self._id
    
    def __eq__(self, __other: MyNode) -> bool:
        ids_equals = self._id == __other._id
        all_properties_equals = super().__eq__(__other)
        return ids_equals and all_properties_equals
    
class MyEdge(dict):
    
    def __init__(self, id: int, u: MyNode, v: MyNode) -> None:
        self._u = u
        self._v = v
    
    def add_property(self, key, value):
        self[key] = value
        
    
    def __eq__(self, __other: object) -> bool:
        nodes_equals = self._u == __other._u and self._v == __other._v
        all_properties_equals = super().__eq__(__other)
        return nodes_equals and all_properties_equals

class MyAdjacencyList(list):

    def __init__(self, u: MyNode):
        self._u = u

    def add_edge(self, e: MyEdge) -> None:
        self.append(e)
        
    def __eq__(self, __other: MyAdjacencyList) -> bool:
        nodes_equals = self._u == __other._u
        all_elements_equals = super().__eq__(__other)
        return nodes_equals and all_elements_equals
        
class MyGraph:
    
    def __init__(self, E = None, num_vertices = None) -> None:
        E = E if E else []
        max_node_index_in_E = max([max(e) for e in E])
        num_vertices = num_vertices if num_vertices else max_node_index_in_E + 1
        
        self._V = [MyNode(i) for i in range(num_vertices)]
        self._E = [MyAdjacencyList(u) for u in self._V]
        
        for i, (u, v) in enumerate(E):
            edege = MyEdge(i, self._V[u], self._V[v])
            self._E[u].add_edge(edege)
        
    def get_node(self, id: int) -> MyNode:
        return self._V[id]
    
    def get_node_adjacency(self, id: int) -> MyAdjacencyList:
        return self._E[id]
        
    def copy(self) -> MyGraph:
        E = [(e._u._id, e._v._id) for u in self._E for e in u]
        num_vertices = len(self._V)
        copied_graph = MyGraph(E, num_vertices)
        
        # Copy node properties
        for i, node in enumerate(self._V):
            for key, value in node.items():
                copied_graph.add_node_property(i, key, value)
        
        return copied_graph
    
    def add_node_properties(self, properties: dict) -> None:
        for v in self._V:
            for key, value in properties.items():
                v.add_property(key, value)
    
    def add_node_property(self, id: int, key: str, value: any) -> None:
        self._V[id].add_property(key, value)
    
    def __eq__(self, other: MyGraph) -> bool:
        return self._V == other._V and self._E == other._E
    
    def get_bst(self, root_id: int) -> MyGraph:
        bst = self.copy()
        
        init_properties = {
            'parent_id': None,
            'distance': None,
            'color': 'white'
        } 
        bst.add_node_properties(init_properties)
        
        root = bst.get_node(root_id)
        root["color"] = "gray"
        root["distance"] = 0
        to_visit_stack = [root]
        while len(to_visit_stack) > 0:
            u = to_visit_stack.pop()
            for e in bst.get_node_adjacency(u._id):
                v = e._v
                if v["color"] == "white":
                    v["parent_id"] = u._id
                    v["distance"] = u["distance"] + 1
                    v["color"] = "gray"
                    to_visit_stack.append(v) 
            u["color"] = "black"
        
        return bst
    
if __name__ == '__main__':
    pass