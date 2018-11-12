from src import bytecode as bc


def test_iterator():

    bytecode = bc.Bytecode("6001600201")

    for byte in bytecode:
        assert (len(byte) % 2) == 0

    assert bytecode[0] == "60"
    assert bytecode[3] == "02"
    assert bytecode[len(bytecode) - 1] == "01"
