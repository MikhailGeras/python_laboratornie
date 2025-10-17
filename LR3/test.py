import unittest
from main import gen_bin_tree, result_list

class TestBinTree(unittest.TestCase):
    def test_height_one(self):
        t = gen_bin_tree(height=1, root=99)
        self.assertEqual(t, {"value": 99})

    def test_default_variant4_result(self):
        # По умолчанию: root=4, height=4, L=x*4, R=x+1
        t = gen_bin_tree()
        expected = [4, 16, 64, 256, 65, 17, 68, 18, 5, 20, 80, 21, 6, 24, 7]
        self.assertEqual(result_list(t), expected)

    def test_custom_root_and_height(self):
        # height=2, root=10 => [10, 40, 11]
        t = gen_bin_tree(height=2, root=10)
        self.assertEqual(result_list(t), [10, 40, 11])

    def test_invalid_height(self):
        with self.assertRaises(ValueError):
            gen_bin_tree(0)

if __name__ == "__main__":
    unittest.main()
