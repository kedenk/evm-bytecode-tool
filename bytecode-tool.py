from src import opcodes
import json
import os
import src.validator as val

# for logging
import logging.config
with open("./logging.json") as logging_config_file:
    logging_config = json.load(logging_config_file)
    logging.config.dictConfig(logging_config)
log = logging.getLogger(__name__)

VALIDATED_SEQUENCES = 0


def checkInputDir(inputdir: str, validator: val.Validator) -> (int, int):

    readFiles = 0
    failed = 0
    for inputFileName in os.listdir(inputdir):
        inputFile = os.path.join(inputdir, inputFileName)

        content = None
        with open(inputFile, "r") as f:
            content = f.read()
            readFiles += 1

        if not validator.checkLength(content):
            log.warn(str.format("Odd input length: {}", inputFileName))
            failed += 1
            continue

        valid, invalidopcode = validator.checkInput(content)
        if not valid:
            log.warn(str.format("Invalid opcode {}: {}", invalidopcode, inputFileName))
            failed += 1

        global VALIDATED_SEQUENCES
        # inc validates sequences counter
        VALIDATED_SEQUENCES += 1

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
    validator = val.Validator()

    if args.validate:
        # inc validates sequences counter
        VALIDATED_SEQUENCES += 1
        valid, invalid_msg = validator.checkInput(args.validate)
        if not valid:
            log.warn("Invalid opcode " + str(invalid_msg))
            log.warn(str.format("[VALIDATION FAILED]"))
        else:
            log.info("[VALIDATION PASSED]")
    elif args.dir:
        readInputs, failed = checkInputDir(args.dir, validator)
        log.info(str.format("{} inputs checked", readInputs))
        if failed > 0:
            log.info(str.format("{} inputs invalid", failed))
        else:
            log.info("[VALIDATION PASSED]")
    else:
        print("Missing command line arguments")
        exit(-1)

    if args.coverage:
        log.info(str(validator.getUsedOpcodes()) + " of " + str(len(opcodes.opcodes)) + " operation codes used.")

    if args.average:
        log.info(str.format("Average used opcodes {}", (validator.getOpcodeCount() / VALIDATED_SEQUENCES)))

    if args.usage:
        validator.printOpcodeUsage()
