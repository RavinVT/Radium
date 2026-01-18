from radium.lib.tokens import Token, TokenType


KEYWORDS = {
    "fun": TokenType.FUN,
    "val": TokenType.VAL,
    "var": TokenType.VAR,
    "class": TokenType.CLASS,
    "print": TokenType.IDENT,
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def current(self):
        return self.source[self.pos] if self.pos < len(self.source) else "\0"

    def advance(self):
        ch = self.current()
        self.pos += 1
        self.col += 1
        return ch

    def _string(self):
        self.advance()  # skip opening quote
        start = self.pos

        while self.current() != '"' and self.current() != "\0":
            self.advance()

        if self.current() == "\0":
            raise SyntaxError("Unterminated string literal")

        value = self.source[start:self.pos]
        self.advance()  # skip closing quote

        return Token(TokenType.STRING, value)

    def tokenize(self):
        tokens = []

        while self.current() != "\0":
            ch = self.current()

            # Whitespace
            if ch.isspace():
                self.advance()
                continue

            if ch == "/" and self.peek() == "/":
                self.skip_line_comment()
                continue

            if ch == "/" and self.peek() == "*":
                self.skip_block_comment()
                continue

            if ch.isalpha():
                tokens.append(self._identifier())
                continue

            if ch.isdigit():
                tokens.append(self._number())
                continue

            if ch == "(":
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
            elif ch == ")":
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
            elif ch == "{":
                tokens.append(Token(TokenType.LBRACE))
                self.advance()
            elif ch == "}":
                tokens.append(Token(TokenType.RBRACE))
                self.advance()
            elif ch == ":":
                tokens.append(Token(TokenType.COLON))
                self.advance()
            elif ch == "=":
                tokens.append(Token(TokenType.EQUAL))
                self.advance()
            elif ch == ",":
                tokens.append(Token(TokenType.COMMA))
                self.advance()
            elif ch == ".":
                tokens.append(Token(TokenType.DOT))
                self.advance()
            elif ch == '"':
                tokens.append(self._string())  # _string() already advances past quotes
            elif ch == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
            elif ch == '-':
                tokens.append(Token(TokenType.MINUS))
                self.advance()
            elif ch == '*':
                tokens.append(Token(TokenType.STAR))
                self.advance()
            elif ch == '/':
                if self.peek() == '/':
                    self.skip_line_comment()
                elif self.peek() == '*':
                    self.skip_block_comment()
                else:
                    tokens.append(Token(TokenType.SLASH))
                    self.advance()
            else:
                raise SyntaxError(f"Unexpected character '{ch}'")

        tokens.append(Token(TokenType.EOF))
        return tokens

    def _identifier(self):
        start = self.pos
        while self.current().isalnum() or self.current() == "_":
            self.advance()
        text = self.source[start:self.pos]
        token_type = KEYWORDS.get(text, TokenType.IDENT)
        return Token(token_type, text)

    def _number(self):
        start = self.pos
        while self.current().isdigit():
            self.advance()
        return Token(TokenType.INT, int(self.source[start:self.pos]))

    def peek(self):
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return "\0"

    def skip_line_comment(self):
        # Skip '//'
        self.advance()
        self.advance()

        while self.current() not in ("\n", "\0"):
            self.advance()

    def skip_block_comment(self):
        # Skip '/*'
        self.advance()
        self.advance()

        while True:
            if self.current() == "\0":
                raise SyntaxError("Unterminated block comment")

            if self.current() == "*" and self.peek() == "/":
                self.advance()
                self.advance()
                break

            self.advance()
