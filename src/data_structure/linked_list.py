class LinkedListNode:
    def __init__(self, value):
        self.previous = None
        self.next = None
        self.value = value

    def set_previous(self, node: "LinkedListNode"):
        self.previous = node
        if self.previous is not None:
            self.previous.set_next(self)

    def set_next(self, node: "LinkedListNode"):
        self.next = node

    def pop(self):
        if self.next:
            self.next.set_previous(self.previous)
        else:
            self.previous.next = self.next

    @classmethod
    def from_iterable(cls, iterable) -> "LinkedListNode":
        first_node = None
        previous_node = None
        for value in iterable:
            node = LinkedListNode(value)

            if previous_node:
                node.set_previous(previous_node)

            previous_node = node

            if not first_node:
                first_node = node
        return first_node

    def find_length(self) -> int:
        pointer = self
        # Backtrack.
        while True:
            if pointer.previous is None:
                break
            pointer = pointer.previous

        # Count.
        length = 1
        while True:
            if pointer.next is None:
                return length
            pointer = pointer.next
            length += 1
