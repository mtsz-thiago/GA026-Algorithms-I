import unittest
import sys
from t_graph import TGraph, TNode, TAdjacencyList, TEdge

class TestTyGraph(unittest.TestCase):

    def setUp(self):
        E1 = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (4,6)]
        self.G1 = TGraph(E1)
        
        E2 = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (4,6)]
        self.G2 = TGraph(E2)
        
        E3 = [(0, 1), (1, 2), (0, 4), (4, 5), (4, 6)]
        self.G3 = TGraph(E3)
        
        self.E_full = [(0,1), (0,2), (0,3), (0,4), 
                  (1,2), (1,3), (1,4), 
                  (2,3), (2,4),
                  (3,4)
                  ]
        self.G_full = TGraph(self.E_full)
        
        disconnected_E = [(0,1), (0,2), 
                          (1,2)]

        self.disconnected_G = TGraph(disconnected_E, num_vertices=4)

    def test_should_assert_property_was_added_to_node_0(self):
        node_id = 0
        key = "color"
        value = "red"
        self.G1.get_node(node_id).add_property(key, value)
        self.assertEqual(self.G1.get_node(node_id)[key], value)
        
    def test_should_assert_list_of_edges_has_no_duplicate(self):
        expected_ids = self.E_full
        actual = self.G_full.get_list_of_edges()
        actual_ids = [(e[0], e[1]) for e in actual]
        self.assertEqual(expected_ids, actual_ids)
        
    def test_should_assert_graph_equals(self):
        self.assertEqual(self.G1, self.G2)
        self.assertNotEqual(self.G1, self.G3)
        
    def test_should_assert_copied_graph_equals(self):
        self.G1.add_node_property(0, "color", "blue")
        copied_graph = self.G1.copy()
        self.assertEqual(self.G1, copied_graph)

    def test_should_assert_graphs_differ(self):
        node_id = 0
        key = "color"
        value = "blue"
        self.G2.add_node_property(node_id, key, value)
        self.assertNotEqual(self.G1, self.G2)
    
    def test_should_add_an_edge_with_properties_to_graph(self):
        edege_u = 0
        edge_v = 6
        edge_properties = {
            "weight": 10
        }
        
        self.G1.add_edge(edege_u, edge_v, edge_properties)
        modified_edge_f = self.G1.get_edge(edege_u, edge_v)
        modified_edge_b = self.G1.get_edge(edge_v, edege_u) 
        
        self.assertEqual(modified_edge_f, modified_edge_b)
        self.assertEqual(modified_edge_f.get_property("weight"), edge_properties["weight"])
        
        
    
    def test_should_assert_property_was_added_to_edge(self):
        edge_u_id = 0
        edge_v_id = 1
        key = "weight"
        value = 10
        
        self.G1.add_edge_property(edge_u_id, edge_v_id, key, value)
        modified_edge_f = self.G1.get_edge(edge_u_id, edge_v_id)
        modified_edge_b = self.G1.get_edge(edge_v_id, edge_u_id)
        
        self.assertEqual(modified_edge_f, modified_edge_b)
        self.assertEqual(modified_edge_f.get_property(key), value)
        
    def test_should_assert_modfying_u_v_also_modifies_v_u_edges(self):
        edge_u_id = 0
        edge_v_id = 1
        
        key = "weight"
        value = 10
        self.G1.add_edge_property(edge_u_id, edge_v_id, key, value)

        edge_f = self.G1.get_edge(edge_u_id, edge_v_id)
        edge_b = self.G1.get_edge(edge_v_id, edge_u_id)
        
        self.assertEqual(edge_f, edge_b)
        
    def test_should_assert_bst_was_found_from_root_node_1(self):
        
        expected = self.G1.copy()
        # add unreached nodes from root node 1
        unreached_props = {
            "parent_id": None,
            "distance": None,
            "color": "white"
        }
        
        expected.add_node_properties(unreached_props)
        
        # add reached nodes from root node 1
        expected.add_node_property(0, "parent_id", 1)
        expected.add_node_property(0, "distance", 1)
        expected.add_node_property(0, "color", "black")
        expected.add_node_property(1, "parent_id", None)
        expected.add_node_property(1, "distance", 0)
        expected.add_node_property(1, "color", "black")
        expected.add_node_property(2, "parent_id", 1)
        expected.add_node_property(2, "distance", 1)
        expected.add_node_property(2, "color", "black")
        expected.add_node_property(3, "parent_id", 2)
        expected.add_node_property(3, "distance", 2)
        expected.add_node_property(3, "color", "black")
        expected.add_node_property(4, "parent_id", 0)
        expected.add_node_property(4, "distance", 2)
        expected.add_node_property(4, "color", "black")
        expected.add_node_property(5, "parent_id", 4)
        expected.add_node_property(5, "distance", 3)
        expected.add_node_property(5, "color", "black")
        expected.add_node_property(6, "parent_id", 4)
        expected.add_node_property(6, "distance", 3)
        expected.add_node_property(6, "color", "black")
        
        actual = self.G1.get_bst(1)
        
        self.assertEqual(actual, expected)
    
    def test_should_assert_prims_algorithm_really_returns_mst(self):
        import itertools
        vertices_indexes = list(range(0, self.G_full.get_num_vertices()))
        for u, v in itertools.product(vertices_indexes,vertices_indexes):
            if u != v:
                self.G_full.add_edge_property(u, v, "weight", (u+v)%5)
        
        expected = TGraph([(0, 1), (1, 4), (4, 2), (2, 3)])
        expected.add_node_property(0, "key", 0)
        expected.add_node_property(0, "pi", None)
        expected.add_edge_property(0, 1, "weight", 1)
        expected.add_node_property(1, "key", 1)
        expected.add_node_property(1, "pi", 0)
        expected.add_edge_property(1, 4, "weight", 0)
        expected.add_node_property(4, "key", 0)
        expected.add_node_property(4, "pi", 1)
        expected.add_edge_property(4, 2, "weight", 1)
        expected.add_node_property(2, "key", 1)
        expected.add_node_property(2, "pi", 4)
        expected.add_edge_property(2, 3, "weight", 0)
        expected.add_node_property(3, "key", 0)
        expected.add_node_property(3, "pi", 2)
        
        actual = self.G_full.prims_mst(0) 
        
        self.assertEqual(actual, expected)
        
    def test_should_assert_kruskals_algorithm_really_returns_mst(self):
        import itertools
        vertices_indexes = list(range(0, self.G_full.get_num_vertices()))
        for u, v in itertools.product(vertices_indexes,vertices_indexes):
            if u != v:
                self.G_full.add_edge_property(u, v, "weight", (u+v)%5)
        
        expected = TGraph([(0, 1), (1, 4), (4, 2), (2, 3)])
        expected.add_edge_property(0, 1, "weight", 1)
        expected.add_edge_property(1, 4, "weight", 0)
        expected.add_edge_property(4, 2, "weight", 1)
        expected.add_edge_property(2, 3, "weight", 0)
        
        actual = self.G_full.kruskal_mst(0) 
        
        self.assertEqual(actual, expected)

    def test_should_assert_methods_dont_throw_exception_when_graph_is_not_connected(self):
        
        expected_edges = [(0,1), (0,2)]
        expected = TGraph(expected_edges, num_vertices=4)
        expected.add_edges_properties({"weight": 1})
        expected.add_node_property(0, "pi", None)
        expected.add_node_property(0, "key", 0)
        expected.add_node_property(1, "pi", 0)
        expected.add_node_property(1, "key", 1)
        expected.add_node_property(2, "pi", 0)
        expected.add_node_property(2, "key", 1)
        expected.add_node_property(3, "pi", None)
        expected.add_node_property(3, "key", sys.float_info.max)
        
        
        self.disconnected_G.add_edges_properties({"weight": 1})
        actual = self.disconnected_G.prims_mst(0)
        
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
