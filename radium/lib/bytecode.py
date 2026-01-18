class OpCode:
    LOAD_MEMBER = "LOAD_MEMBER"
    CALL = "CALL"
    DIV = "DIV"
    MUL = "MUL"
    SUB = "SUB"
    ADD = "ADD"
    LOAD_CONST = "LOAD_CONST"
    STORE = "STORE"
    LOAD = "LOAD"
    PRINT = "PRINT"
    NEW = "NEW"
    LOAD_FIELD = "LOAD_FIELD"
    STORE_FIELD = "STORE_FIELD"
    CALL_METHOD = "CALL_METHOD"
    RETURN = "RETURN"


class Instruction:
    def __init__(self, opcode, operand=None):
        self.opcode = opcode
        self.operand = operand

    def __repr__(self):
        return f"{self.opcode} {self.operand}"
