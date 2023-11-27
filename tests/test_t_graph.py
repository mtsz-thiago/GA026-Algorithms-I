import unittest
from t_graph import TGraph, TNode, TAdjacencyList, TEdge

class TestTyGraph(unittest.TestCase):

    def setUp(self):
        E1 = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (4,6)]
        self.G1 = TGraph(E1)
        
        E2 = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (4,6)]
        self.G2 = TGraph(E2)
        
        E3 = [(0, 1), (1, 2), (0, 4), (4, 5), (4, 6)]
        self.G3 = TGraph(E3)

    def test_should_assert_property_was_added_to_node_0(self):
        node_id = 0
        key = "color"
        value = "red"
        self.G1.get_node(node_id).add_property(key, value)
        self.assertEqual(self.G1.get_node(node_id)[key], value)
        
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

if __name__ == '__main__':
    unittest.main()
