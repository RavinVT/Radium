class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions

class Function(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class VarDecl(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IntLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class VarRef(ASTNode):
    def __init__(self, name):
        self.name = name

class Print(ASTNode):
    def __init__(self, value):
        self.value = value

class ClassDecl(ASTNode):
    def __init__(self, name, members):
        self.name = name
        self.members = members  # VarDecl or Function

class MemberAccess(ASTNode):
    def __init__(self, obj, member):
        self.obj = obj
        self.member = member

class Call(ASTNode):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class ObjectInstance:
    def __init__(self, cls):
        self.cls = cls
        self.fields = {}
class ClassInfo:
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods


class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # TokenType.PLUS, MINUS, etc.
        self.right = right

class ExprStatement:
    def __init__(self, expr):
        self.expr = expr
