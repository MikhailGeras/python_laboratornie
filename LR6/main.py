# ЛР6 — построение бинарного дерева: рекурсивно vs итеративно (вариант №4)

import timeit
import matplotlib.pyplot as plt

# Вариант №4 по умолчанию:
# r = 4, h = 4, lf(x) = x*4, rf(x) = x+1
def build_tree_recursive(h: int = 4, r: float = 4, lf=lambda x: x * 4, rf=lambda x: x + 1):
    """Построить дерево рекурсивно. На листьях нет ключей left/right."""
    if h < 1:
        raise ValueError("h must be >= 1")
    def rec(level: int, x: float):
        node = {"value": x}
        if level >= h:
            return node
        node["left"] = rec(level + 1, lf(x))
        node["right"] = rec(level + 1, rf(x))
        return node
    return rec(1, r)

def build_tree_iterative(h: int = 4, r: float = 4, lf=lambda x: x * 4, rf=lambda x: x + 1):
    """Построить дерево без рекурсии"""
    if h < 1:
        raise ValueError("h must be >= 1")
    t = {"value": r}
    lvl = [t]
    for _ in range(1, h):
        nxt = []
        for n in lvl:
            v = n["value"]
            L = {"value": lf(v)}
            R = {"value": rf(v)}
            n["left"] = L
            n["right"] = R
            nxt.extend([L, R])
        lvl = nxt
    return t

def bench(hs=range(1, 12), rep: int = 5):
    """Вернуть списки: H, T_rec, T_it. Один вызов; минимум среди повторов."""
    H, T_rec, T_it = [], [], []
    for h in hs:
        tr = min(timeit.repeat(lambda: build_tree_recursive(h=h), number=1, repeat=rep))
        ti = min(timeit.repeat(lambda: build_tree_iterative(h=h), number=1, repeat=rep))
        H.append(h); T_rec.append(tr); T_it.append(ti)
    return H, T_rec, T_it

def plot(H, T_rec, T_it):
    plt.figure()
    plt.plot(H, T_rec, label="Рекурсивная")
    plt.plot(H, T_it, label="Итеративная")
    plt.title("Время построения бинарного дерева (вариант №4)")
    plt.xlabel("Высота h"); plt.ylabel("Время (сек)"); plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    H, A, B = bench(hs=range(1, 12), rep=5)
    plot(H, A, B)
