def gen_bin_tree(height=4, root=4):
    """
    Рекурсивно строит бинарное дерево как вложенные словари.
    Вариант 4: левый потомок = x*4, правый потомок = x+1.
    height >= 1.
    """
    if height < 1:
        raise ValueError("Высота должена быть >= 1")

    node = {"value": root}
    if height == 1:
        return node

    node["left"] = gen_bin_tree(height - 1, root * 4)
    node["right"] = gen_bin_tree(height - 1, root + 1)
    return node


def result_list(node):
    """Возвращает список значений в порядке: root -> left -> right."""
    if not node:
        return []
    return [node["value"]] + result_list(node.get("left")) + result_list(node.get("right"))


if __name__ == "__main__":
    # Ввод от пользователя (Enter = значения по умолчанию)
    r = input("Введите root (по умолчанию 4): ").strip()
    h = input("Введите height (по умолчанию 4): ").strip()

    root = int(r) if r else 4
    height = int(h) if h else 4

    tree = gen_bin_tree(height=height, root=root)
    print("Дерево:", tree)
    print("result:", result_list(tree))
