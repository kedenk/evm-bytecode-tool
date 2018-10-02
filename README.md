# evm-bytecode-tool
Ethereum Virtual Machine bytecode tool for validation of bytecode sequences. 


    usage: bytecode-tool.py [-h] [-v code | -d directory] [-g] [-c] [-a] [-u]

    Tool for EVM bytecode validation

    optional arguments:
    -h, --help            show this help message and exit
    -v code, --validate code
                          Validate the given bytecode sequence
    -d directory, --dir directory
                          Validate all bytecode sequence files located in the given
                          directory
    -g, --gas             Calculate the gas consumption of given bytecode sequence
    -c, --coverage        Print opcode coverage (Amount of used opcodes)
    -a, --average         Calculates the average length of the given bytecode
                          sequences
    -u, --usage           Prints the amount of opcode usages
