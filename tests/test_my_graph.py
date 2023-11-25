import unittest
from my_graph import MyGraph, MyGraphNode

class TestMyGraph(unittest.TestCase):
    
    def test_should_return_BST_from_binary_tree_root(self):
        E = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        num_vertices = 7
        g = MyGraph(E, num_vertices)
        expected = g.copy()
        expected_bst_properties = {
            0: ('parent', None),
            0: ('color', 'black'),
            0: ('distance', 0),
            1: ('parent', 0),
            1: ('distance', 1),
            1: ('color', 'black'),
            2: ('parent', 0),
            2: ('distance', 1),
            2: ('color', 'black'),
            3: ('parent', 1),
            3: ('distance', 2),
            3: ('color', 'black'),
            4: ('parent', 1),
            4: ('distance', 2),
            4: ('color', 'black'),
            5: ('parent', 2),
            5: ('distance', 2),
            5: ('color', 'black'),
            6: ('parent', 2),
            6: ('distance', 2),
            6: ('color', 'black'),
        }
        expected.add_node_properties(expected_bst_properties)
        
        self.assertEqual(g.get_bst(0), expected)

if __name__ == '__main__':
    unittest.main()