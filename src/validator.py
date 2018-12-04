import src.computation as comp
import src.bytecode as bc
import src.stack as st
import logging.config
from src import opcodes
from collections import OrderedDict

log = logging.getLogger(__name__)


class Validator(object):

    def __init__(self):
        self.usedOpcodes = {}
        self.opcodeUsageAmount = OrderedDict()
        self.__initUsageStatistic()
        self.opcode_count = 0

    def __initUsageStatistic(self):
        for op in opcodes.opcodes.values():
            self.opcodeUsageAmount[op.opcode] = 0

    def checkLength(self, bytecode: str) -> bool:
        """
        Returns true, if length is ok
        :param input:
        :return:
        """
        return not((len(bytecode) % 2) != 0)

    def checkInput(self, bytecode: str) -> (bool, str):

        computation = comp.Computation(st.Stack())
        if not self.checkLength(bytecode):
            raise opcodes.InvalidSequenceLength(len(bytecode))
        bytecode = bc.Bytecode(bytecode)

        for byte in bytecode:

            byte = byte.lower()
            try:
                opcode = opcodes.opcodes[byte]

                self.__addUsedOpcode(opcode)
                opcode(bytecode, computation.stack)
            except KeyError as e:
                return False, str(e)
            except opcodes.ExceptionalHalt as e:
                return False, str(e.msg)
            except opcodes.HaltException:
                break

        return True, None

    def __incOpcodeCount(self) -> None:
        self.opcode_count += 1

    def getByteCount(self, bytecode: str) -> int:
        return int(len(bytecode) / 2)

    def getOpcodeCount(self) -> int:
        return self.opcode_count

    def __addUsedOpcode(self, opcode: opcodes.Opcode):

        if opcode.opcode not in self.usedOpcodes.keys():
            self.usedOpcodes[opcode.opcode] = opcode

        if opcode.opcode not in self.opcodeUsageAmount.keys():
            self.opcodeUsageAmount[opcode.opcode] = 0

        self.opcodeUsageAmount[opcode.opcode] += 1
        self.__incOpcodeCount()

    def getUsedOpcodes(self) -> int:
        return len(self.usedOpcodes)

    def printOpcodeUsage(self) -> None:

        for key, value in sorted(self.opcodeUsageAmount.items(), key=lambda x: x[0]):
            strKey = hex(key)
            _, _, strKey = strKey.rpartition('x')
            strKey = strKey.rjust(2, '0')
            message = str.format("0x{:02x} {}", key, opcodes.opcodes[strKey].name).ljust(20, ' ')
            log.info("%s%d" % (message, self.opcodeUsageAmount[key]))
