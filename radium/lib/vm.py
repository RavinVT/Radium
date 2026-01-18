from radium.lib.tokens import TokenType
from radium.lib.ast_nodes import *

class VM:
    def __init__(self, instructions, classes, top_level_functions):
        self.instructions = instructions                      # top-level instructions (from top-level main)
        self.classes = classes                                # ClassInfo objects
        self.functions = {f.name: f for f in top_level_functions}  # top-level functions
        self.stack = []
        self.variables = {}                                   # top-level variables

    def run(self):
        if "main" not in self.functions:
            raise RuntimeError("Program must have a top-level fun main()")
        self.call_function("main", [])

    # ---------------- Call Functions ----------------
    def call_function(self, name, args, instance=None):
        if name not in self.functions:
            raise RuntimeError(f"Unknown function: {name}")

        func = self.functions[name]

        # For now, simple execution of statements
        for stmt in func.body:
            self.execute_statement(stmt, instance)

    # ---------------- Execute Statements ----------------
    def execute_statement(self, stmt, instance=None):
        if isinstance(stmt, VarDecl):
            value = self.evaluate_expression(stmt.value, instance)
            if instance is not None:
                instance[stmt.name] = value
            else:
                self.variables[stmt.name] = value

        elif isinstance(stmt, Print):
            value = self.evaluate_expression(stmt.value, instance)
            print(value)

        elif isinstance(stmt, ExprStatement):
            self.evaluate_expression(stmt.expr, instance)

        else:
            raise RuntimeError(f"Unknown statement type: {stmt}")

    # ---------------- Evaluate Expressions ----------------
    def evaluate_expression(self, expr, instance=None):
        if isinstance(expr, IntLiteral):
            return expr.value

        elif isinstance(expr, StringLiteral):
            return expr.value


        elif isinstance(expr, VarRef):

            # First check local instance fields

            if instance is not None and expr.name in instance:
                return instance[expr.name]

            # Then check top-level variables

            if expr.name in self.variables:
                return self.variables[expr.name]

            # Finally, check if it's a class

            if expr.name in self.classes:
                return self.classes[expr.name]

            raise RuntimeError(f"Unknown variable or class: {expr.name}")


        elif isinstance(expr, BinaryOp):
            left = self.evaluate_expression(expr.left, instance)
            right = self.evaluate_expression(expr.right, instance)
            if expr.op == TokenType.PLUS:
                return left + right
            elif expr.op == TokenType.MINUS:
                return left - right
            elif expr.op == TokenType.STAR:
                return left * right
            elif expr.op == TokenType.SLASH:
                return left / right


        elif isinstance(expr, MemberAccess):
            obj = self.evaluate_expression(expr.obj, instance)
            member_name = expr.member
            # If obj is an instance (dict with __class__)
            if isinstance(obj, dict) and "__class__" in obj:
                cls_info = obj["__class__"]
                # First try instance field
                if member_name in obj:
                    return obj[member_name]
                # Then try method
                elif member_name in cls_info.methods:
                    return ("method", obj, member_name)
                else:
                    raise RuntimeError(f"Unknown member: {member_name}")

            # If obj is a ClassInfo (calling a class method)
            elif isinstance(obj, ClassInfo):
                cls_info = obj
                if member_name in cls_info.methods:
                    return ("class_method", cls_info, member_name)
                else:
                    raise RuntimeError(f"Unknown class method: {cls_info.name}.{member_name}")

            else:
                raise RuntimeError(f"Invalid object for member access: {obj}")



        elif isinstance(expr, Call):
            callee_result = self.evaluate_expression(expr.callee, instance)
            args = [self.evaluate_expression(a, instance) for a in expr.args]
            if isinstance(callee_result, tuple):
                kind, target, method_name = callee_result
                method = target.methods[method_name] if kind == "class_method" else target["__class__"].methods[
                    method_name]
                # Create instance if it's a class method call
                if kind == "class_method":
                    obj_instance = {**{k: None for k in target.fields}, "__class__": target}
                else:
                    obj_instance = target
                for stmt in method.body:
                    self.execute_statement(stmt, obj_instance)
                return None

            # Top-level function
            elif isinstance(callee_result, Function):
                for stmt in callee_result.body:
                    self.execute_statement(stmt, instance)
                return None
