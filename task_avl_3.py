from typing import List

# Яндекс Контест считает решение верным
class Node:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def calc_balance(self) -> int:
        h_r, h_l = 0, 0
        if self.right is not None:
            h_r = self.right.height
        if self.left is not None:
            h_l = self.left.height
        return h_r - h_l

    def update_height(self) -> None:
        children_heights = [0]
        if self.left is not None:
            children_heights.append(self.left.height)
        if self.right is not None:
            children_heights.append(self.right.height)
        self.height = 1 + max(children_heights)

class AVLTree:
    def __init__(self):
        self.root = None

    def add(self, key) -> None:
        if self.root is None:
            self.root = Node(key)
            return

        stack = [self.root]
        while True:
            if key < stack[-1].key:
                if stack[-1].left is None:
                    stack[-1].left = Node(key)  # Нашли место для вставки слева
                    break
                else:
                    stack.append(stack[-1].left)  # Идём дальше вглубь налево
            elif key > stack[-1].key:
                if stack[-1].right is None:
                    stack[-1].right = Node(key)  # Нашли место для вставки справа
                    break
                else:
                    stack.append(stack[-1].right)  # Идём дальше вглубь направо
            else:
                return  # Ключ уже есть в дереве, выходим, ничего не делая
        while stack:  # Возвращаемся назад, обновляем высоты, балансируем
            v = stack.pop()
            v.update_height()
            self._rebalance(v, stack[-1] if len(stack) >= 1 else None)

    def _rebalance(self, node, parent) -> None:
        v = node
        if v.calc_balance() == 2:
            u = v.right
            if u.calc_balance() >= 0:
                self._rotate_left(v, parent)
            else:
                self._rotate_right(u, v)
                self._rotate_left(v, parent)
        elif v.calc_balance() == -2:
            u = v.left
            if u.calc_balance() <= 0:
                self._rotate_right(v, parent)
            else:
                self._rotate_left(u, v)
                self._rotate_right(v, parent)

    def delete(self, key):
        if self.root is None:
            return

        stack = [self.root]
        while True:
            if key < stack[-1].key:
                if stack[-1].left is None:
                    return
                else:
                    stack.append(stack[-1].left)
            elif key > stack[-1].key:
                if stack[-1].right is None:
                    return
                else:
                    stack.append(stack[-1].right)
            else:
                # Если у удаляемой вершины нет детей (лист) (не пропаганда чайлдфри)
                if stack[-1].left is None and stack[-1].right is None:
                    if len(stack) > 1:
                        if stack[-2].left is stack[-1]:
                            stack[-2].left = None
                        else:
                            stack[-2].right = None
                    else:
                        self.root = None
                    stack.pop()
                    break
                # Если у удаляемой вершины есть только левый деть
                elif stack[-1].left is not None and stack[-1].right is None:
                    if len(stack) > 1:
                        if stack[-2].left is stack[-1]:
                            stack[-2].left = stack[-1].left
                        else:
                            stack[-2].right = stack[-1].left
                    else:
                        self.root = stack[-1].left
                    stack.pop()
                    break
                # Если у удаляемой вершины есть только правый ребёнок
                elif stack[-1].left is None and stack[-1].right is not None:
                    if len(stack) > 1:
                        if stack[-2].left is stack[-1]:
                            stack[-2].left = stack[-1].right
                        else:
                            stack[-2].right = stack[-1].right
                    else:
                        self.root = stack[-1].right
                    stack.pop()
                    break
                # Если у удаляемой вершины есть оба ребёнка
                else:
                    updated_node = stack[-1]
                    stack.append(updated_node.right)
                    while stack[-1].left is not None:
                        stack.append(stack[-1].left)
                    updated_node.key = stack[-1].key
                    if stack[-1].right is None:
                        if stack[-2].left is stack[-1]:
                            stack[-2].left = None
                        else:
                            stack[-2].right = None
                    else:
                        if stack[-2].left is stack[-1]:
                            stack[-2].left = stack[-1].right
                        else:
                            stack[-2].right = stack[-1].right
                    stack.pop()
                    break
        while stack:  # Возвращаемся назад, обновляем высоты, балансируем
            v = stack.pop()
            v.update_height()
            self._rebalance(v, stack[-1] if len(stack) >= 1 else None)

    def exists(self, key) -> bool:
        if self.root is None:
            return False

        current_node = self.root
        while True:
            if key < current_node.key:
                if current_node.left is None:
                    return False
                else:
                    current_node = current_node.left
            elif key > current_node.key:
                if current_node.right is None:
                    return False
                else:
                    current_node = current_node.right
            else:
                return True

    def next(self, key) -> int | None:
        current_node = self.root
        result = None

        while current_node is not None:
            if current_node.key >= key:
                result = current_node.key
                current_node = current_node.left
            else:
                current_node = current_node.right

        return result

    def prev(self, key) -> int | None:
        current_node = self.root
        result = None

        while current_node is not None:
            if current_node.key <= key:
                result = current_node.key
                current_node = current_node.right
            else:
                current_node = current_node.left

        return result

    def get_tree_height(self) -> int:
        if self.root is None:
            return 0
        return self.root.height

    def get_elements(self) -> List[str]:
        if self.root is None:
            return []
        elements = []
        stack = [self.root]
        while stack:
            parent = stack.pop()
            elements.append(parent.key)
            if parent.right is not None:
                stack.append(parent.right)
            if parent.left is not None:
                stack.append(parent.left)
        return elements

    def _rotate_left(self, node, parent) -> Node:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node

        new_node = right_child
        if parent is None:
            self.root = new_node
        else:
            if parent.left is node:
                parent.left = new_node
            else:
                parent.right = new_node

        node.update_height()
        new_node.update_height()
        return new_node

    def _rotate_right(self, node, parent) -> Node:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node

        new_node = left_child
        if parent is None:
            self.root = new_node
        else:
            if parent.left is node:
                parent.left = new_node
            else:
                parent.right = new_node

        node.update_height()
        new_node.update_height()
        return new_node


if __name__ == "__main__":
    avl = AVLTree()
    Q = int(input())
    result = []
    for _ in range(Q):
        command = input()
        if command[0] == "a":
            avl.add(int(command.split()[1]))
        elif command[0] == "d":
            avl.delete(int(command.split()[1]))
        elif command[0] == "e":
            if avl.exists(int(command.split()[1])):
                result.append("YES")
            else:
                result.append("NO")
        elif command[0] == "n":
            r = avl.next(int(command.split()[1]))
            if r is not None:
                result.append(str(r))
            else:
                result.append("None")
        elif command[0:3] == "pre":
            r = avl.prev(int(command.split()[1]))
            if r is not None:
                result.append(str(r))
            else:
                result.append("None")
        elif command[0] == "r":
            r = avl.root
            result.append(str(r.key) if r is not None else "Empty")
        elif command[0] == "h":
            result.append(str(avl.get_tree_height()))
        elif command[0:3] == "pri":
            r = avl.get_elements()
            result.append(" ".join(map(str, r)) if r != [] else "Empty")

    print("\n".join(result))
