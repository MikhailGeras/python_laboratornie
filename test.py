from main import plohaya_ugadaika, horosh_ugadaika
import unittest
class TestTS(unittest.TestCase):
    def test_plohaya_ugadaika(self):
        """проверить обычные тесты для медленного перебора"""
        self.assertEqual(plohaya_ugadaika(3, 1, 10), (3, 3))
        self.assertEqual(plohaya_ugadaika(743, 5, 1011), (743, 739))
        self.assertEqual(plohaya_ugadaika(743, -100, 1011), (743, 844))
        self.assertEqual(plohaya_ugadaika(743, 743, 1011), (743, 1))
        self.assertEqual(plohaya_ugadaika(743, 5, 743), (743, 739))
    def test_horoshaya_ugadaika(self):
        """проверить обычные тесты для бинарного поиска"""
        self.assertEqual(horosh_ugadaika(3, 1, 10), (3, 3))
        self.assertEqual(horosh_ugadaika(743, 5, 1011), (743, 10))
        self.assertEqual(horosh_ugadaika(743, -100, 1011), (743, 10))
        self.assertEqual(horosh_ugadaika(743, 743, 1011), (743, 8))
        self.assertEqual(horosh_ugadaika(743, 5, 743), (743, 9))
    def test_error(self):
        """проверить ошибки вводы"""
        self.assertEqual(plohaya_ugadaika(3.2, 1, 10), "Формат не подходит")
        self.assertEqual(horosh_ugadaika(743, 5.5, 1011), "Формат не подходит")
        self.assertEqual(plohaya_ugadaika('f', 1, 10), "Формат не подходит")
        self.assertEqual(horosh_ugadaika(743, '-', 1011), "Формат не подходит")
    def test_sluchai(self):
        """проверить случай a == b == c"""
        self.assertEqual(plohaya_ugadaika(3, 3, 3), (3, 1))
        self.assertEqual(horosh_ugadaika(3, 3, 3), (3, 1))
    def test_neverno_interval(self):
        """проверить правильность границ"""
        with self.assertRaises(ValueError):
            plohaya_ugadaika(5, 10, 1)
        with self.assertRaises(ValueError):
            horosh_ugadaika(5, 10, 1)
    def test_vne_intervala(self):
        """проверить, что а в диапазоне b-c"""
        with self.assertRaises(ValueError):
            plohaya_ugadaika(0, 1, 10)
        with self.assertRaises(ValueError):
            horosh_ugadaika(11, 1, 10)
if __name__ == '__main__':
    unittest.main() #проверяем все файлы
