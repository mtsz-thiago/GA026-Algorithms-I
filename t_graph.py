from __future__ import annotations
from collections.abc import Iterable
import networkx as nx
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys
import itertools
        
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
    
    def copy(self) -> TNode:
        copied = TNode(self._id)
        for key, value in self.items():
            copied.add_property(key, value)
        return copied
    
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
        self_edges = sorted(self, key=lambda x: x[0]._id)
        other_edges = sorted(__other, key=lambda x: x[0]._id)
        all_elements_equals = (self_edges == other_edges)
        return nodes_equals and all_elements_equals
    
    def get_edge(self, v: int) -> TEdge:
        for e in self:
            if e[0]._id == v:
                return e
        return None
        
class TGraph:
    
    def __init__(self, E = None, num_vertices = None) -> None:
        E = E if E else []
        max_node_index_in_E = max([max(e) for e in E]) if len(E) > 0 else -1
        num_vertices = num_vertices if num_vertices else max_node_index_in_E + 1
        
        self._V = [TNode(i) for i in range(num_vertices)]
        self._E = [TAdjacencyList(u) for u in self._V]
        
        for i, (u, v) in enumerate(E):
            self.add_edge(u, v)
    
    def add_edge(self, u: int, v: int, edge_properties: dict = None) -> None:
        if self._E[u].get_edge(v) is None:
            edge_properties = edge_properties if edge_properties else {}
            edege_f = TEdge(self._V[v], edge_properties)
            edege_b = TEdge(self._V[u], edge_properties)
            self._E[u].add_edge(edege_f)
            self._E[v].add_edge(edege_b)
    
    def get_node(self, id: int) -> TNode:
        return self._V[id]
    
    def get_num_vertices(self) -> int:
        return len(self._V)
    
    def get_num_edges(self) -> int:
        return sum([len(u) for u in self._E]) //2
    
    def get_node_adjacency(self, id: int) -> TAdjacencyList:
        return self._E[id]
    
    def copy_nodes_properties(self, other: TGraph) -> None:
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
        copied_graph.copy_nodes_properties(self)
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
    
    def prims_mst(self, root_id: int = 0, weight_property = "weight") -> TGraph:
        
        mst = TGraph(num_vertices=self.get_num_vertices())
        mst.copy_nodes_properties(self)
        for v in mst._V:
            mst.add_node_property(v._id, 'pi', None)
            mst.add_node_property(v._id, 'key', sys.float_info.max)
        
        mst.add_node_property(root_id, 'key', 0)
        mst.add_node_property(root_id, 'pi', None)
        Q = [n for n in mst._V]
        
        while len(Q) > 0:
        
            # get node with min edge weight crossing the cut
            u = min(Q, key=lambda x: x['key'])
            
            # add safe edge to tree, must guard against root on first loop
            if u['pi'] is not None:
                edge_propeties = self.get_edge(u['pi'], u._id)[1]
                mst.add_edge(u['pi'], u._id, edge_propeties)    
            
            # update edges weights == keys crossing the cut via u    
            for edge in self._E[u._id]:
                v_id = edge[0]._id
                v = mst.get_node(v_id)
                q_ids = [n._id for n in Q]
                
                if v._id in q_ids and edge.get_property(weight_property) < v['key']:
                    v['pi'] = u._id
                    v['key'] = edge.get_property(weight_property)
            
            # remove u from Q
            Q = [n for n in Q if n._id != u._id]
        
        return mst
    
    def get_list_of_edges(self) -> list[tuple[int, int, TEdge]]:
        return [(u_adj._u._id, e[0]._id, e) for u_adj in self._E for e in u_adj if e[0]._id >= u_adj._u._id]
    
    def kruskal_mst(self, roo_id: int = 0, weight_property = "weight") -> TGraph:
        
        mst = TGraph(num_vertices=self.get_num_vertices())
        mst.copy_nodes_properties(self)
        
        node_component_map = {v._id: i for i, v in enumerate(mst._V)} 
        forest = [set([v._id]) for v in mst._V]
        
        edges = self.get_list_of_edges()
        
        sorted_edges = sorted(edges, key=lambda x: x[2][1][weight_property])
        
        for u_id, e_id, edge in sorted_edges:
            component_u = node_component_map[u_id]
            component_v = node_component_map[e_id]
            if component_u != component_v:
                mst.add_edge(u_id, e_id, edge[1])
                forest[component_u] = forest[component_u].union(forest[component_v])
                for v_id in forest[component_v]:
                    node_component_map[v_id] = component_u
                forest[component_v] = set()
                
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

class WeightedGraphFactory():
    
    def __init__(self, num_vertices_range, num_edges_range,
                 weight_max = sys.float_info.max, weight_min = sys.float_info.min):
        self.num_vertices_range = num_vertices_range
        self.num_edges_range = num_edges_range
        self.weight_max = weight_max
        self.weight_min = weight_min
    
    def create_graph(self, num_vertices: int, num_edges: int) -> TGraph:
        
        weights = np.random.random((int(num_edges), 1))
        weights = weights * (self.weight_max - self.weight_min) + self.weight_min
        
        vertices_list = list(range(0,num_vertices))
        vertices_space = itertools.product(vertices_list, vertices_list)
        vertices_space = [e for e in vertices_space if e[0] > e[1]]
        a_vertices_space = range(0, len(vertices_space))
        
        assert len(a_vertices_space) >= num_edges, f"{num_edges} edges are too many for {num_vertices} vertices."
        
        chosen = np.random.choice(a_vertices_space, num_edges, replace=False)
        E_list = [vertices_space[i] for i in chosen]
        
        new_graph = TGraph(E_list, num_vertices=num_vertices)
        for i, e in enumerate(E_list):
            new_graph.add_edge_property(e[0], e[1], "weight", weights[i])
        
        return new_graph
    
    def __iter__(self) -> TGraph:
        for num_vertices, num_edges in zip(self.num_vertices_range,self.num_edges_range):
            yield self.create_graph(num_vertices, num_edges)

if __name__ == '__main__':
    pass