import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.computation as comp
import src.stack as st
import src.bytecode as bc
from src import opcodes
import string
import random
import pytest

opcodes.initSequenceOpcodes()


def test_dummy_func():

    byte = [
        "41", "32", "33", "34", "42", "43"
    ]
    for entry in byte:
        computation = comp.Computation(st.Stack())
        try:
            opcode = opcodes.opcodes[entry]

            opcode(None, computation.stack)
            assert len(computation.stack) == opcode.produce

        except KeyError as e:
            assert False, str(e)


def test_push_func():

    sample_count = 10
    push = {
        "60": ['60' + ''.join(random.choices(string.hexdigits, k=2)) for _ in range(0, sample_count)],
        "63": ['63' + ''.join(random.choices(string.hexdigits, k=8)) for _ in range(0, sample_count)],
        "69": ['69' + ''.join(random.choices(string.hexdigits, k=20)) for _ in range(0, sample_count)],
        "7f": ['7f' + ''.join(random.choices(string.hexdigits, k=64)) for _ in range(0, sample_count)]
    }
    l = len(push["7f"])
    for key, value in push.items():
        for v in value:
            computation = comp.Computation(st.Stack())
            opcode = opcodes.opcodes[key]

            opcode(bc.Bytecode(v), computation.stack)
            assert len(computation.stack) == opcode.produce

    # test, with invalid bytecode sequence. No item to push
    opcode = opcodes.opcodes["60"]
    with pytest.raises(opcodes.ExceptionalHalt):
        computation = comp.Computation(st.Stack())
        bytecode = bc.Bytecode("60")
        # we have to increment the idx of bytecode first.
        # Otherwse idx is 0 and the push operation will push 60 to the stack
        bytecode.__next__()
        opcode(bytecode, computation.stack)
