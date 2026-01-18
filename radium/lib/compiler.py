from radium.lib.bytecode import Instruction, OpCode
from radium.lib.ast_nodes import ClassDecl, Function, VarDecl, ClassInfo
from radium.lib.tokens import TokenType


class Compiler:
    def __init__(self):
        self.instructions = []
        self.classes = {}

    def compile(self, program):
        # Compile classes
        for node in program.functions:
            if isinstance(node, ClassDecl):
                self.compile_class(node)

        # Collect top-level functions
        top_level_functions = [node for node in program.functions if isinstance(node, Function)]

        # Compile main function body if present
        for node in program.functions:
            if isinstance(node, Function) and node.name == "main":
                for stmt in node.body:
                    self.compile_stmt(stmt)

        return self.instructions, top_level_functions

    def compile_class(self, cls):
        fields = {}
        methods = {}

        for m in cls.members:
            if isinstance(m, VarDecl):
                fields[m.name] = None
            elif isinstance(m, Function):
                methods[m.name] = m

        self.classes[cls.name] = ClassInfo(cls.name, fields, methods)

    def compile_stmt(self, stmt):
        if stmt.__class__.__name__ == "VarDecl":
            self.compile_expr(stmt.value)
            self.instructions.append(Instruction(OpCode.STORE, stmt.name))

        elif stmt.__class__.__name__ == "Print":
            self.compile_expr(stmt.value)
            self.instructions.append(Instruction(OpCode.PRINT))

        elif stmt.__class__.__name__ == "ExprStatement":
            # Just compile the expression for its side effects (like a call)
            self.compile_expr(stmt.expr)

        else:
            raise RuntimeError(f"Unknown statement type: {stmt.__class__.__name__}")

    def compile_expr(self, expr):
        """Compile any expression, including literals, variable refs, binary ops, member access, and calls."""

        # --- Literals and variables ---
        if expr.__class__.__name__ == "IntLiteral":
            self.instructions.append(Instruction(OpCode.LOAD_CONST, expr.value))

        elif expr.__class__.__name__ == "StringLiteral":
            self.instructions.append(Instruction(OpCode.LOAD_CONST, expr.value))

        elif expr.__class__.__name__ == "VarRef":
            self.instructions.append(Instruction(OpCode.LOAD, expr.name))

        # --- Binary operations ---
        elif expr.__class__.__name__ == "BinaryOp":
            self.compile_expr(expr.left)
            self.compile_expr(expr.right)
            if expr.op == TokenType.PLUS:
                self.instructions.append(Instruction(OpCode.ADD))
            elif expr.op == TokenType.MINUS:
                self.instructions.append(Instruction(OpCode.SUB))
            elif expr.op == TokenType.STAR:
                self.instructions.append(Instruction(OpCode.MUL))
            elif expr.op == TokenType.SLASH:
                self.instructions.append(Instruction(OpCode.DIV))
            else:
                raise RuntimeError(f"Unknown binary operator: {expr.op}")

        # --- Member access (obj.field or Class.method) ---
        elif expr.__class__.__name__ == "MemberAccess":
            # Compile the object/class first
            self.compile_expr(expr.obj)
            # Load the member
            self.instructions.append(Instruction(OpCode.LOAD_MEMBER, expr.member))

        # --- Function / method calls ---
        elif expr.__class__.__name__ == "Call":
            # Compile the callee first
            self.compile_expr(expr.callee)
            # Compile arguments in order
            for arg in expr.args:
                self.compile_expr(arg)
            # Call with number of arguments
            self.instructions.append(Instruction(OpCode.CALL, len(expr.args)))

        else:
            raise RuntimeError(f"Unknown expression type: {expr.__class__.__name__}")
