from functools import*
import timeit
import matplotlib.pyplot as plt
import random

def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


@lru_cache(maxsize=None)
def fact_iterative2(n: int) -> int:
    """Нерекурсивный факториал с lru_cache"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def benchmark(func, n, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
    return min(times)


def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(1, 500, 2))

    res_iterative = []
    res_iterative2 = []

    for n in test_data:
        res_iterative.append(benchmark(fact_iterative, n))
        res_iterative2.append(benchmark(fact_iterative2, n))
        
    # Визуализация
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.plot(test_data, res_iterative2, label="Итеративный с lru_cache")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
