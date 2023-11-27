from __future__ import annotations
import networkx as nx
import matplotlib.pyplot as plt
        
class TNode(dict):
    
    def __init__(self, id) -> None:
        self._id = id
    
    def add_property(self, key, value):
        self[key] = value
    
    def __hash__(self):
        return self._id
    
    def __eq__(self, __other: TNode) -> bool:
        ids_equals = self._id == __other._id
        all_properties_equals = super().__eq__(__other)
        return ids_equals and all_properties_equals
    
class TEdge(dict):
    
    def __init__(self, id: int, u: TNode, v: TNode) -> None:
        self._u = u
        self._v = v
    
    def add_property(self, key, value):
        self[key] = value
    
    def __eq__(self, __other: object) -> bool:
        nodes_equals = self._u == __other._u and self._v == __other._v
        all_properties_equals = super().__eq__(__other)
        return nodes_equals and all_properties_equals

class TAdjacencyList(list):

    def __init__(self, u: TNode):
        self._u = u

    def add_edge(self, e: TEdge) -> None:
        self.append(e)
        
    def __eq__(self, __other: TAdjacencyList) -> bool:
        nodes_equals = self._u == __other._u
        all_elements_equals = super().__eq__(__other)
        return nodes_equals and all_elements_equals
        
class TGraph:
    
    def __init__(self, E = None, num_vertices = None) -> None:
        E = E if E else []
        max_node_index_in_E = max([max(e) for e in E])
        num_vertices = num_vertices if num_vertices else max_node_index_in_E + 1
        
        self._V = [TNode(i) for i in range(num_vertices)]
        self._E = [TAdjacencyList(u) for u in self._V]
        
        for i, (u, v) in enumerate(E):
            edege = TEdge(i, self._V[u], self._V[v])
            self._E[u].add_edge(edege)
        
    def get_node(self, id: int) -> TNode:
        return self._V[id]
    
    def get_node_adjacency(self, id: int) -> TAdjacencyList:
        return self._E[id]
        
    def copy(self) -> TGraph:
        E = [(e._u._id, e._v._id) for u in self._E for e in u]
        num_vertices = len(self._V)
        copied_graph = TGraph(E, num_vertices)
        
        # Copy node properties
        for i, node in enumerate(self._V):
            for key, value in node.items():
                copied_graph.add_node_property(i, key, value)
        
        return copied_graph
    
    def add_node_properties(self, properties: dict) -> None:
        for v in self._V:
            for key, value in properties.items():
                v.add_property(key, value)
                
    def add_edges_properties(self, properties: dict) -> None:
        for u in self._E:
            for e in u:
                for key, value in properties.items():
                    e.add_property(key, value)          
    
    def add_node_property(self, id: int, key: str, value: any) -> None:
        self._V[id].add_property(key, value)
        
    def add_edge_property(self, u: int, v: int, key: str, value: any) -> None:
        for e in self._E[u]:
            if e._v._id == v:
                e.add_property(key, value)
                return
                
    def get_edge(self, u: int, v: int) -> TEdge:
        for e in self._E[u]:
            if e._v._id == v:
                return e
        return None
    
    def __eq__(self, other: TGraph) -> bool:
        return self._V == other._V and self._E == other._E
    
    def get_bst(self, root_id: int) -> TGraph:
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
    
    def plot(self,show_edges_properties = False, show_nodes_properties = False):
        
        G = nx.Graph()
        for u in self._V:
            G.add_node(u._id, **u)
        for u in self._E:
            for e in u:
                G.add_edge(e._u._id, e._v._id, **e)
        nx.draw(G, with_labels=True, arrows=True, arrowsize=20, arrowstyle='fancy')
        
        if show_edges_properties:
            # Add edge properties as labels
            edge_labels = {(e._u._id, e._v._id): e for u in self._E for e in u}
            nx.draw_networkx_edge_labels(G,
                                         pos=nx.spring_layout(G), 
                                         edge_labels=edge_labels)
        if show_nodes_properties:
            # Add node properties as labels
            node_labels = {u._id: u for u in self._V}
            nx.draw_networkx_labels(G, 
                                    pos=nx.spring_layout(G), 
                                    labels=node_labels)
        
        plt.show()
        
        return plt.gcf()
    
if __name__ == '__main__':
    pass