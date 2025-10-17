def gen_bin_tree(h: int = 4, r: int = 4, lf=lambda x: x * 4, rf=lambda x: x + 1):
    """
    Построение бинарного дерева БЕЗ рекурсии.
    Дерево — вложенные dict: {"value": v, "left": {...}, "right": {...}}.
    По умолчанию — вариант №4: r=4, h=4, lf(x)=x*4, rf(x)=x+1.
    """
    if h < 1:
        raise ValueError("height must be >= 1")

    t = {"value": r}      # корень
    lvl = [t]             # узлы текущего уровня

    for i in range(1, h):  # уже есть уровень 1 → добавим ещё h-1 уровней
        nxt = []
        for n in lvl:
            v = n["value"]
            L = {"value": lf(v)}
            R = {"value": rf(v)}
            n["left"] = L
            n["right"] = R
            nxt.append(L)
            nxt.append(R)
        lvl = nxt
    return t


def preorder_values(t: dict) -> list:
    """Обход pre-order: root → left → right (для быстрой проверки)."""
    out, st = [], [t]
    while st:
        n = st.pop()
        out.append(n["value"])
        if "right" in n:
            st.append(n["right"])
        if "left" in n:
            st.append(n["left"])
    return out
