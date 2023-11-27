from __future__ import annotations
from collections.abc import Iterable
import networkx as nx
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
        
class TNode(dict):
    
    def __init__(self, id) -> None:
        self._id = id
    
    def add_property(self, key, value):
        self[key] = value
    
    def __hash__(self):
        return self._id
    
    def __eq__(self, __other: TNode) -> bool:
        all_properties_equals = super().__eq__(__other)
        return all_properties_equals
    
class TEdge(tuple[TNode, dict]):
    
    def __new__(cls, n: TNode, props: dict):
        return super().__new__(cls, (n, props))
    
    def add_property(self, key, value):
        self[1][key] = value
    
    def get_property(self, key):
        return self[1][key]
    
    def __eq__(self, __other: object) -> bool:
        return self[1] == __other[1]

class TAdjacencyList(list):

    def __init__(self, u: TNode):
        self._u = u

    def add_edge(self, e: TEdge) -> None:
        self.append(e)
        
    def __eq__(self, __other: TAdjacencyList) -> bool:
        nodes_equals = self._u == __other._u
        all_elements_equals = super().__eq__(__other)
        return nodes_equals and all_elements_equals
    
    def get_edge(self, v: int) -> TEdge:
        for e in self:
            if e[0]._id == v:
                return e
        return None
        
class TGraph:
    
    def __init__(self, E = None, num_vertices = None) -> None:
        E = E if E else []
        max_node_index_in_E = max([max(e) for e in E])
        num_vertices = num_vertices if num_vertices else max_node_index_in_E + 1
        
        self._V = [TNode(i) for i in range(num_vertices)]
        self._E = [TAdjacencyList(u) for u in self._V]
        
        for i, (u, v) in enumerate(E):
            self.add_edge(u, v)
    
    def add_edge(self, u: int, v: int, edge_properties: dict = {}) -> None:
        if self._E[u].get_edge(v) is None:
            edege_f = TEdge(self._V[v], edge_properties)
            edege_b = TEdge(self._V[u], edge_properties)
            self._E[u].add_edge(edege_f)
            self._E[v].add_edge(edege_b)
    
    def get_node(self, id: int) -> TNode:
        return self._V[id]
    
    def get_node_adjacency(self, id: int) -> TAdjacencyList:
        return self._E[id]
    
    def copy_node_properties(self, other: TGraph) -> None:
        for i, node in enumerate(self._V):
            for key, value in other._V[i].items():
                node.add_property(key, value)
    
    def copy_edges_properties(self, other: TGraph) -> None:
        for u in self._E:
            for e in u:
                for key, value in e[1].items():
                    other.add_edge_property(e._u._id, e._v._id, key, value)
    
    def copy(self) -> TGraph:
        E = [(u_adj._u._id, e[0]._id) for u_adj in self._E for e in u_adj]
        num_vertices = len(self._V)
        copied_graph = TGraph(E, num_vertices)
        copied_graph.copy_node_properties(self)
        copied_graph.copy_edges_properties(self)
        
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
            if e[0]._id == v:
                e.add_property(key, value)
                return
                
    def get_edge(self, u: int, v: int) -> TEdge:
        for e in self._E[u]:
            if e[0]._id == v:
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
                v = e[0]
                if v["color"] == "white":
                    v["parent_id"] = u._id
                    v["distance"] = u["distance"] + 1
                    v["color"] = "gray"
                    to_visit_stack.append(v) 
            u["color"] = "black"
        
        return bst
    
    def prims_mst(self, root_id: int = 0) -> TGraph:
        mst = self
        
        return mst
    
    def plot(self, nodes_properties=False, edges_properties=False):

        G = nx.Graph()

        # Add nodes
        for node in self._V:
            G.add_node(node._id)
            if edges_properties:
                for key, value in node.items():
                    G.nodes[node._id][key] = value

        # Add edges
        for edges in self._E:
            u = edges._u._id
            for edge in edges:
                v = edge[0]._id
                G.add_edge(u, v)
                if nodes_properties:
                    for key, value in edge[1].items():
                        G.edges[(u, v)][key] = value

        nx.draw(G, with_labels=True)
        plt.show()

        return plt.gcf()
    
if __name__ == '__main__':
    pass