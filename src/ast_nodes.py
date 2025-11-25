from dataclasses import dataclass
from typing import List, Optional, Any
from abc import ABC, abstractmethod

# Classe base para todos os nós
class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

# Programa
@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_program(self)

# Tipos
@dataclass
class Type(ASTNode):
    name: str
    is_array: bool = False
    array_size: Optional[int] = None
    
    def accept(self, visitor):
        return visitor.visit_type(self)
    
    def __str__(self):
        if self.is_array:
            return f"{self.name}[{self.array_size if self.array_size else ''}]"
        return self.name

# Declarações
@dataclass
class VarDeclaration(ASTNode):
    type: Type
    name: str
    initializer: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_var_declaration(self)

@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    params: List[tuple]  # (type, name)
    return_type: Optional[Type]
    body: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)

# Statements
@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)

@dataclass
class ReturnStatement(ASTNode):
    expression: Optional[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)

@dataclass
class ForStatement(ASTNode):
    init: Optional[ASTNode]
    condition: Optional[ASTNode]
    increment: Optional[ASTNode]
    body: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)

@dataclass
class Block(ASTNode):
    statements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_block(self)

# Expressões
@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)

@dataclass
class Assignment(ASTNode):
    target: ASTNode
    value: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)

@dataclass
class Variable(ASTNode):
    name: str
    
    def accept(self, visitor):
        return visitor.visit_variable(self)

@dataclass
class Literal(ASTNode):
    value: Any
    type: str  # 'int', 'float', 'bool', 'string'
    
    def accept(self, visitor):
        return visitor.visit_literal(self)

@dataclass
class ArrayAccess(ASTNode):
    array: ASTNode
    index: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_array_access(self)

@dataclass
class ArrayLiteral(ASTNode):
    elements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_array_literal(self)

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)

@dataclass
class InputExpression(ASTNode):
    prompt: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_input_expression(self)

# Visitor base
class ASTVisitor(ABC):
    def visit_program(self, node: Program):
        pass
    
    def visit_type(self, node: Type):
        pass
    
    def visit_var_declaration(self, node: VarDeclaration):
        pass
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        pass
    
    def visit_expression_statement(self, node: ExpressionStatement):
        pass
    
    def visit_print_statement(self, node: PrintStatement):
        pass
    
    def visit_return_statement(self, node: ReturnStatement):
        pass
    
    def visit_if_statement(self, node: IfStatement):
        pass
    
    def visit_while_statement(self, node: WhileStatement):
        pass
    
    def visit_for_statement(self, node: ForStatement):
        pass
    
    def visit_block(self, node: Block):
        pass
    
    def visit_binary_op(self, node: BinaryOp):
        pass
    
    def visit_unary_op(self, node: UnaryOp):
        pass
    
    def visit_assignment(self, node: Assignment):
        pass
    
    def visit_variable(self, node: Variable):
        pass
    
    def visit_literal(self, node: Literal):
        pass
    
    def visit_array_access(self, node: ArrayAccess):
        pass
    
    def visit_array_literal(self, node: ArrayLiteral):
        pass
    
    def visit_function_call(self, node: FunctionCall):
        pass
    
    def visit_input_expression(self, node: InputExpression):
        pass