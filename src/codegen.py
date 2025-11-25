from ast_nodes import *

class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.code = []
        self.indent_level = 0
    
    def indent(self):
        return "    " * self.indent_level
    
    def emit(self, line: str):
        if line.strip():
            self.code.append(self.indent() + line)
        else:
            self.code.append("")
    
    def generate(self, program: Program) -> str:
        self.code = []
        self.indent_level = 0
        program.accept(self)
        return "\n".join(self.code)
    
    def visit_program(self, node: Program):
        self.emit("# Código gerado automaticamente")
        self.emit("")
        
        for stmt in node.statements:
            stmt.accept(self)
            if isinstance(stmt, FunctionDeclaration):
                self.emit("")
    
    def visit_var_declaration(self, node: VarDeclaration):
        if node.initializer:
            init_code = node.initializer.accept(self)
            self.emit(f"{node.name} = {init_code}")
        else:
            # Valores padrão
            if node.type.is_array:
                size = node.type.array_size or 0
                if node.type.name == 'int':
                    self.emit(f"{node.name} = [0] * {size}")
                elif node.type.name == 'float':
                    self.emit(f"{node.name} = [0.0] * {size}")
                elif node.type.name == 'bool':
                    self.emit(f"{node.name} = [False] * {size}")
                elif node.type.name == 'string':
                    self.emit(f"{node.name} = [''] * {size}")
            else:
                if node.type.name == 'int':
                    self.emit(f"{node.name} = 0")
                elif node.type.name == 'float':
                    self.emit(f"{node.name} = 0.0")
                elif node.type.name == 'bool':
                    self.emit(f"{node.name} = False")
                elif node.type.name == 'string':
                    self.emit(f"{node.name} = ''")
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        params = ", ".join([name for _, name in node.params])
        self.emit(f"def {node.name}({params}):")
        
        self.indent_level += 1
        if not node.body:
            self.emit("pass")
        else:
            for stmt in node.body:
                stmt.accept(self)
        self.indent_level -= 1
    
    def visit_if_statement(self, node: IfStatement):
        condition = node.condition.accept(self)
        self.emit(f"if {condition}:")
        
        self.indent_level += 1
        if not node.then_branch:
            self.emit("pass")
        else:
            for stmt in node.then_branch:
                stmt.accept(self)
        self.indent_level -= 1
        
        if node.else_branch:
            self.emit("else:")
            self.indent_level += 1
            for stmt in node.else_branch:
                stmt.accept(self)
            self.indent_level -= 1
    
    def visit_while_statement(self, node: WhileStatement):
        condition = node.condition.accept(self)
        self.emit(f"while {condition}:")
        
        self.indent_level += 1
        if not node.body:
            self.emit("pass")
        else:
            for stmt in node.body:
                stmt.accept(self)
        self.indent_level -= 1
    
    def visit_for_statement(self, node: ForStatement):
        # Converter for em while em Python para manter a semântica
        if node.init:
            node.init.accept(self)
        
        condition = node.condition.accept(self) if node.condition else "True"
        self.emit(f"while {condition}:")
        
        self.indent_level += 1
        for stmt in node.body:
            stmt.accept(self)
        
        if node.increment:
            node.increment.accept(self)
        
        self.indent_level -= 1
    
    def visit_return_statement(self, node: ReturnStatement):
        if node.expression:
            expr = node.expression.accept(self)
            self.emit(f"return {expr}")
        else:
            self.emit("return")
    
    def visit_print_statement(self, node: PrintStatement):
        expr = node.expression.accept(self)
        self.emit(f"print({expr})")
    
    def visit_expression_statement(self, node: ExpressionStatement):
        expr = node.expression.accept(self)
        self.emit(expr)
    
    def visit_block(self, node: Block):
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_binary_op(self, node: BinaryOp):
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        op_map = {
            'and': 'and',
            'or': 'or',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '//',  # Divisão inteira
            '%': '%'
        }
        
        operator = op_map.get(node.operator, node.operator)
        return f"({left} {operator} {right})"
    
    def visit_unary_op(self, node: UnaryOp):
        operand = node.operand.accept(self)
        
        op_map = {
            'not': 'not',
            '-': '-'
        }
        
        operator = op_map.get(node.operator, node.operator)
        return f"({operator} {operand})"
    
    def visit_assignment(self, node: Assignment):
        target = node.target.accept(self)
        value = node.value.accept(self)
        self.emit(f"{target} = {value}")
        return f"{target} = {value}"
    
    def visit_variable(self, node: Variable):
        return node.name
    
    def visit_literal(self, node: Literal):
        if node.type == 'string':
            return f'"{node.value}"'
        elif node.type == 'bool':
            return "True" if node.value else "False"
        else:
            return str(node.value)
    
    def visit_array_access(self, node: ArrayAccess):
        array = node.array.accept(self)
        index = node.index.accept(self)
        
        # Adicionar bounds check em Python
        return f"{array}[{index}]"
    
    def visit_array_literal(self, node: ArrayLiteral):
        elements = [elem.accept(self) for elem in node.elements]
        return f"[{', '.join(elements)}]"
    
    def visit_function_call(self, node: FunctionCall):
        args = [arg.accept(self) for arg in node.arguments]
        return f"{node.name}({', '.join(args)})"
    
    def visit_input_expression(self, node: InputExpression):
        if node.prompt:
            prompt = node.prompt.accept(self)
            return f"input({prompt})"
        return "input()"
    
    def visit_type(self, node: Type):
        return str(node)