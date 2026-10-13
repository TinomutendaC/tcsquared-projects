"""
data_structures.py
-------------------
Group 6 - Expression Evaluator (Stack-Based Calculator)
CUITM205 Mini Project

This module implements the two core data structures used by the
calculator:

    1. Stack  -> used to hold operators during infix-to-postfix
                 conversion, and to hold operands during postfix
                 evaluation.
    2. Queue  -> used to hold the output token stream (the postfix
                 expression) produced by the Shunting-Yard algorithm.

Both are implemented from scratch (on top of a Python list) so that
the underlying data-structure operations (push, pop, peek, enqueue,
dequeue) are explicit, rather than relying on Python's built-in list
methods directly inside the algorithm logic.
"""


class Stack:
    """A simple LIFO (Last-In, First-Out) stack."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item of the stack."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __len__(self):
        return self.size()

    def __repr__(self):
        return f"Stack({self._items})"


class Queue:
    """A simple FIFO (First-In, First-Out) queue."""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.pop(0)

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        """Return a shallow copy of the queue's contents, front to back."""
        return list(self._items)

    def __len__(self):
        return self.size()

    def __repr__(self):
        return f"Queue({self._items})"
