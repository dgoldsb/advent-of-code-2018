from src.data_structure.linked_list import LinkedListNode
from src.day_protocol import AocDay


def delete_pairs(pointer: LinkedListNode) -> LinkedListNode:
    while True:
        if (
            pointer.value.isupper()
            and pointer.next is not None
            and pointer.next.value == pointer.value.lower()
        ) or (
            pointer.value.islower()
            and pointer.next is not None
            and pointer.next.value == pointer.value.upper()
        ):
            new_pointer = pointer.previous
            if new_pointer is None:
                new_pointer = pointer.next

            pointer.next.pop()
            pointer.pop()
            pointer = new_pointer
        else:
            if pointer.next is None:
                return pointer
            else:
                pointer = pointer.next


class Day5(AocDay):
    def part_a(self, input_: str) -> str:
        linked_list = LinkedListNode.from_iterable(input_)
        return str(delete_pairs(linked_list).find_length())

    def part_b(self, input_: str) -> str:
        shortest = len(input_)
        elements = {x.lower() for x in input_}
        for element in list(elements):
            edited_input = input_.replace(element.lower(), "").replace(
                element.upper(), ""
            )
            linked_list = LinkedListNode.from_iterable(edited_input)
            length_polymer = delete_pairs(linked_list).find_length()
            if length_polymer < shortest:
                shortest = length_polymer
        return str(shortest)
