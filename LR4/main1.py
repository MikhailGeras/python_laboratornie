from functools import*
import timeit
import matplotlib.pyplot as plt
import random


def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)

@lru_cache(maxsize=None)
def fact_recursive2(n: int) -> int:
    """Рекурсивный факториал c lru_cache"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)

def benchmark(func, n, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
    return min(times)


def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(1, 500, 2))

    res_recursive = []
    res_recursive2 = []

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, n))
        res_recursive2.append(benchmark(fact_recursive2, n))
        
    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_recursive2, label="Рекурсивный с lru_cache")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
