import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Palavras-chave
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNCTION = auto()
    RETURN = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    ARRAY = auto()
    PRINT = auto()
    INPUT = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Identificadores e literais
    IDENTIFIER = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    
    # Operadores aritméticos
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    
    # Operadores relacionais
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()
    
    # Operadores lógicos
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimitadores
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    ASSIGN = auto()
    COLON = auto()
    
    # Especiais
    EOF = auto()
    NEWLINE = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro léxico na linha {line}, coluna {column}: {message}")

class Lexer:
    KEYWORDS = {
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'function': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'int': TokenType.INT,
        'float': TokenType.FLOAT,
        'bool': TokenType.BOOL,
        'string': TokenType.STRING,
        'array': TokenType.ARRAY,
        'print': TokenType.PRINT,
        'input': TokenType.INPUT,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    raise LexerError("Número com múltiplos pontos decimais", self.line, self.column)
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        if has_dot:
            return Token(TokenType.FLOAT_LITERAL, float(num_str), start_line, start_column)
        else:
            return Token(TokenType.INT_LITERAL, int(num_str), start_line, start_column)
    
    def read_string(self) -> Token:
        start_line = self.line
        start_column = self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        string_value = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() in 'nrt"\'\\':
                    escape_map = {'n': '\n', 'r': '\r', 't': '\t', '"': '"', "'": "'", '\\': '\\'}
                    string_value += escape_map[self.current_char()]
                    self.advance()
                else:
                    raise LexerError(f"Sequência de escape inválida: \\{self.current_char()}", 
                                   self.line, self.column)
            else:
                string_value += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexerError("String não terminada", start_line, start_column)
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING_LITERAL, string_value, start_line, start_column)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column
        ident = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        value = ident if token_type == TokenType.IDENTIFIER else ident
        
        if token_type == TokenType.TRUE:
            value = True
        elif token_type == TokenType.FALSE:
            value = False
            
        return Token(token_type, value, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Comentários
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            # Newline
            if self.current_char() == '\n':
                line, col = self.line, self.column
                self.advance()
                continue
            
            # Números
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identificadores e palavras-chave
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operadores e delimitadores
            line, col = self.line, self.column
            char = self.current_char()
            
            # Operadores de dois caracteres
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, '==', line, col))
            elif char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, '!=', line, col))
            elif char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LTE, '<=', line, col))
            elif char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GTE, '>=', line, col))
            # Operadores de um caractere
            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', line, col))
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', line, col))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', line, col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', line, col))
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', line, col))
            elif char == '<':
                self.advance()
                self.tokens.append(Token(TokenType.LT, '<', line, col))
            elif char == '>':
                self.advance()
                self.tokens.append(Token(TokenType.GT, '>', line, col))
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, '=', line, col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', line, col))
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', line, col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', line, col))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', line, col))
            else:
                raise LexerError(f"Caractere inesperado: '{char}'", line, col)
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens