import src.bytecode as bc
import src.stack as st
from src.constants import type_hint_constants


class HaltException(Exception):

    def __init__(self, msg):
        self.msg = msg


class ExceptionalHalt(HaltException):

    def __init__(self, msg):
        super().__init__(msg)


class InvalidSequenceLength(Exception):

    def __init__(self, invalid_length: int):
        self.invalid_length = invalid_length


class Opcode(object):

    def __init__(self, opcode, name: str, gasconsumption, consume, produce, byteshift, func=None):
        self.opcode = opcode
        self.name = name
        self.gasconsumption = gasconsumption
        self.consume = consume
        self.produce = produce
        self.byteshift = byteshift
        self.func = func

    def getShift(self):
        return self.byteshift

    def __validateStack(self, stack: st.Stack):
        stackLen = len(stack.getStack())
        if stackLen < self.consume:
            raise ExceptionalHalt("Stackunderflow: %d != %d" % (stackLen, self.consume))

    def __call__(self, bytecode: bc.Bytecode, stack: st.Stack):
        self.__validateStack(stack)
        if self.func is not None:
            self.func(self, bytecode, stack)


def pushFunc(opcode: Opcode, bytecode: bc.Bytecode, stack: st.Stack):
    toPush = bytecode.read(opcode.getShift())
    if len(toPush) == 0:
        raise ExceptionalHalt("No values to push in bytecode sequence")
    stack.push(toPush)


def haltFunc(opcode: Opcode, bytecode: bc.Bytecode, stack: st.Stack):
    raise HaltException("Halted by %s" % opcode.name)


def dummyFunc(opcode: Opcode, bytecode: bc.Bytecode, stack: st.Stack):

    if opcode.consume > 0:
        stack.pop(opcode.consume, type_hint_constants.ANY)

    if opcode.produce > 0:
        import time
        stack.push(str(int(time.time())))


def initSequenceOpcodes():

    # PUSH opcodes
    k = 1
    for i in range(96, 128, 1):
        hexValue = hex(i)
        _, _, id = hexValue.rpartition("x")
        opcodes[id] = Opcode(int(hexValue, 0), "PUSH" + str(k), 0, 0, 1, k, pushFunc)
        k += 1

    # DUP opcodes
    c = 1
    for i in range(128, 144, 1):
        hexValue = hex(i)
        _, _, id = hexValue.rpartition("x")
        opcodes[id] = Opcode(int(hexValue, 0), "DUP" + str(c), 0, c, (c + 1), 0, dummyFunc)
        c += 1


    # SWAP opcodes
    c = 2
    for i in range(144, 160, 1):
        hexValue = hex(i)
        _, _, id = hexValue.rpartition("x")
        opcodes[id] = Opcode(int(hexValue, 0), "SWAP" + str(c), 0, c, c, 0, dummyFunc)
        c += 1


opcodes = {

    "00": Opcode(0x0, "STOP", 0, 0, 0, 0, haltFunc),

    "01": Opcode(0x01, "ADD", 0, 2, 1, 0, dummyFunc),
    "02": Opcode(0x02, "MUL", 0, 2, 1, 0, dummyFunc),
    "03": Opcode(0x03, "SUB", 0, 2, 1, 0, dummyFunc),
    "04": Opcode(0x04, "DIV", 0, 2, 1, 0, dummyFunc),
    "05": Opcode(0x05, "SDIV", 0, 2, 1, 0, dummyFunc),
    "06": Opcode(0x06, "MOD", 0, 2, 1, 0, dummyFunc),
    "07": Opcode(0x07, "SMOD", 0, 2, 1, 0, dummyFunc),
    "08": Opcode(0x08, "ADDMOD", 0, 3, 1, 0, dummyFunc),
    "09": Opcode(0x09, "MULMOD", 0, 3, 1, 0, dummyFunc),
    "0a": Opcode(0x0a, "EXP", 0, 2, 1, 0, dummyFunc),
    "0b": Opcode(0x0b, "SIGNEXTEND", 0, 2, 1, 0, dummyFunc),

    "10": Opcode(0x10, "LT", 0, 2, 1, 0, dummyFunc),
    "11": Opcode(0x11, "GT", 0, 2, 1, 0, dummyFunc),
    "12": Opcode(0x12, "SLT", 0, 2, 1, 0, dummyFunc),
    "13": Opcode(0x13, "SGT", 0, 2, 1, 0, dummyFunc),
    "14": Opcode(0x14, "EQ", 0, 2, 1, 0, dummyFunc),
    "15": Opcode(0x15, "ISZERO", 0, 1, 1, 0, dummyFunc),
    "16": Opcode(0x16, "AND", 0, 2, 1, 0, dummyFunc),
    "17": Opcode(0x17, "OR", 0, 2, 1, 0, dummyFunc),
    "18": Opcode(0x18, "XOR", 0, 2, 1, 0, dummyFunc),
    "19": Opcode(0x19, "NOT", 0, 1, 1, 0, dummyFunc),
    "1a": Opcode(0x1a, "BYTE", 0, 2, 1, 0, dummyFunc),

    "20": Opcode(0x20, "SHA3", 0, 2, 1, 0, dummyFunc),

    "30": Opcode(0x30, "ADDRESS", 0, 0, 1, 0, dummyFunc),
    "31": Opcode(0x31, "BALANCE", 0, 1, 1, 0, dummyFunc),
    "32": Opcode(0x32, "ORIGIN", 0, 0, 1, 0, dummyFunc),
    "33": Opcode(0x33, "CALLER", 0, 0, 1, 0, dummyFunc),
    "34": Opcode(0x34, "CALLVALUE", 0, 0, 1, 0, dummyFunc),
    "35": Opcode(0x35, "CALLDATALOAD", 0, 1, 1, 0, dummyFunc),
    "36": Opcode(0x36, "CALLDATASIZE", 0, 0, 1, 0, dummyFunc),
    "37": Opcode(0x37, "CALLDATACOPY", 0, 3, 0, 0, dummyFunc),
    "38": Opcode(0x38, "CODESIZE", 0, 0, 1, 0, dummyFunc),
    "39": Opcode(0x39, "CODECOPY", 0, 3, 0, 0, dummyFunc),
    "3a": Opcode(0x3a, "GASPRICE", 0, 0, 1, 0, dummyFunc),
    "3b": Opcode(0x3b, "EXTCODESIZE", 0, 1, 1, 0, dummyFunc),
    "3c": Opcode(0x3c, "EXTCODECOPY", 0, 4, 0, 0, dummyFunc),
    "3d": Opcode(0x3d, "RETURNDATASIZE", 0, 0, 1, 0, dummyFunc),
    "3e": Opcode(0x3e, "RETURNDATACOPY", 0, 3, 0, 0, dummyFunc),

    "40": Opcode(0x40, "BLOCKHASH", 0, 1, 1, 0, dummyFunc),
    "41": Opcode(0x41, "COINBASE", 0, 0, 1, 0, dummyFunc),
    "42": Opcode(0x42, "TIMESTAMP", 0, 0, 1, 0, dummyFunc),
    "43": Opcode(0x43, "NUMBER", 0, 0, 1, 0, dummyFunc),
    "44": Opcode(0x44, "DIFFICULTY", 0, 0, 1, 0, dummyFunc),
    "45": Opcode(0x45, "GASLIMIT", 0, 0, 1, 0, dummyFunc),

    "50": Opcode(0x50, "POP", 0, 1, 0, 0, dummyFunc),
    "51": Opcode(0x51, "MLOAD", 0, 1, 1, 0, dummyFunc),
    "52": Opcode(0x52, "MSTORE", 0, 2, 0, 0, dummyFunc),
    "53": Opcode(0x53, "MSTORE8", 0, 2, 0, 0, dummyFunc),
    "54": Opcode(0x54, "SLOAD", 0, 1, 1, 0, dummyFunc),
    "55": Opcode(0x55, "SSTORE", 0, 2, 0, 0, dummyFunc),
    "56": Opcode(0x56, "JUMP", 0, 1, 0, 0, dummyFunc),
    "57": Opcode(0x57, "JUMPI", 0, 2, 0, 0, dummyFunc),
    "58": Opcode(0x58, "PC", 0, 0, 1, 0, dummyFunc),
    "59": Opcode(0x59, "MSIZE", 0, 0, 1, 0, dummyFunc),
    "5a": Opcode(0x5a, "GAS", 0, 0, 1, 0, dummyFunc),
    "5b": Opcode(0x5b, "JUMPDEST", 0, 0, 0, 0),

    # PUSH opcodes are inserted in initSequenceOpcodes

    # DUP opcodes are inserted in initSequenceOpcodes

    # SWAP opcodes are inserted in initSequenceOpcodes

    "a0": Opcode(0xa0, "LOG0", 0, 2, 0, 0),
    "a1": Opcode(0xa1, "LOG1", 0, 3, 0, 0),
    "a2": Opcode(0xa2, "LOG2", 0, 4, 0, 0),
    "a3": Opcode(0xa3, "LOG3", 0, 5, 0, 0),
    "a4": Opcode(0xa4, "LOG4", 0, 6, 0, 0),

    "f0": Opcode(0xf0, "CREATE", 0, 3, 1, 0),
    "f1": Opcode(0xf1, "CALL", 0, 7, 1, 0),
    "f2": Opcode(0xf2, "CALLCODE", 0, 7, 1, 0),
    "f3": Opcode(0xf3, "RETURN", 0, 2, 0, 0, haltFunc),
    "f4": Opcode(0xf4, "DELEGATECALL", 0, 6, 1, 0),
    "fa": Opcode(0xfa, "STATICCALL", 0, 6, 1, 0),
    "fd": Opcode(0xfd, "REVERT", 0, 2, 0, 0),
    "fe": Opcode(0xfe, "INVALID", 0, 0, 0, 0, haltFunc),
    "ff": Opcode(0xff, "SELFDESTRUCT", 0, 1, 0, 0, haltFunc),
}

