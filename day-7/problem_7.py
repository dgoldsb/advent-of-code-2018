"""
The navigation system's license file consists of a list of numbers (your puzzle input). The numbers define a data structure which, when processed, produces some kind of tree that can be used to calculate the license number.

The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all other nodes in the tree (or contains nodes that contain nodes, and so on).

Specifically, a node consists of:

    A header, which is always exactly two numbers:
        The quantity of child nodes.
        The quantity of metadata entries.
    Zero or more child nodes (as specified in the header).
    One or more metadata entries (as specified in the header).

Each child node is itself a node that has its own header, child nodes, and metadata. For example:

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----

In this example, each node of the tree is also marked with an underline starting with a letter for easier identification. In it, there are four nodes:

    A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
    B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
    C, which has 1 child node (D) and 1 metadata entry (2).
    D, which has 0 child nodes and 1 metadata entry (99).

The first check done on the license file is to simply add up all of the metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

What is the sum of all metadata entries?
"""

class Node:
    def __init__(self, a, b):
        self._child_count = a
        self._meta_count = b
        self.metadata = None


def recursive_decompose(sequence):
    nodes = []

    nodes.append(Node(sequence[0], sequence[1]))
    sequence = sequence[2:]

    if nodes[0]._child_count > 0:
        for _ in range(nodes[0]._child_count):
            children, remainder = recursive_decompose(sequence)
            nodes = nodes + children
            sequence = remainder

    if nodes[0]._meta_count > 0:
        nodes[0].metadata = sequence[0:nodes[0]._meta_count]
        sequence = sequence[nodes[0]._meta_count:]

    return nodes, sequence


if __name__ == '__main__':
    # Read input.
    with open('input', 'r') as file:
        sequence = [int(x) for x in file.read().split(' ')]

    # Process to data structure.
    nodes, _ = recursive_decompose(sequence)

    # Answer 1.
    total = 0
    for node in nodes:
        for meta in node.metadata:
            total += meta
    print(f'Answer 1 is {total}.')
