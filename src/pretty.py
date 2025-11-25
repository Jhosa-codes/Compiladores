
from ast_nodes import *

class ASTPrinter(ASTVisitor):
    def __init__(self):
        self.lines = []
        self.level = 0
    
    def indent(self):
        return "│   " * self.level
    
    def add_line(self, text: str, is_last: bool = False):
        prefix = "└── " if is_last else "├── "
        if self.level > 0:
            self.lines.append(self.indent()[:-4] + prefix + text)
        else:
            self.lines.append(text)
    
    def print_tree(self, node: ASTNode) -> str:
        self.lines = []
        self.level = 0
        node.accept(self)
        return "\n".join(self.lines)
    
    def visit_children(self, children: list):
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            if child:
                self.level += 1
                child.accept(self)
                self.level -= 1
    
    def visit_program(self, node: Program):
        self.add_line("Program")
        self.level += 1
        for i, stmt in enumerate(node.statements):
            stmt.accept(self)
        self.level -= 1
    
    def visit_var_declaration(self, node: VarDeclaration):
        self.add_line(f"VarDeclaration: {node.type} {node.name}")
        if node.initializer:
            self.level += 1
            self.add_line("Initializer:")
            self.level += 1
            node.initializer.accept(self)
            self.level -= 2
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        params_str = ", ".join([f"{t} {n}" for t, n in node.params])
        return_type = str(node.return_type) if node.return_type else "void"
        self.add_line(f"FunctionDeclaration: {node.name}({params_str}) -> {return_type}")
        
        if node.body:
            self.level += 1
            self.add_line("Body:")
            self.level += 1
            for stmt in node.body:
                stmt.accept(self)
            self.level -= 2
    
    def visit_if_statement(self, node: IfStatement):
        self.add_line("IfStatement")
        self.level += 1
        
        self.add_line("Condition:")
        self.level += 1
        node.condition.accept(self)
        self.level -= 1
        
        self.add_line("Then:")
        self.level += 1
        for stmt in node.then_branch:
            stmt.accept(self)
        self.level -= 1
        
        if node.else_branch:
            self.add_line("Else:")
            self.level += 1
            for stmt in node.else_branch:
                stmt.accept(self)
            self.level -= 1
        
        self.level -= 1
    
    def visit_while_statement(self, node: WhileStatement):
        self.add_line("WhileStatement")
        self.level += 1
        
        self.add_line("Condition:")
        self.level += 1
        node.condition.accept(self)
        self.level -= 1
        
        self.add_line("Body:")
        self.level += 1
        for stmt in node.body:
            stmt.accept(self)
        self.level -= 1
        
        self.level -= 1
    
    def visit_for_statement(self, node: ForStatement):
        self.add_line("ForStatement")
        self.level += 1
        
        if node.init:
            self.add_line("Init:")
            self.level += 1
            node.init.accept(self)
            self.level -= 1
        
        if node.condition:
            self.add_line("Condition:")
            self.level += 1
            node.condition.accept(self)
            self.level -= 1
        
        if node.increment:
            self.add_line("Increment:")
            self.level += 1
            node.increment.accept(self)
            self.level -= 1
        
        self.add_line("Body:")
        self.level += 1
        for stmt in node.body:
            stmt.accept(self)
        self.level -= 1
        
        self.level -= 1
    
    def visit_return_statement(self, node: ReturnStatement):
        self.add_line("ReturnStatement")
        if node.expression:
            self.level += 1
            node.expression.accept(self)
            self.level -= 1
    
    def visit_print_statement(self, node: PrintStatement):
        self.add_line("PrintStatement")
        self.level += 1
        node.expression.accept(self)
        self.level -= 1
    
    def visit_expression_statement(self, node: ExpressionStatement):
        self.add_line("ExpressionStatement")
        self.level += 1
        node.expression.accept(self)
        self.level -= 1
    
    def visit_block(self, node: Block):
        self.add_line("Block")
        self.level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.level -= 1
    
    def visit_binary_op(self, node: BinaryOp):
        self.add_line(f"BinaryOp: {node.operator}")
        self.level += 1
        
        self.add_line("Left:")
        self.level += 1
        node.left.accept(self)
        self.level -= 1
        
        self.add_line("Right:")
        self.level += 1
        node.right.accept(self)
        self.level -= 1
        
        self.level -= 1
    
    def visit_unary_op(self, node: UnaryOp):
        self.add_line(f"UnaryOp: {node.operator}")
        self.level += 1
        node.operand.accept(self)
        self.level -= 1
    
    def visit_assignment(self, node: Assignment):
        self.add_line("Assignment")
        self.level += 1
        
        self.add_line("Target:")
        self.level += 1
        node.target.accept(self)
        self.level -= 1
        
        self.add_line("Value:")
        self.level += 1
        node.value.accept(self)
        self.level -= 1
        
        self.level -= 1
    
    def visit_variable(self, node: Variable):
        self.add_line(f"Variable: {node.name}")
    
    def visit_literal(self, node: Literal):
        self.add_line(f"Literal: {node.value} ({node.type})")
    
    def visit_array_access(self, node: ArrayAccess):
        self.add_line("ArrayAccess")
        self.level += 1
        
        self.add_line("Array:")
        self.level += 1
        node.array.accept(self)
        self.level -= 1
        
        self.add_line("Index:")
        self.level += 1
        node.index.accept(self)
        self.level -= 1
        
        self.level -= 1
    
    def visit_array_literal(self, node: ArrayLiteral):
        self.add_line(f"ArrayLiteral ({len(node.elements)} elements)")
        self.level += 1
        for elem in node.elements:
            elem.accept(self)
        self.level -= 1
    
    def visit_function_call(self, node: FunctionCall):
        self.add_line(f"FunctionCall: {node.name}")
        if node.arguments:
            self.level += 1
            self.add_line("Arguments:")
            self.level += 1
            for arg in node.arguments:
                arg.accept(self)
            self.level -= 2
    
    def visit_input_expression(self, node: InputExpression):
        self.add_line("InputExpression")
        if node.prompt:
            self.level += 1
            self.add_line("Prompt:")
            self.level += 1
            node.prompt.accept(self)
            self.level -= 2
    
    def visit_type(self, node: Type):
        self.add_line(f"Type: {node}")