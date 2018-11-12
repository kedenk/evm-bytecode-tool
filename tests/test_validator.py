import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.validator as val
from src import opcodes
import pytest

opcodes.initSequenceOpcodes()


valid_bytecodes = [
    "60013201",
    "634563f365600302"
]

invalid_bytecodes = [
    "600101",
    "60014001"
]

invalid_sequence_length = [
    "60011",
    "6045624575023",
    "403"
]


def test_check_input_invalid_length():

    validator = val.Validator()

    for entry in invalid_sequence_length:
        with pytest.raises(opcodes.InvalidSequenceLength):
            validator.checkInput(entry)


def test_check_input_valid_bytecodes():

    validator = val.Validator()
    for entry in valid_bytecodes:
        valid, invalid_msg = validator.checkInput(entry)
        assert valid, invalid_msg


def test_check_input_invalid_bytecodes():

    validator = val.Validator()
    for entry in invalid_bytecodes:
        valid, invalid_msg = validator.checkInput(entry)
        assert not valid, invalid_msg
