from typing import List

from src.constants import type_hint_constants


class Stack(object):

    def __init__(self):
        self.stack: List[str] = []

    def pop(self, num_items, type_hint) -> str:
        return next(self._pop(num_items, type_hint))

    def _pop(self, num_items, type_hint):
        for _ in range(num_items):
            if type_hint == type_hint_constants.UINT256:
                value = self.stack.pop()
                if isinstance(value, int):
                    yield value
                else:
                    yield self.big_endian_to_int(value)
            elif type_hint == type_hint_constants.ANY:
                yield self.stack.pop()
            else:
                raise TypeError(
                    "Unknown type_hint: {0}.  Must be one of {1}".format(
                        type_hint,
                        ", ".join((type_hint_constants.UINT256, type_hint_constants.ANY)),
                    )
                )

    def big_endian_to_int(self, value: bytes) -> int:
        return int.from_bytes(value, byteorder='big')

    def push(self, item: str):
        self.stack.append(item)

    def printStack(self):
        print(self.stack)

    def getStack(self):
        return self.stack

    def __iter__(self):
        self.iter = 0
        self.maxiter = len(self.stack)
        return self

    def __next__(self):
        if self.iter <= self.maxiter:
            result = self.stack[self.iter]
            self.iter += 1
            return result
        else:
            raise StopIteration