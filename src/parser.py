"""
Analisador Sintático (Parser) para Mini-Lang
"""

from typing import List, Optional
from lexer import Token, TokenType
from ast_nodes import *

class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Erro sintático na linha {token.line}, coluna {token.column}: {message}\n  --> {token}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        token = self.current_token()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise ParserError(f"Esperado {token_type.name}, encontrado {token.type.name}", token)
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        return self.current_token().type in token_types
    
    def parse(self) -> Program:
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        # Declarações de variáveis ou funções
        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL, 
                     TokenType.STRING, TokenType.ARRAY):
            return self.parse_declaration()
        
        # Função
        if self.match(TokenType.FUNCTION):
            return self.parse_function_declaration()
        
        # Print
        if self.match(TokenType.PRINT):
            return self.parse_print_statement()
        
        # Return
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()
        
        # If
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        
        # While
        if self.match(TokenType.WHILE):
            return self.parse_while_statement()
        
        # For
        if self.match(TokenType.FOR):
            return self.parse_for_statement()
        
        # Block
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        # Expression statement
        return self.parse_expression_statement()
    
    def parse_type(self) -> Type:
        type_token = self.current_token()
        type_name = None
        
        if type_token.type == TokenType.INT:
            type_name = 'int'
        elif type_token.type == TokenType.FLOAT:
            type_name = 'float'
        elif type_token.type == TokenType.BOOL:
            type_name = 'bool'
        elif type_token.type == TokenType.STRING:
            type_name = 'string'
        elif type_token.type == TokenType.ARRAY:
            self.advance()
            self.expect(TokenType.LT)
            inner_type = self.parse_type()
            self.expect(TokenType.GT)
            
            array_size = None
            if self.match(TokenType.LBRACKET):
                self.advance()
                if self.match(TokenType.INT_LITERAL):
                    array_size = self.current_token().value
                    self.advance()
                self.expect(TokenType.RBRACKET)
            
            return Type(inner_type.name, is_array=True, array_size=array_size)
        else:
            raise ParserError(f"Tipo esperado, encontrado {type_token.type.name}", type_token)
        
        self.advance()
        
        # Verificar se é array
        if self.match(TokenType.LBRACKET):
            self.advance()
            array_size = None
            if self.match(TokenType.INT_LITERAL):
                array_size = self.current_token().value
                self.advance()
            self.expect(TokenType.RBRACKET)
            return Type(type_name, is_array=True, array_size=array_size)
        
        return Type(type_name)
    
    def parse_declaration(self) -> VarDeclaration:
        var_type = self.parse_type()
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        return VarDeclaration(var_type, name, initializer)
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        params = []
        
        if not self.match(TokenType.RPAREN):
            while True:
                param_type = self.parse_type()
                param_name = self.expect(TokenType.IDENTIFIER).value
                params.append((param_type, param_name))
                
                if not self.match(TokenType.COMMA):
                    break
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        return_type = None
        if self.match(TokenType.COLON):
            self.advance()
            return_type = self.parse_type()
        
        body_statements = []
        self.expect(TokenType.LBRACE)
        while not self.match(TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt:
                body_statements.append(stmt)
        self.expect(TokenType.RBRACE)
        
        return FunctionDeclaration(name, params, return_type, body_statements)
    
    def parse_print_statement(self) -> PrintStatement:
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(expr)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        expr = None
        if not self.match(TokenType.SEMICOLON):
            expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(expr)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        then_branch = []
        if self.match(TokenType.LBRACE):
            self.advance()
            while not self.match(TokenType.RBRACE):
                stmt = self.parse_statement()
                if stmt:
                    then_branch.append(stmt)
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            if stmt:
                then_branch.append(stmt)
        
        else_branch = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_branch = []
            if self.match(TokenType.LBRACE):
                self.advance()
                while not self.match(TokenType.RBRACE):
                    stmt = self.parse_statement()
                    if stmt:
                        else_branch.append(stmt)
                self.expect(TokenType.RBRACE)
            else:
                stmt = self.parse_statement()
                if stmt:
                    else_branch.append(stmt)
        
        return IfStatement(condition, then_branch, else_branch)
    
    def parse_while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        body = []
        if self.match(TokenType.LBRACE):
            self.advance()
            while not self.match(TokenType.RBRACE):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        
        init = None
        if not self.match(TokenType.SEMICOLON):
            if self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING):
                init = self.parse_declaration()
            else:
                init = self.parse_expression()
                self.expect(TokenType.SEMICOLON)
        else:
            self.advance()
        
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        increment = None
        if not self.match(TokenType.RPAREN):
            increment = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        body = []
        if self.match(TokenType.LBRACE):
            self.advance()
            while not self.match(TokenType.RBRACE):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        return ForStatement(init, condition, increment, body)
    
    def parse_block(self) -> Block:
        self.expect(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return Block(statements)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        expr = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_assignment()
            return Assignment(expr, value)
        
        return expr
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op = self.advance().value
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        
        while self.match(TokenType.AND):
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_relational()
        
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.advance().value
            right = self.parse_relational()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_relational(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.match(TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = ArrayAccess(expr, index)
            elif self.match(TokenType.LPAREN):
                self.advance()
                args = []
                if not self.match(TokenType.RPAREN):
                    while True:
                        args.append(self.parse_expression())
                        if not self.match(TokenType.COMMA):
                            break
                        self.advance()
                self.expect(TokenType.RPAREN)
                if isinstance(expr, Variable):
                    expr = FunctionCall(expr.name, args)
                else:
                    raise ParserError("Chamada de função inválida", self.current_token())
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        # Literais
        if token.type == TokenType.INT_LITERAL:
            self.advance()
            return Literal(token.value, 'int')
        
        if token.type == TokenType.FLOAT_LITERAL:
            self.advance()
            return Literal(token.value, 'float')
        
        if token.type == TokenType.STRING_LITERAL:
            self.advance()
            return Literal(token.value, 'string')
        
        if token.type in (TokenType.TRUE, TokenType.FALSE):
            self.advance()
            return Literal(token.value, 'bool')
        
        # Input
        if token.type == TokenType.INPUT:
            self.advance()
            self.expect(TokenType.LPAREN)
            prompt = None
            if not self.match(TokenType.RPAREN):
                prompt = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return InputExpression(prompt)
        
        # Identificador
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)
        
        # Expressão entre parênteses
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Array literal
        if token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            if not self.match(TokenType.RBRACKET):
                while True:
                    elements.append(self.parse_expression())
                    if not self.match(TokenType.COMMA):
                        break
                    self.advance()
            self.expect(TokenType.RBRACKET)
            return ArrayLiteral(elements)
        
        raise ParserError(f"Expressão esperada, encontrado {token.type.name}", token)