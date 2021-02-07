#
class Heap:
    def __init__(self):
        self._array = []

    @staticmethod
    def get_parent(pos):
        return (pos + 1) // 2 - 1

    @staticmethod
    def get_children(pos):
        right = (pos + 1) * 2
        left = right - 1
        return left, right

    @staticmethod
    def swap(array, a, b):
        array[a], array[b] = array[b], array[a]

    @staticmethod
    def backtrack(best_parents, start, end):
        if end not in best_parents:
            return None
        cursor = end
        path = [cursor]
        while cursor in best_parents:
            cursor = best_parents[cursor]
            path.append(cursor)
            if cursor == start:
                return list(reversed(path))
        return None

    def peek(self):
        return self._array[0] if self._array else None

    def _get_smallest_child(self, parent):
        return min([
            it
            for it in Heap.get_children(parent)
            if it < len(self._array)
        ], key=lambda it: self._array[it], default=-1)

    def _sift_down(self):
        parent = 0
        smallest = self._get_smallest_child(parent)
        while smallest != -1 and self._array[smallest] < self._array[parent]:
            Heap.swap(self._array, smallest, parent)
            parent, smallest = smallest, self._get_smallest_child(smallest)

    def pop(self):
        if not self._array:
            return None
        Heap.swap(self._array, 0, len(self._array) - 1)
        node = self._array.pop()
        self._sift_down()
        return node

    def _sift_up(self):
        index = len(self._array) - 1
        parent = Heap.get_parent(index)
        while parent != -1 and self._array[index] < self._array[parent]:
            Heap.swap(self._array, index, parent)
            index, parent = parent, Heap.get_parent(parent)

    def add(self, item):
        self._array.append(item)
        self._sift_up()

    def __bool__(self):
        return bool(self._array)
