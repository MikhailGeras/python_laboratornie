import unittest
from main import gen_bin_tree, preorder_values


class TestBinTree(unittest.TestCase):
    def test_h1(self):
        t = gen_bin_tree(h=1, r=10)
        self.assertEqual(t, {"value": 10})

    def test_default_variant4(self):
        # по умолчанию: r=4, h=4, lf(x)=x*4, rf(x)=x+1
        t = gen_bin_tree()
        vals = preorder_values(t)
        # Полный корректный pre-order для высоты 4:
        exp = [4, 16, 64, 256, 65, 17, 68, 18, 5, 20, 80, 21, 6, 24, 7]
        self.assertEqual(vals, exp)

    def test_variant1_custom(self):
        # вариант №1: lf=x*2, rf=x+3, h=3, r=1
        t = gen_bin_tree(h=3, r=1, lf=lambda x: x * 2, rf=lambda x: x + 3)
        # Корректный pre-order для высоты 3:
        # 1, 2, 4, 5, 4, 8, 7
        self.assertEqual(preorder_values(t), [1, 2, 4, 5, 4, 8, 7])

    def test_bad_h(self):
        with self.assertRaises(ValueError):
            gen_bin_tree(h=0, r=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
