from main import ts
import unittest
class TestTS(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(ts([2,7,11,15], 9), [0,1])
        self.assertEqual(ts([3, 2, 4], 6), [1, 2])
        self.assertEqual(ts([10,2,3,15], 5), [1,2])
        self.assertEqual(ts([3,3], 6), [0, 1])
        self.assertEqual(ts([0,2,3,0], 0), [0,3])
        self.assertEqual(ts([2,7,11,15], 26), [2,3])
        self.assertEqual(ts([-19,7,11,15], -12), [0,1])
        self.assertEqual(ts([-10,-2,11,15], -12), [0,1])
        self.assertEqual(ts([1,2], 3), [0,1])
    def test_error(self):
        self.assertEqual(ts(['o',7,11,15], 18), 'Не является целым числом')
        self.assertEqual(ts(['-',7,11,15], 18), 'Не является целым числом')
        self.assertEqual(ts([8.6,7,11,15], 18), 'Не является целым числом')
    def test_else(self):    
        self.assertEqual(ts([3], 3), None)
        self.assertEqual(ts([1,2,3], 1000), None)
if __name__ == '__main__':
    unittest.main() #проверяем все файлы