from radium.lib.tokens import TokenType
from radium.lib.ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def consume(self, type_):
        token = self.current()
        if token.type != type_:
            raise SyntaxError(f"Expected {type_}, got {token.type}")
        self.pos += 1
        return token

    def parse(self):
        nodes = []
        while self.current().type != TokenType.EOF:
            if self.current().type == TokenType.CLASS:
                nodes.append(self.parse_class())
            elif self.current().type == TokenType.FUN:
                nodes.append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected top-level token: {self.current()}")
        return Program(nodes)

    # ---------------- Functions ----------------
    def parse_function(self):
        self.consume(TokenType.FUN)
        name = self.consume(TokenType.IDENT).value
        self.consume(TokenType.LPAREN)
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)

        body = []
        while self.current().type != TokenType.RBRACE:
            body.append(self.parse_statement())

        self.consume(TokenType.RBRACE)
        return Function(name, body)

    # ---------------- Classes ----------------
    def parse_class(self):
        self.consume(TokenType.CLASS)
        name = self.consume(TokenType.IDENT).value
        self.consume(TokenType.LBRACE)

        members = []
        while self.current().type != TokenType.RBRACE:
            if self.current().type == TokenType.VAL:
                members.append(self.parse_var_decl())
            elif self.current().type == TokenType.FUN:
                members.append(self.parse_function())
            else:
                raise SyntaxError(f"Invalid class member: {self.current()}")

        self.consume(TokenType.RBRACE)
        return ClassDecl(name, members)

    # ---------------- Statements ----------------
    def parse_statement(self):
        tok = self.current()

        if tok.type == TokenType.VAL:
            return self.parse_var_decl()

        if tok.type == TokenType.IDENT and tok.value == "print":
            return self.parse_print()

        # <-- NEW: allow any expression as a statement
        expr = self.parse_expression()
        return ExprStatement(expr)


    def parse_var_decl(self):
        self.consume(TokenType.VAL)
        name = self.consume(TokenType.IDENT).value
        self.consume(TokenType.EQUAL)
        value = self.parse_expression()
        return VarDecl(name, value)

    def parse_print(self):
        self.consume(TokenType.IDENT)  # 'print'
        self.consume(TokenType.LPAREN)
        value = self.parse_expression()
        self.consume(TokenType.RPAREN)
        return Print(value)

    # ---------------- Expressions ----------------
    def parse_expression(self):
        return self.parse_term()

    def parse_term(self):
        expr = self.parse_factor()
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current()
            self.consume(op.type)
            right = self.parse_factor()
            expr = BinaryOp(expr, op.type, right)
        return expr

    def parse_factor(self):
        expr = self.parse_primary()
        while self.current().type in (TokenType.STAR, TokenType.SLASH):
            op = self.current()
            self.consume(op.type)
            right = self.parse_primary()
            expr = BinaryOp(expr, op.type, right)
        return expr

    def parse_primary(self):
        tok = self.current()

        if tok.type == TokenType.INT:
            self.consume(TokenType.INT)
            expr = IntLiteral(tok.value)

        elif tok.type == TokenType.STRING:
            self.consume(TokenType.STRING)
            expr = StringLiteral(tok.value)

        elif tok.type == TokenType.IDENT:
            self.consume(TokenType.IDENT)
            expr = VarRef(tok.value)

        elif tok.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)

        else:
            raise SyntaxError(f"Invalid expression: {tok}")

        # <-- NEW: handle member access and calls like ClassName.method() or obj.method()
        return self.parse_member_access_or_call(expr)

    # ---------------- Member Access & Calls ----------------
    def parse_member_access_or_call(self, expr):
        while self.current().type in (TokenType.DOT, TokenType.LPAREN):
            if self.current().type == TokenType.DOT:
                self.consume(TokenType.DOT)
                member = self.consume(TokenType.IDENT).value
                expr = MemberAccess(expr, member)
            elif self.current().type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                args = []
                if self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                self.consume(TokenType.RPAREN)
                expr = Call(expr, args)
        return expr
