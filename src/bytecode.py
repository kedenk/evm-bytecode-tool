

class Bytecode(object):

    def __init__(self, bytecode: str):
        if (len(bytecode) % 2) != 0:
            raise AssertionError("Bytecode length is not even")
        self.bytecode = bytecode
        self.idx = 0

        self.byterange = 2

    def getLength(self) -> int:
        return int((len(self.bytecode) / self.byterange))

    def getIndex(self) -> int:
        return self.idx

    def addShift(self, shift: int) -> None:
        self.idx += (shift * self.byterange)

    def __len__(self):
        return self.getLength()

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx >= len(self.bytecode): raise StopIteration

        byte = self.bytecode[self.idx:self.idx+self.byterange]

        self.idx += self.byterange
        return byte.lower()

    def read(self, n: int) -> str:

        result = ""
        try:
            for _ in range(0, n, 1):
                result += self.__next__()
        except StopIteration:
            pass

        return result

    def __getitem__(self, item) -> str:
        idx = item * 2
        return self.bytecode[idx:idx+self.byterange]
