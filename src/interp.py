from typing import Any, Dict, Optional
from ast_nodes import *

class RuntimeError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Erro de execução: {message}")

class ReturnValue(Exception):
    def __init__(self, value: Any):
        self.value = value

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any):
        self.values[name] = value
    
    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Variável '{name}' não definida")
    
    def set(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise RuntimeError(f"Variável '{name}' não definida")

class Interpreter(ASTVisitor):
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.output = []
    
    def push_env(self):
        self.current_env = Environment(self.current_env)
    
    def pop_env(self):
        if self.current_env.parent:
            self.current_env = self.current_env.parent
    
    def interpret(self, program: Program) -> str:
        self.output = []
        try:
            program.accept(self)
        except RuntimeError as e:
            return f"Erro: {e}"
        return "\n".join(self.output)
    
    def visit_program(self, node: Program):
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_var_declaration(self, node: VarDeclaration):
        value = None
        if node.initializer:
            value = node.initializer.accept(self)
        elif node.type.is_array:
            # Inicializar array com valores padrão
            size = node.type.array_size or 0
            if node.type.name == 'int':
                value = [0] * size
            elif node.type.name == 'float':
                value = [0.0] * size
            elif node.type.name == 'bool':
                value = [False] * size
            elif node.type.name == 'string':
                value = [''] * size
        else:
            # Valores padrão
            if node.type.name == 'int':
                value = 0
            elif node.type.name == 'float':
                value = 0.0
            elif node.type.name == 'bool':
                value = False
            elif node.type.name == 'string':
                value = ''
        
        self.current_env.define(node.name, value)
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        self.current_env.define(node.name, node)
    
    def visit_if_statement(self, node: IfStatement):
        condition = node.condition.accept(self)
        
        if condition:
            self.push_env()
            for stmt in node.then_branch:
                stmt.accept(self)
            self.pop_env()
        elif node.else_branch:
            self.push_env()
            for stmt in node.else_branch:
                stmt.accept(self)
            self.pop_env()
    
    def visit_while_statement(self, node: WhileStatement):
        while True:
            # Avaliação com curto-circuito
            condition = node.condition.accept(self)
            if not condition:
                break
            
            self.push_env()
            for stmt in node.body:
                stmt.accept(self)
            self.pop_env()
    
    def visit_for_statement(self, node: ForStatement):
        self.push_env()
        
        if node.init:
            node.init.accept(self)
        
        while True:
            if node.condition:
                condition = node.condition.accept(self)
                if not condition:
                    break
            
            for stmt in node.body:
                stmt.accept(self)
            
            if node.increment:
                node.increment.accept(self)
        
        self.pop_env()
    
    def visit_return_statement(self, node: ReturnStatement):
        value = None
        if node.expression:
            value = node.expression.accept(self)
        raise ReturnValue(value)
    
    def visit_print_statement(self, node: PrintStatement):
        value = node.expression.accept(self)
        self.output.append(str(value))
    
    def visit_expression_statement(self, node: ExpressionStatement):
        node.expression.accept(self)
    
    def visit_block(self, node: Block):
        self.push_env()
        for stmt in node.statements:
            stmt.accept(self)
        self.pop_env()
    
    def visit_binary_op(self, node: BinaryOp):
        # Curto-circuito para operadores lógicos
        if node.operator == 'and':
            left = node.left.accept(self)
            if not left:
                return False
            return node.right.accept(self)
        
        if node.operator == 'or':
            left = node.left.accept(self)
            if left:
                return True
            return node.right.accept(self)
        
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise RuntimeError("Divisão por zero")
            return left / right if isinstance(left, float) or isinstance(right, float) else left // right
        elif node.operator == '%':
            if right == 0:
                raise RuntimeError("Módulo por zero")
            return left % right
        elif node.operator == '<':
            return left < right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>':
            return left > right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        
        raise RuntimeError(f"Operador binário desconhecido: {node.operator}")
    
    def visit_unary_op(self, node: UnaryOp):
        operand = node.operand.accept(self)
        
        if node.operator == 'not':
            return not operand
        elif node.operator == '-':
            return -operand
        
        raise RuntimeError(f"Operador unário desconhecido: {node.operator}")
    
    def visit_assignment(self, node: Assignment):
        value = node.value.accept(self)
        
        if isinstance(node.target, Variable):
            self.current_env.set(node.target.name, value)
        elif isinstance(node.target, ArrayAccess):
            array_var = node.target.array
            if not isinstance(array_var, Variable):
                raise RuntimeError("Atribuição a array requer variável")
            
            array = self.current_env.get(array_var.name)
            if not isinstance(array, list):
                raise RuntimeError(f"'{array_var.name}' não é um array")
            
            index = node.target.index.accept(self)
            if not isinstance(index, int):
                raise RuntimeError("Índice do array deve ser inteiro")
            
            # Bounds check
            if index < 0 or index >= len(array):
                raise RuntimeError(f"Índice {index} fora dos limites do array (tamanho {len(array)})")
            
            array[index] = value
        
        return value
    
    def visit_variable(self, node: Variable):
        return self.current_env.get(node.name)
    
    def visit_literal(self, node: Literal):
        return node.value
    
    def visit_array_access(self, node: ArrayAccess):
        array_var = node.array
        if not isinstance(array_var, Variable):
            raise RuntimeError("Acesso a array requer variável")
        
        array = self.current_env.get(array_var.name)
        if not isinstance(array, list):
            raise RuntimeError(f"'{array_var.name}' não é um array")
        
        index = node.index.accept(self)
        if not isinstance(index, int):
            raise RuntimeError("Índice do array deve ser inteiro")
        
        # Bounds check
        if index < 0 or index >= len(array):
            raise RuntimeError(f"Índice {index} fora dos limites do array (tamanho {len(array)})")
        
        return array[index]
    
    def visit_array_literal(self, node: ArrayLiteral):
        return [elem.accept(self) for elem in node.elements]
    
    def visit_function_call(self, node: FunctionCall):
        func = self.current_env.get(node.name)
        
        if not isinstance(func, FunctionDeclaration):
            raise RuntimeError(f"'{node.name}' não é uma função")
        
        if len(node.arguments) != len(func.params):
            raise RuntimeError(f"Função '{node.name}' espera {len(func.params)} argumentos, recebeu {len(node.arguments)}")
        
        # Avaliar argumentos
        args = [arg.accept(self) for arg in node.arguments]
        
        # Novo ambiente para a função
        self.push_env()
        
        # Bind parâmetros
        for (param_type, param_name), arg_value in zip(func.params, args):
            self.current_env.define(param_name, arg_value)
        
        # Executar corpo da função
        return_value = None
        try:
            for stmt in func.body:
                stmt.accept(self)
        except ReturnValue as ret:
            return_value = ret.value
        
        self.pop_env()
        return return_value
    
    def visit_input_expression(self, node: InputExpression):
        prompt = ""
        if node.prompt:
            prompt = str(node.prompt.accept(self))
        
        # Simulação de input (em um sistema real, usaria input())
        return input(prompt) if prompt else input()
    
    def visit_type(self, node: Type):
        return str(node)