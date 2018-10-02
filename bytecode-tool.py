from src import opcodes, bytecode as bc
import json
import os
from collections import OrderedDict
import src.stack as st

# for logging
import logging.config
with open("./logging.json") as logging_config_file:
    logging_config = json.load(logging_config_file)
    logging.config.dictConfig(logging_config)
log = logging.getLogger(__name__)

usedOpcodes = {}
opcodeUsageAmount = OrderedDict()
OPCODE_COUNT = 0
VALIDATED_SEQUENCES = 0


class Computation(object):

    def __init__(self, stack: st.Stack):
        self.stack = stack


def initUsageStatistic():
    for op in opcodes.opcodes.values():
        opcodeUsageAmount[op.opcode] = 0


def addUsedOpcode(opcode: opcodes.Opcode):

    if opcode.opcode not in usedOpcodes.keys():
        usedOpcodes[opcode.opcode] = opcode

    if opcode.opcode not in opcodeUsageAmount.keys():
        opcodeUsageAmount[opcode.opcode] = 0

    opcodeUsageAmount[opcode.opcode] += 1


def getUsedOpcodes():
    return len(usedOpcodes)


def printOpcodeUsage():

    for key, value in sorted(opcodeUsageAmount.items(), key=lambda x: x[0]):
        strKey = hex(key)
        _, _, strKey = strKey.rpartition('x')
        strKey = strKey.rjust(2, '0')
        message = str.format("0x{:02x} {}", key, opcodes.opcodes[strKey].name).ljust(20, ' ')
        log.info("%s%d" % (message, opcodeUsageAmount[key]))


def checkLength(bytecode: str) -> bool:
    """
    Returns true, if length is ok
    :param input:
    :return:
    """
    return not((len(bytecode) % 2) != 0)


def checkInput(bytecode: str, computation: Computation) -> (bool, str):

    bytecode = bc.Bytecode(bytecode)
    global OPCODE_COUNT
    global VALIDATED_SEQUENCES
    # inc validates sequences counter
    VALIDATED_SEQUENCES += 1

    for byte in bytecode:

        byte = byte.lower()
        try:
            opcode = opcodes.opcodes[byte]

            OPCODE_COUNT += 1
            addUsedOpcode(opcode)
            opcode(bytecode, computation.stack)
        except KeyError as e:
            return False, str(e)
        except opcodes.HaltException:
            break

    return True, None


def checkInputDir(inputdir: str, computation: Computation) -> (int, int):

    readFiles = 0
    failed = 0
    for inputFileName in os.listdir(inputdir):
        inputFile = os.path.join(inputdir, inputFileName)

        content = None
        with open(inputFile, "r") as f:
            content = f.read()
            readFiles += 1

        if not checkLength(content):
            log.warn(str.format("Odd input length: {}", inputFileName))
            failed += 1
            continue

        valid, invalidopcode = checkInput(content, computation)
        if not valid:
            log.warn(str.format("Invalid opcode {}: {}", invalidopcode, inputFileName))
            failed += 1

    return readFiles, failed


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Tool for EVM bytecode validation")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--validate", metavar="code",
                        help="Validate the given bytecode sequence")
    group.add_argument("-d", "--dir", metavar="directory",
                       help="Validate all bytecode sequence files located in the given directory")

    parser.add_argument("-g", "--gas",
                        help="Calculate the gas consumption of given bytecode sequence",
                        action="store_true")
    parser.add_argument("-c", "--coverage",
                        help="Print opcode coverage (Amount of used opcodes)",
                        action="store_true")
    parser.add_argument("-a", "--average",
                        help="Calculates the average length of the given bytecode sequences",
                        action="store_true")
    parser.add_argument("-u", "--usage",
                        help="Prints the amount of opcode usages",
                        action="store_true")

    args = parser.parse_args()
    opcodes.initSequenceOpcodes()
    initUsageStatistic()
    computation = Computation(st.Stack())

    if args.validate:
        valid, invalid = checkInput(args.validate, computation)
        if not valid:
            log.warn("Invalid opcode " + str(invalid))
            log.warn(str.format("[VALIDATION FAILED]"))
        else:
            log.info("[VALIDATION PASSED]")
    elif args.dir:
        readInputs, failed = checkInputDir(args.dir, computation)
        log.info(str.format("{} inputs checked", readInputs))
        if failed > 0:
            log.info(str.format("{} inputs invalid", failed))
        else:
            log.info("[VALIDATION PASSED]")
    else:
        print("Missing command line arguments")
        exit(-1)

    if args.coverage:
        log.info(str(getUsedOpcodes()) + " of " + str(len(opcodes.opcodes)) + " operation codes used.")

    if args.average:
        log.info(str.format("Average used opcodes {}", (OPCODE_COUNT / VALIDATED_SEQUENCES)))

    if args.usage:
        printOpcodeUsage()
